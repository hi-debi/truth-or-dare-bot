"""
Truth or Dare Bot — Group Edition 🎮
Bot ikut komentar jawaban pemain secara random & lucu
pip install python-telegram-bot==21.6
"""

import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

BOT_TOKEN = "8588161571:AAEoEcZEX-lKsK9N_kcmdS8PF0-gE3zRzoM"

TRUTH_NORMAL = [
    "Siapa orang yang paling sering kamu stalking di media sosial?",
    "Apa kebohongan terbesar yang pernah kamu ucapkan ke orang tua?",
    "Pernah nggak kamu suka sama teman sendiri? Siapa?",
    "Apa hal paling memalukan yang pernah terjadi padamu di depan umum?",
    "Kalau bisa hapus satu memory, memory apa yang kamu pilih?",
    "Siapa di grup ini yang menurutmu paling misterius?",
    "Apa hal yang paling kamu sembunyikan dari teman-teman di sini?",
    "Pernah nggak kamu nangis gara-gara nonton film/drakor? Film apa?",
    "Apa makanan yang paling kamu benci tapi pura-pura suka?",
    "Siapa di grup ini yang pertama kamu hubungi kalau ada masalah?",
    "Pernah nggak kamu sengaja ignore chat seseorang? Siapa?",
    "Berapa lama waktu terlama kamu tidak mandi?",
    "Apa hal paling konyol yang pernah kamu lakuin demi gebetan?",
    "Pernah nggak kamu bohong soal posisi kamu ke orang tua?",
    "Siapa di grup ini yang paling kamu kagumi diam-diam?",
    "Apa kebiasaan jelek kamu yang tidak banyak orang tahu?",
    "Kapan terakhir kali kamu nangis dan kenapa?",
    "Apa hal yang paling kamu sesali dalam hidup?",
    "Siapa mantan yang masih kamu stalk sampai sekarang?",
    "Pernah nggak kamu pura-pura sakit biar nggak masuk sekolah/kerja?",
    "Apa ketakutan terbesar kamu yang belum banyak orang tahu?",
    "Pernah nggak kamu naksir teman yang sudah punya pacar?",
    "Kalau bisa jujur ke satu orang di grup ini, apa yang mau kamu katakan?",
    "Berapa nilai paling jelek yang pernah kamu dapat dan mata pelajaran apa?",
    "Apa lagu yang selalu kamu putar waktu galau?",
    "Siapa di grup ini yang paling susah dibaca perasaannya?",
    "Pernah nggak kamu baca chat orang lain tanpa izin?",
    "Apa aplikasi yang paling banyak kamu pakai tapi malu ngakuinnya?",
    "Apa hal paling mahal yang pernah kamu sembunyikan dari orang tua?",
    "Pernah nggak kamu kirim pesan ke orang yang salah? Isi pesannya apa?",
]

TRUTH_BERANI = [
    "Siapa di grup ini yang menurutmu paling good-looking?",
    "Pernah nggak kamu punya perasaan lebih ke salah satu orang di grup ini?",
    "Apa tipe orang yang bikin kamu langsung baper?",
    "Ceritakan pengalaman kencan paling canggung yang pernah kamu alami!",
    "Siapa yang pertama kali kamu suka dan apa yang terjadi?",
    "Pernah nggak kamu di-ghosting? Bagaimana perasaanmu?",
    "Apa hal romantis yang ingin kamu lakukan tapi belum kesampaian?",
    "Siapa orang yang pernah bikin jantung kamu deg-degan cuma dengan tatapannya?",
    "Apa yang bikin kamu jatuh cinta sama seseorang?",
    "Pernah nggak kamu naksir teman dekat sendiri?",
    "Kalau harus pilih satu orang di grup ini untuk dijadikan pasangan, siapa?",
    "Apa hal paling berani yang pernah kamu lakukan untuk seseorang yang kamu suka?",
    "Apa tipe pasangan ideal kamu? Sebutkan 3 kriteria!",
    "Pernah nggak kamu dapat atau kirim pesan yang terlalu personal ke orang yang salah?",
    "Kalau bisa kencan sama satu orang di grup ini, siapa yang kamu pilih?",
]

DARE_NORMAL = [
    {"text": "Nyanyikan lagu yang sedang hits sekarang selama 30 detik, harus keras!", "timer": 30},
    {"text": "Lakukan 15 push-up sekarang juga di depan semua orang!", "timer": 90},
    {"text": "Kirim pesan 'Aku kangen kamu 😘' ke kontak pertama di HP kamu!", "timer": 0},
    {"text": "Tirukan gaya bicara dan tingkah laku salah satu orang di grup ini!", "timer": 30},
    {"text": "Posting foto selfie paling jelek kamu di story selama 5 menit!", "timer": 300},
    {"text": "Telepon seseorang secara acak dari kontakmu dan bilang 'Halo, ini dari pizza?'", "timer": 0},
    {"text": "Lakukan catwalk dari ujung ruangan ke ujung lainnya dengan pose model!", "timer": 20},
    {"text": "Ceritakan lelucon terbodoh yang kamu tahu!", "timer": 60},
    {"text": "Bicara dengan aksen Sunda/Jawa/Batak selama 2 menit ke depan!", "timer": 120},
    {"text": "Lakukan 20 jumping jack sambil menyebut nama orang di sebelahmu!", "timer": 60},
    {"text": "Gambar potret salah satu orang di grup dalam 30 detik, tunjukkan hasilnya!", "timer": 30},
    {"text": "Tirukan 3 seleb Indonesia yang berbeda dalam 1 menit!", "timer": 60},
    {"text": "Kirim GIF paling cringe ke grup keluarga dan screenshot reaksinya!", "timer": 0},
    {"text": "Berikan pidato motivasi selama 1 menit dengan penuh semangat!", "timer": 60},
    {"text": "Tirukan suara 5 binatang berbeda!", "timer": 30},
    {"text": "Buat status WA yang aneh dan biarkan minimal 10 menit!", "timer": 600},
    {"text": "Lakukan gerakan dance TikTok paling viral yang kamu tahu selama 30 detik!", "timer": 30},
    {"text": "Ceritakan kisah hidupmu dalam 60 detik, harus dramatis!", "timer": 60},
    {"text": "Lakukan plank selama 30 detik!", "timer": 30},
    {"text": "Foto bareng orang di sebelahmu dengan ekspresi paling lebay!", "timer": 30},
    {"text": "Berdiri dan lakukan gerakan senam poco-poco selama 30 detik!", "timer": 30},
    {"text": "Tirukan cara jalan robot selama 1 menit!", "timer": 60},
    {"text": "Makan sesuatu dengan mata tertutup dan tebak apa itu!", "timer": 30},
    {"text": "Berikan pidato singkat betapa luar biasanya orang di sebelahmu!", "timer": 45},
    {"text": "Kirim voice note nyanyi ke grup keluarga kamu!", "timer": 0},
]

DARE_BERANI = [
    {"text": "Bisikkan kata-kata gombal ke telinga orang di sebelahmu!", "timer": 0},
    {"text": "Berikan pijatan bahu ke orang di sebelahmu selama 1 menit!", "timer": 60},
    {"text": "Tulis nama crush kamu di tangan dan tunjukkan ke semua orang!", "timer": 30},
    {"text": "Kirim voice note ke mantan/gebetanmu dengan isi 'Aku kangen'!", "timer": 0},
    {"text": "Pegang tangan orang di sebelahmu dan tatap matanya selama 30 detik tanpa ketawa!", "timer": 30},
    {"text": "Ceritakan tipe idealmu dengan detail di depan semua orang!", "timer": 60},
    {"text": "Kirim pesan 'Aku suka kamu' ke gebetan kamu sekarang!", "timer": 0},
    {"text": "Nyanyikan lagu romantis untuk orang di sebelahmu meski fals, minimal 1 menit!", "timer": 60},
    {"text": "Ceritakan pengalaman jatuh cinta pertamamu dengan detail!", "timer": 90},
    {"text": "Tuliskan nama orang yang kamu suka di kertas dan tunjukkan ke semua orang!", "timer": 0},
    {"text": "Bilang 'Kamu cantik/ganteng banget' ke setiap orang di grup satu per satu!", "timer": 60},
    {"text": "Deskripsikan orang yang kamu suka tanpa menyebut nama, biarkan orang lain tebak!", "timer": 60},
    {"text": "Berikan high five ke semua orang di grup sambil bilang 'Kamu luar biasa!'", "timer": 30},
    {"text": "Rekam video 30 detik kenapa kamu masih jomblo / kenapa kamu happy punya pasangan!", "timer": 30},
    {"text": "Minta foto bareng salah satu orang di grup dengan gaya paling romantis!", "timer": 30},
]

KOMENTAR_TRUTH = [
    "Wkwkwk jujur banget sih! Respect! 😂🔥",
    "Ohhh serius?! Nggak nyangka sama sekali! 👀",
    "Hahaha makasih udah jujur, berani banget~ 😄",
    "Itu sih... cukup mengejutkan wkwk 😮",
    "Wow, berani banget ngaku! Salut! 🔥",
    "Hmmm... noted. Kita semua tau sekarang 😏",
    "HAHAHA aku nggak nyangka sih 💀",
    "Anjay jujur banget, aku kira bakal bohong 😂",
    "Oalah jadi gitu ceritanya~ 👁️👁️",
    "Makasih kejujurannya! Sekarang kita tau rahasiamu 🤭",
    "Itu... lebih dari yang aku perkirakan 😅",
    "Nah lho ketauan deh! Wkwkwk 😆",
]

KOMENTAR_DARE = [
    "Yesss berhasil! Gila berani banget! 🔥🔥",
    "Wkwkwk itu tadi epic banget sumpah 😂",
    "Mantap jiwa! Nggak ada takut-takutnya 💪",
    "Hahahaha aku nggak bisa, kocak banget 💀",
    "Itu tadi keren banget, salut! 👏",
    "Wah berani! Aku mah nggak bakalan mau 😅",
    "Goks sih, beneran dilakuin! Respect 🫡",
    "HAHAHA aku ngakak nonton itu 😂😂",
    "Legit keren! Challenge accepted dan berhasil! ✅",
    "Nggak nyangka beneran mau, hebat! 🎉",
]

AJAKAN_NEXT = [
    "Oke sekarang giliran siapa? Jangan pada kabur! 👇",
    "Next player mana nih? Berani nggak? 😏",
    "Siapa yang berani giliran berikutnya? 🎯",
    "Yuk lanjut! Giliran siapa sekarang? 👀",
    "Satu lagi! Siapa yang mau cobain? 🎲",
    "Jangan berhenti di sini dong~ Siapa next? 🔥",
    "Ayo ayo, siapa yang berani giliran berikutnya? 💪",
    "Mantap! Sekarang giliran siapa lagi nih? 🎮",
]

def main_keyboard(mode="normal"):
    label = "🌶️ Berani ON" if mode == "berani" else "😇 Normal ON"
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🤔 TRUTH", callback_data="get_truth"),
            InlineKeyboardButton("🔥 DARE", callback_data="get_dare"),
        ],
        [InlineKeyboardButton("🎲 ACAK!", callback_data="get_acak")],
        [InlineKeyboardButton(label, callback_data="toggle_mode")],
    ])

def play_again_keyboard(timer=0):
    rows = []
    if timer > 0:
        rows.append([InlineKeyboardButton(f"⏱️ Mulai Timer {timer}s", callback_data=f"timer_{timer}")])
    rows.append([
        InlineKeyboardButton("🤔 TRUTH", callback_data="get_truth"),
        InlineKeyboardButton("🔥 DARE", callback_data="get_dare"),
    ])
    rows.append([InlineKeyboardButton("🎲 ACAK!", callback_data="get_acak")])
    return InlineKeyboardMarkup(rows)

def get_mode(context):
    return context.chat_data.get("mode", "normal")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = get_mode(context)
    context.chat_data["last_question"] = None
    text = (
        "🎮 *TRUTH OR DARE — Siap main!*\n\n"
        "• Klik *TRUTH* → dapat pertanyaan jujur-jujuran\n"
        "• Klik *DARE* → dapat tantangan\n"
        "• Klik *ACAK* → bot yang milih!\n\n"
        "💬 _Reply pesan bot setelah jawab — bot ikut komentar!_\n\n"
        "Giliran siapa dulu? 👇"
    )
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=main_keyboard(mode))

async def skor_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    scores = context.chat_data.get("scores", {})
    if not scores:
        await update.message.reply_text("📊 Belum ada skor! Mulai main dulu~")
        return
    text = "📊 *Skor Permainan:*\n\n"
    medals = ["🥇", "🥈", "🥉"]
    for i, (name, score) in enumerate(sorted(scores.items(), key=lambda x: x[1], reverse=True)):
        medal = medals[i] if i < 3 else "🏅"
        text += f"{medal} *{name}*: {score} poin\n"
    await update.message.reply_text(text, parse_mode="Markdown")

async def reset_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.chat_data["scores"] = {}
    context.chat_data["last_question"] = None
    await update.message.reply_text("🔄 Skor di-reset! Mulai lagi~")

async def handle_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.reply_to_message:
        return
    if not msg.reply_to_message.from_user or not msg.reply_to_message.from_user.is_bot:
        return

    last_q = context.chat_data.get("last_question")
    if not last_q:
        return

    q_type = last_q.get("type", "truth")
    player_name = msg.from_user.first_name

    if q_type == "truth":
        komentar = random.choice(KOMENTAR_TRUTH)
    else:
        komentar = random.choice(KOMENTAR_DARE)

    ajakan = random.choice(AJAKAN_NEXT)

    await msg.reply_text(
        f"🎮 {komentar}\n\n{ajakan}",
        reply_markup=play_again_keyboard()
    )

    context.chat_data["last_question"] = None

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user = query.from_user.first_name
    mode = get_mode(context)

    if data == "toggle_mode":
        new_mode = "berani" if mode == "normal" else "normal"
        context.chat_data["mode"] = new_mode
        label = "🌶️ Mode Berani aktif!" if new_mode == "berani" else "😇 Mode Normal aktif!"
        await query.answer(label, show_alert=True)
        try:
            await query.edit_message_reply_markup(reply_markup=main_keyboard(new_mode))
        except Exception:
            pass
        return

    if data in ("get_truth", "get_dare", "get_acak"):
        if data == "get_truth":
            q_type = "truth"
        elif data == "get_dare":
            q_type = "dare"
        else:
            q_type = random.choice(["truth", "dare"])

        emoji = "🌶️" if mode == "berani" else "😇"

        if q_type == "truth":
            pool = TRUTH_BERANI if mode == "berani" else TRUTH_NORMAL
            q = random.choice(pool)
            label = f"🎲 *ACAK → TRUTH {emoji}*" if data == "get_acak" else f"🤔 *TRUTH {emoji}*"
            text = (
                f"{label}\n"
                f"_Giliran: {user}_\n\n"
                f"_{q}_\n\n"
                f"✅ Jawab dengan jujur!\n"
                f"💬 _Reply pesan ini dengan jawabanmu_"
            )
            context.chat_data["last_question"] = {"type": "truth", "text": q, "player": user}
            await query.edit_message_text(text, parse_mode="Markdown", reply_markup=play_again_keyboard())

        else:
            pool = DARE_BERANI if mode == "berani" else DARE_NORMAL
            d = random.choice(pool)
            timer_text = f"\n\n⏱️ *Waktu: {d['timer']} detik*" if d["timer"] > 0 else ""
            label = f"🎲 *ACAK → DARE {emoji}*" if data == "get_acak" else f"🔥 *DARE {emoji}*"
            text = (
                f"{label}\n"
                f"_Giliran: {user}_\n\n"
                f"_{d['text']}_{timer_text}\n\n"
                f"💬 _Reply pesan ini setelah selesai!_"
            )
            context.chat_data["last_question"] = {"type": "dare", "text": d["text"], "player": user}
            await query.edit_message_text(text, parse_mode="Markdown", reply_markup=play_again_keyboard(d["timer"]))

    elif data.startswith("timer_"):
        seconds = int(data.split("_")[1])
        msg = await query.message.reply_text(
            f"⏱️ *Timer dimulai!* — {seconds} detik\n\n🟢 *MULAI SEKARANG!*",
            parse_mode="Markdown"
        )
        total = seconds
        remaining = seconds
        while remaining > 10:
            await asyncio.sleep(10)
            remaining -= 10
            pct = remaining / total
            bar = "🟩" * int(pct * 10) + "⬜" * (10 - int(pct * 10))
            try:
                await msg.edit_text(f"⏱️ *Timer berjalan...*\n\n{bar}\n⏳ Sisa: *{remaining} detik*", parse_mode="Markdown")
            except Exception:
                pass
        await asyncio.sleep(remaining)
        try:
            await msg.edit_text(
                "🔔 *WAKTU HABIS!* ⏰\n\nApakah berhasil? 👇",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("✅ Berhasil (+1)", callback_data=f"win_{query.from_user.first_name}"),
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
            f"🎉 *{name} berhasil!* +1 poin\nTotal: *{score} poin* 🏆",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎮 Lanjut Main!", callback_data="get_acak")]])
        )

    elif data == "fail":
        await query.edit_message_text(
            f"😅 Sayang sekali, *{user}*! Coba lagi next round~",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎮 Lanjut Main!", callback_data="get_acak")]])
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("skor", skor_cmd))
    app.add_handler(CommandHandler("reset", reset_cmd))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(
        filters.TEXT & filters.REPLY & ~filters.COMMAND,
        handle_reply
    ))
    print("🎮 Bot Truth or Dare aktif!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
