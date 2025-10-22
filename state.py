from aiogram.fsm.state import State, StatesGroup
class LoginStates(StatesGroup):
    waiting_id = State()
    waiting_password = State()

class EditStates(StatesGroup):
    waiting_new_name = State()
    waiting_new_surname = State()

class FeedbackStates(StatesGroup):
    waiting_feedback = State()
