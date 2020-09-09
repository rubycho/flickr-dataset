import os
import sys
import json
import glob
import click

from PySide2 import QtWidgets

from utils.downloader import FlickrDownloader
from utils.checker import ImageChecker


class Config:
    def __init__(self, config: str):
        f = open(config, 'r')
        j = json.loads(f.read())

        self.api_key = j['API_KEY']
        self.api_secret = j['API_SECRET']
        self.keyword = j['KEYWORD']

        size = j.get('SIZE', 128)
        if size < 128:
            size = 128
        if size > 640:
            size = 640
        self.size = size

        self.sp = j.get('START_PAGE', 1)
        self.ep = j.get('END_PAGE', 10)

        f.close()

        print('=========config=========')
        print('keyword: ', self.keyword)
        print('size: ', self.size)
        print('start page: ', self.sp)
        print('end page: ', self.ep)
        print('========================')


@click.command('download')
@click.option('--config', default='./config.json', show_default=True,
              help='path to config file')
def download(config: str):
    conf = Config(config)
    downloader = FlickrDownloader(conf.api_key, conf.api_secret)

    base_path = './tmp_%s/' % conf.keyword
    os.makedirs(base_path)

    urls = downloader.search(conf.keyword, conf.sp, conf.ep)
    downloader.download(base_path, urls, (conf.size, conf.size))


@click.command()
@click.option('--config', default='./config.json', show_default=True,
              help='path to config file')
def check(config: str):
    conf = Config(config)
    base_path = './tmp_%s/' % conf.keyword
    if not os.path.exists(base_path):
        print('no directory called tmp_%s.' % conf.keyword)
        return

    paths = glob.glob(base_path + '*.jpg')
    if len(paths) < 1:
        print('no image on ./tmp_%s/' % conf.keyword)
        return

    app = QtWidgets.QApplication([])

    image_checker = ImageChecker(paths)
    image_checker.setWindowTitle('flickr-dataset')
    image_checker.show()

    sys.exit(app.exec_())


@click.group()
@click.pass_context
def main(*args, **kwargs):
    pass


if __name__ == '__main__':
    main.add_command(download)
    main.add_command(check)
    main()
