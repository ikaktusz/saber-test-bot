from ast import Num
import os
import re
import logging

from aiogram import Bot, Dispatcher, executor, types

import db
from exceptions import (
    OperandsException,
    LettersInStringException,
    NumLengthException
)


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
            nums = re.split("[-|+|/|*|(|)]", message.text)
            nums = list(filter(('').__ne__, nums)) # Delete all empty elements.

            if any([x.isalpha() for x in message.text]): # If where is any letter in string.
                raise LettersInStringException("You can't use letters.")
            elif len(nums) > 10:
                raise OperandsException("Too many operands(>10)")
            elif any(len(x) > 13 for x in nums):
                raise NumLengthException("Numbers cannot be longer than 13 characters.")
            
            result = eval(message.text.replace(',', '.'))

        except ZeroDivisionError:
            return await message.answer("Error: Division by 0")

        except (LettersInStringException, OperandsException, NumLengthException) as err:
            return await message.answer("Error: " + str(err))

        except (SyntaxError, TypeError, NameError) as err:
            return await message.answer("Error: Something went wrong:)")

        if result == int(result):
            await message.answer(str(int(result)))
        else:
            await message.answer(f"{result:.4f}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)