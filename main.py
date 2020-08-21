import os
import json
import glob
import click
import requests

from tqdm import tqdm

from utils.downloader import FlickrDownloader
from utils.checker import ImageChecker


@click.command('download')
@click.option('--config', default='./config.json', show_default=True,
              help='config file that contains flickr credentials.')
@click.option('--keyword', required=True, help='keyword to search.')
@click.option('--img_num', default=1000, show_default=True,
              help='max num of images to fetch (multiple of 100).')
@click.option('--offset', default=0, show_default=True,
              help='num of images to skip from start (multiple of 100).')
def download(config: str, keyword: str, img_num: int, offset: int):
    try:
        f = open(config, 'r')
        j = json.loads(f.read())

        api_key = j['API_KEY']
        api_secret = j['API_SECRET']

        f.close()
    except OSError:
        print('wrong config file path.')
        return
    except KeyError:
        print('api keys missing.')
        return

    downloader = FlickrDownloader(api_key, api_secret)

    base_path = './tmp_%s/' % keyword
    os.makedirs(base_path)

    urls = downloader.search(keyword, img_num, offset)
    pbar = tqdm(total=len(urls), postfix='downloading images')
    for idx, url in enumerate(urls):
        r = requests.get(url)
        with open(os.path.join(base_path, str(idx) + '.jpg'), 'wb') as f:
            f.write(r.content)
        pbar.n = idx
        pbar.refresh()
    pbar.close()


@click.command()
@click.option('--keyword', required=True, help='keyword which was used on download.')
def check(keyword: str):
    base_path = './tmp_%s/' % keyword
    if not os.path.exists(base_path):
        print('no directory called tmp_%s.' % keyword)
        return

    paths = glob.glob(base_path + '*.jpg')
    if len(paths) < 1:
        print('no image on ./tmp_%s/' % keyword)
        return

    ImageChecker(paths)


@click.group()
@click.pass_context
def main(*args, **kwargs):
    pass


if __name__ == '__main__':
    main.add_command(download)
    main.add_command(check)
    main()
