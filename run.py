import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QAbstractButton
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
import yfinance as yf
import TickerWindow
import util
import time
# TODO:
# Add Info about tickers
# Save ticker info



class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Qt Stock Analyzer")
        settings = util.load_settings()
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
                self.GUI_add_new_ticker(ticker, True)
        else:
            self.tickers = []

        self.closeEvent = self.on_close

    def on_close(self, event):
        util.save_settings(self)
        event.accept()

    def setup_GUI(self):
        self.layout = QVBoxLayout()
        #self.message_label = QLabel("", self)
        #self.layout.addWidget(self.message_label)
        buttons = QHBoxLayout()
        button_Add = QPushButton("Add stocks", self)
        button_Add.setToolTip("Click here to add new stocks")
        button_Live = QPushButton("Live off", self)
        button_Live.setCheckable(True)
        button_Live.setToolTip("Click here to fetch real time prices")
        buttons.addWidget(button_Add)
        buttons.addWidget(button_Live)
        self.layout.addLayout(buttons)
        button_Add.clicked.connect(self.open_stockwindow)
        button_Live.toggled.connect(self.run_live)
        # Add column names
        templayout = QHBoxLayout()
        ticker_label = QLabel("Symbol", self)
        ticker_label.setStyleSheet("font-weight: bold;")
        ticker_name = QLabel("  -  Name", self)
        ticker_name.setStyleSheet("font-weight: bold;")
        ticker_price = QLabel("Price", self)
        ticker_price.setStyleSheet("font-weight: bold;")
        remove_button = QLabel("Remove", self)
        remove_button.setStyleSheet("font-weight: bold;")
        columnNames = QHBoxLayout()
        columnNames.addWidget(ticker_label, alignment=Qt.AlignLeft)
        columnNames.addWidget(ticker_name, alignment=Qt.AlignRight)
        columnNames.addStretch()
        columnNames.addWidget(ticker_price, alignment=Qt.AlignRight)
        columnNames.addWidget(remove_button, alignment=Qt.AlignRight)
        self.layout.addLayout(columnNames)
             
        self.setLayout(self.layout)
     
    def run_live(self):
        button = self.layout.itemAt(0).itemAt(1).widget()
        if button.isChecked():
            self.timer = QTimer(self)
            self.timer.setInterval(10000)
            self.timer.timeout.connect(self.update_prices)
            self.timer.start()
            button.setText("Live on")
        else:
            self.timer.stop()
            button.setText("Live off")

    def open_stockwindow(self):
        self.ticker_listwindow = TickerWindow.TickerWindow(self.size(), self.pos())
        self.ticker_listwindow.ticker_selected.connect(self.GUI_add_new_ticker)
        self.ticker_listwindow.show()
    
    def GUI_add_new_ticker(self, ticker, init=False):
        
        if (init or (ticker not in self.tickers)):
            if ticker not in self.tickers:
                self.tickers.append(ticker)
            ticker_label = QLabel("", self)
            ticker_name = QLabel("", self)
            ticker_price = QLabel("0.00", self)
            remove_button = QPushButton("X", self)
            templayout = QHBoxLayout()
            templayout.addWidget(ticker_label, alignment=Qt.AlignLeft)
            templayout.addWidget(ticker_name, alignment=Qt.AlignRight)
            templayout.addStretch()
            templayout.addWidget(ticker_price, alignment=Qt.AlignRight)
            templayout.addWidget(remove_button, alignment=Qt.AlignRight)
            remove_button.clicked.connect(lambda: self.remove_ticker(templayout, ticker))
            self.labels.append(templayout)
            self.layout.addLayout(templayout)
            ticker_label.setText(f"{ticker[0]}")
            ticker_name.setText(f"  -  {ticker[1]}")


    def remove_ticker(self, sublayout, ticker):
        
        while sublayout.count():
            item = sublayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater() 
        self.layout.removeItem(sublayout)
        self.labels.remove(sublayout)
        self.tickers.remove(ticker)
        sublayout.deleteLater()
        self.adjustSize()

    def update_prices(self):
        for layout in self.labels:
            ticker = layout.itemAt(0).widget().text()
            price = self.get_current_price(ticker)
            label = layout.itemAt(3).widget()
            if label is not None:
                label.setText("{:.2f}".format(price))
    
    def get_current_price(self, symbol):
        ticker = yf.Ticker(symbol)
        todays_data = ticker.history(period='1d')
        return todays_data['Close'].iloc[0]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())



# Download data for Apple from 2020 to 2023
#data = yf.download('AAPL', start='2020-01-01', end='2023-01-01')


