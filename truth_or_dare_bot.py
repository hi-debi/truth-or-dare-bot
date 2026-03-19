"""
Truth or Dare Bot Telegram — Couple Edition 🔥
Bahasa Indonesia | Konten: Sedang (berani tapi tidak vulgar)
Fitur: Timer tantangan, mode couple

Cara pakai:
1. Install: pip install python-telegram-bot==20.7
2. Ganti BOT_TOKEN dengan token dari @BotFather
3. Jalankan: python truth_or_dare_bot.py
"""

import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)

BOT_TOKEN = "8588161571:AAEoEcZEX-lKsK9N_kcmdS8PF0-gE3zRzoM"

# ─────────────────────────────────────────────
#   DATABASE PERTANYAAN & TANTANGAN
# ─────────────────────────────────────────────

TRUTH_NORMAL = [
    "Apa hal paling memalukan yang pernah kamu lakukan di depan aku?",
    "Siapa orang pertama yang kamu suka sebelum kenal aku?",
    "Apa yang paling kamu suka dari aku secara fisik?",
    "Pernah nggak kamu pura-pura tidur biar nggak diajak ngobrol?",
    "Apa mimpi paling aneh yang pernah kamu alami?",
    "Kalau bisa mengubah satu hal dari aku, apa itu?",
    "Apa hal yang paling kamu sembunyikan dari orang tuamu?",
    "Seberapa sering kamu stalking media sosial mantan?",
    "Apa yang pertama kali kamu pikirin waktu pertama lihat aku?",
    "Pernah nggak kamu bohong ke aku? Soal apa?",
    "Kapan terakhir kali kamu nangis dan karena apa?",
    "Apa fantasi liburan impianmu bersama aku?",
    "Kalau aku jadi makanan, aku jadi makanan apa?",
    "Apa hal paling konyol yang pernah kamu lakukan demi cinta?",
    "Siapa teman aku yang menurutmu paling menyebalkan?",
    "Apa yang paling kamu rindukan dari aku saat jauh?",
    "Pernah nggak kamu cemburu tapi pura-pura nggak?",
    "Apa yang bikin kamu pertama kali jatuh cinta sama aku?",
    "Kalau kita putus (amit-amit), apa yang paling kamu rindukan?",
    "Seberapa sering kamu kepikiran aku dalam sehari?",
    "Apa kebiasaan aku yang diam-diam mengganggu kamu?",
    "Pernah nggak kamu bacain chat aku tanpa bilang?",
    "Apa hal terkonyol yang pernah kamu lakuin buat impress aku?",
    "Siapa artis yang menurut kamu paling mirip aku?",
    "Apa yang paling kamu banggain dari hubungan kita?",
]

TRUTH_18PLUS = [
    "Bagian tubuhku mana yang paling kamu suka?",
    "Apa hal romantis yang pengen banget kamu lakuin sama aku tapi belum kesampaian?",
    "Ceritain mimpi terliar tentang aku yang pernah kamu alami!",
    "Di mana tempat paling 'gila' yang pengen kamu kunjungi berdua sama aku?",
    "Apa kalimat rayuan yang paling mempan buat kamu?",
    "Kalau kita bisa kencan mewah tanpa batas budget, kamu mau ngapain?",
    "Hal apa yang bisa bikin kamu langsung baper sama seseorang?",
    "Apa tipe sentuhan yang paling bikin kamu merasa dicintai?",
    "Pernah nggak kamu punya pikiran nakal tentang aku di tempat umum?",
    "Apa yang pengen kamu lakukan kalau kita berdua sendirian tanpa gangguan seharian penuh?",
    "Apa kata-kata dari aku yang paling bikin kamu meleleh?",
    "Kalau kamu bisa milih, mau kencan di mana yang paling romantis dan intim?",
    "Apa hal yang bikin kamu merasa paling dicintai oleh aku?",
    "Bagaimana cara pelukan yang paling kamu suka dari aku?",
    "Apa yang kamu pikirkan saat aku pergi dan kita lagi LDR?",
]

DARE_NORMAL = [
    {"text": "Nyanyiin lagu favorit kamu dengan suara paling fals selama 30 detik!", "timer": 30},
    {"text": "Kirim pesan 'I love you' ke kontak pertama di HP kamu (selain aku)!", "timer": 0},
    {"text": "Lakukan 10 push-up sekarang juga!", "timer": 60},
    {"text": "Telepon seseorang secara acak dan bilang 'Halo, ini dari pizza?'", "timer": 0},
    {"text": "Posting foto paling jelek kamu di story selama 5 menit!", "timer": 300},
    {"text": "Tirukan gaya jalan model catwalk dari ujung ruangan ke ujung lainnya!", "timer": 20},
    {"text": "Minta aku foto kamu dengan pose paling aneh!", "timer": 30},
    {"text": "Ceritain lelucon terbodoh yang kamu tahu!", "timer": 60},
    {"text": "Bicara dengan aksen bahasa Inggris Inggris selama 2 menit ke depan!", "timer": 120},
    {"text": "Kirim GIF paling memalukan ke grup keluarga!", "timer": 0},
    {"text": "Makan sesuatu dengan mata tertutup dan tebak apa itu!", "timer": 30},
    {"text": "Dance selama 1 menit dengan lagu yang aku pilihkan!", "timer": 60},
    {"text": "Lakukan 20 lompatan bintang (jumping jack) sekarang!", "timer": 60},
    {"text": "Ceritakan kisah hidup kamu dalam 60 detik!", "timer": 60},
    {"text": "Tirukan suara 3 binatang berbeda!", "timer": 30},
    {"text": "Tulis status WA yang aneh dan biarkan selama 10 menit!", "timer": 600},
    {"text": "Lakukan push-up sambil menyebut nama aku setiap kali turun!", "timer": 45},
    {"text": "Berikan pidato singkat tentang betapa luar biasanya aku!", "timer": 60},
    {"text": "Tirukan 3 seleb berbeda dalam 1 menit!", "timer": 60},
    {"text": "Gambar potret wajahku dalam 30 detik!", "timer": 30},
]

DARE_18PLUS = [
    {"text": "Berikan pijatan bahu ke aku selama 2 menit!", "timer": 120},
    {"text": "Bisikkan kata-kata manis di telinga aku selama 30 detik!", "timer": 30},
    {"text": "Cium kening aku tiga kali berturut-turut!", "timer": 0},
    {"text": "Peluk aku dari belakang selama 1 menit penuh tanpa bicara!", "timer": 60},
    {"text": "Tuliskan namaku di tanganmu sekarang!", "timer": 30},
    {"text": "Kirim voice note yang isinya kamu nyatain cinta dengan serius!", "timer": 0},
    {"text": "Pegang tanganku dan tatap mataku selama 30 detik tanpa senyum!", "timer": 30},
    {"text": "Deskripsikan aku menggunakan 5 kata yang paling romantis menurut kamu!", "timer": 60},
    {"text": "Berikan aku compliment tulus tentang 3 hal berbeda dari aku!", "timer": 60},
    {"text": "Nyanyi lagu romantis untuk aku meski fals, selama 1 menit!", "timer": 60},
    {"text": "Kirim pesan panjang ke aku tentang kenapa kamu bersyukur kita bersama!", "timer": 0},
    {"text": "Gambar hati di tangan aku menggunakan jarimu!", "timer": 20},
    {"text": "Bilang 'Aku sayang kamu' dengan 5 bahasa berbeda!", "timer": 60},
    {"text": "Berikan ciuman di pipi aku sekarang!", "timer": 0},
    {"text": "Rekam video pendek 30 detik tentang hal yang paling kamu cintai dari aku!", "timer": 30},
]

# ─────────────────────────────────────────────
#   HELPER FUNCTIONS
# ─────────────────────────────────────────────

def get_main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🤔 TRUTH", callback_data="truth_menu"),
            InlineKeyboardButton("🔥 DARE", callback_data="dare_menu"),
        ],
        [InlineKeyboardButton("🎲 RANDOM!", callback_data="random_all")],
        [InlineKeyboardButton("📊 Skor Kita", callback_data="score")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_truth_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("😇 Normal", callback_data="truth_normal"),
            InlineKeyboardButton("🌶️ Berani", callback_data="truth_18"),
        ],
        [InlineKeyboardButton("🔙 Kembali", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_dare_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("😇 Normal", callback_data="dare_normal"),
            InlineKeyboardButton("🌶️ Berani", callback_data="dare_18"),
        ],
        [InlineKeyboardButton("🔙 Kembali", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_after_keyboard(has_timer=False, timer_seconds=0, callback_timer=""):
    keyboard = []
    if has_timer and timer_seconds > 0:
        keyboard.append([InlineKeyboardButton(
            f"⏱️ Mulai Timer {timer_seconds}s", callback_data=f"timer_{timer_seconds}"
        )])
    keyboard.append([
        InlineKeyboardButton("🤔 Truth Lagi", callback_data="truth_menu"),
        InlineKeyboardButton("🔥 Dare Lagi", callback_data="dare_menu"),
    ])
    keyboard.append([InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

# ─────────────────────────────────────────────
#   COMMAND HANDLERS
# ─────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if "scores" not in context.chat_data:
        context.chat_data["scores"] = {}
    
    text = (
        f"🎮 *Halo, {user.first_name}!* Selamat datang di\n\n"
        "💕 *TRUTH OR DARE — Couple Edition* 💕\n\n"
        "Permainan jujur-jujuran dan tantangan seru buat kalian berdua! "
        "Ada mode normal dan mode *berani* 🌶️\n\n"
        "Pilih giliran siapa dulu, lalu mulai! 🎲"
    )
    await update.message.reply_text(
        text, parse_mode="Markdown", reply_markup=get_main_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📖 *Cara Main Truth or Dare:*\n\n"
        "1️⃣ Pilih *TRUTH* untuk pertanyaan jujur-jujuran\n"
        "2️⃣ Pilih *DARE* untuk tantangan\n"
        "3️⃣ Pilih *RANDOM* biar bot yang milih!\n"
        "4️⃣ Mode *Normal* = aman dan seru\n"
        "5️⃣ Mode *Berani* 🌶️ = lebih intim & romantis\n\n"
        "⏱️ Tantangan dengan timer: kamu harus selesaikan dalam waktu yang ditentukan!\n\n"
        "Gunakan /skor untuk lihat poin kalian.\n"
        "Gunakan /reset untuk mulai ulang permainan."
    )
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=get_main_keyboard())

async def skor_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    scores = context.chat_data.get("scores", {})
    if not scores:
        text = "📊 Belum ada skor! Mainkan dulu yuk~ 🎮"
    else:
        text = "📊 *Skor Kalian:*\n\n"
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        medals = ["🥇", "🥈", "🥉"]
        for i, (name, score) in enumerate(sorted_scores):
            medal = medals[i] if i < 3 else "🏅"
            text += f"{medal} *{name}*: {score} poin\n"
    await update.message.reply_text(text, parse_mode="Markdown")

async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.chat_data["scores"] = {}
    await update.message.reply_text(
        "🔄 *Permainan di-reset!* Mulai lagi dari awal ya~ 💕",
        parse_mode="Markdown", reply_markup=get_main_keyboard()
    )

# ─────────────────────────────────────────────
#   CALLBACK HANDLERS
# ─────────────────────────────────────────────

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main_menu":
        await query.edit_message_text(
            "🎮 *TRUTH OR DARE — Couple Edition* 💕\n\nPilih giliran siapa dulu!",
            parse_mode="Markdown", reply_markup=get_main_keyboard()
        )

    elif data == "truth_menu":
        await query.edit_message_text(
            "🤔 *TRUTH* — Pilih levelnya:\n\n"
            "😇 *Normal* — Pertanyaan seru dan lucu\n"
            "🌶️ *Berani* — Lebih intim dan romantis",
            parse_mode="Markdown", reply_markup=get_truth_keyboard()
        )

    elif data == "dare_menu":
        await query.edit_message_text(
            "🔥 *DARE* — Pilih levelnya:\n\n"
            "😇 *Normal* — Tantangan seru dan kocak\n"
            "🌶️ *Berani* — Lebih intim dan romantis",
            parse_mode="Markdown", reply_markup=get_dare_keyboard()
        )

    elif data == "truth_normal":
        q = random.choice(TRUTH_NORMAL)
        text = f"🤔 *TRUTH — Normal*\n\n_{q}_\n\n✅ Jawab dengan jujur ya!"
        await query.edit_message_text(
            text, parse_mode="Markdown", reply_markup=get_after_keyboard()
        )

    elif data == "truth_18":
        q = random.choice(TRUTH_18PLUS)
        text = f"🌶️ *TRUTH — Berani*\n\n_{q}_\n\n✅ Jujur ya, nggak boleh bohong! 😏"
        await query.edit_message_text(
            text, parse_mode="Markdown", reply_markup=get_after_keyboard()
        )

    elif data == "dare_normal":
        d = random.choice(DARE_NORMAL)
        has_timer = d["timer"] > 0
        text = (
            f"🔥 *DARE — Normal*\n\n_{d['text']}_\n\n"
            + (f"⏱️ Waktu: *{d['timer']} detik*" if has_timer else "")
        )
        await query.edit_message_text(
            text, parse_mode="Markdown",
            reply_markup=get_after_keyboard(has_timer, d["timer"])
        )

    elif data == "dare_18":
        d = random.choice(DARE_18PLUS)
        has_timer = d["timer"] > 0
        text = (
            f"🌶️ *DARE — Berani*\n\n_{d['text']}_\n\n"
            + (f"⏱️ Waktu: *{d['timer']} detik*" if has_timer else "")
        )
        await query.edit_message_text(
            text, parse_mode="Markdown",
            reply_markup=get_after_keyboard(has_timer, d["timer"])
        )

    elif data == "random_all":
        coin = random.choice(["truth", "dare"])
        level = random.choice(["normal", "berani"])

        if coin == "truth":
            pool = TRUTH_NORMAL if level == "normal" else TRUTH_18PLUS
            q = random.choice(pool)
            emoji = "😇" if level == "normal" else "🌶️"
            text = f"🎲 *RANDOM — TRUTH {emoji}*\n\n_{q}_\n\n✅ Jawab dengan jujur!"
            await query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=get_after_keyboard()
            )
        else:
            pool = DARE_NORMAL if level == "normal" else DARE_18PLUS
            d = random.choice(pool)
            has_timer = d["timer"] > 0
            emoji = "😇" if level == "normal" else "🌶️"
            text = (
                f"🎲 *RANDOM — DARE {emoji}*\n\n_{d['text']}_\n\n"
                + (f"⏱️ Waktu: *{d['timer']} detik*" if has_timer else "")
            )
            await query.edit_message_text(
                text, parse_mode="Markdown",
                reply_markup=get_after_keyboard(has_timer, d["timer"])
            )

    elif data == "score":
        scores = context.chat_data.get("scores", {})
        if not scores:
            text = "📊 Belum ada skor! Mainkan dulu yuk~ 🎮"
        else:
            text = "📊 *Skor Kalian:*\n\n"
            for name, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
                text += f"• *{name}*: {score} poin\n"
        keyboard = [[InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")]]
        await query.edit_message_text(
            text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("timer_"):
        seconds = int(data.split("_")[1])
        mins = seconds // 60
        secs = seconds % 60
        time_str = f"{mins}m {secs}s" if mins > 0 else f"{secs}s"
        
        # Kirim pesan timer countdown
        msg = await query.message.reply_text(
            f"⏱️ *Timer dimulai!* — {time_str}\n\n🟢 MULAI SEKARANG!",
            parse_mode="Markdown"
        )
        
        # Countdown setiap 10 detik
        remaining = seconds
        checkpoints = []
        while remaining > 10:
            remaining -= 10
            checkpoints.append(remaining)
        
        for cp in checkpoints:
            await asyncio.sleep(10)
            try:
                await msg.edit_text(
                    f"⏱️ *Timer berjalan...*\n\n⏳ Sisa: *{cp} detik*",
                    parse_mode="Markdown"
                )
            except Exception:
                pass
        
        await asyncio.sleep(min(10, seconds))
        try:
            await msg.edit_text(
                "🔔 *WAKTU HABIS!* ⏰\n\n"
                "Apakah berhasil? 🎉",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("✅ Berhasil (+1 poin)", callback_data=f"win_{query.from_user.first_name}"),
                    InlineKeyboardButton("❌ Gagal", callback_data="fail"),
                ]])
            )
        except Exception:
            pass

    elif data.startswith("win_"):
        name = data.split("_", 1)[1]
        if "scores" not in context.chat_data:
            context.chat_data["scores"] = {}
        context.chat_data["scores"][name] = context.chat_data["scores"].get(name, 0) + 1
        score = context.chat_data["scores"][name]
        await query.edit_message_text(
            f"🎉 *{name} berhasil!* +1 poin\n\n"
            f"Total skor *{name}*: {score} poin 🏆",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")
            ]])
        )

    elif data == "fail":
        await query.edit_message_text(
            "😅 *Sayang sekali!* Coba lagi next round ya~\n\nTetap semangat! 💪",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")
            ]])
        )

# ─────────────────────────────────────────────
#   MAIN
# ─────────────────────────────────────────────

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("skor", skor_command))
    app.add_handler(CommandHandler("reset", reset_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("🤖 Bot Truth or Dare aktif! Tekan Ctrl+C untuk berhenti.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
