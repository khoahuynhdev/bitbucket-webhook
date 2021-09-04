from skpy import Skype
import datetime
import sys
from os import environ
from dotenv import load_dotenv

load_dotenv()
# prepare
email = environ.get("SKYPE_BOT_EMAIL", "")
password = environ.get("SKYPE_BOT_PASSWORD", "")
channels = {'bitbucket': '19:a95a15304480452cb0ffd8bf8a2668a5@thread.skype',
           'admin': '19:26b7238d7a35454cbbe21263842f5155@thread.skype'
           }

def send_message_bitbucket(msg):
  sk = Skype(email, password)
  channel = sk.chats.chat(channels['bitbucket'])
  channel.sendMsg(msg)


# channel = sk.chats.chat('19:da65748f22ed4d0184f8404aafa79a3a@thread.skype')
# channel.sendMsg('automated detach message at: ' +
#                 datetime.datetime.now().strftime('%c') + sys.argv[1])
