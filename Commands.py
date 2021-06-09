import Messages, JsonHandler, DataRetriever

Messages = Messages.Messages()
DataRetriever = DataRetriever.DataRetriever()

def start(update, context):
    JsonHandler.createUserFile(update)
    update.message.reply_text(Messages.help())

def help(update, context):
    update.message.reply_text(Messages.help())

def countryData(update, context):
    update.message.reply_text(Messages.countryData(update.message.text))

def sendMsg(update, context):
    update.message.reply_text(Messages.sendMsgToDeveloper(update))

def list(update, context):
    update.message.reply_text(DataRetriever.getListOfCountriesText())

def world(update, context):
    update.message.reply_text(DataRetriever.getWorldDataText())

def subscribe(update, context):
    update.message.reply_text(JsonHandler.subscribe(update))

def sendSubscriptions(update, context):
    update.message.reply_text(JsonHandler.getSubscriptions(update))

def sendSubscriptionsData(update, context):
    update.message.reply_text(JsonHandler.getSubscriptionsData(update))

def unsubscribeAll(update, context):
    update.message.reply_text(JsonHandler.unsubscribeAll(update))

def dailyMsg(_):
    JsonHandler.dailyMsg()

def plainText(update, context):
    update.message.reply_text(Messages.plainText(update))