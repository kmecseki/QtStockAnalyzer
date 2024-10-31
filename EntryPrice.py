#import os
#import pandas as pd
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QDoubleValidator, QIntValidator
import math

class EntryPrice(QWidget):
    entry_price = pyqtSignal(str)

    def __init__(self, size, pos):
        super().__init__()
        
        layout = QVBoxLayout()
        self.setWindowTitle('Add entry price')
        self.setGeometry(pos.x() - 100, pos.y() + size.height(), math.floor(size.width() / 2), 150)#pos.x()-100, pos.y(), size.width(), size.height())

        price_label = QLabel("Price bought", self)

        stock_price_bought = QLineEdit()
        stock_price_bought.setValidator(QDoubleValidator())
        amount_label = QLabel("Amount bought", self)
        stock_amount_bought = QLineEdit()
        stock_amount_bought.setValidator(QIntValidator())
        layout.addWidget(price_label)
        layout.addWidget(stock_price_bought)
        layout.addWidget(amount_label)
        layout.addWidget(stock_amount_bought)
        button_price = QPushButton("Add stock bought", self)
        button_price.resize(100, 40)
        layout.addWidget(button_price)
        #self.button_add.clicked.connect(self.add_stock)


        self.setLayout(layout)
        self.show()



