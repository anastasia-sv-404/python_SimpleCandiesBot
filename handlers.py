from bot_config import dp
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
import rules
import data
import random


@dp.message_handler(commands=['start'])
async def on_start(message: Message):
    await message.answer(text=f'{message.from_user.first_name}, '
                              f'{rules.hello_message}')


@dp.message_handler(commands=['new_game'])
async def start_new_game(message: Message):
    data.start_new_game()
    if data.game():
        who_is_first = random.randint(0, 1)
        if who_is_first == 1:
            await human_turn(message)
        else:
            await PC_turn(message)


async def human_turn(message: Message):
    await message.answer(f'{message.from_user.first_name}, твой ход! '
                         f'Сколько конфет ты хочет забрать со стола?')


async def PC_turn(message):
    total = data.get_total()
    if total <= 28:
        taken_candies = total
    else:
        taken_candies = random.randint(1, 28)
    data.take_candies(taken_candies)
    await message.answer(f'РC взял {taken_candies} конфет(у/ы).\n'
                         f'На столе осталось {data.get_total()} конфет(у/ы).')
    if await who_is_win(message, taken_candies, 'PC'):
        return
    await human_turn(message)


async def who_is_win(message, taken_candies: int, player: str):
    if data.get_total() <= 0:
        if player == 'human':
            await message.answer(f'{message.from_user.first_name} взял(а) {taken_candies} конфет(у/ы).\n'
                                 f'Победил(а) {message.from_user.first_name}!')
        else:
            await message.answer(f'Победил PC!')
        data.start_new_game()
        return True
    else:
        return False


@dp.message_handler()
async def take_candies(message: Message):
    if data.game():
        if message.text.isdigit():
            taken_candies = int(message.text)
            if (1 <= taken_candies <= 28) and (taken_candies <= data.get_total()):
                data.take_candies(taken_candies)
                if await who_is_win(message, taken_candies, 'human'):
                    return
                await message.answer(f'{message.from_user.first_name} взял(а) {taken_candies} конфет(у/ы)\n'
                                     f'На столе осталось {data.get_total()} конфет(у/ы).\n'
                                     f'Теперь ходит РС.')
                await PC_turn(message)
            else:
                await message.answer(f'{message.from_user.first_name}, ты указал(а) неправильное число конфет.\n'
                                     f'Бери от 1 до 28 конфет за ход.')
        else:
            pass
