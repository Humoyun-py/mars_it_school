import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from keybords import get_main_menu
from state import LoginStates, EditStates, FeedbackStates
from config import TOKEN, ADMIN_ID
from info import STUDENTS
from aiogram.types import (
    Message, 
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    CallbackQuery,
    FSInputFile
)

# Logging sozlash
logging.basicConfig(level=logging.INFO)


# /start komandasi
async def cmd_start(message: Message, state: FSMContext):
    """Bot boshlanishi - ID so'rash"""
    await state.clear()
    
    await message.answer(
        "🚀 <b>MARS IT School botiga xush kelibsiz!</b>\n\n"
        "Davom etish uchun <b>ID raqamingizni</b> kiriting:",
        parse_mode='HTML'
    )
    await state.set_state(LoginStates.waiting_id)

# ID qabul qilish
async def process_id(message: Message, state: FSMContext):
    """ID ni tekshirish"""
    user_id = message.text.strip()
    
    if user_id in STUDENTS:
        await state.update_data(temp_id=user_id)
        await message.answer(
            "🔐 <b>Parolingizni kiriting:</b>",
            parse_mode='HTML'
        )
        await state.set_state(LoginStates.waiting_password)
    else:
        await message.answer(
            "❌ <b>Bunday o'quvchi topilmadi!</b>\n\n"
            "Iltimos, ID raqamingizni tekshirib, qaytadan kiriting:",
            parse_mode='HTML'
        )

# Parol qabul qilish
async def process_password(message: Message, state: FSMContext):
    """Parolni tekshirish va kirish"""
    password = message.text.strip()
    data = await state.get_data()
    user_id = data.get('temp_id')
    
    if not user_id:
        await message.answer("⚠️ Xatolik! Qaytadan /start bosing.")
        await state.clear()
        return
    
    if STUDENTS[user_id]['parol'] == password:
        # Muvaffaqiyatli kirish
        await state.update_data(logged_in_id=user_id)
        student = STUDENTS[user_id]
        
        await message.answer(
            f"✅ <b>Xush kelibsiz, {student['ism']} {student['familiya']}!</b>\n\n"
            f"👤 Ism: <b>{student['ism']}</b>\n"
            f"👥 Familiya: <b>{student['familiya']}</b>\n"
            f"📚 Guruh: <b>{student['guruh']}</b>\n"
            f"🪙 Coinlar: <b>{student['coin']}</b>\n\n"
            f"Quyidagi tugmalardan birini tanlang:",
            parse_mode='HTML',
            reply_markup=get_main_menu()
        )
        await state.set_state(None)
    else:
        await message.answer(
            "❌ <b>Parol noto'g'ri!</b>\n\n"
            "Iltimos, parolni qaytadan kiriting:",
            parse_mode='HTML'
        )

# Profil ko'rsatish
async def show_profile(message: Message, state: FSMContext):
    """Foydalanuvchi profili"""
    data = await state.get_data()
    user_id = data.get('logged_in_id')
    
    if not user_id:
        await message.answer(
            "⚠️ <b>Avval tizimga kirish kerak!</b>\n"
            "Iltimos /start buyrug'ini bosing.",
            parse_mode='HTML'
        )
        return
    
    student = STUDENTS[user_id]
    
    await message.answer(
        f"👤 <b>Sizning profilingiz</b>\n\n"
        f"🆔 ID: <code>{user_id}</code>\n"
        f"👤 Ism: <b>{student['ism']}</b>\n"
        f"👥 Familiya: <b>{student['familiya']}</b>\n"
        f"📚 Guruh: <b>{student['guruh']}</b>\n"
        f"🪙 Coinlar: <b>{student['coin']}</b>",
        parse_mode='HTML',
     
    )

# Coinlar ko'rsatish
async def show_coins(message: Message, state: FSMContext):
    """Foydalanuvchi coinlari"""
    data = await state.get_data()
    user_id = data.get('logged_in_id')
    
    if not user_id:
        await message.answer(
            "⚠️ <b>Avval tizimga kirish kerak!</b>\n"
            "Iltimos /start buyrug'ini bosing.",
            parse_mode='HTML'
        )
        return
    
    student = STUDENTS[user_id]
    
    await message.answer(
        f"🪙 <b>Sizning coinlaringiz</b>\n\n"
        f"💰 Jami coinlar: <b>{student['coin']}</b>\n\n"
        f"💡 Coinlarni Space Shop'da turli sovg'alarga almashtirishingiz mumkin!",
        parse_mode='HTML'
    )

# Space Shop
async def show_space_shop(message: Message):
    """Space Shop havolasi"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🛒 Space Shop'ga o'tish", 
                url="https://space.marsit.uz/shop-page"
            )]
        ]
    )
    
    await message.answer(
        "💥 <b>Space Shop</b>\n\n"
        "Space Shop'da siz coinlaringizni quyidagilarga almashtira olasiz:\n\n"
        "🎁 Sovg'alar\n"
        "👕 Brendli kiyimlar\n"
        "💻 Texnika aksessuarlari\n"
        "📚 Kitoblar\n"
        "🎮 Va boshqalar!\n\n"
        "Quyidagi tugmani bosing:",
        parse_mode='HTML',
        reply_markup=keyboard
    )

# Maktab haqida
async def show_about_school(message: Message):
    """MARS IT School haqida"""
    photo_url = "https://marsit.uz/static/media/logo.png"
    
    try:
        await message.answer_photo(
            photo=photo_url,
            caption=(
                "🏫 <b>MARS IT School haqida</b>\n\n"
                "MARS IT School - O'zbekistondagi eng yaxshi IT ta'lim markazi!\n\n"
                "📚 <b>Bizning kurslarimiz:</b>\n"
                "• Python dasturlash\n"
                "• Web Development (Frontend/Backend)\n"
                "• Mobile Development (Android/iOS)\n"
                "• Data Science & AI\n"
                "• Grafik Dizayn\n\n"
                "🎯 <b>Bizning maqsadimiz:</b>\n"
                "Har bir o'quvchini professional IT mutaxassis qilish va ularga yorqin kelajak yaratish!\n\n"
                "🌟 <b>Afzalliklarimiz:</b>\n"
                "✅ Tajribali va professional ustozlar\n"
                "✅ Real loyihalar ustida amaliy ish\n"
                "✅ Ish bilan ta'minlash kafolati\n"
                "✅ Xalqaro sertifikatlar\n"
                "✅ Zamonaviy o'quv materiallari\n"
                "✅ Coworking zonasi\n\n"
                "📍 <b>Manzil:</b> Toshkent, Chilonzor tumani\n"
                "📞 <b>Telefon:</b> +998 90 123 45 67\n"
                "🌐 <b>Website:</b> https://marsit.uz\n"
                "📱 <b>Instagram:</b> @marsit.uz"
            ),
            parse_mode='HTML'
        )
    except Exception as e:
        await message.answer(
            "🏫 <b>MARS IT School haqida</b>\n\n"
            "MARS IT School - O'zbekistondagi eng yaxshi IT ta'lim markazi!\n\n"
            "📚 <b>Bizning kurslarimiz:</b>\n"
            "• Python dasturlash\n"
            "• Web Development (Frontend/Backend)\n"
            "• Mobile Development (Android/iOS)\n"
            "• Data Science & AI\n"
            "• Grafik Dizayn\n\n"
            "🎯 <b>Bizning maqsadimiz:</b>\n"
            "Har bir o'quvchini professional IT mutaxassis qilish va ularga yorqin kelajak yaratish!\n\n"
            "🌟 <b>Afzalliklarimiz:</b>\n"
            "✅ Tajribali va professional ustozlar\n"
            "✅ Real loyihalar ustida amaliy ish\n"
            "✅ Ish bilan ta'minlash kafolati\n"
            "✅ Xalqaro sertifikatlar\n"
            "✅ Zamonaviy o'quv materiallari\n"
            "✅ Coworking zonasi\n\n"
            "📍 <b>Manzil:</b> Toshkent, Chilonzor tumani\n"
            "📞 <b>Telefon:</b> +998 90 123 45 67\n"
            "🌐 <b>Website:</b> https://marsit.uz\n"
            "📱 <b>Instagram:</b> @marsit.uz",
            parse_mode='HTML'
        )

# Fikr-mulohaza yuborish
async def start_feedback(message: Message, state: FSMContext):
    """Fikr-mulohaza jarayonini boshlash"""
    data = await state.get_data()
    user_id = data.get('logged_in_id')
    
    if not user_id:
        await message.answer(
            "⚠️ <b>Avval tizimga kirish kerak!</b>\n"
            "Iltimos /start buyrug'ini bosing.",
            parse_mode='HTML'
        )
        return
    
    await message.answer(
        "📝 <b>Fikr-mulohaza qoldirish</b>\n\n"
        "Iltimos, fikr-mulohazangizni yozing.\n"
        "Biz sizning fikringizni qadrlaymiz va doim takomillashishga intilamiz! 💙\n\n"
        "✍️ Fikringizni yozing:",
        parse_mode='HTML'
    )
    await state.set_state(FeedbackStates.waiting_feedback)

# Fikr-mulohaza qabul qilish va adminga yuborish
async def receive_feedback(message: Message, state: FSMContext, bot: Bot):
    """Fikr-mulohazani qabul qilish va adminga yuborish"""
    data = await state.get_data()
    user_id = data.get('logged_in_id')
    
    if not user_id:
        await message.answer(
            "⚠️ <b>Avval tizimga kirish kerak!</b>",
            parse_mode='HTML'
        )
        await state.clear()
        return
    
    feedback_text = message.text
    student = STUDENTS[user_id]
    
    # Adminga fikr-mulohaza yuborish
    # Prepare a safe username display string to avoid backslashes inside f-string expressions
    username_display = message.from_user.username if message.from_user.username else "Username yo'q"

    admin_message = (
        "📨 <b>Yangi fikr-mulohaza keldi!</b>\n\n"
        f"👤 <b>O'quvchi:</b> {student['ism']} {student['familiya']}\n"
        f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
        f"📚 <b>Guruh:</b> {student['guruh']}\n"
        f"💬 <b>Telegram:</b> @{username_display}\n"
        f"🆔 <b>Telegram ID:</b> <code>{message.from_user.id}</code>\n\n"
        f"💬 <b>Fikr-mulohaza:</b>\n"
        f"{feedback_text}"
    )
    
    try:
        # Adminga yuborish
        await bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_message,
            parse_mode='HTML'
        )
        
        # Foydalanuvchiga tasdiqlash
        await message.answer(
            "✅ <b>Rahmat!</b>\n\n"
            f"Sizning fikr-mulohazangiz qabul qilindi va administratorga yuborildi.\n\n"
            f"Bizning xizmatimizni yaxshilashga yordam berganingiz uchun tashakkur! 💙",
            parse_mode='HTML',
            reply_markup=get_main_menu()
        )
    except Exception as e:
        logging.error(f"Adminga yuborishda xatolik: {e}")
        await message.answer(
            "⚠️ <b>Xatolik yuz berdi!</b>\n\n"
            "Iltimos, keyinroq qayta urinib ko'ring.",
            parse_mode='HTML',
            reply_markup=get_main_menu()
        )
    
    await state.set_state(None)

# Inline tugmalar uchun callback
async def process_callback(callback: CallbackQuery, state: FSMContext):
    """Inline tugmalarni qayta ishlash"""
    data = await state.get_data()
    user_id = data.get('logged_in_id')
    
    if not user_id:
        await callback.answer("⚠️ Tizimga kirish kerak!", show_alert=True)
        return
    
    if callback.data.startswith("edit_name_"):
        await callback.message.answer(
            "✏️ <b>Yangi ismingizni kiriting:</b>",
            parse_mode='HTML',
            reply_markup=get_main_menu()
        )
        await state.set_state(EditStates.waiting_new_name)
        await callback.answer()
        
    elif callback.data.startswith("edit_surname_"):
        await callback.message.answer(
            "✏️ <b>Yangi familiyangizni kiriting:</b>",
            parse_mode='HTML',
            reply_markup=get_main_menu()
        )
        await state.set_state(EditStates.waiting_new_surname)
        await callback.answer()

# Yangi ism qabul qilish
async def process_new_name(message: Message, state: FSMContext):
    """Yangi ismni saqlash"""
    data = await state.get_data()
    user_id = data.get('logged_in_id')
    
    if not user_id:
        await message.answer("⚠️ Xatolik! /start bosing.")
        await state.clear()
        return
    
    new_name = message.text.strip()
    STUDENTS[user_id]['ism'] = new_name
    
    await message.answer(
        f"✅ <b>Ismingiz muvaffaqiyatli o'zgartirildi!</b>\n\n"
        f"Yangi ism: <b>{new_name}</b>",
        parse_mode='HTML',
        reply_markup=get_main_menu()
    )
    await state.set_state(None)

# Yangi familiya qabul qilish
async def process_new_surname(message: Message, state: FSMContext):
    """Yangi familiyani saqlash"""
    data = await state.get_data()
    user_id = data.get('logged_in_id')
    
    if not user_id:
        await message.answer("⚠️ Xatolik! /start bosing.")
        await state.clear()
        return
    
    new_surname = message.text.strip()
    STUDENTS[user_id]['familiya'] = new_surname
    
    await message.answer(
        f"✅ <b>Familiyangiz muvaffaqiyatli o'zgartirildi!</b>\n\n"
        f"Yangi familiya: <b>{new_surname}</b>",
        parse_mode='HTML',
        reply_markup=get_main_menu()
    )
    await state.set_state(None)

async def main():
    """Botni ishga tushirish"""
    # O'z bot tokeningizni kiriting
    TOKEN 
    
    # Bot va Dispatcher yaratish
    bot = Bot(token=TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Komanda handler'lar
    dp.message.register(cmd_start, Command("start"))
    
    # State handler'lar - Login
    dp.message.register(process_id, LoginStates.waiting_id)
    dp.message.register(process_password, LoginStates.waiting_password)
    
    # State handler'lar - Tahrirlash
    dp.message.register(process_new_name, EditStates.waiting_new_name)
    dp.message.register(process_new_surname, EditStates.waiting_new_surname)
    
    # State handler'lar - Fikr-mulohaza (bot parametrini qo'shdik)
    async def _receive_feedback_wrapper(msg: Message, state: FSMContext):
        # await the actual coroutine to avoid 'coroutine was never awaited' warnings
        await receive_feedback(msg, state, bot)

    dp.message.register(
        _receive_feedback_wrapper,
        FeedbackStates.waiting_feedback
    )
    
    # Menyu handler'lar
    dp.message.register(show_profile, F.text == "🧑‍🎓 Профиль")
    dp.message.register(show_coins, F.text == "🪙 Мои монеты")
    dp.message.register(show_space_shop, F.text == "💥 Space Shop")
    dp.message.register(show_about_school, F.text == "🏫 О школе")
    dp.message.register(start_feedback, F.text == "✍️ Оставить отзыв")
    
    # Callback handler
    dp.callback_query.register(process_callback)
    
    # Botni ishga tushirish
    print("🚀 Bot ishga tushdi!")
    print("✅ Tayyor ishlashga!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())