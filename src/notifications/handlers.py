from aiogram import types, F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from config.logger import setup_logger
from db.crud_operations import UsersCRUD, UserProductsCRUD
from src.monitoring.custom_exceptions import ProductNotFound
from src.monitoring.tasks import task_get_product_price_and_name
from src.notifications import kb, text
from src.notifications.states import AddProductStateMachine, DeleteProductCallback, UniversalCallback, \
    ChooseIsIncludeSales
from src.notifications.utils import generate_message_for_each_products


logger = setup_logger(__name__)


router = Router()


@router.message(CommandStart())
async def start_handler(msg: Message):
    await msg.answer(text.greet, reply_markup=kb.menu)

    telegram_user_id = msg.from_user.id
    if not UsersCRUD.add_new_user(telegram_user_id):
        logger.warning(f'Ошибка при добавлении пользователся в БД!'
                       f'{msg} {telegram_user_id}')


@router.callback_query(UniversalCallback.filter(F.action == 'exit_to_menu'))
async def menu_query(query: CallbackQuery, callback_data: UniversalCallback, state: FSMContext):
    await state.clear()
    await query.message.answer(text.menu, reply_markup=kb.menu)


@router.message((F.text == "Меню") | (F.text == "Выйти в меню") | (F.text == "◀️ Выйти в меню"))
async def menu(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(text.menu, reply_markup=kb.menu)


# ----------------------ADD PRODUCT-----------------
@router.message(F.text == 'Начать отслеживание')
async def start_add_product_handler(message: Message, state: FSMContext):
    await state.set_state(AddProductStateMachine.EnterLink)
    await message.answer(text.get_link, reply_markup=kb.exit_kb)


# ---LINK HANDLER
@router.message(AddProductStateMachine.EnterLink)
async def enter_link_handler(message: Message, state: FSMContext):
    link = message.text
    try:
        result = task_get_product_price_and_name.delay(link)
        product_price, product_name = result.get()
        await message.answer(f'{product_name}\n'
                             f'Текущая цена: {product_price} руб.\n'
                             f'[Cсылка на товар]({link})', parse_mode=ParseMode.MARKDOWN)
        callback_data = UniversalCallback(action='enter_any_price').pack()
        callback_data_menu = UniversalCallback(action='exit_to_menu').pack()
        await message.answer(text.get_price, reply_markup=kb.create_any_product_price(callback_data, callback_data_menu))
        await message.delete()
        await state.update_data(link=link, product_price=product_price, product_name=product_name)
        await state.set_state(AddProductStateMachine.EnterPrice)
    except KeyError:
        logger.info(link)
        await message.answer(text.parser_not_found, reply_markup=kb.exit_kb)
    except AttributeError:
        await message.answer(text.invalid_link, reply_markup=kb.exit_kb)
        await message.delete()
    except ProductNotFound:
        logger.warning(f'Не определна цена или наименование товара {link}')
        await message.answer(text.price_or_name_not_detected)


# ---PRICE HANDLERS
@router.callback_query(UniversalCallback.filter(F.action == 'enter_any_price'))
async def handle_any_price_change(query: CallbackQuery, callback_data: UniversalCallback, state: FSMContext):
    await state.update_data(any_price_change=True, threshold_price=0)
    await state.set_state(AddProductStateMachine.TrackSales)

    callback_data_include = ChooseIsIncludeSales(sales='True', is_include='include').pack()
    callback_data_not_include = ChooseIsIncludeSales(sales='True', is_include='not_include').pack()

    await query.message.answer(text.get_sales,
                               reply_markup=kb.create_include_sales(callback_data_include,
                                                                    callback_data_not_include))


@router.message(AddProductStateMachine.EnterPrice)
async def handle_threshold_price(message: Message, state: FSMContext):
    try:
        threshold_price = float(message.text)
        await state.update_data(any_price_change=False, threshold_price=threshold_price)
        await state.set_state(AddProductStateMachine.TrackSales)

        callback_data_include = ChooseIsIncludeSales(sales='True', is_include='include').pack()
        callback_data_not_include = ChooseIsIncludeSales(sales='True', is_include='not_include').pack()

        await message.answer(text.get_sales,
                             reply_markup=kb.create_include_sales(callback_data_include,
                                                                  callback_data_not_include))
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число для установки порога цены.",
                             reply_markup=kb.price_change)


# ---BONUSES HANDLERS
@router.callback_query(ChooseIsIncludeSales.filter(F.sales))
async def enter_consider_bonuses(query: CallbackQuery, callback_data: ChooseIsIncludeSales, state: FSMContext):
    is_include_sales = True if callback_data.is_include == "include" else False
    state_data = await state.get_data()
    UserProductsCRUD.add_user_product(telegram_id=query.from_user.id,
                                      product_url=state_data['link'],
                                      threshold_price=state_data['threshold_price'],
                                      last_product_price=state_data['product_price'],
                                      product_name=state_data['product_name'],
                                      is_any_change=state_data['any_price_change'],
                                      is_take_into_account_bonuses=is_include_sales)
    await state.clear()
    await query.message.answer('Товар успешно добавлен!', reply_markup=kb.menu) #написать подробно про добавленный товар


@router.message(AddProductStateMachine.TrackSales)
async def enter_consider_bonuses_handler(message: Message, state: FSMContext):
    callback_data_include = UniversalCallback(action='callback_data_include').pack()
    callback_data_not_include = UniversalCallback(action='callback_data_not_include').pack()
    await message.answer('Выберите, пожалуйста, учитывать или не учитывать скидки и бонусные баллы',
                         reply_markup=kb.create_include_sales(callback_data_include,
                                                              callback_data_not_include))


# ------------------GET USER PRODUCTS--------------------------
@router.message(F.text == 'Мои товары')
async def get_user_products_handler(message: Message):
    products_list = UserProductsCRUD.get_user_products(message.from_user.id)
    if products_list:
        for user_products, users, products in products_list:
            callback_data = DeleteProductCallback(action='delete', user_product_id=str(user_products.id)).pack()
            inline_keyboard = kb.create_delete_product_keyboard(callback_data)
            msg = generate_message_for_each_products(product_name=products.product_name,
                                                     product_last_price=products.last_price,
                                                     product_url=products.url, is_any_change=user_products.is_any_change,
                                                     threshold_price=user_products.threshold_price,
                                                     is_include_bonuses=user_products.is_take_into_account_bonuses)
            await message.answer(msg, reply_markup=inline_keyboard, parse_mode=ParseMode.MARKDOWN)
    else:
        await message.answer(text.products_are_not_being_monitored,
                             reply_markup=kb.menu)

# -----------------DELETE PRODUCT-----------------


@router.callback_query(DeleteProductCallback.filter(F.action == 'delete'))
async def delete_product_handler(query: CallbackQuery, callback_data: DeleteProductCallback):
    user_product_id = callback_data.user_product_id
    if not UserProductsCRUD.delete_user_products(user_product_id):
        logger.warning(f'Не найдена запись {user_product_id}')
    await query.answer(text.stop_monitoring_product)


@router.message()
async def de_product_handler(msg: Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}")
