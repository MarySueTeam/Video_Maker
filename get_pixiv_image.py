from pixivpy3 import *
from rich.progress import track
from rich.console import Console
import os
import time
import random

console = Console()

api = AppPixivAPI()
api.auth(refresh_token='ADpdU_RmJzHQ1-o_5o5ZXAhNx3HVAZqPhjgd-ZN2o8E')


def _get_img(user_id: str, offset: int = 0):
    ans = api.user_illusts(user_id=user_id, offset=offset)

    for item in track(ans.illusts):
        download_url = item.image_urls['large']
        api.download(url=download_url,
                     path=os.path.curdir + '/src/images',
                     replace=True)
    # INFO 获取偏移量
    offset = api.parse_qs(ans['next_url'])['offset']
    # INFO 返回偏移量,以便进行之后的执行
    return offset


def get_all_img(user_id: str):
    offset = 0
    while True:
        try:
            offset = _get_img(user_id, offset)
            # console.print(offset)
        except TypeError:
            console.log("下载完毕")
            break


if __name__ == '__main__':
    get_all_img('4792861')