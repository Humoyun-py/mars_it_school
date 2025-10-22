from aiogram.types import ( 
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
)
def get_main_menu():
    """Asosiy menyu klaviaturasi"""
    keyboard = [
        [
            KeyboardButton(text="🧑‍🎓 Профиль"), 
            KeyboardButton(text="🪙 Мои монеты")
        ],
        [
            KeyboardButton(text="💥 Space Shop"), 
            KeyboardButton(text="🏫 О школе")
        ],
        [
            KeyboardButton(text="✍️ Оставить отзыв")
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard, 
        resize_keyboard=True,
        input_field_placeholder="Tanlang..."
    )
