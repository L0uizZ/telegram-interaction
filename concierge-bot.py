"""
-------------------------------------------------
# Telegram - Automated Concierge Bot
-------------------------------------------------
"""
__author__ = "Louis Hinz"
__version__ = "0.0.1"

from telegram.ext import MessageHandler, Filters, Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import Update
import sys, logging, json, requests
from urllib.parse import urlparse
import telegram, os, random

updater = Updater(token=sys.argv[1], use_context=True)
dispatcher = updater.dispatcher
                    
# FUNCTIONAL METHODS
def start(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=telegram.ChatAction.TYPING)
    context.bot.send_message(chat_id=update.effective_chat.id, text="hello friend, please run /help to see our services")
    
def select(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=telegram.ChatAction.TYPING)

    keyboard = [[InlineKeyboardButton("1", callback_data='1'), InlineKeyboardButton("2", callback_data='2'), InlineKeyboardButton("3", callback_data='3'), InlineKeyboardButton("4", callback_data='4'), InlineKeyboardButton("X", callback_data='5')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("please select a service:\n\n1) DoSomething\n2) DoSomething\n3) DoSomething\n4) DoSomething", reply_markup=reply_markup)
    order(update.effective_user.username, context.effective_chat.message)

def about(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=telegram.ChatAction.TYPING)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.")

def callback(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=telegram.ChatAction.TYPING)
    update.callback_query.edit_message_text('[*] done')
    #context.bot.send_message(chat_id=update.effective_chat.id, text="special text", reply_markup = InlineKeyboardMarkup([[ InlineKeyboardButton('???🔒', url = 'https://startpage.com/')]]))
    order(update.effective_user.username , update.callback_query.Filters.text)

def helpme(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=telegram.ChatAction.TYPING)
    context.bot.send_message(chat_id=update.effective_chat.id, text="⚠️                      ¯\_(ツ)_/¯                     ⚠️\n\n/start       run automated-concierge-bot\n/help        show help menu\n/about     show about menu\n/select     show select menu\n/meme    show a meme")
        
def unknown(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=telegram.ChatAction.TYPING)
    if (is_url(update.message.text) == True):
      context.bot.send_message(chat_id=update.effective_chat.id, text="📣 received posting & stored url ✅️")
      file_object = open('requests.txt', 'a')
      file_object.write(userstr+"\n")
      file_object.close()
    else:
      context.bot.send_message(chat_id=update.effective_chat.id, text="Need help?\nHit /halalp Mr.♿")
    
def order(user, message):
    print("> new service request from", user, "selected service:","x",message)
    
def meme(update, context):
    randompic = random.randint(1, 2)
    if(randompic == 1):
      context.bot.send_chat_action(chat_id=update.effective_chat.id, action=telegram.ChatAction.UPLOAD_PHOTO)
      context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('memeoftheday.jpg', 'rb'))
    elif(randompic == 2):
      context.bot.send_chat_action(chat_id=update.effective_chat.id, action=telegram.ChatAction.UPLOAD_PHOTO)
      context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('memeoftheday2.jpg', 'rb'))

def is_url(url):
  try:
    result = urlparse(url)
    file_object = open('requests.txt', 'a')
    file_object.write(url+"\n")
    file_object.close()
    return all([result.scheme, result.netloc])
  except ValueError:
    return False

# MAIN METHOD
def main():
  start_handler = CommandHandler('start', start)
  dispatcher.add_handler(start_handler)

  select_handler = CommandHandler('select', select)
  dispatcher.add_handler(select_handler)

  about_handler = CommandHandler('about', about)
  dispatcher.add_handler(about_handler)

  help_handler = CommandHandler('help', helpme)
  dispatcher.add_handler(help_handler)

  meme_handler = CommandHandler('meme', meme)
  dispatcher.add_handler(meme_handler)

  url_handler = MessageHandler(Filters.text, unknown)
  dispatcher.add_handler(url_handler)

  unknown_handler = MessageHandler(Filters.command, unknown)
  dispatcher.add_handler(unknown_handler)

  callback_handler = CallbackQueryHandler(callback)
  dispatcher.add_handler(callback_handler)

  updater.start_polling()
  updater.idle()

main()