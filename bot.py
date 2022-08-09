import logging

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.utils.markdown import text, bold, italic
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

import keyboard as kb
import game_classes as gc
import file_id_storage as ids
from enemies import enemy
from emoji import emojize
from config import TOKEN

logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

dp.middleware.setup(LoggingMiddleware())

player = gc.Warior(emojize(":smiling_face_with_sunglasses: Player"))

lvl = gc.LevelProgress(enemy_amount=4)


#############################################################################################


@dp.message_handler(state="*", commands=["start"])
async def process_start_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(gc.States.all()[0])
    await message.answer(text(emojize(":fire:"), bold("GAME STARTED"), emojize(":fire:")),
                         parse_mode=ParseMode.MARKDOWN, reply_markup=kb.fight_kb1)
    await message.answer(player.get_info(),
                         parse_mode=ParseMode.MARKDOWN)
    await message.answer(enemy[lvl.enemy].get_info(),
                         parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(state=gc.States.STATE_0, commands=["restart"])
async def process_start_command(message: types.Message):
    for i in range(lvl.enemy_amount):
        enemy[i].health = enemy[i].max_health
        enemy[i].is_alive = True
    player.reset()
    lvl.reset()
    await message.answer(text(emojize(":fire:"), bold("GAME STARTED"), emojize(":fire:")),
                         parse_mode=ParseMode.MARKDOWN, reply_markup=kb.fight_kb1)
    await message.answer(player.get_info(),
                         parse_mode=ParseMode.MARKDOWN)
    await message.answer(enemy[lvl.enemy].get_info(),
                         parse_mode=ParseMode.MARKDOWN)


#############################################################################################


@dp.message_handler(state=gc.States.STATE_0, commands=["ATTACK"])
async def process_attack_command(message: types.Message):
    if not lvl.attacked:
        await message.answer(enemy[lvl.enemy].get_damage(player.damage),
                             parse_mode=ParseMode.MARKDOWN)
        lvl.turn_attack()
        if not enemy[lvl.enemy].is_alive:
            lvl.next_enemy()
            if lvl.enemy < lvl.enemy_amount:
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(gc.States.all()[1])
                await message.answer(text(emojize(":up_arrow:"), bold("NEW LEVEL"), emojize(":up_arrow:")),
                                     parse_mode=ParseMode.MARKDOWN, reply_markup=kb.enhance_kb1)
                if lvl.attacked:
                    lvl.turn_attack()

                if lvl.healed:
                    lvl.turn_heal()
            else:
                await message.answer(text(emojize(":sparkles:"), bold("YOU WIN"), emojize(":sparkles:")),
                                     parse_mode=ParseMode.MARKDOWN, reply_markup=kb.restart_kb1)
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(gc.States.all()[0])
    else:
        await message.answer(text(emojize(":worried_face:"), bold("NO ATTACK LEFT"),
                                  emojize(":worried_face:")),
                             parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(state=gc.States.STATE_0, commands=["HEAL"])
async def process_heal_command(message: types.Message):
    if not lvl.healed:
        await message.answer(player.heal(),
                             parse_mode=ParseMode.MARKDOWN)
        lvl.turn_heal()
    else:
        await message.answer(text(emojize(":disappointed_face:"), bold("NO HEAL LEFT"),
                                  emojize(":disappointed_face:")),
                             parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(state=gc.States.STATE_0, commands=["PASS"])
async def process_pass_command(message: types.Message):
    await message.answer(player.get_damage(enemy[lvl.enemy].damage),
                         parse_mode=ParseMode.MARKDOWN)
    if lvl.attacked:
        lvl.turn_attack()

    if lvl.healed:
        lvl.turn_heal()

    if not player.is_alive:
        await message.answer(text(emojize(":skull_and_crossbones:"), bold("GAME END"),
                                  emojize(":skull_and_crossbones:")),
                             parse_mode=ParseMode.MARKDOWN, reply_markup=kb.restart_kb1)


#############################################################################################


@dp.message_handler(state=gc.States.STATE_1, commands=["ATTACK_ENHANCE"])
async def process_attack_enhance_command(message: types.Message):
    await message.answer(player.add_damage(),
                         parse_mode=ParseMode.MARKDOWN, reply_markup=kb.fight_kb1)
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(gc.States.all()[0])
    await message.answer(enemy[lvl.enemy].get_info(),
                         parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(state=gc.States.STATE_1, commands=["HEALTH_ENHANCE"])
async def process_health_enhance_command(message: types.Message):
    await message.answer(player.add_max_health(),
                         parse_mode=ParseMode.MARKDOWN, reply_markup=kb.fight_kb1)
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(gc.States.all()[0])
    await message.answer(enemy[lvl.enemy].get_info(),
                         parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(state=gc.States.STATE_1, commands=["HEAL_ENHANCE"])
async def process_heal_enhance_command(message: types.Message):
    await message.answer(player.add_heal(),
                         parse_mode=ParseMode.MARKDOWN, reply_markup=kb.fight_kb1)
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(gc.States.all()[0])
    await message.answer(enemy[lvl.enemy].get_info(),
                         parse_mode=ParseMode.MARKDOWN)


#############################################################################################


@dp.message_handler(state="*", commands=["help"])
async def process_help_command(message: types.Message):
    await message.reply("Nothig can help you now")


@dp.message_handler(state="*", commands=["secret"])
async def process_secret_command(message: types.Message):
    msg = text(bold("SECRET COMMANDS LIST"), "", italic("/secret"), "",
               "/monkey", "/music", "/kittenfight", "/sadkitten", "/kittendance",
               sep='\n')
    await message.answer(msg, parse_mode=ParseMode.MARKDOWN, reply_markup=kb.secret_kb1)


#############################################################################################


@dp.message_handler(state="*", commands=["monkey"])
async def process_monkey_command(message: types.Message):
    await message.reply(emojize(":banana::monkey_face:"))


@dp.message_handler(state="*", commands=['music'])
async def process_voice_command(message: types.Message):
    await bot.send_voice(message.from_user.id, ids.MUSIK)


@dp.message_handler(state="*", commands=['kittenfight'])
async def process_kittenfight_command(message: types.Message):
    await bot.send_video(message.from_user.id, ids.KITTEN_FIGHT)


@dp.message_handler(state="*", commands=['sadkitten'])
async def process_sadkitten_command(message: types.Message):
    await bot.send_photo(message.from_user.id, ids.SAD_KITTEN,
                         caption=emojize(":crying_cat:\t:crying_cat:\t:crying_cat:"))


@dp.message_handler(state="*", commands=['kittendance'])
async def process_kittendance_command(message: types.Message):
    await bot.send_video(message.from_user.id, ids.KITTEN_DANCE)


#############################################################################################

"""@dp.message_handler()
async def echo_message(message: types.Message):
    await bot.send_message(message.from_user.id, message.text)"""


#############################################################################################


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)
