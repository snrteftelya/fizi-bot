import requests
import time
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
import os
import psycopg2
from aiogram.utils.markdown import hbold, hcode, hunderline, pre, hitalic, hspoiler
from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image

proxies = {"http": "195.201.19.84:443"}
DB_URI = "postgres://beazbjbqcqpwpk:419e837d6540dbd640e083b10e15711e16f411740ce38a1719564ce9018d8c3b@ec2-52-48-159-67.eu-west-1.compute.amazonaws.com:5432/d8gbkt2qdpd7fv"
token = "5339329933:AAGy-RfAx48MgtMXdJ2djuGpNJpfqZwdKh8"
storage = MemoryStorage()
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
admin_id = 644784412
db_connection = psycopg2.connect(DB_URI, sslmode="require")
db_object = db_connection.cursor()
start_buttons = ["Задача с Капельяна", "Задача с РешуЦт"]
reset_button = ["Вернуться➡"]


class get_reshuct(StatesGroup):
    get_num = State()


class get_paragraph(StatesGroup):
    get_parag = State()
    get_lev = State()
    get_number = State()


class get_ot(StatesGroup):
    get_num = State()
    get_number = State()


class get_kt(StatesGroup):
    get_number = State()


class check_yourself(StatesGroup):
    get_num = State()
    get_lev = State()
    get_number = State()


class get_ct(StatesGroup):
    get_num = State()
    get_lev = State()
    get_number = State()


@dp.message_handler(commands='start', state="*")
async def command_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*start_buttons)
    await message.answer(f'Привет, {message.from_user.username}', reply_markup=keyboard)
    await state.finish()

@dp.message_handler(Text(equals="Вернуться➡"), state="*")
async def get_reset(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*start_buttons)
    await message.answer(f'Вы вернулись в меню', reply_markup=keyboard)
    await state.finish()

@dp.message_handler(Text(equals="Задача с Капельяна"))
async def get_taskkap(message: types.Message):
    kap_buttons = ["Параграфы", "Обобщающий тест", "Контрольный тест", "Проверь себя", "Итоговый тест"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*kap_buttons).add(*reset_button)
    await message.answer(f'Выберите тип задачи', reply_markup=keyboard)


@dp.message_handler(Text(equals="Параграфы"))
async def get_option(message: types.Message, state: FSMContext):
    option_buttons = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
                     "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37",
                     "38", "39", "40"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    keyboard.add(*option_buttons).add(*reset_button)
    await message.answer(f'Теперь выберите параграф', reply_markup=keyboard)
    await get_paragraph.get_parag.set()

@dp.message_handler(state=get_paragraph.get_parag)
async def get_par(message: types.Message, state: FSMContext):
    global par
    par = message.text
    par_buttons = ["A1", "A2", "B1", "B2"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    keyboard.add(*par_buttons).add(*reset_button)
    await message.answer(f'Вы выбрали {par} параграф, теперь введите уровень сложности', reply_markup=keyboard)
    await get_paragraph.get_lev.set()

@dp.message_handler(state=get_paragraph.get_lev)
async def get_lev(message: types.Message, state: FSMContext):
    global lev
    lev = message.text
    lev_buttons = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    keyboard.add(*lev_buttons).add(*reset_button)
    await message.answer(f'Вы выбрали {lev} уровень сложности, теперь введите номер задания', reply_markup=keyboard)
    await get_paragraph.get_number.set()

@dp.message_handler(state=get_paragraph.get_number)
async def get_num(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*start_buttons)
    try:
        global num
        num = message.text
        wait = await message.answer("Подождите немного...")
        global lev
        lev1 = lev
        if par == "40" and lev1 == "A2":
            lev1 = "%D0%902"
        response = requests.get(f"https://fizika.help/image/catalog/P{par}/P{par}Test{lev1}_{num}.jpg", verify=False)
        soup = BeautifulSoup(response.text, "lxml")
        answer_from_host = str(soup.find("h1"))
        await wait.delete()
        if answer_from_host == "<h1>Запрашиваемая страница не найдена!</h1>":
            response_1 = requests.get(f"https://fizika.help/image/catalog/P{par}/P{par}Test{lev1}_{num}_1.jpg", verify=False)
            file = open("sample_image_1.png", "wb")
            file.write(response_1.content)
            file.close()
            photo_1 = open("sample_image_1.png", "rb")
            await message.answer_photo(photo=photo_1, reply_markup=keyboard)
            response_2 = requests.get(f"https://fizika.help/image/catalog/P{par}/P{par}Test{lev1}_{num}_2.jpg", verify=False)
            soup = BeautifulSoup(response_2.text, "lxml")
            answer_from_host = str(soup.find("h1"))
            if answer_from_host != "<h1>Запрашиваемая страница не найдена!</h1>":
                file = open("sample_image_2.png", "wb")
                file.write(response_2.content)
                file.close()
                photo_2 = open("sample_image_2.png", "rb")
                await message.answer_photo(photo=photo_2)
        else:
            file = open("sample_image.png", "wb")
            file.write(response.content)
            file.close()
            photo = open("sample_image.png", "rb")
            await message.answer_photo(photo=photo, reply_markup=keyboard)
    except:
        await message.answer("Повторите попытку", reply_markup=keyboard)
    finally:
        await state.finish()

@dp.message_handler(Text(equals="Обобщающий тест"))
async def get_option(message: types.Message, state: FSMContext):
    option_buttons = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    keyboard.add(*option_buttons).add(*reset_button)
    await message.answer(f'Теперь выберите номер "Обобщающего теста"', reply_markup=keyboard)
    await get_ot.get_num.set()

@dp.message_handler(state=get_ot.get_num)
async def get_lev(message: types.Message, state: FSMContext):
    lev_buttons = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
    global num_ot
    num_ot = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    keyboard.add(*lev_buttons).add(*reset_button)
    await message.answer(f'Вы выбрали "Обобщающий тест" №{num_ot}, теперь введите номер задания', reply_markup=keyboard)
    await get_ot.get_number.set()

@dp.message_handler(state=get_ot.get_number)
async def get_photo(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*start_buttons)
    try:
        global number_ot
        number_ot = message.text
        wait = await message.answer("Подождите немного...")
        response = requests.get(f"https://fizika.help/image/catalog/ObTest{num_ot}/ObTest{num_ot}_{number_ot}.jpg", verify=False)
        soup = BeautifulSoup(response.text, "lxml")
        answer_from_host = str(soup.find("h1"))
        await wait.delete()
        if answer_from_host == "<h1>Запрашиваемая страница не найдена!</h1>":
            response_1 = requests.get(f"https://fizika.help/image/catalog/ObTest{num_ot}/ObTest{num_ot}_{number_ot}_1.jpg", verify=False)
            file = open("sample_image_1.png", "wb")
            file.write(response_1.content)
            file.close()
            photo_1 = open("sample_image_1.png", "rb")
            await message.answer_photo(photo=photo_1, reply_markup=keyboard)
            response_2 = requests.get(f"https://fizika.help/image/catalog/ObTest{num_ot}/ObTest{num_ot}_{number_ot}_2.jpg", verify=False)
            soup = BeautifulSoup(response_2.text, "lxml")
            answer_from_host = str(soup.find("h1"))
            if answer_from_host != "<h1>Запрашиваемая страница не найдена!</h1>":
                file = open("sample_image_2.png", "wb")
                file.write(response_2.content)
                file.close()
                photo_2 = open("sample_image_2.png", "rb")
                await message.answer_photo(photo=photo_2)
        else:
            file = open("sample_image.png", "wb")
            file.write(response.content)
            file.close()
            photo = open("sample_image.png", "rb")
            await message.answer_photo(photo=photo, reply_markup=keyboard)
    except:
        await message.answer("Повторите попытку", reply_markup=keyboard)
    finally:
        await state.finish()

@dp.message_handler(Text(equals="Контрольный тест"))
async def get_option(message: types.Message, state: FSMContext):
    option_buttons = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                     "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    keyboard.add(*option_buttons).add(*reset_button)
    await message.answer(f'Теперь выберите номер задачи', reply_markup=keyboard)
    await get_kt.get_number.set()

@dp.message_handler(state=get_kt.get_number)
async def get_photo(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*start_buttons)
    try:
        global number_kt
        number_kt = message.text
        wait = await message.answer("Подождите немного...")
        response = requests.get(f"https://fizika.help/image/catalog/KontrTest/KontrTest_{number_kt}.jpg", verify=False)
        soup = BeautifulSoup(response.text, "lxml")
        answer_from_host = str(soup.find("h1"))
        await wait.delete()
        if answer_from_host == "<h1>Запрашиваемая страница не найдена!</h1>":
            response_1 = requests.get(f"https://fizika.help/image/catalog/KontrTest/KontrTest_{number_kt}_1.jpg", verify=False)
            file = open("sample_image_1.png", "wb")
            file.write(response_1.content)
            file.close()
            photo_1 = open("sample_image_1.png", "rb")
            await message.answer_photo(photo=photo_1, reply_markup=keyboard)
            response_2 = requests.get(f"https://fizika.help/image/catalog/KontrTest/KontrTest_{number_kt}_2.jpg", verify=False)
            soup = BeautifulSoup(response_2.text, "lxml")
            answer_from_host = str(soup.find("h1"))
            if answer_from_host != "<h1>Запрашиваемая страница не найдена!</h1>":
                file = open("sample_image_2.png", "wb")
                file.write(response_2.content)
                file.close()
                photo_2 = open("sample_image_2.png", "rb")
                await message.answer_photo(photo=photo_2)
        else:
            file = open("sample_image.png", "wb")
            file.write(response.content)
            file.close()
            photo = open("sample_image.png", "rb")
            await message.answer_photo(photo=photo, reply_markup=keyboard)
    except:
        await message.answer("Повторите попытку", reply_markup=keyboard)
    finally:
        await state.finish()

@dp.message_handler(Text(equals="Проверь себя"))
async def get_option(message: types.Message, state: FSMContext):
    option_buttons = ["1", "2", "3"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    keyboard.add(*option_buttons).add(*reset_button)
    await message.answer(f'Теперь выберите номер "Проверь себя"', reply_markup=keyboard)
    await check_yourself.get_num.set()

@dp.message_handler(state=check_yourself.get_num)
async def get_par(message: types.Message, state: FSMContext):
    global num_check
    num_check = message.text
    num_buttons = ["A", "B"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*num_buttons).add(*reset_button)
    await message.answer(f'Вы выбрали {num_check} номер "Проверь себя", теперь введите уровень сложности', reply_markup=keyboard)
    await check_yourself.get_lev.set()

@dp.message_handler(Text(equals="A"), state=check_yourself.get_lev)
async def get_lev(message: types.Message, state: FSMContext):
    global lev_check
    lev_check = message.text
    lev_buttons = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "12", "13", "14", "15", "16", "17", "18"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    keyboard.add(*lev_buttons).add(*reset_button)
    await message.answer(f'Вы выбрали уровень сложности {lev_check}, теперь введите номер задания', reply_markup=keyboard)
    await check_yourself.get_number.set()

@dp.message_handler(Text(equals="B"), state=check_yourself.get_lev)
async def get_lev(message: types.Message, state: FSMContext):
    global lev_check
    lev_check = message.text
    lev_buttons = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "12"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    keyboard.add(*lev_buttons).add(*reset_button)
    await message.answer(f'Вы выбрали уровень сложности {lev_check}, теперь введите номер задания', reply_markup=keyboard)
    await check_yourself.get_number.set()

@dp.message_handler(state=check_yourself.get_number)
async def get_number(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*start_buttons)
    try:
        global number_check
        number_check = message.text
        wait = await message.answer("Подождите немного...")
        response = requests.get(f"https://fizika.help/image/catalog/ProverSebya{num_check}/ProverSebya{num_check}_{lev_check}1_{number_check}.jpg", verify=False)
        soup = BeautifulSoup(response.text, "lxml")
        answer_from_host = str(soup.find("h1"))
        await wait.delete()
        if answer_from_host == "<h1>Запрашиваемая страница не найдена!</h1>":
            response_1 = requests.get(f"https://fizika.help/image/catalog/ProverSebya{num_check}/ProverSebya{num_check}_{lev_check}1_{number_check}_1.jpg", verify=False)
            file = open("sample_image_1.png", "wb")
            file.write(response_1.content)
            file.close()
            photo_1 = open("sample_image_1.png", "rb")
            await message.answer_photo(photo=photo_1, reply_markup=keyboard)
            response_2 = requests.get(f"https://fizika.help/image/catalog/ProverSebya{num_check}/ProverSebya{num_check}_{lev_check}1_{number_check}_2.jpg", verify=False)
            soup = BeautifulSoup(response_2.text, "lxml")
            answer_from_host = str(soup.find("h1"))
            if answer_from_host != "<h1>Запрашиваемая страница не найдена!</h1>":
                file = open("sample_image_2.png", "wb")
                file.write(response_2.content)
                file.close()
                photo_2 = open("sample_image_2.png", "rb")
                await message.answer_photo(photo=photo_2)
        else:
            file = open("sample_image.png", "wb")
            file.write(response.content)
            file.close()
            photo = open("sample_image.png", "rb")
            await message.answer_photo(photo=photo, reply_markup=keyboard)
    except:
        await message.answer("Повторите попытку", reply_markup=keyboard)
    finally:
        await state.finish()

@dp.message_handler(Text(equals="Итоговый тест"))
async def get_option(message: types.Message, state: FSMContext):
    option_buttons = ["1", "2", "3", "4", "5", "6", "7", "8"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    keyboard.add(*option_buttons).add(*reset_button)
    await message.answer(f'Теперь выберите номер', reply_markup=keyboard)
    await get_ct.get_num.set()

@dp.message_handler(state=get_ct.get_num)
async def get_par(message: types.Message, state: FSMContext):
    global num_ct
    num_ct = message.text
    par_buttons = ["A", "B"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    keyboard.add(*par_buttons).add(*reset_button)
    await message.answer(f'Вы выбрали {num_ct} номер, теперь введите уровень сложности', reply_markup=keyboard)
    await get_ct.get_lev.set()

@dp.message_handler(Text(equals="A"), state=get_ct.get_lev)
async def get_lev(message: types.Message, state: FSMContext):
    global lev_ct
    lev_ct = message.text
    lev_buttons = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "12", "13", "14", "15", "16", "17", "18"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    keyboard.add(*lev_buttons).add(*reset_button)
    await message.answer(f'Вы выбрали {lev_ct} уровень сложности, теперь введите номер задания', reply_markup=keyboard)
    await get_ct.get_number.set()

@dp.message_handler(Text(equals="B"), state=get_ct.get_lev)
async def get_lev(message: types.Message, state: FSMContext):
    global lev_ct
    lev_ct = message.text
    lev_buttons = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "12"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    keyboard.add(*lev_buttons).add(*reset_button)
    await message.answer(f'Вы выбрали {lev_ct} уровень сложности, теперь введите номер задания', reply_markup=keyboard)
    await get_ct.get_number.set()

@dp.message_handler(state=get_ct.get_number)
async def get_number(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*start_buttons)
    try:
        global number_ct
        number_ct = message.text
        wait = await message.answer("Подождите немного...")
        response = requests.get(f"https://fizika.help/image/catalog/ItogTest{num_ct}/ItogTest{num_ct}_{lev_ct}_{number_ct}.jpg", verify=False)
        soup = BeautifulSoup(response.text, "lxml")
        answer_from_host = str(soup.find("h1"))
        await wait.delete()
        if answer_from_host == "<h1>Запрашиваемая страница не найдена!</h1>":
            response_1 = requests.get(f"https://fizika.help/image/catalog/ItogTest{num_ct}/ItogTest{num_ct}_{lev_ct}_{number_ct}_1.jpg", verify=False)
            file = open("sample_image_1.png", "wb")
            file.write(response_1.content)
            file.close()
            photo_1 = open("sample_image_1.png", "rb")
            await message.answer_photo(photo=photo_1, reply_markup=keyboard)
            response_2 = requests.get(f"https://fizika.help/image/catalog/ItogTest{num_ct}/ItogTest{num_ct}_{lev_ct}_{number_ct}_2.jpg", verify=False)
            soup = BeautifulSoup(response_2.text, "lxml")
            answer_from_host = str(soup.find("h1"))
            if answer_from_host != "<h1>Запрашиваемая страница не найдена!</h1>":
                file = open("sample_image_2.png", "wb")
                file.write(response_2.content)
                file.close()
                photo_2 = open("sample_image_2.png", "rb")
                await message.answer_photo(photo=photo_2)
        else:
            file = open("sample_image.png", "wb")
            file.write(response.content)
            file.close()
            photo = open("sample_image.png", "rb")
            await message.answer_photo(photo=photo, reply_markup=keyboard)
    except:
        await message.answer("Повторите попытку", reply_markup=keyboard)
    finally:
        await state.finish()


@dp.message_handler(Text(equals="Задача с РешуЦт"))
async def get_taskreshuct(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*reset_button)
    await message.answer("Введите номер задания", reply_markup=keyboard)
    await get_reshuct.get_num.set()

@dp.message_handler(state=get_reshuct.get_num)
async def get_id(message:types.Message, state: FSMContext):
    if message.text.isdigit():
        try:
            global i
            i = message.text
            url = f"https://phys.reshuct.by/problem?id={i}"
            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),
                                      chrome_options=chrome_options)
            try:
                buttons = [
                    types.InlineKeyboardButton("Решение", callback_data="resh")
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(*buttons)
                text_test = await message.answer(f"Задание №{i}\nПодождите немного...")
                driver.get(url=url)
                driver.get_window_size()
                required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
                required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
                driver.set_window_size(required_width, required_height)
                element_all = driver.find_element(By.CLASS_NAME, 'prob_maindiv')
                location_all = element_all.location
                element_resh = driver.find_element(By.CLASS_NAME, 'solution')
                location_resh = element_resh.location
                right = element_all.size['width']
                y1 = location_all['y']
                y2 = location_resh['y']
                y_for_crop = y2 - y1
                resh_photo = driver.find_element(By.CLASS_NAME, 'prob_maindiv')
                time.sleep(1)
                resh_photo.screenshot("test.png")
                im = Image.open('test.png')
                im = im.crop((0, 0, right, y_for_crop))
                im.save('test.png')
                photo1 = open("test.png", "rb")
                global photo_task
                photo_task = await message.answer_photo(photo=photo1)
                global id_task
                id_task = photo_task['photo'][0]['file_id']
                print(id_task)
                await text_test.edit_text(text=f"Условие задания №{i}", reply_markup=keyboard)
            except:
                await message.answer("Такого задания не существует...")
            finally:
                driver.close()
                driver.quit()
        except:
            await state.finish()
    else:
        await message.answer("Проверьте номер задания...")


@dp.callback_query_handler(text="resh", state=get_reshuct.get_num)
async def resh(call: types.CallbackQuery):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    url = f"https://phys.reshuct.by/problem?id={i}"
    try:
        buttons = [
            types.InlineKeyboardButton("К тесту", callback_data="test")
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        await call.message.edit_text(text=f"Подождите немного...")
        driver.get(url=url)
        driver.get_window_size()
        required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(required_width, required_height)
        element = driver.find_element(By.CLASS_NAME, 'solution')
        location = element.location
        y = location['y']
        driver.execute_script(f"window.scrollTo(0, {y})")
        resh_photo = driver.find_element(By.CLASS_NAME, 'solution')
        time.sleep(1)
        resh_photo.screenshot("resh.png")
        photo2 = open("resh.png", "rb")
        global photo_answ
        photo_answ = await call.message.answer_photo(photo=photo2)
        global id_answ
        id_answ = photo_answ['photo'][0]['file_id']
        print(id_answ)
        await call.message.edit_text(text=f"Решение задания №{i}", reply_markup=keyboard)
        await call.answer(show_alert=True)
        try:
            await photo_task.delete()
        except:
            pass
    except:
        await call.message.answer("У этого номера нет ответа😢")
    finally:
        postgres_insert_query = """ INSERT INTO photo_id(number, test_id, resh_id) VALUES (%s, %s, %s)"""
        record_to_insert = (i, id_task, id_answ)
        db_object.execute(postgres_insert_query, record_to_insert)
        db_connection.commit()
        db_object.close()
        db_connection.close()
        driver.close()
        driver.quit()

@dp.callback_query_handler(text="test", state=get_reshuct.get_num)
async def test(call: types.CallbackQuery, state: FSMContext):
    try:
        url = f"https://phys.reshuct.by/problem?id={i}"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        buttons = [
            types.InlineKeyboardButton("Решение", callback_data="resh")
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        await call.message.edit_text(text=f"Подождите немного...")
        driver.get(url=url)
        driver.get_window_size()
        required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(required_width, required_height)
        element_all = driver.find_element(By.CLASS_NAME, 'prob_maindiv')
        location_all = element_all.location
        element_resh = driver.find_element(By.CLASS_NAME, 'solution')
        location_resh = element_resh.location
        right = element_all.size['width']
        y1 = location_all['y']
        y2 = location_resh['y']
        y_for_crop = y2 - y1
        resh_photo = driver.find_element(By.CLASS_NAME, 'prob_maindiv')
        time.sleep(1)
        resh_photo.screenshot("test.png")
        im = Image.open('test.png')
        im = im.crop((0, 0, right, y_for_crop))
        im.save('test.png')
        photo1 = open("test.png", "rb")
        global photo_task
        photo_task = await call.message.answer_photo(photo=photo1)
        await call.message.edit_text(text=f"Условие задания №{i}", reply_markup=keyboard)
        try:
            await photo_answ.delete()
        except:
            pass
        finally:
            driver.close()
            driver.quit()
    except:
        await call.message.answer("Ой, что-то пошло не так😢")
    finally:
        await call.answer(show_alert=True)


if __name__ == '__main__':
    while True:
        try:
            executor.start_polling(dp, skip_updates=True)
        except:
            time.sleep(5)
