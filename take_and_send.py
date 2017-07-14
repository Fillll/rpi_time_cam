import time

import picamera
import telepot
import yaml


def take_pic(filename):
    camera = picamera.PiCamera()
    camera.resolution = (3280, 2464)
    camera.rotation = 180
    camera.capture(filename)


def send_to_tg(filename):
    with open('/home/pi/rpi_time_cam/config.yml') as config_file:
        config = yaml.load(config_file.read())
    tg_bot = telepot.Bot(config['telegram_token'])
    text = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    f = open(filename, 'rb')
    tg_bot.sendPhoto(config['channel_id'], f, caption=text, disable_notification=True)
    f.close()


if __name__ == '__main__':
    filename = '/tmp/test.jpg'
    take_pic(filename)
    send_to_tg(filename)
