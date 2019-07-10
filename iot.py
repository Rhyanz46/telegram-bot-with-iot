import RPi.GPIO as GPIO
import time
import picamera
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import os
import sys


GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN) #PIR
camera = picamera.PiCamera()

update_id = None


# Sets the id for the active chat
#857399797
pathname = os.path.dirname(sys.argv[0])
tempat = os.path.abspath(pathname) + "/capture.jpg"
bot = telegram.Bot('857399797:AAHkSZbQ5xPBvrcSl_Bih7PIPBvG1K2ytQQ')
response = bot.getUpdates()



def main():
    """Run the bot."""
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot('857399797:AAHkSZbQ5xPBvrcSl_Bih7PIPBvG1K2ytQQ')

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            echo(bot)
        except NetworkError:
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
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            # Reply to the message
            if update.message.text == "minta foto":
                try:
                    time.sleep(2) # to stabilize sensor
                    while True:
                        if GPIO.input(23):
                            camera.start_preview()
                            camera.capture(tempat)
                            camera.stop_preview()
                            print("Motion Detected...")
                            if os.path.exists(tempat):
                               print("ada")
                               bot.send_photo(chat_id=update.message.chat_id, photo=open(tempat,'rb'))
                               update.message.reply_text("ok gk ni ?")#
                            else:
                                print("ada gan")        
                                time.sleep(5) #to avoid multiple detection
                                time.sleep(0.1) #loop delay, should be less than detection delay
                except:
                # Sends a message to the chat
                    print("error bro")
                #bot.sendPhoto(chat_id= 857399797, photo=open(tempat))
                # bot.sendMessage(chat_id=857399797, str("Hi! MakerPro"))
                    GPIO.cleanup()
            else:
                update.message.reply_text(update.message.text)
                print(update.to_json())
                print("")
                print("")

           


if __name__ == '__main__':
    main()
    
    

