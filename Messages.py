import DataRetriever
import requests
import Token

dr = DataRetriever.DataRetriever()
token = Token.getToken()


class Messages():

    def help(self):
        return  ("This bot will update you on the Covid-19🦠 outbreak.\n\nAll you need to do is send"
							   " /country <country> (e.g. /country Italy) and it will send you the latest data about that country. \n\n"
							   "If you want to see the list of countries available, type /list.\n\n"
							   "If you prefer, you can also see the situation update worldwide by typing /world.\n\n"
							   "You can also subscribe to this bot and get updates everyday by sending /subscribe <country>")

    def countryData(self, message):
        if len(message) < 9:
            return "You didn't use the command properly.\n\n" \
                   "/country <country>\ne.g. : /country Italy"
        message = message[9:].lower()
        if not(any(message in i for i in dr.getListOfCountries())):
            if (dr.didYouMean(message)):
                return ("I couldn't find that country.\nMaybe you meant:\n\n{} ".format(
                    dr.didYouMean(message)))
            else:
                return ("I couldn't find that country.")
        return dr.getCountryDataText(dr.convertCountryToId(message))

    def sendMsgToDeveloper(self, update, developer_id = 264780265):
        requests.post('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(
            token, developer_id, '{} ({}): {}'.format(update.message.chat.username,
                                                   update.message.chat.id,
                                                   update.message.text[9:])
        ))
        return "Message sent!"

    def plainText(self, update):
        return "Command not found.\n/help"


