import json
import os.path
from os import path
import datetime
from datetime import timedelta
import DataRetriever
import requests
import Token


dr = DataRetriever.DataRetriever()
token = Token.getToken()


def loadDict(id):
    json_file = open("users/{}.json".format(id))
    dictionary = json.load(json_file)
    return (dictionary)


def saveDict(data,id):
    with open("users/{}.json".format(id), "w") as f:
        json.dump(data, f)

def userExists(id):
    return(path.exists('users/{}.json'.format(id)))

def createUserFile(update):
    if not userExists(update.message.chat.id):
        saveDict({'id': update.message.chat.id,
                  'username': update.message.chat.username,
                  'first_name': update.message.chat.first_name,
                  'last_name': update.message.chat.last_name,
                  'first_message': ((update.message.date + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')),
                  'subscribed': False,
                  'subscriptions': []
                  }, update.message.chat.id)
        printUserData(update.message.chat.id)

def printUserData(id):
    if not userExists(id):
        return None
    user_data = loadDict(id)
    print("\n\n- - - New user - - -\n")
    [print("{}: {}".format(i,k)) for i, k in user_data.items()]
    saveDict(user_data, id)

def subscribe(update):
    country = (update.message.text[11:]).lower()
    if not userExists(update.message.chat.id):
        createUserFile(update)
    if country == '':
        return("You didn't use the command properly.\n\n" 
                   "/subscribe <country>\ne.g. : /subscribe Italy")
    if any(country in i for i in country):
        return("No data found about {}".format(country))

    user_data = loadDict(update.message.chat.id)
    if country not in user_data['subscriptions']:
        user_data['subscribed'] = True
        user_data['subscriptions'].append(country)
        saveDict(user_data, update.message.chat.id)
        return ("You will now receive daily updates about {}.".format(update.message.text[11:]))
    return ("You're already subscribed to {}!".format(update.message.text[11:]))

def getSubscriptions(update):
    user_data = loadDict(update.message.chat.id)
    subscriptions = user_data['subscriptions']
    if subscriptions and isSubscribed(update.message.chat.id):
        return "You are subscribed to:\n" + "\n".join(subscriptions)
    return "You aren't subscribed to any country."

def getSubscriptionsData(update = None, id = None):
    if update:
        user_data = loadDict(update.message.chat.id)
    else:
        user_data = loadDict(id)
    subscriptions = []
    [subscriptions.append(dr.getCountryDataText(dr.convertCountryToId(i))) for i in user_data['subscriptions']]
    if subscriptions:
        return '\n\n'.join(subscriptions)
    return "You aren't subscribed to any country."

def unsubscribeAll(update):
    user_data = loadDict(update.message.chat.id)
    user_data['subscribed'] = False
    user_data['subscriptions'] = []
    saveDict(user_data, update.message.chat.id)
    return("Unsubscribed from all countries.")

def isSubscribed(id):
    user_data = loadDict(id)
    return user_data['subscribed']

def dailyMsg():
    for i in os.listdir('users'):
        id = id = i.rsplit('.',1)[0]
        if isSubscribed(id):
            data = getSubscriptionsData(id = id)
            requests.post('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(
                token, i, '-- Daily Update --\n\n{}'.format(data)))


