import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import re
import urllib.request as ur
from bs4 import BeautifulSoup

updater = Updater(token='741003970:AAHRxKNpNVtyeH5SCA7o0PJNu3bmlbeEam8')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


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

def start(bot, update):
    update.effective_message.reply_text("Hello! I'm a bot, please send following commands: \n /breakfast - to get breakfast \n /lunch - to get lunch \n /dinner - to get dinner.")	

def echo(bot, update):
    update.effective_message.reply_text(update.effective_message.text)
	
def send_breakfast(bot, update):
    update.effective_message.reply_text("Today's for breakfast:")
    update.effective_message.reply_text(breakfast)

def send_lunch(bot, update):
    update.effective_message.reply_text("Today's lunch options are:")
    update.effective_message.reply_text(lunch)

def send_dinner(bot, update):
    update.effective_message.reply_text("Today's dinner choices are:")
    update.effective_message.reply_text(dinner)



if __name__ == "__main__":
    # Set these variable to the appropriate values
    TOKEN = "741003970:AAHRxKNpNVtyeH5SCA7o0PJNu3bmlbeEam8"
    NAME = "secure-spire-56488"

    # Port is given by Heroku
    PORT = os.environ.get('PORT')

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Set up the Updater
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    # Add handlers
    dp.add_handler(CommandHandler('start', start))
	dp.add_handler(CommandHandler('breakfast', send_breakfast))
	dp.add_handler(CommandHandler('lunch', send_lunch))
	dp.add_handler(CommandHandler('dinner', send_dinner))
    dp.add_handler(MessageHandler(Filters.text, echo))

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    updater.idle()
