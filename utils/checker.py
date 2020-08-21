import os

from typing import List
from tqdm import tqdm

import matplotlib.pyplot as plt
import matplotlib.image as mimg
import matplotlib.widgets as widgets


class ImageChecker:
    def __init__(self, imgs: List[str]):
        self.idx = 0
        self.imgs = imgs
        self.pbar = tqdm(total=len(imgs), postfix='current progress')
        self.dels = []

        self.plt = None

        ca = plt.gca()

        ax_del = plt.axes([0.7, 0.0, 0.1, 0.075])
        ax_pass = plt.axes([0.8, 0.0, 0.1, 0.075])
        ax_stop = plt.axes([0.9, 0.0, 0.1, 0.075])

        btn_del = widgets.Button(ax_del, 'DEL')
        btn_pass = widgets.Button(ax_pass, 'PASS')
        btn_stop = widgets.Button(ax_stop, 'STOP')

        btn_del.on_clicked(self.on_del)
        btn_pass.on_clicked(self.on_pass)
        btn_stop.on_clicked(self.on_stop)

        plt.sca(ca)
        self.show()

    def on_del(self, event=None):
        self.dels.append(self.imgs[self.idx])
        self.idx += 1
        self.show(event)

    def on_pass(self, event=None):
        self.idx += 1
        self.show(event)

    def on_stop(self, event=None):
        self.pbar.close()
        self.pbar = tqdm(self.dels, postfix='removing files')
        for img in self.pbar:
            os.remove(img)
        self.pbar.close()
        plt.close('all')

    def show(self, event=None):
        if len(self.imgs) <= self.idx:
            self.on_stop()
            return
        self.pbar.n = self.idx
        self.pbar.refresh()

        img = mimg.imread(self.imgs[self.idx], format='jpeg')

        # performance issue
        # 1. use set_data instead of imshow: causes lagging.
        # 2. use canvas.draw instead of show: causes maximum recursion depth.
        if self.plt is None:
            self.plt = plt.imshow(img, interpolation=None)
        else:
            self.plt.set_data(img)

        if event is None:
            plt.show()
        else:
            event.canvas.draw()
