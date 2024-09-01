
import telebot, subprocess, os, json

API_TOKEN = '7510919657:AAGNJZRu9tDWIWV041UrpwWrOHbtUY1Stno'

bot = telebot.TeleBot(API_TOKEN)

json_data = dict.fromkeys(['description', 'no_of_objects', 'room_dimensions'])

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
TEST_TEST_TEST_TEST\
""")
@bot.message_handler(commands=['gen'])
def get_room_description(message):
    bot.reply_to(message, "Please give me a room description:")
    bot.register_next_step_handler(message, save_room_description)

def save_room_description(message):
    text_description = message.text
    json_data['description'] = text_description
    get_no_of_objects(message)

def get_no_of_objects(message):
    bot.reply_to(message, "Please give me a number of objects in room:")
    bot.register_next_step_handler(message, save_no_of_objects)
def save_no_of_objects(message):
    no_of_objects = int(message.text)
    json_data['no_of_objects'] = no_of_objects
    get_room_dimensions(message)
    

def get_room_dimensions(message):
    bot.reply_to(message, "Please give me a room size(legth, width, height) in format like '8, 8, 2.5':")
    bot.register_next_step_handler(message, save_room_dimensions)
def save_room_dimensions(message):
    room_dimensions_str = message.text.split(',')
    room_dimensions =[float(num) for num in room_dimensions_str]
    json_data['room_dimensions'] = room_dimensions
    bot.send_message(message.chat.id, json_data)
    save_json(message)
def save_json(message):
    with open('room.json', 'w') as f:
        json.dump(json_data, f)
    generate_script(message)

def generate_script(message):
    
    bot.send_message(message.chat.id, "Generation starting...")
    try:
        os.system("chmod +x run.sh")
        subprocess.call("./run.sh")
        bot.send_message(message.chat.id, "Script started! Please wait until it generates")
    except Exception as e:
        bot.send_message(message.chat.id, "Error: " + str(e))  

bot.infinity_polling()