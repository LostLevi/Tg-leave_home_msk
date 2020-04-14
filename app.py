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
        self.inn = None
        self.org_name = None


@bot.message_handler(commands=['start'])
def start(message):
    send_mess = 'На работу - /work'
    bot.send_message(message.chat.id, send_mess, parse_mode = 'html')
    #bot.register_next_step_handler(sent, Hello)

@bot.message_handler(commands=['work'])
def start(message):
    send_mess = f'Тип паспорта(<i>цифра</i>):\n<b>1</b> - паспорт РФ\n<b>2</b> - иностранный паспорт\n<b>3</b> - другое'
    send = bot.send_message(message.chat.id, send_mess, parse_mode = 'html')
    bot.register_next_step_handler(send, Step0)

def Step0(message):
    chat_id = message.chat.id
    name = message.from_user.first_name
    pass_type = message.text
    data = Go_work(name, pass_type)
    work_dict[chat_id] = data
    send_mess = f"Серия пасспорта (если нет, то отправьте - <b>*</b>)"
    send = bot.send_message(message.chat.id, send_mess, parse_mode = 'html')
    bot.register_next_step_handler(send, Step2)

def Step1(message):
    chat_id = message.chat.id
    pass_ser = message.text
    data = work_dict[chat_id]
    data.pass_ser = pass_ser
    send_mess = f"Номер пасспорта (если нет, то отправьте - <b>*</b>)"
    send = bot.send_message(message.chat.id, send_mess, parse_mode = 'html')
    bot.register_next_step_handler(send, Step2)

def Step2(message):
    chat_id = message.chat.id
    pass_num = message.text
    data = work_dict[chat_id]
    data.pass_num = pass_num
    send_mess = f"Номер машины в формате <b>X999XX777</b>, если используется (если нет, то отправьте - <b>*</b>)"
    send = bot.send_message(message.chat.id, send_mess, parse_mode = 'html')
    bot.register_next_step_handler(send, Step3)

def Step3(message):
    chat_id = message.chat.id
    car_num = message.text
    data = work_dict[chat_id]
    data.car_num = car_num
    send_mess = f"Номер карты "Тройка", при наличии (если нет, то отправьте - <b>*</b>)"
    send = bot.send_message(message.chat.id, send_mess, parse_mode = 'html')
    bot.register_next_step_handler(send, Step4)

def Step4(message):
    chat_id = message.chat.id
    troyka_num = message.text
    data = work_dict[chat_id]
    data.troyka_num = troyka_num
    send_mess = f"Номер карты "Стрелка", при наличиии (если нет, то отправьте - <b>*</b>"
    send = bot.send_message(message.chat.id, send_mess, parse_mode = 'html')
    bot.register_next_step_handler(send, Step5)


def Step5(message):
    chat_id = message.chat.id
    strelka_num = message.text
    data = work_dict[chat_id]
    data.strelka_num = strelka_num
    send_mess = f"Вы ввели общие данные, на данный момент необходимо выбрать куда вы направляетесь"
    send = bot.send_message(message.chat.id, send_mess, parse_mode = 'html')
    bot.register_next_step_handler(send, Step_work_last)

def Step_work_last(message):
    chat_id = message.chat.id
    data = work_dict[chat_id]
    bot.send_message(chat_id, f'Код снизу сформирован из ваших данных, его необходимо копировать и отправить как смс на номер <b>7377</b>:')
    bot.send_message(chat_id, f"Пропуск*1*{str(data.pass_type)}*{str(data.pass_ser)}*")

bot.polling(none_stop=True)
