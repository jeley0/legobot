import asyncio
import logging
import sys
from PIL import Image
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, FSInputFile
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
from aiogram import F

import torch
from ultralytics import YOLO

TOKEN = ''

dp = Dispatcher()


def searchparts():
    model = YOLO('best.pt').to(torch.device('cuda'))
    results = model.predict("2000.jpg", save=True, max_det=400, imgsz=640)
    result = results[0]
    a = []
    for i in range(len(result.boxes)):
        a.append(result.names[int(result.boxes.cls[i])])
    a = dict((x, a.count(x)) for x in set(a))
    print(a)
    return str(a)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}!", reply_markup=main_kb(message.from_user.id))


@dp.message(F.photo)
async def download_photo(message: Message, bot: Bot):
    await bot.download(
        message.photo[-1],
        destination="2000.jpg"
    )
    await message.answer(searchparts())


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
