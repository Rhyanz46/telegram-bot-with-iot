import RPi.GPIO as GPIO
import picamera
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import os
import sys
import datetime


GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)

update_id = None



def main():
    """Run the bot."""
    global update_id
    bot = telegram.Bot('857399797:AAHkSZbQ5xPBvrcSl_Bih7PIPBvG1K2ytQQ')

    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            echo(bot)
        except NetworkError:
            print("gk ada internet bos")
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1
        except KeyboardInterrupt:
            print("press control-c again to quit")
            return "ok"
            


def echo(bot):
    """Echo the message the user sent."""
    global update_id
    # print("Sekarang id yang ke : {}".format(update_id))
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:
            if update.message.text == "/start":
                update.message.reply_text("Selamat datang di aplikasi deteksi pergerakan, kamu akan mendapatkan notifikasi jika ada pergerakan")
                # try:
                sleep(2)
                while True:
                    if GPIO.input(23): # nilai awalnya adalah 0, jika terdeteksi maka nilainya 1
                        update.message.reply_text("Ada Pergerakan")
                        update_id = update.update_id + 1
                    if update.message.text == "minta foto":
                        update.message.reply_text("ok, isi pesan : {}".format(update.message.text))
                    sleep(2)
                        # terminta = 0
                        
                        # if update.message:
                        #     update.message.reply_text('mantap')
                        # for update in bot.get_updates(offset=update_id, timeout=10):
                        #     # sleep(1)
                        #     update.message.reply_text('mantap')
                            # if GPIO.input(23):
                            # terminta +=1
                            # if terminta == 1:
                            #     break
                            #     terminta = 0
                            # update_id = update.update_id + 1
                            # if update.message and update.message.text == "minta foto":
                            #     update.message.reply_text("ok wait")
                            #     break
                            #     terminta = 0
            else:
                print("")
                print("")
                update.message.reply_text("ketik '/start' untuk memulai, isi pesan : {}".format(update.message.text))
                print(update.to_json())
                print("")
                print("")
        else:
            sleep(2)

           


if __name__ == '__main__':
    main()
    
    



