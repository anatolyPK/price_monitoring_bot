from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import StatesGroup, State


class AddProductStateMachine(StatesGroup):
    EnterLink = State()
    EnterPrice = State()
    TrackSales = State()


class DeleteProductCallback(CallbackData, prefix='delete'):
    action: str
    user_product_id: int


class UniversalCallback(CallbackData, prefix='callback'):
    action: str


class ChooseIsIncludeSales(CallbackData, prefix='sales'):
    sales: bool
    is_include: str


