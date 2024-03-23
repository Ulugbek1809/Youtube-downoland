import asyncio
import os
import datetime
from aiogram import types
from data.config import ADMINS
from loader import dp, db, bot
from utils import onoff
from pytube import YouTube
from keyboards.default import repley
from keyboards.inline import inline
from states.states import amal


@dp.message_handler(state=amal.admin)
async def get_all_users(message: types.Message):
    data = message.text
    mid = str(message.from_user.id)
    if ADMINS == mid:
        if data == "Bot foydalanuvchilari":
            count = db.count_users()[0]
            users = db.select_all_users()
            k = f'Bot foydalanuvchilari soni: {count} \n'
            uch = 0
            for user in users:
                uch += 1
                if not onoff.read_onoffpermission():
                    match user[3]:
                        case 0:
                            k += f'\n{uch}.🔴 {user[0]} | {user[1]} | @{user[2]}'
                        case 1:
                            k += f'\n{uch}.🟢 {user[0]} | {user[1]} | @{user[2]}'
                else:
                    k += f'\n{uch}.{user[0]} | {user[1]} | @{user[2]}'
            if not onoff.read_onoffpermission():
                await bot.send_message(ADMINS, k, reply_markup=inline.admin_locked_button(uch))
            else:
                await bot.send_message(ADMINS, k)
        elif data == "🟢Ruxsat : on":
            onoff.write_onoffpermission(False)
            await message.answer('🔴 Locked', reply_markup=repley.admin_but())
        elif data == "🔴Ruxsat : off":
            onoff.write_onoffpermission(True)
            await message.answer('🟢 Unlocked', reply_markup=repley.admin_but())
        elif data.lower().find('https://www.youtube.com/') != -1:
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
                        if siz <= 1024:
                            j += f'\n     ✅144p : {siz}MB'
                            l.append("144p")
                        else:
                            j += f"\n     ❌144p : 1024MB dan ko'p"
                    except Exception as e:
                        print(e)
                if k.find("240p") != -1:
                    try:
                        s = y.streams.filter(res="240p", mime_type="video/mp4")
                        siz = s.first().filesize // 1024 // 1024
                        if siz <= 1024:
                            j += f'\n     ✅240p : {siz}MB'
                            l.append("240p")
                        else:
                            j += f"\n     ❌240p : 1024MB dan ko'p"
                    except Exception as e:
                        print(e)
                if k.find("360p") != -1:
                    try:
                        s = y.streams.filter(res="360p", mime_type="video/mp4")
                        siz = s.first().filesize // 1024 // 1024
                        if siz <= 1024:
                            j += f'\n     ✅360p : {siz}MB'
                            l.append("360p")
                        else:
                            j += f"\n     ❌360p : 1024MB dan ko'p"
                    except Exception as e:
                        print(e)
                if k.find("480p") != -1:
                    try:
                        s = y.streams.filter(res="480p", mime_type="video/mp4")
                        siz = s.first().filesize // 1024 // 1024
                        if siz <= 1024:
                            j += f'\n     ✅480p : {siz}MB'
                            l.append("480p")
                        else:
                            j += f"\n     ❌480p : 1024MB dan ko'p"
                    except Exception as e:
                        print(e)
                if k.find("720p") != -1:
                    try:
                        s = y.streams.filter(res="720p", mime_type="video/mp4")
                        siz = s.first().filesize // 1024 // 1024
                        if siz <= 1024:
                            j += f'\n     ✅720p : {siz}MB'
                            l.append("720p")
                        else:
                            j += f"\n     ❌720p : 1024MB dan ko'p"
                    except Exception as e:
                        print(e)
                await message.answer_photo(photo=y.thumbnail_url,
                                           caption=j,
                                           parse_mode="html", reply_markup=inline.video(l, data, y.channel_url))
                await bot.delete_message(message.from_user.id, tek.message_id)
            except Exception as e:
                print(e)
                await bot.delete_message(message.from_user.id, tek.message_id)
                await message.answer(f"❌ Video mavjud emas !\n{data}")
        elif data=="⬇️ Yuklab olingan videolar":
            y=db.count_Youtube()[0]
            i=db.count_Instagram()[0]
            await message.answer(f"Yotubedan yuklab olinganlar soni : {y}\n Instagramdan yuklab olingan soni : {i}")
            


@dp.callback_query_handler(state=amal.admin, user_id=ADMINS)
async def on_of_locked(call: types.CallbackQuery):
    data = call.data
    uid = call.from_user.id
    if data.lower().find('restr_') != -1:
        s = call.data[6:]
        count = 0
        users = db.select_all_users()
        for i in users:
            count += 1
            if count == int(s):
                id1 = i[0]
                loc = i[3]
                if loc == 1:
                    db.updata_user(id1, 0)
                else:
                    db.updata_user(id1, 1)
                break
        await call.message.delete()
    else:
        if data.lower().startswith("mp3"):
            y = YouTube(data[3:])
            await call.message.delete()
            mid = await call.message.answer(text="⏳ Audio fayl tayyorlanmoqda... ")
            k = y.streams.filter(only_audio=True).first()
            k.download(f"data", f"{uid}.mp3")
            await bot.delete_message(chat_id=uid, message_id=mid.message_id)
            mid = await call.message.answer('⬇️ Audio fayl sizga yuborilmoqda...')
            if os.path.exists(f"data/{uid}.mp3"):
                await call.message.answer_audio(audio=open(f"data/{uid}.mp3", "rb"), caption=f"{y.title}",
                                                reply_markup=inline.url_video(y.channel_url))
                await bot.delete_message(chat_id=uid, message_id=mid.message_id)
                os.remove(f"data/{uid}.mp3")
                d = datetime
                db.add_yotube(uid, data[3:], "NONE", "audio/mp3", f"{d.datetime.now()}")
            else:
                await bot.delete_message(chat_id=uid, message_id=mid.message_id)
                await call.message.answer(f"❌ Audioni faylni yuklab bo'lmadi.")
        elif data.upper().startswith("FPS"):
            j = data[3:]
            p = j[:4]
            v = j[4:]
            try:
                await call.message.delete()
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
                else:
                    await bot.delete_message(chat_id=uid, message_id=mid.message_id)
                    await call.message.answer(f"❌ Videoni yuklab bo'lmadi.\n{v}")
            except Exception as e:
                await call.message.answer(f"Botda Xatolik /start ni bosing")


@dp.message_handler(text="/cleandb", user_id=ADMINS)
async def get_all_users(message: types.Message):
    db.delete_users()
    await message.answer("Baza tozalandi!")
