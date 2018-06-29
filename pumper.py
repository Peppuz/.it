import telegram, json, time, os
from datetime import datetime
from telegram.ext import Updater, Filters, MessageHandler

config = json.load(open('config.json'))


def handit(b, u):
	print(u.message.from_user)
	file_id = u.message.document.file_id
	fi = bot.get_file(file_id)
	file_name = u.message.document.file_name
	if u.message.from_user.id == config['bot']['telegram']['peppuz']:	
		fi.download('./src/dw/%s' % file_name)
		bot.send_message(u.message.chat_id, "Link http://peppuz.it/dw/%s" % file_name)
	else:
		bot.send_message(u.message.chat_id, "Sorry, you are NOT allowed to use this funcition") 


bot = telegram.Bot(config['bot']['telegram']['token'])
updater = Updater(config['bot']['telegram']['token'])
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.document, handit))

updater.start_polling()



