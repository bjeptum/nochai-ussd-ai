# NoChai — An Intelligent Bribe Refusal Coach for Kenya

An intelligent Swahili-first system that helps everyday Kenyans refuse and report micro-corruption via USSD and WhatsApp. 

**Theme:** Governance & Public Policy | Combating Corruption

## Why This Matters 
- 70% of Kenyans pay bribes monthly (EACC)
- Gen-Z protests fueled by graft in public services
- Rural citizens lose fertilizer subsidies to "kitu kidogo"

NoChai turns victims into empowered whistleblowers using **voice + USSD + Swahili AI**

## Key Features
- Dial `*384*xxxx#` on any feature phone and report in Sheng/Swahili
- AI generates **real-time refusal scripts**
- Anonymous reports logged to public **Corruption Heatmap**
- Works on WhatsApp with rich responses
- Built for Kenya with multilingual support (Swahili, Sheng, English)

## Tech Stack
- **Backend:** Python 3.8+ + Flask
- **USSD:** Africa's Talking API
- **WhatsApp:** Twilio Sandbox
- **AI Model:** BLOOM-560M (multilingual language model)
- **Framework:** LangChain + HuggingFace Transformers
- **Database:** SQLite
- **Dashboard:** Streamlit + Folium
- **Tunneling:** Ngrok

##Set up & Installation

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment tool (venv)
- Ngrok account (free tier)
- Hugging Face account (for model access)

### Step 1: Clone the Repository
```bash
git clone https://github.com/bjeptum/nochai-ussd-ai.git
cd nochai-ussd-ai
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate  # On Windows
```

### Step 3: Install Dependencies
```bash
# Upgrade pip first
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt

# Download spaCy English model
python3 -m spacy download en_core_web_sm
```

### Step 4: Configure Environment Variables
Create a `.env` file in the project root:
```bash
# .env
HUGGINGFACE_API_TOKEN=your_huggingface_token_here
ASSEMBLYAI_API_KEY=your_assemblyai_key_here
AFRICASTALKING_USERNAME=your_at_username
AFRICASTALKING_API_KEY=your_at_api_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
```

**Getting API Keys:**
- **Hugging Face:** Sign up at https://huggingface.co, go to Settings → Access Tokens
- **Africa's Talking:** Register at https://africastalking.com
- **Twilio:** Sign up at https://www.twilio.com/try-twilio
- **AssemblyAI:** Get key at https://www.assemblyai.com

### Step 5: Authenticate with Hugging Face (if needed)
```bash
# Login to Hugging Face CLI
huggingface-cli login

# Paste your token when prompted
# Choose 'n' when asked to add as git credential
```

### Step 6: Initialize Database
The database will be created automatically when you first run the app, but you can verify:
```bash
python3 -c "from db import init_db; init_db()"
```

## Running the Application

### Start the Flask Server
```bash
# Make sure venv is activated
python3 app.py

# You should see:
# Loading language model... (takes ~20s first time)
# Database initialized
# * Running on http://127.0.0.1:5000
```

### Expose with Ngrok (in another terminal)
```bash
# In a new terminal window
ngrok http 5000

# Copy the https forwarding URL (e.g., https://abcd1234.ngrok.io)
```

### Run the Dashboard (optional, in another terminal)
```bash
# Activate venv first
source venv/bin/activate

# Run streamlit
streamlit run dashboard.py

# Opens at http://localhost:8501
```

## Webhook Configuration

### For WhatsApp (Twilio)
1. Go to Twilio Console → Messaging → Try it out → Send a WhatsApp message
2. Set webhook URL to: `https://your-ngrok-url.ngrok.io/whatsapp`
3. Method: POST

### For USSD (Africa's Talking)
1. Go to Africa's Talking Dashboard → USSD
2. Create a USSD code (e.g., `*384*xxxx#`)
3. Set callback URL to: `https://your-ngrok-url.ngrok.io/ussd`
4. Method: POST

## Testing the Application

### Test WhatsApp
Send a message to your Twilio WhatsApp sandbox number:
```
Nilikuwa roadblock Githurai, polisi alitaka 500 bob
```

You should receive:
- Acknowledgment of report
- Anti-corruption refusal script
- Link to heatmap

### Test USSD
Dial your USSD code on a phone or simulator:
```
*384*xxxx#
```

Follow the menu:
1. Report corruption
2. Get refusal script
3. View heatmap

## Project Structure
```
nochai-ussd-ai/
├── app.py              # Flask server (WhatsApp + USSD endpoints)
├── agents.py           # AI processing logic & LLM integration
├── db.py               # SQLite database operations
├── dashboard.py        # Streamlit heatmap visualization
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── nochai.db          # SQLite database (auto-generated)
└── README.md          # This file
```

## Troubleshooting

### Model Loading Issues
**Problem:** `GatedRepoError` or `401 Unauthorized`
```bash
# Solution: Make sure you're logged in
huggingface-cli login
```

### Module Not Found Errors
**Problem:** `ModuleNotFoundError: No module named 'spacy'`
```bash
# Solution: Make sure venv is activated and reinstall
source venv/bin/activate
pip install -r requirements.txt
```

### spaCy Model Missing
**Problem:** `Can't find model 'en_core_web_sm'`
```bash
# Solution: Download the model
python3 -m spacy download en_core_web_sm
```

### Port Already in Use
**Problem:** `Address already in use`
```bash
# Solution: Kill the process or use different port
# Find process on port 5000
lsof -ti:5000 | xargs kill -9

# Or run on different port
flask run --port 5001
```

### Database Locked
**Problem:** `database is locked`
```bash
# Solution: Close other connections or delete and recreate
rm nochai.db
python3 -c "from db import init_db; init_db()"
```

## Usage Examples

### WhatsApp Message Examples
```
"Polisi Thika road wanataka kitu kidogo 200"
"Ofisi ya huduma wataka 1000 shillings niskie maji"
"Afande anataka 500 bob kwa roadblock Nakuru"
```

### USSD Flow Example
```
User: *384*2001#
System: Karibu NoChai - Ripoti Rushwa
        1. Ripoti rushwa
        2. Pata script ya kukataa rushwa
        3. Angalia heatmap

User: 1
System: Wapi rushwa ilitokea?
        Andika jina la mahali (mfano: Nairobi, Kisumu)

User: Nairobi
System: Kiasi gani kilitakiwa?
        Andika kiasi kwa shillings (mfano: 500)

User: 500
System: Eleza kwa ufupi kilichotokea:

User: Polisi roadblock
System: Asante! Ripoti yako imepokelewa.
        Imetumwa bila kujulikana.
```

## Contributing
Currently I am the sole contributor.

Contributions are welcome! Please feel free to submit a Pull Request.

## License
Totally free! Just give me credit for my work.

## Team
Built for tackling corruption in Kenya through accessible technology.

## Links
- **GitHub:** https://github.com/bjeptum/nochai-ussd-ai
- **Live Demo:** https://www.loom.com/share/244bae959f444167a0df709be9b78e55


**NoChai** - Empowering Kenyans to say NO to corruption, one report at a time.
