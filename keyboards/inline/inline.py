from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_locked_button(m: int) -> InlineKeyboardMarkup:
    k = InlineKeyboardMarkup(row_width=5)
    for i in range(1, m + 1):
        s = InlineKeyboardButton(text=str(i), callback_data=f'restr_{i}')
        k.insert(s)
    return k


def video(fps: list, url: str, chan: str) -> InlineKeyboardMarkup:
    k = InlineKeyboardMarkup(row_width=3)
    for i in fps:
        s = InlineKeyboardButton(text="📹 " + str(i), callback_data=f'FPS{i}{url}')
        k.insert(s)
    s = InlineKeyboardButton(text="🎵 MP3", callback_data=f"mp3{url}")
    k.insert(s)
    s = InlineKeyboardButton(text="Kanalni ochish", url=chan)
    k.insert(s)
    return k


def url_video(url: str) -> InlineKeyboardMarkup:
    k = InlineKeyboardMarkup(row_width=3)
    s = InlineKeyboardButton(text="Kanalni ochish", url=url)
    k.insert(s)
    return k
