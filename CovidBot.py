import datetime
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, JobQueue
import Token, Commands

#Gets the bot token from the class Token.
token = "PASTE HERE YOUR TELEGRAM BOT'S TOKEN"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)



def error(update, context):
    # Prints any error thrown by the bot.
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():

    #Instanciating the updater and the dispatcher.
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    # Series of handlers that call different functions.
    dp.add_handler(CommandHandler("start", Commands.start))
    dp.add_handler(CommandHandler("help", Commands.help))
    dp.add_handler(CommandHandler("world", Commands.world))
    dp.add_handler(CommandHandler("sendmsg", Commands.sendMsg))
    dp.add_handler(CommandHandler("list", Commands.list))
    dp.add_handler(CommandHandler("subscribe", Commands.subscribe))
    dp.add_handler(CommandHandler("subscriptions", Commands.sendSubscriptions))
    dp.add_handler(CommandHandler("sendsubscriptions", Commands.sendSubscriptionsData))
    dp.add_handler(CommandHandler("unsubscribeall", Commands.unsubscribeAll))
    dp.add_handler(CommandHandler("country", Commands.countryData))

    #Hacky way to send updates everyday at 16:00.
    job = updater.job_queue
    t = datetime.time(16, 00, 00, 000000)
    job.run_daily(Commands.dailyMsg, t, days=(0, 1, 2, 3, 4, 5, 6), context=None, name='dailyMsg')

    # If a user sends plain text they will be sent the /help message.
    dp.add_handler(MessageHandler(Filters.text, Commands.plainText))

    # Error logging
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
