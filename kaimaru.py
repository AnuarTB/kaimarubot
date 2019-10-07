# A very simple Flask Hello World app for you to get started with...
from flask import Flask, request
import telepot
import urllib3
import urllib as ur
import datetime
from bs4 import BeautifulSoup

proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

secret = "SECRET"
bot = telepot.Bot('SECRET API HERE')
bot.setWebhook("https://kaimaru.pythonanywhere.com/{}".format(secret), max_connections=1)


app = Flask(__name__)

surl = "http://www.kaist.edu/_prog/fodlst/?site_dvs_cd=en&menu_dvs_cd=050303"
html = ur.request.urlopen(surl).read()
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
#removing unnecessary html tags, getting a cleaner return
for r in (("<br/>","")),(("<td class=\"t_end\">","")),(("<td>","")),(("</td>","")),(("&amp;"," & ")):
    dinner = dinner.replace(*r)


@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        text = update["message"]["text"]
        chat_id = update["message"]["chat"]["id"]
        if text == "/start":
            bot.sendMessage(chat_id, "Hello! I'm a bot, please send following commands: \n /breakfast - to get breakfast \n /lunch - to get lunch \n /dinner - to get dinner.")
        elif datetime.date.today().strftime("%A") == "Saturday":
            bot.sendMessage(chat_id, "kaimaru is closed today.")
        elif text == "/breakfast":
            bot.sendMessage(chat_id, breakfast)
        elif text == "/lunch":
            bot.sendMessage(chat_id, lunch)
        elif text == "/dinner":
            bot.sendMessage(chat_id, dinner)
        else:
            bot.sendMessage(chat_id, "The command is not recognized. Be sure to send the right one!")
    return "OK"

