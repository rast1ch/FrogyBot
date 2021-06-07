import telebot
import datetime
import pickle
import atexit

class Player:
    ''' Класс Player имеет поля:
            _id - неизмняемое поле - id игрока
            _name - неизменяемое поле - имя жабки
            last_feed - время последнего кормления
            size - размер жабки'''
    def __init__(self, id : str, name: str ):
        '''
        Конструктор класса принимает 2 аргумента:
            id - строчное значение id пользователя
            name - строчное представление имени жабы'''
        self._id = id
        self._name = name
        self.last_feed =datetime.datetime.now() - datetime.timedelta(minutes=20)
        self.size = 1
    def feed(self):
        '''
        Функция проверяет прошло ли 20 минут с последнего кормления и
        прибавлет 1 к размеру(size)'''
        if datetime.datetime.now() - self.last_feed > datetime.timedelta(minutes=20):
            self.size += 1
            self.last_feed  = datetime.datetime.now()
        else:
            raise PlayerException
    def __str__(self):
        '''Шаблон для вывода экземпляра класса в строчном виде'''
        return f"{self._name}🐸  ==>  {self.size} кг."

class PlayerException(Exception):
    def __init__(self):
        self.message = "Жаба ще не голодна"
        super().__init__(self.message)



try:
    with open('data.pickle', 'rb') as f:
       players =  pickle.load(f)
except FileNotFoundError as e:
    players = []
    print(e)



bot = telebot.TeleBot("1876587727:AAGtGvs8iwNyF9ocTt-svNSffMixkc6xrKM")

@bot.message_handler(commands=['start',])
def send_welcome(message):
	bot.send_message(message.from_user.id, f"""
💖 {message.from_user.first_name}, Привіт!

Щоб створити жабку 🐸 та почати гру пиши /frog

Правила гри прості, годуй жабку🐸 раз в 20 хвилин і вона буде рости, чим більша жаба 🐸 тим вище рейтинг📈""")



@bot.message_handler(commands = ['frog'])
def register_user(message):
    msg = bot.send_message(message.from_user.id, "Тепер потрібно обрати Жабці🐸 ім'я. Введи його наступним повідомленням")
    bot.register_next_step_handler(msg, create_user)

def create_user(message):
    for i in players:
        if str(message.from_user.id) == i._id:
            bot.send_message(message.from_user.id , "Ви вже створили жабку🐸")
            return
    try:
        players.append(Player(str(message.from_user.id), message.text))
        bot.send_message(message.from_user.id, "Жабка🐸 успішно створена ✅, тепер її можна погодувати🪲 за допомогою /feed")
    except Exception:
        bot.send_message(message.from_user.id, "Упс, щось пішло не так ⛔")
 

@bot.message_handler(commands  = ['feed'])
def feed(message):
    for i in players:
        if str(message.from_user.id) == i._id:
            try:
                i.feed()
                bot.send_message(message.from_user.id, f"{i._name}🐸 нагодована🪲")
            except PlayerException:
                time  = (i.last_feed + datetime.timedelta(minutes = 20)) - datetime.datetime.now() 
                bot.send_message(message.from_user.id,
                 f"Жабу можна буде погодувати через {(time.seconds//60)%60} хв. 🕘")
            return
    bot.send_message(message.from_user.id, "Спочатку потрібно створити жабку🐸 за допомогою /frog")



@bot.message_handler(commands = ['rating'])
def rating(message):
    temp = ""
    if players:
        for i in players:
            temp += f"{str(i)}\n"
        bot.reply_to(message, temp)
    else:
        bot.reply_to(message, "Рейтинг поки що пустий")

def serialize():
    with open('data.pickle', 'wb') as f:
        pickle.dump(players, f)

if __name__ == "__main__":
    bot.polling()
    atexit.register(serialize)

