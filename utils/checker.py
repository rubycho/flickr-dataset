import os
import sys

from typing import List

from PySide2 import QtCore, QtWidgets, QtGui


class ImageChecker(QtWidgets.QWidget):
    def __init__(self, paths: List[str]):
        super().__init__()

        self.idx = 0
        self.paths = paths
        self.path_len = len(self.paths)

        self.history = dict()
        for path in paths:
            self.history[path] = False

        self.marked_text = 'Will be deleted: YES'
        self.unmarked_text = 'Will be deleted: NO'

        self.status = QtWidgets.QLabel('')
        self.path_status = QtWidgets.QLabel('')
        self.marked = QtWidgets.QLabel('')

        self.image = QtWidgets.QLabel(self)
        self.image.setAlignment(QtCore.Qt.AlignCenter)

        self.mark_btn = QtWidgets.QPushButton('Mark/Unmark')
        self.mark_btn.clicked.connect(self.on_mark)

        self.prev_btn = QtWidgets.QPushButton('Prev')
        self.prev_btn.clicked.connect(self.on_prev)

        self.next_btn = QtWidgets.QPushButton('Next')
        self.next_btn.clicked.connect(self.on_next)

        self.stop_btn = QtWidgets.QPushButton('Stop')
        self.stop_btn.clicked.connect(self.on_stop)

        self.btn_layout = QtWidgets.QHBoxLayout()
        self.btn_layout.addWidget(self.mark_btn)
        self.btn_layout.addWidget(self.prev_btn)
        self.btn_layout.addWidget(self.next_btn)
        self.btn_layout.addWidget(self.stop_btn)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.status)
        self.layout.addWidget(self.path_status)
        self.layout.addWidget(self.marked)
        self.layout.addWidget(self.image)
        self.layout.addLayout(self.btn_layout)

        self.setLayout(self.layout)
        self.on_click()

    def on_mark(self):
        path = self.paths[self.idx]
        self.history[path] = not self.history[path]
        self.on_click()

    def on_prev(self):
        self.idx -= 1
        self.on_click()

    def on_next(self):
        self.idx += 1
        self.on_click()

    def on_stop(self):
        self.setEnabled(False)
        for path in self.paths:
            if self.history[path]:
                os.remove(path)
                print('Removed %s.' % path)
        sys.exit(0)

    def on_click(self):
        self.status.setText('Current %d / Total %d' % (self.idx + 1, self.path_len))

        path = self.paths[self.idx]
        self.path_status.setText('Path: %s' % path)
        self.marked.setText(self.marked_text if self.history[path] else self.unmarked_text)

        pixmap = QtGui.QPixmap(path)
        self.image.setPixmap(pixmap)

        self.next_btn.setEnabled(self.idx + 1 < self.path_len)
        self.prev_btn.setEnabled(self.idx > 0)
