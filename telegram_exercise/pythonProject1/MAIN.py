import asyncio
import logging
import psycopg2
from aiogram import Bot, Dispatcher, types
from config import host, user, password, database,BOT_TOKEN
from aiogram.filters import CommandStart, Command


conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=database
     )

cur = conn.cursor()
conn.commit()


logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(msg: types.Message) -> None:
     await msg.answer(text="Привет, я бот который умеет записывать ваши задачи.\n Я могу добавить задачу командой /add <Ваш текст>. \n Показать список всех задач /select. \n Удалить задачу /del <id вашей задачи>.")


@dp.message(Command("add"))
async def add_task(message: types.Message) -> None:
    task_text = message.text.replace('/add', '').strip()
    if task_text:
        cur.execute("INSERT INTO postgres (task) VALUES (%s)", (task_text,))
        conn.commit()
        await message.answer(f"Задача \"{task_text}\" добавлена.")
    else:
        await message.answer("Пожалуйста, введите текст задачи после команды /add.")


@dp.message(Command("select"))
async def select_task(message: types.Message) -> None:
    cur.execute("SELECT * FROM task orders")
    result = cur.fetchall()
    cur.close()
    conn.close()
    await message.answer(text="Все задачи : \n{}".format(result))

@dp.message(Command("del"))
async def del_task(message: types.Message) -> None:

    try:
        order_id = int(message.text.split(" ")[1])
    except (ValueError, IndexError):
        await message.answer("Неправильный ввод, Пожалуйста используйте /del <Нужный id>")
        return


    cur.execute("DELETE FROM postgres WHERE order_id = %s", (order_id,))
    conn.commit()
    cur.close()
    conn.close()

    await message.answer(text="Задача удалена успешно!")




async def main() -> None:
    await dp.start_polling(bot)

if __name__ == '__main__':
    print("Bot started...")
    asyncio.run(main())