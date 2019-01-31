from telegram.ext import Updater, CommandHandler
import requests
import re
import urllib.request as ur
from bs4 import BeautifulSoup

updater = Updater(token='')
dispatcher = updater.dispatcher
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please send following commands: \n /breakfast - to get breakfast \n /lunch - to get lunch \n /dinner - to get dinner.")

url = "http://www.kaist.edu/_prog/fodlst/?site_dvs_cd=en&menu_dvs_cd=050303"
html = ur.urlopen(url).read()
soup = BeautifulSoup(html, features = "lxml")

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

#extracting breakfast menu
menuraw = soup.find_all(["td"])
breakfast = str(menuraw[0])
#removing unnecessary html tags, getting a cleaner return
for r in (("<br/>","")),(("<td>","")),(("</td>","")),(("&amp;"," & ")):
    breakfast = breakfast.replace(*r)

lunch = str(menuraw[1])
#removing unnecessary html tags, getting a cleaner return
for r in (("<br/>","")),(("<td>","")),(("</td>","")),(("&amp;"," & ")):
    lunch = lunch.replace(*r)


dinner = str(menuraw[2])
for r in (("<br/>","")),(("<td>","")),(("</td>","")),(("&amp;"," & ")),(('<td class="t_end">','')):
    dinner = dinner.replace(*r)

def send_breakfast(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Today's for breakfast:")
    bot.send_message(chat_id=update.message.chat_id, text=breakfast)

def send_lunch(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Today's lunch options are:")
    bot.send_message(chat_id=update.message.chat_id, text=lunch)

def send_dinner(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Today's dinner choices are:")
    bot.send_message(chat_id=update.message.chat_id, text=dinner)


start_handler = CommandHandler('start', start)
bf_handler = CommandHandler('breakfast', send_breakfast)
ln_handler = CommandHandler('lunch', send_lunch)
dn_handler = CommandHandler('dinner', send_dinner)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(bf_handler)
dispatcher.add_handler(ln_handler)
dispatcher.add_handler(dn_handler)
updater.start_polling()
