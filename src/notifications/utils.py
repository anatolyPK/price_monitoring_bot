from aiogram.enums import ParseMode

from config.logger import setup_logger

logger = setup_logger(__name__)


def generate_message_for_each_products(product_name, product_last_price, product_url,
                                       is_any_change, threshold_price, is_include_bonuses):
    bonuses = '\U00002705 Бонусы учитываются' if is_include_bonuses else '❌ Бонусы не учитываются'
    if is_any_change:
        notification = 'любом изменении цены'
    else:
        notification = f'цене ниже {threshold_price} руб.'

    message = (f'[{product_name}]({product_url})\n'
               f'{product_last_price} руб\n'
               f'\U00002705 Оповещение при {notification}\n'
               f'{bonuses}')
    return message


async def send_message_price_changed(chat_id: int, message_text: str):
    from src.notifications.bot_start_up import bot
    # // TODO add kb for delete
    await bot.send_message(chat_id=chat_id, text=message_text, parse_mode=ParseMode.MARKDOWN)
