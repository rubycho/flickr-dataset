import os
import json
import glob
import click

from utils.downloader import FlickrDownloader
from utils.checker import ImageChecker


@click.command('download')
@click.option('--config', default='./config.json', show_default=True,
              help='config file that contains flickr credentials.')
@click.option('--keyword', required=True, help='keyword to search.')
@click.option('--sp', default=1, show_default=True,
              help='start page (each page has approx. 100 images)')
@click.option('--ep', default=10, show_default=True,
              help='end page (each page has approx. 100 images)')
def download(config: str, keyword: str, sp: int, ep: int):
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

    urls = downloader.search(keyword, sp, ep)
    downloader.download(base_path, urls)


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
