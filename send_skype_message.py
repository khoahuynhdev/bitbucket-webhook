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

sk = Skype()

def send_message_bitbucket(msg):
  if is_token_expired():
    login_with_soap()
  channel = sk.chats.chat(channels['bitbucket'])
  channel.sendMsg(msg)


def is_authenticated():
  return sk.conn.connected

def login_with_soap():
  try:
    sk.conn.soapLogin(email, password)
  except Exception as e:
    print("Oops!", e.__class__, "occurred.")
    print("Next entry.")
    print()

def is_token_expired():
  try:
    if is_authenticated():
      return datetime.datetime.now() > sk.conn.tokenExpiry['skype']
    else:
      return True
  except Exception as e:
    print("Oops!", e.__class__, "occurred.")
    return True



# channel = sk.chats.chat('19:da65748f22ed4d0184f8404aafa79a3a@thread.skype')
# channel.sendMsg('automated detach message at: ' +
#                 datetime.datetime.now().strftime('%c') + sys.argv[1])
