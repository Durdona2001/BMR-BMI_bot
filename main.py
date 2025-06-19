from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

# 🔐 Tokenni shu yerga to‘g‘ridan-to‘g‘ri yozamiz
BOT_TOKEN = "8120595784:AAFbNco72kQ2GYjOvgsvyGYEBxWMKJoWc60"

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Holatlar (States)
class Form(StatesGroup):
    gender = State()
    age = State()
    height = State()
    weight = State()

# /start
@dp.message_handler(commands="start")
async def start_handler(message: types.Message):
    await message.answer("Salom! BMR/BMI hisoblovchi botga xush kelibsiz.\nJinsingizni kiriting (Erkak/Ayol):")
    await Form.gender.set()

@dp.message_handler(state=Form.gender)
async def process_gender(message: types.Message, state: FSMContext):
    gender = message.text.lower()
    if gender not in ["erkak", "ayol"]:
        return await message.reply("Iltimos, 'Erkak' yoki 'Ayol' deb yozing.")
    await state.update_data(gender=gender)
    await message.answer("Yoshingizni yozing:")
    await Form.next()

@dp.message_handler(state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.reply("Faqat son yozing. Masalan: 24")
    await state.update_data(age=int(message.text))
    await message.answer("Bo'yingizni kiriting (sm):")
    await Form.next()

@dp.message_handler(state=Form.height)
async def process_height(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.reply("Faqat son yozing. Masalan: 168")
    await state.update_data(height=int(message.text))
    await message.answer("Vazningizni yozing (kg):")
    await Form.next()

@dp.message_handler(state=Form.weight)
async def process_weight(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.reply("Faqat son yozing. Masalan: 70")
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    gender, age, height, weight = data['gender'], data['age'], data['height'], data['weight']

    # BMI
    height_m = height / 100
    bmi = weight / (height_m ** 2)

    # BMR hisoblash (Mifflin-St Jeor formulasi)
    if gender == "erkak":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    natija = f"✅ Natijangiz:\n\n🧮 BMR: {bmr:.2f} kcal/kun\n⚖️ BMI: {bmi:.2f}"

    await message.answer(natija)
    await state.finish()

# Botni ishga tushirish
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
