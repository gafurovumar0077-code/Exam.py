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
        [KeyboardButton(text="📋 Мy recipe")]
    ],
    resize_keyboard=True,
)


@dp.message(CommandStart())
async def start_bot(message: Message):
    if await  get_user_by_id(message.from_user.id):
        await message.answer(f"""
👋 Привет! Я бот для управления рецептами и планом питания 🍽️
📋 Доступные команды:
📝 /add_recipe [название] - добавить рецепт
🥕 /add_ingredient [id рецепта] [ингредиент] [количество] - добавить ингредиент
📖 /recipe [id рецепта] - посмотреть рецепт и ингредиенты
📅 /plan — добавить рецепт в план питания (подсказка)
                                """, reply_markup=main_kb)
    else:
        user = message.from_user
        await create_user(user.username, user.full_name, user.id)
        await message.answer(f"""
👋 Привет! Я бот для управления рецептами и планом питания 🍽️
📋 Доступные команды:
📝 /add_recipe [название] - добавить рецепт
🥕 /add_ingredient [id рецепта] [ингредиент] [количество] - добавить ингредиент
📖 /recipe [id рецепта] - посмотреть рецепт и ингредиенты
📅 /plan — добавить рецепт в план питания (подсказка)
                                """, reply_markup=main_kb)



@dp.message(Command("help"))
async def start_bot(message: Message):
    if await  get_user_by_id(message.from_user.id):
        await message.answer(f"""
📋 Доступные команды:
📝 /add_recipe [название] - добавить рецепт
🥕 /add_ingredient [id рецепта] [ингредиент] [количество] - добавить ингредиент
📖 /recipe [id рецепта] - посмотреть рецепт и ингредиенты
📅 /plan — добавить рецепт в план питания (подсказка)
📖 /recipes [id рецепта] - посмотреть всех рецептов и ингредиентов
""")




@dp.message(Command("add_recipe"))
async def add_recipe_handler(message: Message, command: CommandObject):
    if not command.args:
        return await message.answer("ℹ️ Использование: /add_recipe Борщ 🍲")
    recipe_id = await add_recipe(command.args, message.from_user.id)
    if recipe_id:
        await message.answer(f"✅ Рецепт успешно сохранён! 🆔 ID: {recipe_id}")
    else:
        ("❌ Ошибка при сохранении.")


@dp.message(Command("add_ingredient"))
async def add_ingred(message:Message, command:CommandObject):
    com=command.args
    if not com:
        await message.answer("ℹ️ Использование: /add_ingredient 1 Картошка 5")
    recipe_id, name, amount = com.split()
    adding = await add_ingredient(int(recipe_id), name, int(amount))
    
    if adding:
        await message.answer("✅ Ингредиент успешно добавлен! 🥕")
    else:
        await message.answer("❌ Ошибка при добавлении ингредиента!")
        


@dp.message(F.text == "📋 Мy recipe")
@dp.message(Command("recipes"))
async def all_recipes(message: Message):
    recs = await all_recipe(message.from_user.id)

    if not recs:
        await message.answer("🔍 Рецептов пока нет.")
        return

    text = "📋 Мои рецепты:"
    for rec in recs:
        text += f"""
🍽️ {rec['recipe_id']}. {rec['title']}
🛒 Ингредиенты:"""
        ingred = await ingredints(rec["recipe_id"])
        if ingred:
            for ing in ingred:
                text += f"""
🔸 {ing["name"]}: {ing["amount"]}-шт"""
        else:
            text += " 🤷 Ингредиентов пока нет."
    await message.answer(text)
    



@dp.message(Command("recipe"))
async def recips(message:Message, command:CommandObject):
    if command is None or not command.args:
        await message.answer("ℹ️ Использование: /recipe 1")
        return
    try:
        recipe_id = int(command.args)
    except ValueError:
        await message.answer("⚠️ ID рецепта должен быть числом! Пример: /recipe 1")
        return
    
    rec = await recipe(recipe_id)
    ing = await ingredints(recipe_id)
    
    if not rec or not rec["title"]:
        await message.answer("🔍 Рецепт не найден.")
        return
    
    text = f"""
    🍽️ {rec['title']}
    
    🛒 Ингредиенты:"""
    if ing:
        for ingred in ing:
            text += f"""
🔸 {ingred["name"]}: {ingred["amount"]}-шт"""
    else:
        text += "🤷 Ингредиентов пока нет."
    await message.answer(text)
    
    
         
        
@dp.message(Command("plan"))
async def add_plan(message: Message, command: CommandObject):
    if not command.args:
       s = await message.answer("""
📅 Как добавить рецепт в план питания:
    1 — Понедельник
    2 — Вторник
    3 — Среда
    4 — Четверг
    5 — Пятница
    6 — Суббота
    7 — Воскресенье
    📌 Пример использования:
    /plan 1 5  (добавит рецепт с ID 5 на понедельник)
                             """) 

    parts = command.args.split()
    try:
        day_of_week=int(parts[0])
        recipe_id=int(parts[1])
    except ValueError:
        await message.answer("⚠️ День недели и ID должны быть целыми числами! Пример: `/plan 1 5`")
        return
    telegram_id=message.from_user.id
    
    date=await add_to_plan(telegram_id, day_of_week, recipe_id)
    
    if date:
        await message.answer("✅ Рецепт успешно добавлен в план питания!")
    else:
        await message.answer("❌ Не удалось добавить. Убедитесь, что такой рецепт существует и вы зарегистрированы в боте.")
        
        
        
        
async def main():
    await create_table_db()
    print("Bot started")
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())




