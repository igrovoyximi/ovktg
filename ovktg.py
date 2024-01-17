import telebot
import requests
bot = telebot.TeleBot('')
registered_users = {}
tokenurl = 0
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    login = telebot.types.KeyboardButton('Войти')
    keyboard.add(login)
    bot.send_message(chat_id, 'Добро пожаловать! Этот бот создан для посещения OpenVK и OpenVK-подобных сайтов (которые построенны на OVKAPI). Бот создан @Loroteber, зеркало от @MT657x', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == 'Войти')

def login(message):
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    ovk = telebot.types.KeyboardButton('ovk.to')
    vovk = telebot.types.KeyboardButton('vepurovk.xyz')
    keyboard.add(ovk, vovk)
    bot.send_message(chat_id, 'Выберите предложенный или введите совместимый с OpenVK API домен:', reply_markup=keyboard)
    bot.register_next_step_handler(message, get_domain)
def get_domain(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    ovk = telebot.types.KeyboardButton('ovk.to')
    vovk = telebot.types.KeyboardButton('vepurovk.xyz')
    keyboard.add(ovk, vovk)
    chat_id = message.chat.id
    domain = message.text
    registered_users[chat_id] = {'domain': domain}
    bot.send_message(chat_id, 'Введите электронную почту:', reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_email)
def get_email(message):
    chat_id = message.chat.id
    email = message.text
    registered_users[chat_id]['email'] = email
    bot.send_message(chat_id, 'Введите пароль:')
    bot.register_next_step_handler(message, get_password)
def get_password(message):
    chat_id = message.chat.id
    password = message.text
    registered_users[chat_id]['password'] = password
    user_data = registered_users[chat_id]
    global tokenurl
    tokenurl = f'https://{user_data["domain"]}/token?username={user_data["email"]}&password={user_data["password"]}&grant_type=password'
    try:
        response = requests.get(url=tokenurl).json()
        if 'access_token' in response:
            ovktoken = response['access_token']
            accountbruh = requests.get(url=f'https://{user_data["domain"]}/method/Account.getProfileInfo?access_token={ovktoken}').json()
            account = accountbruh['response']
            global name
            global lname
            global aid
            global home
            global status
            global bdate
            name = account['first_name']
            lname = account['last_name']
            aid = account['id']
            home = account['home_town']
            status = account['status']
            bdate = account['bdate']
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            menu = telebot.types.KeyboardButton('Главная')
            keyboard.add(menu)
            bot.send_message(chat_id, f'Вы удачно вошли!\nПриветствуем, <b>{name}</b>', parse_mode='HTML', reply_markup=keyboard)
        else:
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            login = telebot.types.KeyboardButton('Войти')
            keyboard.add(login)
            tokenurl = 0
            bot.send_message(chat_id, 'Неправильный логин или пароль!\nПопробуйте снова', reply_markup=keyboard)
    except requests.exceptions.ConnectionError:
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        login = telebot.types.KeyboardButton('Войти')
        keyboard.add(login)
        bot.send_message(chat_id, 'Ошибка при подключении!\nВведённый домен не совместим или не доступен на данный момент.', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == 'Главная')
def menu(message):
    if tokenurl == 0:
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        login = telebot.types.KeyboardButton('Войти')
        keyboard.add(login)
        bot.send_message(message.chat.id, 'Вы ещё не вошли!', reply_markup=keyboard)
    else:
        chat_id = message.chat.id
        global name
        global lname
        global status
        bot.send_message(chat_id, f'<u>Главная</u>\n\n<b>{name} {lname}</b>\n<i>{status}</i>\n\nВыберите действие:', parse_mode='HTML', reply_markup=telebot.types.ReplyKeyboardRemove())
bot.polling()