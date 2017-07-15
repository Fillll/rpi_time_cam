import time

import picamera
import telepot
import yaml


class TakeAndSend(object):
    def __init__(self, config_filename):
        super(TakeAndSend, self).__init__()
        self.config_filename = config_filename
        with open(config_filename) as config_file:
            self.config = yaml.load(config_file.read())
        self._init_camera()
        self._init_tg()
        time.sleep(self.config['init_sleep'])

    def _init_camera(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (self.config['camera_resolution_x'], self.config['camera_resolution_y'])
        self.camera.rotation = self.config['camera_rotaion']

    def _init_tg(self):
        self.tg_bot = telepot.Bot(self.config['telegram_token'])

    def take_pic(self):
        self.camera.capture(self.config['camera_pic_filename'])

    def send_pic(self):
        with open(self.config['camera_pic_filename'], 'rb') as picture:
            text = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.gmtime())
            self.tg_bot.sendPhoto(self.config['channel_id'], picture, caption=text, disable_notification=True)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config.yml')
    args = parser.parse_args()

    take_n_send = TakeAndSend(args.config)
    take_n_send.take_pic()
    take_n_send.send_pic()
