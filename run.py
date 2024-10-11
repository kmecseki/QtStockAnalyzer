import sys
import os
import json
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal
import yfinance as yf
# TODO:
# Add Info about tickers

cfgfile = "settings.json"
sp500_tickers = pd.read_csv('https://datahub.io/core/s-and-p-500-companies/r/constituents.csv')


def load_settings():
    if os.path.exists(cfgfile):
        with open(cfgfile, "r") as f:
            return json.load(f)
    return None


def save_settings(widget):
    position = widget.pos()
    size = widget.size()
    all_data = {"position" : {"x": position.x(), "y": position.y()}}
    all_data["size"] = {"width": size.width(), "height": size.height()}
    with open(cfgfile, "w") as f:
        json.dump(all_data, f)



class App(QWidget):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("Qt Stock Analyzer")
        settings = load_settings()

        if "position" in settings:
            position = settings["position"]
            self.move(position["x"], position["y"])
        else:
            self.move(100, 100)

        if "size" in settings:
            size = settings["size"]
            self.resize(size["width"], size["height"])
        else:
            self.resize(300, 200)

        self.setup_GUI()


        self.closeEvent = self.on_close

    def on_close(self, event):
        save_settings(self)
        event.accept()

    def setup_GUI(self):
        self.layout = QVBoxLayout()
        button_Add = QPushButton("Add stocks", self)
        button_Add.setToolTip("Click here to add new stocks")
        #button_Add.resize(100, 40)
        #button_Add.move(100, 80)
        button_Add.clicked.connect(self.open_stockwindow)
        self.selected_ticker_label = QLabel('No Ticker Selected', self)
        self.layout.addWidget(button_Add)
        self.layout.addWidget(self.selected_ticker_label)
        self.setLayout(self.layout)
        

    def open_stockwindow(self):
        self.ticker_listwindow = TickerWindow(self.size(), self.pos())
        self.ticker_listwindow.ticker_selected.connect(self.add_new_ticker)
        self.ticker_listwindow.show()
    
    def add_new_ticker(self, ticker):
        self.selected_ticker_label.setText(f"{ticker}")


class TickerWindow(QWidget):
    ticker_selected = pyqtSignal(str)

    def __init__(self, size, pos):
        super().__init__()
        
        self.setWindowTitle('S&P 500 Ticker List')
        self.setGeometry(pos.x()-100, pos.y(), size.width(), size.height())

        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.fill_ticker_list()

        self.button_add = QPushButton("Add", self)
        self.button_add.resize(100, 40)
        self.button_add.clicked.connect(self.add_stock)
        selection = self.list_widget.itemClicked.connect(self.list_item_selected)
        #self.button_add.clicked.connect(self.add_stock(selection))
        
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
        self.ticker = 
        
    def add_stock(self, ticker):
        self.ticker_selected.emit(ticker)
        self.close()
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())



# Download data for Apple from 2020 to 2023
#data = yf.download('AAPL', start='2020-01-01', end='2023-01-01')


