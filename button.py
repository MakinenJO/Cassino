'''
A QPushButton subclass for easier button managing
'''
from PyQt5.Qt import QPushButton, QPalette
from PyQt5.QtCore import Qt

class Button(QPushButton):
    
    def __init__(self, parent, text):
        super(Button, self).__init__(parent)
        self.setText(text)
        self.setPalette(QPalette(Qt.white))