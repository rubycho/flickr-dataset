import os
import io
import requests

from typing import List
from PIL import Image, ImageOps

from flickrapi import FlickrAPI
from tqdm import tqdm


class FlickrDownloader:
    def __init__(self, api_key: str, api_secret: str):
        self.flickr = FlickrAPI(api_key, api_secret, format='parsed-json')

    def search(self, keyword: str, sp: int, ep: int):
        per_page = 100
        pbar = tqdm(range(sp, ep+1), postfix='fetching image urls')

        extras = 'url_z'

        data = []
        for p in pbar:
            result = self.flickr.photos.search(
                text=keyword,
                per_page=per_page, page=p,
                sort='relevance', extras=extras
            )

            if int(result['photos']['page']) != p:
                break

            data = data + [item['url_z'] for item in result['photos']['photo'] if 'url_z' in item]
        pbar.close()

        print('total: %d images.' % len(data))
        return data

    def download(self, path: str, urls: List[str], size: tuple = (300, 300)):
        pbar = tqdm(total=len(urls), postfix='downloading images')
        for idx, url in enumerate(urls):
            r = requests.get(url)

            img = Image.open(io.BytesIO(r.content))
            th = ImageOps.fit(img, size, Image.ANTIALIAS)
            th.save(str(os.path.join(path, str(idx) + '.jpg')))

            pbar.n = idx + 1
            pbar.refresh()
        pbar.close()
