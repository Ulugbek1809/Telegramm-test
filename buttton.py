from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup

main_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
main_menu.row("📚 Test yechish", "📝 Test tuzish")
main_menu.row("👤 Account", "🔠 Mening testlarim")
main_menu.row("👥 Botdan foydalanuvchilar")

orqaga = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
orqaga.row("🔙 orqaga")
test_meth = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
test_meth.row("🖼 Rasm", "✏️ Yozish")
test_meth.row("❌ Bekor qilish")
telefon = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Telefon raqamni ulashish", request_contact=True)]
    ],
    resize_keyboard=True
)
test_meth2 = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
test_meth2.row("🖼 Rasm", "✏️ Yozish")
test_meth2.row("❌ Bekor qilish", "🔙 avvalgi testga qaytish")


def otkazish(value: int) -> ReplyKeyboardMarkup:
    s = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    s.row(f"{value} ga o'tish")
    return s


def tj2(a, b: str) -> InlineKeyboardMarkup:
    inl = InlineKeyboardMarkup(row_width=2)
    A = InlineKeyboardButton(text=a, callback_data=a)
    B = InlineKeyboardButton(text=b, callback_data=b)
    inl.insert(A)
    inl.insert(B)
    return inl


def tj4(a, b, c, d: str) -> InlineKeyboardMarkup:
    inl = InlineKeyboardMarkup(row_width=2)
    A = InlineKeyboardButton(text=a, callback_data=a)
    B = InlineKeyboardButton(text=b, callback_data=b)
    C = InlineKeyboardButton(text=c, callback_data=c)
    D = InlineKeyboardButton(text=d, callback_data=d)
    inl.insert(A)
    inl.insert(B)
    inl.insert(C)
    inl.insert(D)
    return inl


deletebutton = ReplyKeyboardRemove()


def start_test_button(cod: str) -> InlineKeyboardMarkup:
    a = InlineKeyboardMarkup(row_width=1)
    b = InlineKeyboardButton(text="Boshlash", callback_data=cod)
    a.insert(b)
    return a


def var4(A, B, C, D) -> InlineKeyboardMarkup:
    inl = InlineKeyboardMarkup(row_width=2)
    a = InlineKeyboardButton(text="A." + A, callback_data=A)
    b = InlineKeyboardButton(text="B." + B, callback_data=B)
    c = InlineKeyboardButton(text="C." + C, callback_data=C)
    d = InlineKeyboardButton(text="D." + D, callback_data=D)
    inl.insert(a)
    inl.insert(b)
    inl.insert(c)
    inl.insert(d)
    return inl


def var2(a, b: str) -> InlineKeyboardMarkup:
    inl = InlineKeyboardMarkup(row_width=2)
    A = InlineKeyboardButton(text="A." + a, callback_data=a)
    B = InlineKeyboardButton(text="B." + b, callback_data=b)
    inl.insert(A)
    inl.insert(B)
    return inl


delet_test = InlineKeyboardMarkup(row_width=1)
delet = InlineKeyboardButton(text="❌ o'chirish", callback_data="del")
delet_test.insert(delet)
profil = InlineKeyboardMarkup(row_width=2)
ism = InlineKeyboardButton(text="🧑 Ismni o'zgartirish", callback_data="ism")
fam = InlineKeyboardButton(text="🧑 Familiyani o'zgartirish", callback_data="fam")
tel = InlineKeyboardButton(text="📞 Telefon raqamni o'zgartirish", callback_data="tel")
profil.insert(ism)
profil.insert(fam)
profil.insert(tel)
