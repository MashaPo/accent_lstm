import config
import telebot
import text_accentAPI

print(text_accentAPI.for_bot('проверка связи'))

bot = telebot.TeleBot(config.TOKEN)
#polling doesn't work if any webhook is running
bot.remove_webhook()

@bot.message_handler(commands = ['start', 'help'])
def send_message(message):
    bot.send_message(message.chat.id, "Hi! Feed this bot with russian text and it will put stress there (At least it'll try to do it)")

#@bot.message_handler(content_types = "text")
@bot.message_handler(func=lambda m: True)  # этот обработчик реагирует на любое сообщение
def put_stress(message):
    try:
        answer = text_accentAPI.for_bot(message.text)
    except:
        answer = "я устал акцентуировать."
    bot.send_message(message.chat.id, answer)
    print(message.text)
    print(answer)


if __name__ == '__main__':
    bot.polling(none_stop = True)

