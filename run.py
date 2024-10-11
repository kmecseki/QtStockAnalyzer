import sys
import os
import json
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal
import yfinance as yf
import TickerWindow

# TODO:
# Add Info about tickers
# Save ticker info

cfgfile = "settings.json"


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
    all_data["tickers"] = widget.tickers
    with open(cfgfile, "w") as f:
        json.dump(all_data, f)



class App(QWidget):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("Qt Stock Analyzer")
        settings = load_settings()
        self.labels = []

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
        if "tickers" in settings:
            self.tickers = settings["tickers"]
            for ticker in self.tickers:
                self.add_new_ticker(ticker)
        else:
            self.tickers = []

        self.closeEvent = self.on_close

    def on_close(self, event):
        save_settings(self)
        event.accept()

    def setup_GUI(self):
        self.layout = QVBoxLayout()
        button_Add = QPushButton("Add stocks", self)
        button_Add.setToolTip("Click here to add new stocks")
        self.layout.addWidget(button_Add)
        button_Add.clicked.connect(self.open_stockwindow)
        self.setLayout(self.layout)
        

    def open_stockwindow(self):
        self.ticker_listwindow = TickerWindow.TickerWindow(self.size(), self.pos())
        self.ticker_listwindow.ticker_selected.connect(self.add_new_ticker)
        self.ticker_listwindow.show()
    
    def add_new_ticker(self, ticker):
        selected_ticker_label = QLabel("", self)
        remove_button = QPushButton("X", self)
        templayout = QHBoxLayout()
        templayout.addWidget(selected_ticker_label)
        templayout.addWidget(remove_button)
        remove_button.clicked.connect(lambda: self.remove_ticker(templayout))
        if ticker not in self.tickers:
            self.tickers.append(ticker)
        self.labels.append(templayout)
        self.layout.addLayout(templayout)
        selected_ticker_label.setText(f"{ticker}")
        
    def remove_ticker(self, sublayout):
        while sublayout.count():
            item = sublayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater() 
        self.layout.removeItem(sublayout)
        self.labels.remove(sublayout)
        sublayout.deleteLater()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())



# Download data for Apple from 2020 to 2023
#data = yf.download('AAPL', start='2020-01-01', end='2023-01-01')


