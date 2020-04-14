import telebot
from telebot import types
from telebot import apihelper
import config


apihelper.proxy = {
  'https': config.proxy
}

work_dict = {}

bot = telebot.TeleBot(config.token)

class Go_work:
    def __init__(self, name, pass_type):
        self.name = name
        self.pass_type = pass_type
        self.pass_ser = None
        self.pass_num = None
        self.car_num = None
        self.troyka_num = None
        self.strelka_num = None
        self.step = None
        self.inn = None
        self.org_name = None
        self.bth_date = None
        self.med_org_name = None
        self.exit_reason = None
        self.exit_addr = None

@bot.message_handler(commands=['start'])
def start(message):
    send_mess = f"Данный бот создан, что бы помочь сформировать код необходимый для получения пропусков в г. Москва\n\nВозможно код подойдет, также для других областей\n\nЧто бы сформировать код введите команду /run и последовательно заполните все данные\n\nДля дополнительной информации введите команду /about\n\nДля получения информации по кодам, введите /info"
    bot.send_message(message.chat.id, send_mess, parse_mode = 'html')
    #bot.register_next_step_handler(sent, Hello)

@bot.message_handler(commands=['about'])
def start(message):
    send_mess = f'Бот не использует базу данных и генерирует код в процессе введения данных\nСпасибо за разработку инструмента генерации кодов в Excel пикабушнику Fu1crum\nСсылка на пост - https://pikabu.ru/story/shablon_sms_dlya_propuska_po_moskve_7368626'
    bot.send_message(message.chat.id, send_mess, parse_mode = 'html')

@bot.message_handler(commands=['info'])
def start(message):
    send_mess = f'Вся информация по кодам и пропускам указанна по ссылке - https://www.mos.ru/news/item/72520073/'
    bot.send_message(message.chat.id, send_mess, parse_mode = 'html')



@bot.message_handler(commands=['run'])
def start(message):
    send_mess = f'Тип паспорта(<i>цифра</i>):\n<b>1</b> - паспорт РФ\n<b>2</b> - иностранный паспорт\n<b>3</b> - другое'
    send = bot.send_message(message.chat.id, send_mess, parse_mode = 'html')
    bot.register_next_step_handler(send, Step0)

def Step0(message):
    chat_id = message.chat.id
    name = message.from_user.first_name
    pass_type = str(message.text) + '*'
    if pass_type == '**':
        pass_type = '*'
    data = Go_work(name, pass_type)
    work_dict[chat_id] = data
    send_mess = f"Серия паспорта (если нет, то отправьте - <b>*</b>)"
    send = bot.send_message(message.chat.id, send_mess, parse_mode = 'html')
    bot.register_next_step_handler(send, Step1)

def Step1(message):
    chat_id = message.chat.id
    pass_ser = str(message.text) + '*'
    if pass_ser == '**':
        pass_ser = '*'
    data = work_dict[chat_id]
    data.pass_ser = pass_ser
    send_mess = f"Номер паспорта (если нет, то отправьте - <b>*</b>)"
    send = bot.send_message(message.chat.id, send_mess, parse_mode = 'html')
    bot.register_next_step_handler(send, Step2)

def Step2(message):
    chat_id = message.chat.id
    pass_num = str(message.text) + '*'
    if pass_num == '**':
        pass_num = '*'
    data = work_dict[chat_id]
    data.pass_num = pass_num
    send_mess = f"Номер машины в формате <b>X999XX777</b>, если используется (если нет, то отправьте - <b>*</b>)"
    send = bot.send_message(message.chat.id, send_mess, parse_mode = 'html')
    bot.register_next_step_handler(send, Step3)

def Step3(message):
    chat_id = message.chat.id
    car_num = str(message.text) + '*'
    if car_num == '**':
        car_num = '*'
    data = work_dict[chat_id]
    data.car_num = car_num
    send_mess = f"Номер карты Тройка, при наличии (если нет, то отправьте - <b>*</b>)"
    send = bot.send_message(message.chat.id, send_mess, parse_mode = 'html')
    bot.register_next_step_handler(send, Step4)

def Step4(message):
    chat_id = message.chat.id
    troyka_num = str(message.text) + '*'
    if troyka_num == '**':
        troyka_num = '*'
    data = work_dict[chat_id]
    data.troyka_num = troyka_num
    send_mess = f"Номер карты Стрелка, при наличиии (если нет, то отправьте - <b>*</b>"
    send = bot.send_message(message.chat.id, send_mess, parse_mode = 'html')
    bot.register_next_step_handler(send, Step5)

def Step5(message):
    chat_id = message.chat.id
    strelka_num = str(message.text) + '*'
    if strelka_num == '**':
        strelka_num = '*'
    data = work_dict[chat_id]
    data.strelka_num = strelka_num
    send_mess = f"Вы ввели общие данные, на данный момент необходимо выбрать куда вы направляетесь и отправить соответствующую цифру:\n<b>1</b>. На работу\n<b>2</b>. Разовое посещение мед. организации\n<b>3</b>. Разовая поездка в иных целях (не более 2х раз в неделю)"
    send = bot.send_message(message.chat.id, send_mess, parse_mode = 'html')
    bot.register_next_step_handler(send, Step_way)

def Step_way(message):
    chat_id = message.chat.id
    step = message.text
    data = work_dict[chat_id]
    data.step = str(step) + '*'
    if step == '1':
        send_mess = f"Для отправки на работу введите ИНН организации, не обязательно (если нет, то отправьте - <b>*</b>)"
        send = bot.send_message(message.chat.id, send_mess, parse_mode = 'html')
        bot.register_next_step_handler(send, Step_Work)
    if step == '2':
        send_mess = f"Для отправки в мед. организацию введите дату рождения в формате <b>31.12.2020</b>"
        send = bot.send_message(message.chat.id, send_mess, parse_mode = 'html')
        bot.register_next_step_handler(send, Step_Med)
    if step == '3':
        send_mess = f"Для выхода по иным причинам, укажите цель выхода (до 20 символов, без кавычек)"
        send = bot.send_message(message.chat.id, send_mess, parse_mode = 'html')
        bot.register_next_step_handler(send, Step_Idk)

def Step_Work(message):
    chat_id = message.chat.id
    inn = str(message.text) + '*'
    if inn == '**':
        inn = '*'
    data = work_dict[chat_id]
    data.inn = inn
    send_mess = f"Введите краткое название вашей организации (до 20 символов, без кавычек, или иных спец. символов)"
    send = bot.send_message(message.chat.id, send_mess, parse_mode = 'html')
    bot.register_next_step_handler(send, Step_work_last)

def Step_work_last(message):
    chat_id = message.chat.id
    org_name = str(message.text)
    data = work_dict[chat_id]
    data.org_name = org_name
    send_mess = f"Код снизу сформирован из ваших данных, его необходимо копировать и отправить как смс на номер\n<b>7377</b> для жителей Москвы"
    bot.send_message(chat_id, send_mess, parse_mode = 'html')
    bot.send_message(chat_id, f"Пропуск*{str(data.step)}{str(data.pass_type)}{str(data.pass_ser)}{str(data.pass_num)}{str(data.car_num)}{str(data.troyka_num)}{str(data.strelka_num)}{str(data.inn)}{str(data.org_name)}", parse_mode = 'html')

def Step_Med(message):
    chat_id = message.chat.id
    bth_date = str(message.text) + '*'
    data = work_dict[chat_id]
    data.bth_date = bth_date
    send_mess = f"Введите краткое название мед. организации (до 20 символов, без кавычек, или иных спец. символов)"
    send = bot.send_message(message.chat.id, send_mess, parse_mode = 'html')
    bot.register_next_step_handler(send, Step_med_last)

def Step_med_last(message):
    chat_id = message.chat.id
    med_org_name = str(message.text)
    data = work_dict[chat_id]
    data.med_org_name = med_org_name
    send_mess = f"Код снизу сформирован из ваших данных, его необходимо копировать и отправить как смс на номер\n<b>7377</b> для жителей Москвы"
    bot.send_message(chat_id, send_mess, parse_mode = 'html')
    bot.send_message(chat_id, f"Пропуск*{str(data.step)}{str(data.pass_type)}{str(data.pass_ser)}{str(data.pass_num)}{str(data.bth_date)}{str(data.car_num)}{str(data.troyka_num)}{str(data.strelka_num)}{str(data.med_org_name)}", parse_mode = 'html')

def Step_Idk(message):
    chat_id = message.chat.id
    exit_reason = str(message.text) + '*'
    data = work_dict[chat_id]
    data.exit_reason = exit_reason
    send_mess = f"Введите краткое адрес места назначения (желательно до 20 символов, без кавычек, или иных спец. символов)"
    send = bot.send_message(message.chat.id, send_mess, parse_mode = 'html')
    bot.register_next_step_handler(send, Step_idk_last)

def Step_idk_last(message):
    chat_id = message.chat.id
    exit_addr = str(message.text)
    data = work_dict[chat_id]
    data.exit_addr = exit_addr
    send_mess = f"Код снизу сформирован из ваших данных, его необходимо копировать и отправить как смс на номер\n<b>7377</b> для жителей Москвы"
    bot.send_message(chat_id, send_mess, parse_mode = 'html')
    bot.send_message(chat_id, f"Пропуск*{str(data.step)}{str(data.pass_type)}{str(data.pass_ser)}{str(data.pass_num)}{str(data.car_num)}{str(data.troyka_num)}{str(data.strelka_num)}{str(data.exit_reason)}{str(data.exit_addr)}", parse_mode = 'html')

bot.polling(none_stop=True)
