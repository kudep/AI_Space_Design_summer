
import telebot, subprocess, os

API_TOKEN = '7510919657:AAGNJZRu9tDWIWV041UrpwWrOHbtUY1Stno'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
TEST_TEST_TEST_TEST_Nuger\
""")
@bot.message_handler(commands=['gen'])
def get_room_description(message):
    bot.reply_to(message, "Please give me a room description:")
    bot.register_next_step_handler(message, get_no_of_objects)
    text_description = message.text

def get_no_of_objects(message):
    bot.reply_to(message, "Please give me a number of objects in room:")
    bot.register_next_step_handler(message, get_room_dimensions)
    no_of_objects = message.text

def get_room_dimensions(message):
    bot.reply_to(message, "Please give me a room size(legth, width, height) in format like '8, 8, 2.5':")
    bot.register_next_step_handler(message, generate_script)
    room_dimensions_str = message.text.split(', ')
    room_dimensions = [float(num) for num in room_dimensions_str]

def generate_script(message):
    bot.send_message(message.chat.id, "Generating...")
    try:
        os.system("chmod +x run.sh")
        subprocess.call("./run.sh")
        bot.send_message(message.chat.id, "Script started!")
    except Exception as e:
        bot.send_message(message.chat.id, "Error: " + str(e))  

bot.infinity_polling()