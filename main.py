from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
from dotenv import load_dotenv 
from service import *
from connection import *
import asyncio
import os

load_dotenv()

token = os.getenv("BOT_TOKEN")

bot = Bot(token=token)
dp = Dispatcher()


main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=""), KeyboardButton(text="")]
    ],
    resize_keyboard=True,
)


@dp.message(CommandStart())
async def start_bot(message: Message):
    if await  get_user_by_id(message.from_user.id):
        await message.answer(f"""
                Привет! Я бот для управления рецептами и планом питания.
                Доступные команды:
                /add_recipe [название] - добавить рецепт
                /add_ingredient [id рецепта] [ингредиент] [количество] - добавить ингредиент
                /recipe [id рецепта] - посмотреть рецепт и ингредиенты
                /plan — добавить рецепт в план питания (подсказка)
                                """)
    else:
        user = message.from_user
        await create_user(user.username, user.full_name, user.id)
        await message.answer(f"""
                Привет! Я бот для управления рецептами и планом питания.
                Доступные команды:
                /add_recipe [название] - добавить рецепт
                /add_ingredient [id рецепта] [ингредиент] [количество] - добавить ингредиент
                /recipe [id рецепта] - посмотреть рецепт и ингредиенты
                /plan — добавить рецепт в план питания (подсказка)
                                """)



@dp.message(Command("add_recipe"))
async def add_recipe_handler(message: Message, command: CommandObject):
    # Шаг 1-2: Если аргументов нет, бот просто отправляет подсказку и останавливается
    if not command.args:
        return await message.answer("Использование: /add_recipe Борщ")
    recipe_id = await add_recipe(command.args)
    if recipe_id:
        await message.answer(f"Рецепт успешно сохранён! ID: {recipe_id}")
    else:
        "Ошибка при сохранении."



async def main():
    await create_table_db()
    print("Bot started")
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())






         
