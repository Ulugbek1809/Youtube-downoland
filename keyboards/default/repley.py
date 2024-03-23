from aiogram.types import ReplyKeyboardMarkup
from utils import onoff


def admin_but() -> ReplyKeyboardMarkup:
    admin_button = ReplyKeyboardMarkup(resize_keyboard=True);
    if onoff.read_onoffpermission():
        admin_button.row("Bot foydalanuvchilari", "🟢Ruxsat : on")
    else:
        admin_button.row("Bot foydalanuvchilari", "🔴Ruxsat : off")
    admin_button.row("⬇️ Yuklab olingan videolar")
    return admin_button


def user_keybord() -> ReplyKeyboardMarkup:
    user = ReplyKeyboardMarkup(resize_keyboard=True)
    user.row("👥 bot foydalanuvchilari soni")
    return user
