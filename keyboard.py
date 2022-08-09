from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.markdown import text

from emoji import emojize

button_attack = KeyboardButton(text("/ATTACK", emojize(":dagger:")))
button_heal = KeyboardButton(text("/HEAL", emojize(":pill:")))
button_pass = KeyboardButton(text("/PASS", emojize(":stopwatch:")))

button_attack_enhance = KeyboardButton(text("/ATTACK_ENHANCE", emojize(":plus::dagger:")))
button_heal_enhance = KeyboardButton(text("/HEAL_ENHANCE", emojize(":plus::pill:")))
button_health_enhance = KeyboardButton(text("/HEALTH_ENHANCE", emojize(":plus::red_heart:")))

button_start = KeyboardButton(text("/START", emojize(":video_game:")))
button_restart = KeyboardButton(text("/RESTART", emojize(":repeat_button:")))

button_monkey = KeyboardButton(text("/MONKEY", emojize(":monkey:")))
button_music = KeyboardButton(text("/MUSIC", emojize(":musical_note:")))
button_kittenfight = KeyboardButton(text("/KITTENFIGHT", emojize(":cat_with_wry_smile:")))
button_sadkitten = KeyboardButton(text("/SADKITTEN", emojize(":crying_cat:")))
button_kittendance = KeyboardButton(text("/KITTENDANCE", emojize(":grinning_cat_with_smiling_eyes:")))

fight_kb1 = ReplyKeyboardMarkup(resize_keyboard=True).row(button_attack, button_heal, button_pass)

enhance_kb1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_attack_enhance)
enhance_kb1.add(button_heal_enhance).add(button_health_enhance)

restart_kb1 = ReplyKeyboardMarkup().add(button_restart)

secret_kb1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_monkey, button_music)
secret_kb1.add(button_kittenfight, button_sadkitten).add(button_kittendance).add(button_start)
