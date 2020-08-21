from tqdm import tqdm
from flickrapi import FlickrAPI


class FlickrDownloader:
    def __init__(self, api_key: str, api_secret: str):
        self.flickr = FlickrAPI(api_key, api_secret, format='parsed-json')

    def search(self, keyword: str, img_num: int = 1000, offset: int = 0):
        per_page = 100
        pbar = tqdm(total=img_num, postfix='fetching image urls')

        page = (offset // per_page) + 1
        curr_img_num = 0
        extras = 'url_q'

        data = []
        while curr_img_num < img_num:
            result = self.flickr.photos.search(
                text=keyword,
                per_page=per_page, page=page,
                sort='relevance', extras=extras
            )

            if int(result['photos']['page']) != page:
                break

            data = data + [item['url_q'] for item in result['photos']['photo']]
            curr_img_num = len(data)

            pbar.n = len(data)
            pbar.refresh()
        pbar.close()
        return data
