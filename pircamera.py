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
balas = 0

pathname = os.path.dirname(sys.argv[0])
tempat = os.path.abspath(pathname)
tempat_foto = tempat + "/foto"


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
    balasan = False
    for update in bot.get_updates(offset=update_id, timeout=100000):
        update_id = update.update_id + 1

        if update.message:
            if update.message.text == "/start":
                update.message.reply_text("Selamat datang di aplikasi deteksi pergerakan, kamu akan mendapatkan notifikasi jika ada pergerakan")
                # try:
                sleep(2)
                while True:
                    if GPIO.input(23): # nilai awalnya adalah 0, jika terdeteksi maka nilainya 1
                        nama = str(datetime.datetime.now()) + ".jpg"
                        alamat_foto = tempat_foto + nama
                        camera.capture(alamat_foto)
                        if balasan:
                            file = open("foto/log.txt","w+")
                        else:
                            file = open("foto/log.txt","a+")
                        file.write(alamat_foto)
                        file.close()
                        update.message.reply_text("Ada Pergerakan")
                        if os.path.exists(tempat_foto):
                            bot.send_photo(chat_id=update.message.chat_id, photo=open(tempat_foto,'rb'))
                        else:
                            update.message.reply_text("maaf gambarnya terhapus")
                        
                        
                # except:
                #     print("exit")
                #     try:
                #         os.remove(tempat_foto)
                #         GPIO.cleanup()
                #         print("sukses")
                #     except:
                #         print("error bro")
                        
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
    
    


