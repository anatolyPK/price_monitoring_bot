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
        InlineKeyboardButton(text="Любое изменение цены", callback_data="any_price_change"),
        InlineKeyboardButton(text="◀️ Выйти в меню", callback_data=""),
    ]
]
price_change = InlineKeyboardMarkup(inline_keyboard=price_change)

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


def create_delete_product_keyboard(callback_data) -> InlineKeyboardMarkup:
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Удалить продукт",
                                                                                  callback_data=callback_data)]])
    return inline_keyboard


def create_any_product_price(callback_data, callback_data_menu) -> InlineKeyboardMarkup:
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Любое изменение цены", callback_data=callback_data)],
        [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data=callback_data_menu)]
    ])
    return inline_keyboard


def create_include_sales(callback_data_include, callback_data_not_include) -> InlineKeyboardMarkup:
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Учитывать", callback_data=callback_data_include)],
        [InlineKeyboardButton(text="Не учитывать", callback_data=callback_data_not_include)]
    ])
    return inline_keyboard
