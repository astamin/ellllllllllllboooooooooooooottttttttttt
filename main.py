import telebot
from telebot import types
import os
import requests , time ,threading , random , string , fake_useragent
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)
userrun = True
creds = {}
def sender(target):
    characters = string.ascii_letters + string.digits
    random_word = ''.join(random.choice(characters) for _ in range(8))
    emails = [f'{random_word}@yahoo.com' , f'{random_word}@gmail.com' , f'{random_word}@outlook.com' , f'{random_word}@aol.com' , f'{random_word}@icloud.com' , f'{random_word}@gmx.com' , f'{random_word}@mail.ru']
    email = random.choice(emails)
    messages = [
        f'Hello! Today , I wanna tell telegram support that i have a important reason to send this report this channel @{target} is violated the terms and you need to take action on it because if you let it active it may cause a lot of problems to a lot of things this is user @{target} and this is link t.me/{target}' ,
        f"Reporting @{target} for posting offensive and violated content on your platform. Thank you." ,
        f"Reportando a @{target} por publicar contenido ofensivo y violatorio en su plataforma. Gracias.",
        f"Meldung von @{target} wegen Veröffentlichung von beleidigendem und verletzendem Inhalt auf Ihrer Plattform. Danke.",
        f"Segnalazione di @{target} per la pubblicazione di contenuti offensivi e violatori sulla tua piattaforma. Grazie." ,
        f"Сообщение о нарушении @{target} за размещение оскорбительного и нарушающего контента на вашей платформе. Спасибо." ,
        f"الإبلاغ عن @{target} بنشر محتوى مسيء ومخالف على منصتكم. شكرًا لكم."
                ]
    url = "https://telegram.org/support"
    data ={
        "message": random.choice(messages) ,
        "email": email ,
        "phone": '42777' ,
        "setln": ""
        }
    headers = {
        'user-agent' : fake_useragent.UserAgent().random
    }

    try :
        response = requests.post(url=url , headers=headers , data=data  , timeout=5)
        if 'Thanks for' in response.text :
            return True
        else :
            return False
    except : return False

@bot.message_handler(commands=['start'])
def start(message):
    global creds
    userid = message.from_user.id
    if userid not in creds :
        creds[userid] = {}
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True )
    markup.add('Run')
    markup.add('Stop')
    markup.add('Set user')
    bot.send_message(message.from_user.id , f'Welcome @{message.from_user.username} in **TG-REPORTER**\nDev : `ASTA 404`\nVersion : 2.2.1' , reply_markup=markup , parse_mode='Markdown')

@bot.message_handler(content_types=['text'])
def getmessage(message):
    userid = message.from_user.id
    if message.text == 'Set user':
        bot.send_message(userid , 'root@asta : ~$ Send the target now')
        bot.register_next_step_handler(message , getuser)
    elif message.text == 'About you':
        photos = bot.get_user_profile_photos(userid).photos
        if photos:
            photo = photos[0][-1]
            user = message.from_user
            name = user.first_name + " " + user.last_name if user.last_name else user.first_name
            user_id = user.id
            print(user)
            bot.send_photo(chat_id=message.chat.id,
                       photo=photo.file_id,
                       caption=f"Username: @{user.username}\nName: {name}\nuser id : `{user_id}`" , parse_mode='Markdown')

    elif message.text == 'Run':
        run(message=message)
    elif message.text == 'Stop':
        stop(message)
    else :
        bot.reply_to(message=message , text=message.text)
def run(message):
    userid = message.from_user.id
    if 'target' not in creds[userid] :
        bot.send_message(userid , 'root@asta : ~$ Setup target firstly Please !')
        return
    target = creds[userid]['target']
    me1 = bot.send_message(userid , "root@asta : ~$ Please wait while checking information !")

    global userrun
    userrun = True
    good = 0
    error = 0
    messageid= me1.message_id
    while userrun :
        send = sender(target)
        if send :
            good += 1
            bot.edit_message_text(f"Good Report : {good} \nError Report : {error} \nTarget : @{target}" ,chat_id=userid , message_id=messageid)
        else :
            error +=1
            bot.edit_message_text(f"Good Report : {good} \nError Report : {error} \nTarget : @{target}" ,chat_id=userid , message_id=messageid)
        time.sleep(10)


def stop(message):
    global userrun
    userrun = False
    bot.reply_to(message, "Reporter is stopped now")

def getuser(message):
    userid = message.from_user.id
    target =message.text
    if userid not in creds:
        creds[userid] = {}
    creds[userid]['target'] = target
    bot.send_message(userid , 'root@asta : ~$ Target is setupped to @{}'.format(target) )


bot.polling()
