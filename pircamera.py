import RPi.GPIO as GPIO
import picamera
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import os
import sys


GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)
camera = picamera.PiCamera()

update_id = None

pathname = os.path.dirname(sys.argv[0])
tempat = os.path.abspath(pathname) + "/capture.jpg"


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
    for update in bot.get_updates(offset=update_id, timeout=100000):
        update_id = update.update_id + 1

        if update.message:
            if update.message.text == "/start":
                update.message.reply_text("Selamat datang di aplikasi deteksi pergerakan, kamu akan mendapatkan notifikasi jika ada pergerakan")
                try:
                    time.sleep(2)
                    while True:
                        if GPIO.input(23): # nilai awalnya adalah 0, jika terdeteksi maka nilainya 1
                            # camera.start_preview() jika kau mau tampilin gambar di monitor aktifkan kodingan ini
                            camera.capture(tempat)
                            # camera.resolution = (524, 568)
                            # camera.stop_preview() jika kau mau matikan kamera
                            print("Motion Detected...")
                            print("-----------------")
                            print(update.to_json())
                            print("-----------------")
                                # if os.path.exists(tempat):
                                #     print("ada")
                                #     bot.send_photo(chat_id=update.message.chat_id, photo=open(tempat,'rb'))
                                #     update.message.reply_text("ok gk ni ?")
                                # else:
                                #     print("tidak ada gambarnya")        
                                
                        
                except:
                    try:
                        os.remove(tempat)
                        GPIO.cleanup()
                    except:
                        print("error bro")
                        
            else:
                print("")
                print("")
                update.message.reply_text(update.message.text)
                print(update.to_json())
                print("")
                print("")
        else:
            sleep(2)

           


if __name__ == '__main__':
    main()
    
    


