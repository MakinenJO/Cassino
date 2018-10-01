import sys
from PyQt5.Qt import QApplication
from game_gui import MainWindow

def main():
    app = QApplication(sys.argv)
    print('Loading Game...')
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
    