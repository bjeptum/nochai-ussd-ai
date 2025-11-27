# agents.py
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import torch
import spacy
import re
from db import add_report

# Load Swahili-fine-tuned Gemma-2B (fast & accurate)
print("Loading Swahili Gemma-2B... (takes ~20s first time)")
tokenizer = AutoTokenizer.from_pretrained("alfaxadeyembe/gemma2-2b-swahili-preview")
model = AutoModelForCausalLM.from_pretrained(
    "alfaxadeyembe/gemma2-2b-swahili-preview",
    torch_dtype=torch.bfloat16,
    device_map="auto",
    low_cpu_mem_usage=True
)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=180,
    temperature=0.7,
    top_p=0.9,
    do_sample=True
)
llm = HuggingFacePipeline(pipeline=pipe)

# Simple entity extraction (location & amount)
nlp = spacy.load("en_core_web_sm")

def extract_info(text):
    text = text.lower()
    location = "Unknown"
    amount = 0

    # Common Kenyan locations
    places = ["nairobi", "kisumu", "mombasa", "eldoret", "nakuru", "githurai", "kitui", "kangemi", "dandora"]
    for place in places:
        if place in text:
            location = place.title()
            break

    # Extract money (Sh100, 200 bob, etc.)
    money_match = re.search(r"(sh|\b)\s?(\d{2,5})\b", text)
    if money_match:
        amount = int(money_match.group(2))

    return location, amount


# WHATSAPP MESSAGE PROCESSING
def process_whatsapp_message(message, media_url=None, name="Mkenya"):
    if not message:
        return "Karibu NoChai! 💪\nAndika rushwa uliyokutana nayo na nitakusaidia kukataa na kuripoti."

    location, amount = extract_info(message)
    category = "Police" if "polisi" in message.lower() else "Service Delivery"

    # Generate refusal script in Sheng/Swahili
    prompt = f"""
    Wewe ni Mama Pima, mama hodari wa Nairobi anayekataa rushwa.
    Mkenya amesema: "{message}"
    Toa script fupi ya kumudu afisa anayeomba kitu kidogo.
    Tumia Sheng au Kiswahili cha mtaa. Fanya iwe ya heshima lakini nguvu.
    """
    try:
        result = llm.invoke(prompt)
        script = result.split("Response:")[-1].strip() if "Response:" in result else result
        script = script.split("\n\n")[0][:300]
    except:
        script = "Afande, asante kwa kazi yako. Lakini sitoi kitu kidogo. Hii ni haki yangu. Nitapita."

    add_report(location, amount, category, message)

    return f"""
Asante {name}! Ripoti yako imepokelewa bila jina lako.

💬 *Script ya kukataa rushwa*:
{script}

Ripoti imetumwa kwa mamlaka bila kujulikana.
Angalia heatmap: https://kitu-haina.streamlit.app
""".strip()


# USSD MESSAGE PROCESSING
def process_ussd_input(session_id, phone_number, user_input, step, temp_data):
    from db import update_session

    if step == 1:
        # First input: collect report
        location, amount = extract_info(user_input)
        update_session(session_id, phone_number, step=2,
                       temp_data=f"{user_input}||{location}||{amount}")
        return f"""
CON Asante! Umesema:
"{user_input}"

Uliza swali lolote la ziada au bonyeza 1 kuendelea na script ya kukataa rushwa.
""".strip()

    elif step == 2:
        # Final: generate script
        original, location, amount = temp_data.split("||")
        category = "Police" if "polisi" in original.lower() else "Huduma"

        prompt = f"""
        Wewe ni Mzee wa Mtaa, mtu wa hekima anayewafundisha vijana kukataa rushwa.
        Mkenya amesema: "{original}"
        Toa script fupi ya kukataa rushwa kwa heshima lakini kwa nguvu.
        Tumia Sheng au Kiswahili rahisi.
        """
        try:
            result = llm.invoke(prompt)
            script = result.split("Response:")[-1].strip() if "Response:" in result else result
            script = script.split("\n\n")[0][:200]
        except:
            script = "Asante afisa. Sitaki kutoa kitu kidogo. Hii ni haki yangu. Endelea na kazi yako."

        add_report(location, amount, category, original)

        return f"""
END Asante sana! 💪

*Script yako ya kukataa rushwa*:
{script}

Ripoti yako imetumwa bila kujulikana.
Pamoja tujenge Kenya bila rushwa!

Tuma neno KITU kwa 22123 kupata heatmap
""".strip()

    return "END Asante kwa kutumia NoChai!"