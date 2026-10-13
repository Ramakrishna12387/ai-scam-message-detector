import telebot
import re

# Ungaloda BotFather token-ah inga double quotes kulla podunga:
BOT_TOKEN = "8888481527:AAFLeMjMDPmaBZX0U_p2eWMNIUXmbR7s2Zg"

bot = telebot.TeleBot(BOT_TOKEN)

SCAM_KEYWORDS = [
    "won", "winner", "prize", "lottery", "free money", "claim", 
    "urgent", "immediately", "verify", "verification", "blocked", 
    "account blocked", "bank account", "otp", "password", "pin", 
    "cvv", "credit card", "click here", "click link", "transfer money", 
    "pay now", "refund", "kyc", "suspended", "guaranteed", "job offer"
]

def analyze_message(text):
    text_lower = text.lower()
    score = 0
    flags = []

    for word in SCAM_KEYWORDS:
        if word in text_lower:
            flags.append(word)
            score += 15

    if re.search(r'https?://|www\.|\.xyz|\.tk|\.top|\.bit\.ly', text_lower):
        flags.append("suspicious url/link")
        score += 25

    if any(sym in text for sym in ['₹', '$', '€', 'rs']):
        score += 10

    if "otp" in text_lower or "password" in text_lower or "pin" in text_lower:
        score += 20

    threat_score = min(score, 100)
    return threat_score, list(set(flags))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👋 **AI Scam Detector Bot-ku vanakkam!**\n\n"
        "SMS, WhatsApp, alladhu Email messages-ah inga forward/paste pannunga. Scam-ah nu scan panni solren!"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    threat_score, detected_flags = analyze_message(user_text)

    if threat_score >= 40:
        response = (
            f"🚨 **SCAM ALERT! (Risk: {threat_score}%)**\n\n"
            f"⚠️ **Result:** Idhu Scam / Phishing message aaga irukka athiga vaaipu ullathu!\n\n"
            f"🔍 **Detected Red Flags:** `{', '.join(detected_flags)}`\n\n"
            f"🛡️ Link click pannadheenga, OTP/details share pannadheenga."
        )
    elif threat_score >= 20:
        response = (
            f"⚠️ **CAUTION: SUSPICIOUS CONTENT (Risk: {threat_score}%)**\n\n"
            f"🔍 **Flags:** `{', '.join(detected_flags)}`"
        )
    else:
        response = f"✅ **SAFE MESSAGE (Risk: {threat_score}%)**\n\nSuspicious patterns edhuvum theriya villai."

    bot.reply_to(message, response, parse_mode="Markdown")

print("🤖 Bot running successfully...")
bot.infinity_polling()