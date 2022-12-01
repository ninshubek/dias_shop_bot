import telebot
from telebot import types

from config import TOKEN
from main import insert_user, is_user_exists, create_inline_markup
from location import insert_location, is_location_exists, update_location


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Зарегистрироваться', request_contact=True)
    item2 = types.KeyboardButton('Отправить геоданные', request_location=True)
    markup.add(item1, item2)

    text = "Привет это Бот Диаса типо интернет магазин\n Для получения данных ЗАРЕГИСТРИРУЙТЕСЬ"
    bot.send_message(message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(content_types=['contact'])
def contact(message: types.Message):
    if message.contact is not None:

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Продукты')
        item2 = types.KeyboardButton('Корзина')
        markup.add(item1, item2)

        if not is_user_exists(message.chat.id):
            insert_user(
                phone_number=message.contact.phone_number,
                first_name=message.contact.first_name,
                last_name=message.contact.last_name,
                chat_id=message.chat.id
            )
            bot.send_message(message.chat.id, 'Вы успешно зарегистровались!', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Вы уже зарегистрованы!', reply_markup=markup)

@bot.message_handler(content_types=['location'])
def location(message: types.Message):
    if message.location is not None:
        if not is_location_exists(message.chat.id):
            insert_location(
                chat_id=message.chat.id,
                latitude=message.location.latitude,
                longitude=message.location.longitude
            )
            bot.send_message(message.chat.id, 'Вы успешно отправили геоданные!')
        else:
            update_location(
                chat_id=message.chat.id,
                latitude=message.location.latitude,
                longitude=message.location.longitude
            )
            bot.send_message(message.chat.id, 'Вы успешно обновили геоданные!')

            

@bot.message_handler(content_types=['text'])
def text(message: types.Message):
    if message.chat.type == 'private':
        if message.text.lower() == 'продукты':
            markup = create_inline_markup(
                    row_width=3,
                    apple='Apple',
                    xiaomi='Xiaomi',
                    samsung='Samsung')
            
            bot.send_message(message.chat.id, 'Выберите: ', reply_markup=markup)

            
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    try:
        if call.message:
            if call.data == 'apple':
                markup = create_inline_markup(
                    row_width=3,
                    iphone14='IPhone 14',
                    iphone13='IPhone 13',
                    iphone12='IPhone 12',
                    iphone11='IPhone 11',
                    iphoneX='IPhone X',
                    ipad='IPad',
                    products='<<< Назад')
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text='Выберите модель:',
                    reply_markup=markup
                )
            elif call.data == 'products':
                """продукты call back """
                markup = create_inline_markup(
                    row_width=3,
                    apple='Apple',
                    xiaomi='Xiaomi',
                    samsung='Samsung')
                
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text='Выберите :',
                    reply_markup=markup
                )
    except: 
        pass
bot.polling(non_stop=True)