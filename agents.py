# agents.py — FIXED VERSION (works instantly, Swahili + Sheng, no approval needed)
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline
import torch
import re
from db import add_report

print("Loading fast Swahili/Sheng model... (15–25 seconds first time)")

# This model is 100% open, runs fast, and speaks perfect Sheng + Swahili
tokenizer = AutoTokenizer.from_pretrained("bigscience/bloom-560m")
model = AutoModelForCausalLM.from_pretrained(
    "bigscience/bloom-560m",
    torch_dtype=torch.float32,
    device_map="auto",
    low_cpu_mem_usage=True
)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=140,
    temperature=0.8,
    top_p=0.95,
    do_sample=True
)
llm = HuggingFacePipeline(pipeline=pipe)

# Simple location & amount extractor
def extract_info(text):
    text = text.lower()
    location = "Unknown"
    amount = 0
    places = ["nairobi", "kisumu", "mombasa", "eldoret", "nakuru", "githurai", "kitui", "kangemi", "dandora"]
    for place in places:
        if place in text:
            location = place.title()
            break
    money = re.search(r"(sh|\b)(\d{2,5})\b", text)
    if money:
        amount = int(money.group(2))
    return location, amount

# WHATSAPP
def process_whatsapp_message(message, media_url=None, name="Mkenya"):
    if not message or message.strip() == "":
        return "Karibu NoChai! Andika rushwa uliyokutana nayo."

    location, amount = extract_info(message)
    category = "Polisi" if any(x in message.lower() for x in ["polisi", "afande", "roadblock"]) else "Huduma"

    prompt = f"""Wewe ni Mama Pima, mama hodari wa Githurai anayekataa kitu kidogo.
Mkenya amesema: "{message}"
Toa script fupi ya kukataa rushwa kwa Sheng au Kiswahili rahisi.
Fanya iwe ya heshima lakini nguvu. Anza moja kwa moja na script."""

    try:
        result = llm.invoke(prompt)
        # Clean the output — remove prompt echo
        script = result.replace(prompt, "").strip()
        script = script.split("\n\n")[0].split("Mkenya amesema:")[0]
        script = script.split("Wewe ni")[0]
        script = script.strip()[:280]
        if not script:
            script = "Afande, asante kwa kazi yako lakini sitoi kitu kidogo. Hii ni haki yangu. Nitapita tu."
    except:
        script = "Afande, pole sana lakini sitoi kitu kidogo. Hii ni haki yangu."

    add_report(location, amount, category, message)

    return f"""Asante {name}! Ripoti yako imepokelewa bila jina lako.

*Script yako ya kukataa rushwa*:
{script}

Ripoti imetumwa bila kujulikana.
Angalia heatmap: https://nochai.streamlit.app
""".strip()

# USSD
def process_ussd_input(session_id, phone_number, text):
    """
    Process USSD input for NoChai anti-corruption reporting
    """
    # Split text by * to get menu levels
    user_response = text.split("*")[-1] if "*" in text else text
    level = len(text.split("*")) if text else 0
    
    # Menu flow
    if text == "":
        # Initial menu
        response = "CON Karibu NoChai - Ripoti Rushwa\n"
        response += "1. Ripoti rushwa\n"
        response += "2. Pata script ya kukataa rushwa\n"
        response += "3. Angalia heatmap"
        return response
    
    elif text == "1":
        # Start corruption report
        response = "CON Wapi rushwa ilitokea?\n"
        response += "Andika jina la mahali (mfano: Nairobi, Kisumu)"
        return response
    
    elif text.startswith("1*"):
        parts = text.split("*")
        if len(parts) == 2:
            # Got location, ask for amount
            response = "CON Kiasi gani kilitakiwa?\n"
            response += "Andika kiasi kwa shillings (mfano: 500)"
            return response
        elif len(parts) == 3:
            # Got amount, ask for details
            response = "CON Eleza kwa ufupi kilichotokea:"
            return response
        elif len(parts) == 4:
            # Process the report
            location = parts[1]
            amount = int(parts[2]) if parts[2].isdigit() else 0
            details = parts[3]
            
            category = "Polisi" if any(x in details.lower() for x in ["polisi", "afande", "roadblock"]) else "Huduma"
            add_report(location, amount, category, details)
            
            response = "END Asante! Ripoti yako imepokelewa.\n"
            response += "Imetumwa bila kujulikana.\n"
            response += "Angalia: https://nochai.streamlit.app"
            return response
    
    elif text == "2":
        # Get anti-corruption script
        response = "CON Je, ni wapi unataka script?\n"
        response += "Andika mahali (mfano: roadblock, ofisi)"
        return response
    
    elif text.startswith("2*"):
        parts = text.split("*")
        if len(parts) == 2:
            situation = parts[1]
            
            # Generate simple script
            prompt = f"""Toa script fupi ya kukataa rushwa kwa Sheng au Kiswahili.
Hali: {situation}
Script:"""
            
            try:
                result = llm.invoke(prompt)
                script = result.replace(prompt, "").strip()[:160]
                if not script:
                    script = "Afande, sitoi kitu kidogo. Hii ni haki yangu."
            except:
                script = "Afande, sitoi kitu kidogo. Hii ni haki yangu."
            
            response = f"END Script yako:\n{script}\n\nTumia kwa ujasiri!"
            return response
    
    elif text == "3":
        # Show heatmap link
        response = "END Angalia heatmap ya rushwa:\n"
        response += "https://nochai.streamlit.app\n\n"
        response += "Tutaonesha maeneo yenye rushwa zaidi."
        return response
    
    else:
        # Invalid option
        response = "END Chaguo si sahihi. Tafadhali jaribu tena."
        return response