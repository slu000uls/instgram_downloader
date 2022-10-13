import logging
import http.client
import json
import re
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
bot = telegram.Bot("your bot tokens")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
def start(update, context):
    update.message.reply_text('Welcome to instagram Downloader!')

def help(update, context):
    update.message.reply_text('Give a post link and then bot sent to you a video')

def echo(update, context):
    regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'instagram' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(regex, update.message.text) is not None:
        connection = http.client.HTTPSConnection("apicade.ir")
        connection.request("GET", "/?url="+update.message.text)
        response = connection.getresponse()
        response = response.read().decode()
        response = json.loads(response)
        media = response["media"]
        connection.close()
        
        bot.sendVideo(update.message.chat.id, media)
    else:
        update.message.reply_text("link is not true")



def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater("your bot token", use_context=True)
    dp = updater.dispatcher
    

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))


    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()