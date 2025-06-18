import telebot

# Ganti dengan token bot kamu
TOKEN = '8057913893:AAEjGd0918v2Lp1yJTpwsKPd65soGfTeao0'

bot = telebot.TeleBot(TOKEN)

# Simulasi data pengguna dan OTP
user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'step': 'phone'}
    bot.reply_to(message, "☕ Selamat datang di layanan pendaftaran Kopi Kenangan!\n\nSilakan masukkan nomor HP Anda:")
    
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if chat_id not in user_data:
        bot.send_message(chat_id, "Silakan ketik /start untuk memulai proses.")
        return

    step = user_data[chat_id]['step']

    # Step 1: Masukkan nomor HP
    if step == 'phone':
        if not text.isdigit() or len(text) < 10:
            bot.send_message(chat_id, "Nomor HP tidak valid. Silakan coba lagi.")
            return

        user_data[chat_id]['phone'] = text
        user_data[chat_id]['step'] = 'otp'
        otp = '123456'  # Simulasi OTP yang dikirim oleh Kopi Kenangan
        user_data[chat_id]['otp'] = otp

        bot.send_message(chat_id, f"📲 Kami telah mengirimkan kode OTP ke {text}.\n\n🔑 Masukkan kode OTP: `{otp}`")

    # Step 2: Verifikasi OTP
    elif step == 'otp':
        if text != user_data[chat_id]['otp']:
            bot.send_message(chat_id, "❌ Kode OTP salah. Silakan coba lagi.")
            return

        user_data[chat_id]['step'] = 'username'
        bot.send_message(chat_id, "Masukkan username yang Anda inginkan:")

    # Step 3: Masukkan username
    elif step == 'username':
        username = text
        phone = user_data[chat_id]['phone']

        bot.send_message(chat_id, f"✅ Akun berhasil dibuat!\n\n📱 Nomor HP: {phone}\n👤 Username: {username}")
        bot.send_message(chat_id, "Selamat menikmati Kopi Kenangan! ☕")

        del user_data[chat_id]

bot.polling()
