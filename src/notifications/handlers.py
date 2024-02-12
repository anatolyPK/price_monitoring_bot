from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart

from config.logger import setup_logger
from db.crud_operations import UsersCRUD, ProductsCRUD, UserProductsCRUD
from src.monitoring.monitoring import get_product_price_and_name
from src.notifications import kb, text
from src.notifications.states import AddProductStateMachine


logger = setup_logger(__name__)


router = Router()


@router.message(CommandStart())
async def start_handler(msg: Message):
    await msg.answer(text.greet, reply_markup=kb.menu)

    telegram_user_id = msg.from_user.id
    if not UsersCRUD.add_new_user(telegram_user_id):
        logger.warning(f'Ошибка при добавлении пользователся в БД!'
                       f'{msg} {telegram_user_id}')


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)


# ----------------------ADD PRODUCT-----------------
@router.message(F.text == 'Начать отслеживание')
async def start_add_product_handler(message: Message, state: FSMContext):
    await state.set_state(AddProductStateMachine.EnterLink)
    await message.answer(text.get_link, reply_markup=kb.exit_kb)


@router.message(AddProductStateMachine.EnterLink)
async def enter_link_handler(message: Message, state: FSMContext):
    link = message.text
    try:
        product_price, product_name = get_product_price_and_name(link)
        await message.answer(f'{product_name}\n'
                             f'Текущая цена: {product_price} руб.\n'
                             f'{link}', reply_markup=kb.price_change)
        await message.answer(text.get_price, reply_markup=kb.price_change)
        await state.update_data(link=link, product_price=product_price, product_name=product_name)
        await state.set_state(AddProductStateMachine.EnterPrice)
    except KeyError:
        await message.answer(text.parser_not_found, reply_markup=kb.exit_kb) #что будет дальше??? будет ли повтор ?
    except AttributeError:
        await message.answer(text.invalid_link, reply_markup=kb.exit_kb)  # что будет дальше??? будет ли повтор ?


@router.message(AddProductStateMachine.EnterPrice, F.text == "Любое изменение цены") # как использовать f.data
async def handle_any_price_change(message: Message, state: FSMContext):
    await state.update_data(any_price_change=True, threshold_price=0)
    await state.set_state(AddProductStateMachine.TrackSales)
    await message.answer(text.get_sales, reply_markup=kb.include_sales)


@router.message(AddProductStateMachine.EnterPrice)
async def handle_threshold_price(message: Message, state: FSMContext):
    try:
        threshold_price = float(message.text)
        await state.update_data(any_price_change=False, threshold_price=threshold_price)
        await state.set_state(AddProductStateMachine.TrackSales)
        await message.answer(text.get_sales, reply_markup=kb.include_sales)
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число для установки порога цены.",
                             reply_markup=kb.price_change)


@router.message(AddProductStateMachine.TrackSales, (F.text == "Учитывать") | (F.text == "Не учитывать"))
async def enter_consider_bonuses(message: Message, state: FSMContext):
    is_include_sales = True if message.text == "Учитывать" else False
    state_data = await state.get_data()

    UserProductsCRUD.add_user_product(telegram_id=message.from_user.id,
                                      product_url=state_data['link'],
                                      threshold_price=state_data['threshold_price'],
                                      last_product_price=state_data['product_price'],
                                      product_name=state_data['product_name'],
                                      is_any_change=state_data['any_price_change'],
                                      is_take_into_account_bonuses=is_include_sales)

    logger.debug(state_data)
    await state.clear()
    await message.answer('Товар успешно добавлен!', reply_markup=kb.menu)
    await message.answer(str(state_data), reply_markup=kb.menu)


@router.message(AddProductStateMachine.TrackSales)
async def enter_consider_bonuses_handler(message: Message, state: FSMContext):
    await message.answer('Выберите, пожалуйста, учитывать или не учитывать скидки и бонусные баллы', reply_markup=kb.include_sales)


#------------------GET USER PRODUCTS--------------------------
@router.message(F.text == 'Мои товары')
async def get_user_products_handler(message: Message):
    products_list = UserProductsCRUD.get_user_products(message.from_user.id)
    for user_products, users, products in products_list:
        await message.answer(f'{products.product_name} \n {products.last_price} руб. \n {products.url}', reply_markup=kb.menu)


@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}")
