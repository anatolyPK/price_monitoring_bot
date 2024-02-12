from aiogram.fsm.state import StatesGroup, State


class AddProductStateMachine(StatesGroup):
    EnterLink = State()
    EnterPrice = State()
    TrackSales = State()
