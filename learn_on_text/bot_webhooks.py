import flask
import config
import telebot #pip install pyTelegramBotAPI
import text_accentAPI

WEBHOOK_URL_BASE = "https://{}:{}".format(config.WEBHOOK_HOST, config.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(config.TOKEN)


bot = telebot.TeleBot(config.TOKEN, threaded=False)
#удаление предыдущих вебхуков
bot.remove_webhook()
#создаем приложение фласка
app = flask.Flask(__name__)

bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

print(text_accentAPI.for_bot('проверка связи'))


@bot.message_handler(commands = ['start', 'help'])
def send_message(message):
    bot.send_message(message.chat.id, "Hi! Feed this bot with russian text and it will put stress there (At least it'll try to do it)")

#@bot.message_handler(content_types = "text")
@bot.message_handler(func=lambda m: True)  # этот обработчик реагирует на любое сообщение
def put_stress(message):
    try:
        answer = text_accentAPI.for_bot(message.text)
    except:
        answer = "я устал акцентуировать"
    bot.send_message(message.chat.id, answer)
    print(message.text)
    print(answer)

# пустая главная страничка для проверки
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

#запустится, когда постучится телеграм
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)



