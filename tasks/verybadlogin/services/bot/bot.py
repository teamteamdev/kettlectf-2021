import config
import telebot

bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=["text"])
def help(message):
	
	if message.text == "/help":
		bot.send_message(message.from_user.id, "Hello there o/! What are you looking for?\n Here is my commands:\n /help - Information about commands\n /id - TelegramBot ID\n /notifications  - Turn on Notifications \n /time - What time is it")
	
	elif message.text == "/time":
		bot.send_message(message.from_user.id, "IT'S TIME TO CTF!")
		
	elif message.text == "/id":
		bot.send_message(message.from_user.id, "Here is it: @teamTeam2BOT")
		
	elif message.text == "/notifications":
		bot.send_message(message.from_user.id, "Read first chars of commands")	
		
	elif message.text == "/hint":
		bot.send_message(message.from_user.id, "Here is what you need : NP7382ODI:Hiu1dplskj")
	
	else:
		bot.send_message(message.from_user.id, "Type a command please: /help - Information about commands")
		

if __name__ == '__main__':
	bot.infinity_polling()
