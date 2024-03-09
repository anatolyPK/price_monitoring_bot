class ProductNotFound(Exception):
    '''Ошибки при невозможности определения цены или названия товара'''


class InvalidMessageWithUrl(Exception):
    """Ошибка при извлечении домена или ссылки из сообщения пользователя"""