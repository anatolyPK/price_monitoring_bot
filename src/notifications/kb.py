from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


menu = [
        [
            KeyboardButton(text="Мои товары"),
            KeyboardButton(text="Начать отслеживание"),
            KeyboardButton(text="О боте"),
        ]
    ]

price_change = [
    [
        KeyboardButton(text="Любое изменение цены", callback_data="any_price_change"),
        KeyboardButton(text="◀️ Выйти в меню", callback_data="any_price_change"),
    ]
]
price_change = ReplyKeyboardMarkup(keyboard=price_change, resize_keyboard=True)

include_sales = [
    [
        KeyboardButton(text="Учитывать", callback_data="consider"),
        KeyboardButton(text="Не учитывать", callback_data="not_consider"),
        KeyboardButton(text="◀️ Выйти в меню"),
    ]
]
include_sales = ReplyKeyboardMarkup(keyboard=include_sales, resize_keyboard=True)


menu = ReplyKeyboardMarkup(keyboard=menu, resize_keyboard=True)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])