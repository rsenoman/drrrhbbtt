import requests
import telebot, time
from telebot import types
from gatet import Tele
import os

BOT_TOKEN = "7992415258:AAGJrBd519cd0pLcnedclr6KoYQYpSQhJHg"
bot = telebot.TeleBot(BOT_TOKEN)

subscriber = '7519839885'
allowed_users = ['7519839885']  # Your ID

@bot.message_handler(commands=["start"])
def start(message):
    if str(message.chat.id) not in allowed_users:
        bot.reply_to(message, "🚫 You cannot use this bot. Contact developers to purchase a subscription @Parael1101")
        return
    bot.reply_to(message, "Send the txt file now")

@bot.message_handler(commands=["add_user"])
def add_user(message):
    if str(message.chat.id) == '7519839885':  # Only bot owner can add new users
        try:
            new_user_id = message.text.split()[1]  # Extract new user ID from the command
            allowed_users.append(new_user_id)
            bot.reply_to(message, f"User {new_user_id} has been added successfully.✅")
        except IndexError:
            bot.reply_to(message, "Please provide a valid user ID. Example: /add_user 123456789")
    else:
        bot.reply_to(message, "You do not have permission to add users.🚫")

@bot.message_handler(content_types=["document"])
def main(message):
    if str(message.chat.id) not in allowed_users:
        bot.reply_to(message, "🚫 You cannot use the bot. Contact developers to purchase a bot subscription @Parael1101")
        return
    dd, live = 0, 0
    ko = bot.reply_to(message, "Processing card checking...⌛").message_id
    ee = bot.download_file(bot.get_file(message.document.file_id).file_path)
    
    with open("combo.txt", "wb") as w:
        w.write(ee)
    
    try:
        with open("combo.txt", 'r') as file:
            lino = file.readlines()
            total = len(lino)
            
            for cc in lino:
                current_dir = os.getcwd()
                for filename in os.listdir(current_dir):
                    if filename.endswith(".stop"):
                        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='Stopped ✅\nBot by ➜ @Parael1101')
                        os.remove('stop.stop')
                        return
                
                try:
                    data = requests.get(f'https://bins.antipublic.cc/bins/{cc[:6]}').json()
                except:
                    data = {}
                
                brand = data.get('brand', 'Unknown')
                card_type = data.get('type', 'Unknown')
                country = data.get('country_name', 'Unknown')
                country_flag = data.get('country_flag', 'Unknown')
                bank = data.get('bank', 'Unknown')
                
                start_time = time.time()
                try:
                    last = str(Tele(cc))
                except Exception as e:
                    print(e)
                    last = "Gateway Error"
                
                if 'risk' in last:
                    last = 'declined'
                elif 'Duplicate' in last:
                    last = 'Approved'
                
                mes = types.InlineKeyboardMarkup(row_width=1)
                cm1 = types.InlineKeyboardButton(f"• {cc} •", callback_data='u8')
                status = types.InlineKeyboardButton(f"• STATUS  : {last} ", callback_data='u8')
                cm3 = types.InlineKeyboardButton(f"• APPROVED ✅ : [ {live} ] •", callback_data='x')
                cm4 = types.InlineKeyboardButton(f"• DECLINED ❌ : [ {dd} ] •", callback_data='x')
                cm5 = types.InlineKeyboardButton(f"• TOTAL 🎉    : [ {total} ] •", callback_data='x')
                stop = types.InlineKeyboardButton(f"[ STOP 🚫 ]", callback_data='stop')
                mes.add(cm1, status, cm3, cm4, cm5, stop)
                
                end_time = time.time()
                execution_time = end_time - start_time
                
                bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''Wait for processing 
By ➜ @Parael1101 ''', reply_markup=mes)
                
                msg = f'''
<a href='t.me/Approved_Raven'>-</a> Approved ✅
<a href='t.me/Approved_Raven'>┏━━━━━━━⍟</a>           
<a href='t.me/Approved_Raven'>┃</a>CC: <code>{cc}</code>
<a href='t.me/Approved_Raven'>┗━━━━━━━━━━━⊛</a>
<a href='t.me/Approved_Raven'>-</a> Gateway: <code>Braintree Charge</code>       
<a href='t.me/Approved_Raven'>-</a> Response: <code>{last}</code>

<a href='t.me/Approved_Raven'>-</a> Info: <code>{cc[:6]}-{card_type} - {brand}</code>
<a href='t.me/Approved_Raven'>-</a> Country: <code>{country} - {country_flag}</code>
<a href='t.me/Approved_Raven'>-</a> Bank: <code>{bank}</code>

<a href='t.me/Approved_Raven'>-</a> Time: <code>{"{:.1f}".format(execution_time)} second</code> 
<a href='t.me/Approved_Raven'>-</a> Bot About: <a href='t.me/Approved_Raven'>⏤͟͞𝑮𝑺𝑰𝑿 𓆩 𝑪𝑯𝑲 𓆪ꪾᶜⁿꪜ</a>
<a href='t.me/Approved_Raven'>-</a> By: <a href='t.me/Approved_Raven'>『ᝯׁhׁׅ֮ꪱׁׅtׁׅꪀׁׅᧁׁꫀׁׅܻ 』【𝐂𝐇】ᶜⁿꪜ 💤</a>
'''
                print(last)
                if 'success' in last or 'Payment method successfully added.' in last:
                    live += 1
                    bot.reply_to(message, msg)
                elif 'Nice! New payment method added' in last or 'Insufficient Funds' in last:
                    live += 1
                    bot.reply_to(message, msg)
                else:
                    dd += 1
                    time.sleep(1)
    except Exception as e:
        print(e)
    
    bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='Completed ✅\nBot by ➜ @Parael1101')

@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def menu_callback(call):
    with open("stop.stop", "w") as file:
        pass

bot.polling()
