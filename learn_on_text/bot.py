import config
import telebot
import text_accentAPI
HANDLER = open('log.txt', 'w', encoding = 'utf-8')

#print(text_accentAPI.for_bot('проверка связи'))

def log(text):
    HANDLER.write(text+'\n')

bot = telebot.TeleBot(config.TOKEN)
@bot.message_handler(commands = ['start', 'help'])
def send_message(message):
    bot.send_message(message.chat.id, "Hi! Feed this bot with russian text and it will put stress there (At least try to do it)")

#@bot.message_handler(content_types = "text")
@bot.message_handler(func=lambda m: True)  # этот обработчик реагирует на любое сообщение
def put_stress(message):
    try:
        bot.send_message(message.chat.id, text_accentAPI.for_bot(message.text))
    except:
        bot.send_message(message.chat.id, "tensorflow не хочет обрабатывать, вот тебе длина сообщения: " + str(len(message.text)))

    print(message.text)
    log(message.text)


if __name__ == '__main__':
    bot.polling(none_stop = True)

