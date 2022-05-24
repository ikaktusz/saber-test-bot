import os
import logging
import hashlib

from aiogram import Bot, Dispatcher, executor, types

import db

API_TOKEN = os.getenv("TOKEN")
BOT_PASSWORD = os.getenv("BOT_PASSWORD")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def auth_required(func):
    async def wrapper(message):
        if not db.user_exists(message.from_user.id):
            if message.text == BOT_PASSWORD:
                db.login(message.from_user.id)
                await message.answer("Login succsessful!")
                await message.answer("Now you can use this bot!")
                await info(message)
                message = None
            else:
                return await message.answer("Access denied!\nEnter password:")

        return await func(message)
    return wrapper


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Hello this is calculator, written with python and aiogram.")
    if not db.user_exists(message.from_user.id):
        await message.answer("Enter password:")


@dp.message_handler(commands=['logout'])
@auth_required
async def logout(message: types.Message):
    db.logout(message.from_user.id)
    await message.answer("You are logged out!")

@dp.message_handler(commands=['help'])
@auth_required
async def info(message: types.Message):
    await message.answer("Enter the expression\n"
                        "to be calculated, and I will\n"
                        "send the answer!\n"
                        "Example:\n\n"
                        "1+3+5\n"
                        "123/3*5-4*(2+1)\n"
                        "etc.\n\n"
                        "Commands:\n"
                        "/help\n/logout"
                        )

@dp.message_handler()
@auth_required
async def calculate(message: types.Message):
    if message:
        try:
            result = eval(message.text)
        except ZeroDivisionError:
            return await message.answer("Division by 0")
        except (SyntaxError, TypeError, NameError):
            return await message.answer("Error")

        if result == int(result):
            await message.answer(str(int(result)))
        else:
            await message.answer(str(result))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)