# NoChai — An Intelligent Bribe Refusal Coach for Kenya

An intelligent Swahili-first system that helps everyday Kenyans refuse and report micro-corruption via USSD (*384*xxxx#) and WhatsApp. 

Theme: Governance & Public Policy | Combating Corruption

## Live Demo Video
https://github.com/yourname/kitu-haina-ussd-ai/blob/main/demo/demo.mp4

## Why This Matters 
- 70% of Kenyans pay bribes monthly (EACC)
- Gen-Z protests fueled by graft in public services
- Rural citizens lose fertilizer subsidies to "kitu kidogo"

NoChai turn victims into empowered whistleblowers using **voice + USSD + Swahili AI**

## Key Features
- Dial `*384*xxxx#` on any feature phone and report in Sheng/Swahili
- AI asks clarifying questionsand generates **real-time refusal script** as "Mama Pima" or "Mzee wa Mtaa"
- Anonymously logs to public **Corruption Heatmap**
- Works on WhatsApp voice notes too
- Built with Africa's Talking USSD + fine-tuned Swahili Gemma-2B

## Tech Stack (All Open Source / Free Tier)
- Python + Flask
- Africa's Talking (USSD)
- Twilio (WhatsApp sandbox)
- Gemma-2B Swahili (`alfaxadeyembe/gemma2-2b-swahili-preview`)
- LangChain (agentic flows)
- Streamlit (heatmap dashboard)
- SQLite + Ngrok

## How to Run Locally (5 minutes)
```bash
git clone git@github.com:bjeptum/kitu-haina-ussd-ai.git
cd kitu-haina-ussd-ai
pip install -r requirements.txt

# Copy env and fill your keys
cp .env.example .env

# Run server
python app.py

# In another terminal
ngrok http 5000