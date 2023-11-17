import logging
import re

from aiogram import types, Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

import buttton
import config
import database
import ran
from buttton import telefon
from config import TOKEN
from states import registr

andoza_phone = "(?:\+[9]{2}[8][0-9]{2}[0-9]{3}[0-9]{2}[0-9]{2})"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=["start"], state='*')
async def start_send(message: types.Message):
    ID = message.from_user.id
    n = message.from_user.username
    name = message.from_user.first_name
    if len(database.ac.get_mal(ID)) == 3:
        await message.answer(f"Assalomu allaykum {database.ac.get_full_name(ID)}")
        await message.answer(f"Botdan foydalanishingiz mumkin !", reply_markup=buttton.main_menu)
        await registr.main.set()
    else:
        database.ac.user_name_id(ID, n)
        r = ReplyKeyboardRemove()
        await message.answer(f"Assalomu allaykum {name} tizimdan ro'yhatdan o'ting")
        await message.answer("Ismingizni kiriting:", reply_markup=r)
        await registr.ism.set()


@dp.message_handler(state=registr.ism)
async def send_ism(message: types.Message, state: FSMContext):
    ism = message.text
    await state.update_data(
        {"ism": ism},
    )
    await message.answer(f"familyangizni kiriting:")
    await registr.next()


@dp.message_handler(state=registr.familya)
async def send_familya(message: types.Message, state: FSMContext):
    familya = message.text
    await state.update_data(
        {'familya': familya}
    )
    await message.answer(f"Telefon raqamingizni yuboring:", reply_markup=telefon)
    await registr.next()


@dp.message_handler(state=registr.main)
async def test_tuzish(message: types.Message):
    a = message.text
    d = str(message.from_user.id)
    if a == "📝 Test tuzish":
        await message.answer("Test nomini yozing", reply_markup=buttton.orqaga)
        await registr.testnomi.set()
    elif a == "🔠 Mening testlarim":
        aso = database.ac.may_test(d)
        if aso != "😥 Siz hali test tuzmadingiz.":
            await message.answer(aso, reply_markup=buttton.delet_test)
        else:
            await message.answer(aso)
    elif a == "📚 Test yechish":
        await message.answer("Test kodini kiriting", reply_markup=buttton.orqaga)
        await registr.testcod.set()
    elif a == "👤 Account":
        await message.answer(database.ac.get_account(d), reply_markup=buttton.profil)
    elif a == "👥 Botdan foydalanuvchilar":
        await message.answer(database.ac.get_bot_soni())


@dp.message_handler(state=registr.telefon, content_types=['contact'])
async def telefon_send(message: types.Message, state: FSMContext):
    number = message.contact["phone_number"]
    ID = message.from_user.id
    n = number[:1]
    if n != "+":
        n = number
        number = "+"
        number += n
    if re.match(andoza_phone, number):
        await state.update_data(
            {"number": number}
        )
        data = await state.get_data()
        ism = data.get('ism')
        familya = data.get('familya')
        number = data.get("number")
        database.ac.set_mal(ID, [ism, familya, number])
        await bot.send_message(config.ADMIN, f"Botda yangi foydalanuvhi {familya} {ism}",
                               reply_markup=buttton.main_menu)
        await message.answer("Bot dan foydalanishingiz mumkin !")
        await registr.main.set()
    else:
        await message.answer("Bot faqat o'zbeklar uchun uchun")


@dp.message_handler(state=registr.rtel, content_types=['contact'])
async def rtelefon_send(message: types.Message):
    number = message.contact["phone_number"]
    ID = str(message.from_user.id)
    j = database.ac.get_mal(ID)
    del j[2]
    j.append(str(number))
    database.ac.set_mal(ID, j)
    await message.answer("Telefon raqam o'zgartirildi.", reply_markup=buttton.main_menu)
    await registr.main.set()


@dp.message_handler(state=registr.testnomi, text="🔙 orqaga")
async def test_tuzish(message: types.Message):
    await message.answer("Bosh menyuga qaytdingiz", reply_markup=buttton.main_menu)
    await registr.main.set()


@dp.message_handler(state=registr.testnomi)
async def test_tanlash(message: types.Message):
    d = message.from_user.id
    database.temp.start(d, message.text)
    await message.answer(f"{str(database.temp.testvalue(d) + 1)}-Test savol metodini tanlang ",
                         reply_markup=buttton.test_meth)
    await registr.tan.set()


@dp.message_handler(state=registr.tan)
async def bekor(message: types.Message, state: FSMContext):
    d = message.from_user.id
    mm = message.text
    if mm == "❌ Bekor qilish":
        if database.temp.testvalue(str(d)) == 0:
            await message.answer(f"❌ {database.temp.get_test_name(d)} bekor qilindi.", reply_markup=buttton.main_menu)
            await registr.main.set()
        else:
            g = ran.generator_cod()
            database.ac.save_cod(d, g)
            database.tes.savetest(str(d), g, database.temp.get_test(str(d)))
            await message.answer(f"✔ {database.temp.get_test_name(d)} saqlandi cod {g}.",
                                 reply_markup=buttton.main_menu)
            await registr.main.set()
    elif mm == "🖼 Rasm":
        await state.update_data(
            {"method": "rasm"}
        )
        await message.answer("Rasm yuboring", reply_markup=buttton.orqaga)
        await registr.rasm.set()
    elif mm == "✏️ Yozish":
        await state.update_data(
            {"method": "yoz"}
        )
        await message.answer("savolni yozing", reply_markup=buttton.orqaga)
        await registr.izohrasm.set()
    elif mm == "🔙 avvalgi testga qaytish":
        database.temp.delet(d)
        a = database.temp.testvalue(d) + 1
        if a != 1:
            await message.answer(f"{str(a)}-Test savol metodini tanlang ",
                                 reply_markup=buttton.test_meth2)
        else:
            await message.answer(f"{str(a)}-Test savol metodini tanlang ",
                                 reply_markup=buttton.test_meth)
        await registr.tan.set()
    else:
        await message.answer("savol metodini tanlang")


@dp.message_handler(state=registr.rasm, content_types=["photo"])
async def rasm(message: types.Message, state: FSMContext):
    p = message.photo[-1].file_id
    r = ReplyKeyboardRemove()
    await state.update_data({"rasm": p})
    await message.answer("Izoh yozing", reply_markup=r)
    await registr.izohrasm.set()


@dp.message_handler(state=registr.rasm)
async def rasm_xato(message: types.Message):
    d = message.text
    if d != "🔙 orqaga":
        await message.answer("Rasm yuboring")
    else:
        d = message.from_user.id
        await message.answer(f"{str(database.temp.testvalue(d) + 1)}-savol metodini tanlang ",
                             reply_markup=buttton.test_meth)
        await registr.tan.set()


@dp.message_handler(state=registr.izohrasm)
async def izohras(message: types.Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    aso = data.get("method")
    if aso == "rasm" and text != "🔙 orqaga":
        rasm = data.get("rasm")
        await state.update_data({"izohrasm": text})
        await message.answer_photo(photo=rasm, caption=f"{text}\n\nA varinatni kiriting")
        await registr.avar.set()
    elif aso == "yoz" and text != "🔙 orqaga":
        await state.update_data({"izoh": text})
        await message.answer(f"{text}\n\nA varinatni kiriting", reply_markup=buttton.deletebutton)
        await registr.avar.set()
    else:
        d = str(message.from_user.id)
        await message.answer(f"{str(database.temp.testvalue(d) + 1)}-savol metodini tanlang ",
                             reply_markup=buttton.test_meth)
        await registr.tan.set()


@dp.message_handler(state=registr.avar)
async def avar(message: types.Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    aso = data.get("method")
    if aso == "rasm":
        iz = data.get("izohrasm")
        rasm = data.get("rasm")
        await state.update_data({"A": text})
        await message.answer_photo(photo=rasm, caption=f"{iz}\nA.{text}\n\n B variantni kiriting")
    elif aso == "yoz":
        iz = data.get("izoh")
        await state.update_data({"A": text})
        await message.answer(f"{iz}\nA.{text}\n\nB variantni kiriting")
    await registr.bvar.set()


@dp.message_handler(state=registr.bvar)
async def bvar(message: types.Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    a = data.get("A")
    aso = data.get("method")
    if aso == "rasm":
        rasm = data.get("rasm")
        iz = data.get("izohrasm")
        await state.update_data({"B": text})
        await message.answer_photo(photo=rasm, caption=f"{iz}\n\nA.{a}\nB.{text}\n\n C variantni kiriting",
                                   reply_markup=buttton.otkazish(
                                       database.temp.testvalue(str(message.from_user.id)) + 2))
    elif aso == "yoz":
        iz = data.get("izoh")
        await state.update_data({"B": text})
        await message.answer(f"{iz}\nA.{a}\nB.{text}\n\n C variantni kiriting",
                             reply_markup=buttton.otkazish(
                                 database.temp.testvalue(str(message.from_user.id)) + 2))
    await registr.cvar.set()


@dp.message_handler(state=registr.cvar)
async def cvar(message: types.Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    a = data.get("A")
    b = data.get("B")
    aso = data.get("method")
    rasm = data.get("rasm")
    if text != str(database.temp.testvalue(str(message.from_user.id)) + 2) + " ga o'tish":
        if aso == "rasm":
            iz = data.get("izohrasm")
            await state.update_data({"C": text})
            await message.answer_photo(photo=rasm, caption=f"{iz}\n\nA.{a}\nB.{b}\nC.{text}\n\n D variantni kiriting",
                                       reply_markup=buttton.deletebutton)
        elif aso == "yoz":
            iz = data.get("izoh")
            await state.update_data({"C": text})
            await message.answer(f"{iz}\n\nA.{a}\nB.{b}\nC.{text}\n\n D variantni kiriting",
                                 reply_markup=buttton.deletebutton)
        await registr.dvar.set()
    else:
        if aso == "rasm":
            iz = data.get("izohrasm")
            await message.answer("Keyingi testga o'tish", reply_markup=buttton.deletebutton)
            await message.answer_photo(photo=rasm, caption=f"{iz} \n\nTo'g'ri javobni belgilang",
                                       reply_markup=buttton.tj2(a, b))
        elif aso == "yoz":
            iz = data.get("izoh")
            await message.answer("Keyingi testga o'tish", reply_markup=buttton.deletebutton)
            await message.answer(f"{iz} \n\nTo'g'ri javobni belgilang",
                                 reply_markup=buttton.tj2(a, b))
        await registr.tj2.set()


@dp.callback_query_handler(state=registr.tj2)
async def cvar(call: types.CallbackQuery, state: FSMContext):
    text = call.data
    d = str(call.from_user.id)
    data = await state.get_data()
    a = data.get("A")
    b = data.get("B")
    m = data.get("method")
    da = {}
    aso = data.get("method")
    if aso == "rasm":
        rasm = data.get("rasm")
        iz = data.get("izohrasm")
        da = {
            database.temp.get_test_name(d): {"method": m, "var": 2, "rasm": rasm, "iz": iz, "A": a, "B": b, "tj": text}}
    elif aso == "yoz":
        iz = data.get("izoh")
        da = {database.temp.get_test_name(d): {"method": m, "var": 2, "iz": iz, "A": a, "B": b, "tj": text}}
    base = database.temp.get_test(str(d))
    base.append(da)
    database.temp.set_test(str(d), base)
    await call.message.answer(f"{str(database.temp.testvalue(d) + 1)}-Test savol metodini tanlang ",
                              reply_markup=buttton.test_meth2)
    await call.message.delete()
    await registr.tan.set()


@dp.message_handler(state=registr.dvar)
async def dvar(message: types.Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    rasm = data.get("rasm")
    iz = data.get("izohrasm")
    a = data.get("A")
    b = data.get("B")
    c = data.get("C")
    aso = data.get("method")
    await state.update_data(
        {"D": text}
    )
    if aso == "rasm":
        await message.answer_photo(photo=rasm,
                                   caption=f"{iz}\n\nA.{a}\nB.{b}\nC.{c}\nD.{text}\n\nTo'g'ri javobni belgilang",
                                   reply_markup=buttton.tj4(a, b, c, text))
    elif aso == "yoz":
        iz = data.get("izoh")
        await message.answer(f"{iz}\n\nA.{a}\nB.{b}\nC.{c}\nD.{text}\n\nTo'g'ri javobni belgilang",
                             reply_markup=buttton.tj4(a, b, c, text))
    await registr.tj4.set()


@dp.callback_query_handler(state=registr.tj4)
async def tj4(call: types.CallbackQuery, state: FSMContext):
    text = call.data
    d = str(call.from_user.id)
    data = await state.get_data()
    rasm = data.get("rasm")
    a = data.get("A")
    b = data.get("B")
    c = data.get("C")
    d1 = data.get("D")
    m = data.get("method")
    da = {}
    if m == "rasm":
        iz = data.get("izohrasm")
        da = {database.temp.get_test_name(d): {"method": m, "var": 4, "rasm": rasm, "iz": iz, "A": a, "B": b, "C": c,
                                               "D": d1, "tj": text}}
    elif m == "yoz":
        iz = data.get("izoh")
        da = {database.temp.get_test_name(d): {"method": m, "var": 4, "iz": iz, "A": a, "B": b, "C": c, "D": d1,
                                               "tj": text}}
    base = database.temp.get_test(str(d))
    base.append(da)
    database.temp.set_test(str(d), base)
    await call.message.delete()
    await call.message.answer(f"{str(database.temp.testvalue(d) + 1)}-Test savol metodini tanlang ",
                              reply_markup=buttton.test_meth2)
    await registr.tan.set()


@dp.message_handler(state=registr.testcod)
async def test_yechish(message: types.Message, state: FSMContext):
    text = message.text
    cod = database.tes.get_test_mal(str(text))
    if text != "🔙 orqaga":
        if cod == "none":
            await message.answer(f"❌ {text} bunday test mavjud emas !")
        else:
            cod2 = database.tes.get_test_mal_full(text)
            await state.update_data({"bolim": list(cod2['test'][0].keys())[0]})
            await state.update_data({"soni": len(cod2['test']) - 1})
            await state.update_data({"xozir": -1})
            await state.update_data({"tru": []})
            await state.update_data({"cod": text})
            await state.update_data({"vaz": "sav"})
            await message.answer(cod, reply_markup=buttton.start_test_button(text))
            await registr.testyechish.set()
    else:
        await message.answer("Bosh sahifaga qaytdingiz", reply_markup=buttton.main_menu)
        await registr.main.set()


@dp.message_handler(state=registr.testyechish, text="🔙 orqaga")
async def test_tu(message: types.Message):
    await message.answer("Bosh menyuga qaytdingiz", reply_markup=buttton.main_menu)
    await registr.main.set()


@dp.callback_query_handler(state=registr.testyechish)
async def test_yechi(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tcod = data.get("cod")
    dat = call.data
    hoz = data.get("xozir")
    ish = data.get("vaz")
    son = data.get("soni")
    tru = data.get("tru")
    bolim = data.get("bolim")
    cod = database.tes.get_test_mal_full(str(tcod))
    await call.answer(cache_time=15)
    await call.message.delete()
    if ish == "tj" and cod['test'][hoz][bolim]["tj"] == dat:
        await state.update_data({"vaz": "tj"})
        tru.append(1)
        await state.update_data({"tru": tru})
        await call.message.answer(f"✔ {hoz + 1}-to'g'ri javob")
    elif ish == "tj" and cod['test'][hoz][bolim]["tj"] != dat:
        await state.update_data({"vaz": "tj"})
        await call.message.answer(f"❌ {hoz + 1}-xato javob")
    if hoz < son:
        await state.update_data({"xozir": hoz + 1})
        if cod['test'][hoz + 1][bolim]["method"] == "yoz" and cod['test'][hoz + 1][bolim]["var"] == 4:
            a = cod['test'][hoz + 1][bolim]["A"]
            b = cod['test'][hoz + 1][bolim]["B"]
            c = cod['test'][hoz + 1][bolim]["C"]
            d = cod['test'][hoz + 1][bolim]["D"]
            await state.update_data({"vaz": "tj"})
            await call.message.answer(cod['test'][hoz + 1][bolim]["iz"], reply_markup=buttton.var4(a, b, c, d))
        elif cod['test'][hoz + 1][bolim]["method"] == "yoz" and cod['test'][hoz + 1][bolim]["var"] == 2:
            a = cod['test'][hoz + 1][bolim]["A"]
            b = cod['test'][hoz + 1][bolim]["B"]
            await state.update_data({"vaz": "tj"})
            await call.message.answer(cod['test'][hoz + 1][bolim]["iz"], reply_markup=buttton.var2(a, b))
        elif cod['test'][hoz + 1][bolim]["method"] == "rasm" and cod['test'][hoz + 1][bolim]["var"] == 2:
            a = cod['test'][hoz + 1][bolim]["A"]
            b = cod['test'][hoz + 1][bolim]["B"]
            await state.update_data({"vaz": "tj"})
            await call.message.answer_photo(photo=cod['test'][hoz + 1][bolim]["rasm"],
                                            caption=cod['test'][hoz + 1][bolim]["iz"], reply_markup=buttton.var2(a, b))
        elif cod['test'][hoz + 1][bolim]["method"] == "rasm" and cod['test'][hoz + 1][bolim]["var"] == 4:
            a = cod['test'][hoz + 1][bolim]["A"]
            b = cod['test'][hoz + 1][bolim]["B"]
            c = cod['test'][hoz + 1][bolim]["C"]
            d = cod['test'][hoz + 1][bolim]["D"]
            await state.update_data({"vaz": "tj"})
            await call.message.answer_photo(photo=cod['test'][hoz + 1][bolim]["rasm"],
                                            caption=cod['test'][hoz + 1][bolim]["iz"],
                                            reply_markup=buttton.var4(a, b, c, d))
    else:
        await call.message.answer(
            f"Test tugadi ! \n✔ To'g'ri javoblar soni: {len(tru)}\n❌ Noto'g'ri javoblar soni: {(son + 1) - len(tru)}",
            reply_markup=buttton.main_menu)
        await registr.main.set()


@dp.callback_query_handler(state=registr.main)
async def delet_test(call: types.CallbackQuery):
    a = call.data
    await call.message.delete()
    if a == "del":
        await call.message.answer("O'chirmoqchi bo'lgan testingizni tartib raqamini yuboring:",
                                  reply_markup=buttton.orqaga)
        await registr.delet_test.set()
    elif a == "ism":
        await call.message.answer("Ismingizni kiriting:", reply_markup=buttton.deletebutton)
        await registr.rism.set()
    elif a == "fam":
        await call.message.answer("Familiyangizni kiriting:", reply_markup=buttton.deletebutton)
        await registr.rfam.set()
    elif a == "tel":
        await call.message.answer("Telefon raqamingizni yuboring:", reply_markup=buttton.telefon)
        await registr.rtel.set()


@dp.message_handler(state=registr.rism)
async def rname(message: types.Message):
    i = message.from_user.id
    a = database.ac.get_mal(str(i))
    del a[0]
    a.insert(0, str(message.text))
    database.ac.set_mal(i, a)
    await message.answer("Ism muafaqiyatli o'zgartirildi", reply_markup=buttton.main_menu)
    await registr.main.set()


@dp.message_handler(state=registr.rfam)
async def rname(message: types.Message):
    i = message.from_user.id
    a = database.ac.get_mal(str(i))
    del a[1]
    a.insert(1, str(message.text))
    database.ac.set_mal(i, a)
    await message.answer("Familiya muafaqiyatli o'zgartirildi", reply_markup=buttton.main_menu)
    await registr.main.set()


@dp.message_handler(state=registr.delet_test)
async def delet_test_ort(message: types.Message):
    text = message.text
    i = str(message.from_user.id)
    if text == "🔙 orqaga":
        await message.answer("Bosh sahifaga qaytdingiz", reply_markup=buttton.main_menu)
        await registr.main.set()
    else:
        try:
            a1 = database.ac.delet_cod(i, int(text))
            if a1 == True:
                await message.answer(f"✔ {text}-o'chirildi.", reply_markup=buttton.main_menu)
                await registr.main.set()
            else:
                await message.answer(f"{text} mavjud emas")
        except Exception:
            await message.answer("xato xabar yubordingiz")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
