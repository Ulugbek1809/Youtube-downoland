import sqlite3
import datetime
import asyncio
import os
import ddinsta
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.repley import admin_but, user_keybord
from data.config import ADMINS
from pytube import YouTube
from keyboards.inline import inline
from states.states import amal
from loader import dp, db, bot
from utils.onoff import read_onoffpermission


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    if ADMINS != str(message.from_user.id):
        name = message.from_user.full_name
        await amal.user.set()
        # Foydalanuvchini bazaga qo'shamiz
        try:
            db.add_user(id=message.from_user.id,
                        name=name, profil=message.from_user.username)
            await message.answer(text=f"Xush kelibsiz! {name}", reply_markup=user_keybord())
            # Adminga xabar beramiz
            count = db.count_users()[0]
            msg = f"{message.from_user.full_name} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
            await bot.send_message(chat_id=ADMINS, text=msg)
        except sqlite3.Error:
            await message.answer(f"Xush kelibsiz! {name}")
    else:
        await amal.admin.set()
        await message.answer(f"Xush kelibsiz! ADMIN {message.from_user.full_name}", reply_markup=admin_but())


@dp.message_handler(state=amal.user)
async def userhandler(message: types.Message):
    data = message.text
    # print(db.block_test(message.from_user.id),read_onoffpermission())
    if db.block_test(message.from_user.id) or read_onoffpermission(): 
        print(data.lower().find('https://www.youtu'))
        if data == "👥 bot foydalanuvchilari soni":
            count = db.count_users()[0]
            await message.answer(f"👥 bot foydalanuvchilari soni {count}")
        elif data.lower().startswith('https://www.youtube.com/') or data.lower().startswith('https://youtu'):
            await message.delete()
            tek = await message.answer("⏳ Tekshirilmoqda...")
            try:
                y = YouTube(data)
                l = []
                j = f'{y.title} <a href="{data}"> --> </a>'
                k = ''
                for i in y.streams.filter(mime_type="video/mp4"):
                    k += str(i)
                print(k)
                if k.find("144p") != -1:
                    try:
                        s = y.streams.filter(res="144p", mime_type="video/mp4")
                        siz = s.first().filesize // 1024 // 1024
                        if siz < 500:
                            j += f'\n     ✅144p : {siz}MB'
                            l.append("144p")
                        else:
                            j += f"\n     ❌144p : 500MB dan ko'p"
                    except Exception as e:
                        print(e)
                if k.find("240p") != -1:
                    try:
                        s = y.streams.filter(res="240p", mime_type="video/mp4")
                        siz = s.first().filesize // 1024 // 1024
                        if siz < 500:
                            j += f'\n     ✅240p : {siz}MB'
                            l.append("240p")
                        else:
                            j += f"\n     ❌240p : 500MB dan ko'p"
                    except Exception as e:
                        print(e)
                if k.find("360p") != -1:
                    try:
                        s = y.streams.filter(res="360p", mime_type="video/mp4")
                        siz = s.first().filesize // 1024 // 1024
                        if siz < 500:
                            j += f'\n     ✅360p : {siz}MB'
                            l.append("360p")
                        else:
                            j += f"\n     ❌360p : 500MB dan ko'p"
                    except Exception as e:
                        print(e)
                if k.find("480p") != -1:
                    try:
                        s = y.streams.filter(res="480p", mime_type="video/mp4")
                        siz = s.first().filesize // 1024 // 1024
                        if siz < 500:
                            j += f'\n     ✅480p : {siz}MB'
                            l.append("480p")
                        else:
                            j += f"\n     ❌480p : 500MB dan ko'p"
                    except Exception as e:
                        print(e)
                if k.find("720p") != -1:
                    try:
                        s = y.streams.filter(res="720p", mime_type="video/mp4")
                        siz = s.first().filesize // 1024 // 1024
                        if siz < 500:
                            j += f'\n     ✅720p : {siz}MB'
                            l.append("720p")
                        else:
                            j += f"\n     ❌720p : 500MB dan ko'p"
                    except Exception as e:
                        print(e)
                await message.answer_photo(photo=y.thumbnail_url,
                                        caption=j,
                                        parse_mode="html", reply_markup=inline.video(l, data, y.channel_url))
                await bot.delete_message(message.from_user.id, tek.message_id)
            except Exception as e:
                print(e)
                await bot.delete_message(message.from_user.id, tek.message_id)
                await message.answer(f"❌ Videoni yuklab olib bo'lmadi. !\n{data}")
        elif data.lower().startswith("https://www.instagram.com"):
            await message.delete()
            mid = await message.answer("🕦 Navbatingiz kutilmoqda...")
            # v = data[data.find("reel/"):]
            # v = str(v[5:])
            # j = v[:v.find("/")]
            # await message.answer(f"{j}")
            while True:
                await asyncio.sleep(3.10)
                if os.path.exists("uch.txt"):
                    continue
                else:
                    open("uch.txt", "x")
                    await bot.delete_message(chat_id=message.from_user.id, message_id=mid.message_id)
                    mid = await message.answer("⏳ Video fayl tayyorlanmoqda...")
                    ins = ddinsta.save_video(data)
                    if ins.find("Success") != -1:
                        await bot.delete_message(chat_id=message.from_user.id, message_id=mid.message_id)
                        mid = await message.answer("⬇️ Video fayl sizga yuborilmoqda...")
                        v = data[data.find("reel/"):]
                        v = str(v[5:])
                        j = v[:v.find("/")]
                        if os.path.exists(f"{j}.mp4"):
                            await message.answer_video(video=open(f"{j}.mp4", "rb"), caption=data)
                            await bot.delete_message(chat_id=message.from_user.id, message_id=mid.message_id)
                            os.remove(f"{j}.mp4")
                            os.remove("uch.txt")
                            d = datetime
                            db.add_instagram(id=message.from_user.id, url=data, date=d.datetime.now())
                        else:
                            os.remove("uch.txt")
                            await bot.delete_message(chat_id=message.from_user.id, message_id=mid.message_id)
                            await message.answer(f"❌ Videoni yuklab bo'lmadi.\n{data}")
                    else:
                        os.remove("uch.txt")
                        await bot.delete_message(chat_id=message.from_user.id, message_id=mid.message_id)
                        await message.answer(f"❌ Videoni yuklab bo'lmadi.\n{data}")
                    break
        else:
            await message.answer(f"Yotube va instagram video havolasini yubormadingiz")
    else:
        await message.answer("❌ ADMIN sizga botdan foydalanish uchun ruxsat bermagan")


@dp.callback_query_handler(state=amal.user)
async def user_dow(call: types.CallbackQuery):
    data = call.data
    uid = call.from_user.id
    if data.lower().startswith("mp3"):
        await call.message.delete()
        mid = await call.message.answer("🕦 Navbatingiz kutilmoqda...")
        while True:
            await asyncio.sleep(3.10)
            if os.path.exists("uch.txt"):
                continue
            else:
                open("uch.txt", "x")
                await bot.delete_message(chat_id=uid, message_id=mid.message_id)
                y = YouTube(data[3:])
                mid = await call.message.answer(text="⏳ Audio fayl tayyorlanmoqda... ")
                k = y.streams.filter(only_audio=True).first()
                k.download(f"data", f"{uid}.mp3")
                await bot.delete_message(chat_id=uid, message_id=mid.message_id)
                mid = await call.message.answer('⬇️ Audio fayl sizga yuborilmoqda...')
                if os.path.exists(f"data/{uid}.mp3"):
                    await call.message.answer_audio(audio=open(f"data/{uid}.mp3", "rb"), caption=f"{y.title}",
                                                    reply_markup=inline.url_video(y.channel_url))
                    await bot.delete_message(chat_id=uid, message_id=mid.message_id)
                    os.remove("uch.txt")
                    os.remove(f"data/{uid}.mp3")
                    d = datetime
                    db.add_yotube(uid, data[3:], "NONE", "audio/mp3", f"{d.datetime.now()}")
                else:
                    os.remove("uch.txt")
                    await bot.delete_message(chat_id=uid, message_id=mid.message_id)
                    await call.message.answer(f"❌ Audioni faylni yuklab bo'lmadi.")
                break
    elif data.upper().startswith("FPS"):
        j = data[3:]
        p = j[:4]
        v = j[4:]
        try:
            await call.message.delete()
            mid = await call.message.answer("🕦 Navbatingiz kutilmoqda...")
            while True:
                await asyncio.sleep(3.10)
                if os.path.exists("uch.txt"):
                    continue
                else:
                    open("uch.txt", "x")
                    await bot.delete_message(chat_id=uid, message_id=mid.message_id)
                    mid = await call.message.answer("⏳ Video fayl tayyorlanmoqda...")
                    y = YouTube(v)
                    q = y.streams.filter(res=p, mime_type="video/mp4").first()
                    q.download('data', f"{uid}.mp4")
                    await bot.delete_message(chat_id=uid, message_id=mid.message_id)
                    if os.path.exists(f"data/{uid}.mp4"):
                        mid = await call.message.answer("⬇️ Video fayl sizga yuborilmoqda...")
                        await call.message.answer_video(video=open(f"data/{uid}.mp4", "rb"),
                                                        caption=f'{y.title}<a href="{v}"> --> </a>', parse_mode="html",
                                                        reply_markup=inline.url_video(y.channel_url))
                        await bot.delete_message(chat_id=uid, message_id=mid.message_id)
                        os.remove(f"data/{uid}.mp4")
                        d = datetime
                        db.add_yotube(uid, v, p, "video/mp4", f"{d.datetime.now()}")
                        os.remove("uch.txt")
                    else:
                        await bot.delete_message(chat_id=uid, message_id=mid.message_id)
                        await call.message.answer(f"❌ Videoni yuklab bo'lmadi.\n{v}")
                        os.remove("uch.txt")
                    break
        except Exception:
            os.remove("uch.txt")
            await call.message.answer(f"Botda Xatolik yuklab bo'lmadi /start ni bosing")
