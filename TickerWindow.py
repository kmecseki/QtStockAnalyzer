import os
import pandas as pd
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton
from PyQt5.QtCore import pyqtSignal

sp500_tickers = pd.read_csv('https://datahub.io/core/s-and-p-500-companies/r/constituents.csv')

class TickerWindow(QWidget):
    ticker_selected = pyqtSignal(str)

    def __init__(self, size, pos):
        super().__init__()
        
        self.ticker = ""
        self.setWindowTitle('S&P 500 Ticker List')
        self.setGeometry(pos.x()-100, pos.y(), size.width(), size.height())

        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.fill_ticker_list()

        self.button_add = QPushButton("Add", self)
        self.button_add.resize(100, 40)
        self.button_add.clicked.connect(self.add_stock)
        self.list_widget.itemClicked.connect(self.list_item_selected)
        
        layout.addWidget(self.list_widget)
        layout.addWidget(self.button_add)

        self.setLayout(layout)

    def fill_ticker_list(self):
        if os.path.exists('constituents.csv'):
            tickers = pd.read_csv('constituents.csv')
            tickers = tickers['Symbol'].tolist()
        else:
            tickers = sp500_tickers['Symbol'].tolist()
        self.list_widget.addItems(tickers)

    def list_item_selected(self):
        self.ticker = self.list_widget.currentItem().text()

    def add_stock(self):
        self.ticker_selected.emit(self.ticker)
        self.close()
    