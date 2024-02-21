
def generate_message_for_each_products(product_name, product_last_price, product_url,
                                       is_any_change, threshold_price, is_include_bonuses):
    bonuses = 'учитываются' if is_include_bonuses else 'не учитываются'
    if is_any_change:
        notification = 'любом изменении цены'
    else:
        notification = f'цене ниже {threshold_price} руб.'
    message = (f'{product_name}\n'
               f'{product_last_price}\n'
               f'[Cсылка на товар]({product_url})\n'
               f'\U00002705Оповещение при {notification}\n'
               f'\U00002705Бонусы {bonuses}')

    return message


def send_message_price_changed():
    pass