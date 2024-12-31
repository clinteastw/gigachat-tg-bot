from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from sqlalchemy.ext.asyncio import AsyncSession

from database import async_session_maker
from config import GIGACHAT_TOKEN, BOT_TOKEN
from models.users import User
from models.conversations import Conversation


prompt_system = """Ты вежливый и услужливый бот.
"""


prompt_regular = """
Ответь на вопрос пользователя:
%s"""


async def callGiga(session: AsyncSession, message: str, prompt_system: str = prompt_system,
                   prompt_regular:str = prompt_regular) -> str:
    payload = Chat(
        messages=[
            Messages(
                role=MessagesRole.SYSTEM,
                content=prompt_system
            )
        ],
        temperature=0.7,
        max_tokens=500,
        n=1,
        top_p=0.2,
        repetition_penalty=1,
    )
    user_history = await Conversation.get_history(session, message.from_user.id)

    if user_history:
        for conversation in user_history:
            payload.messages.append(
                Messages(role=MessagesRole.USER, content=conversation.user_message)
                )
            payload.messages.append(
                Messages(role=MessagesRole.ASSISTANT, content=conversation.assistant_message)
                )
            
    payload.messages.append(
        Messages(role=MessagesRole.USER, content=prompt_regular % message.text)
        )

    with GigaChat(credentials=GIGACHAT_TOKEN,
                  scope="GIGACHAT_API_PERS",
                  model='GigaChat:latest',
                  verify_ssl_certs=False) as giga:
        response = giga.chat(payload)

    return response.choices[0].message.content


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    print(f'Приветсвую нового пользователя с ID {message.from_user.id}! ')
    await message.answer("""Привет! Я бот сделанный для тестового задания. Знаю ответы на пару вопросов.
    Вызвать помощь команда /help""")


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("""Чтобы очистить нашу историю общения, выполните команду /clear""")


@dp.message(Command("clear"))
async def cmd_clear(message: types.Message):
    async with async_session_maker() as session:
        await Conversation.clear_history(session, message.from_user.id)
    await message.answer("История очищена!")


@dp.message()
async def echo_message(message: types.Message):
    async with async_session_maker() as session:
        response = await callGiga(session, message)
        user = await User.get_or_create(session, message.from_user.id)
        await Conversation.save_message(session, user.tg_id, message.text, response)
    await message.answer(response)


if __name__ == '__main__':
    dp.run_polling(bot)
