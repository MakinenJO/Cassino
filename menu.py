from PyQt5.Qt import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QComboBox,\
    QLabel, QLineEdit, QPalette, QCheckBox, QSpacerItem, QSizePolicy, QPixmap
    
from PyQt5.QtCore import Qt
from button import Button
from game import Game

class MainMenu(QWidget):
    def __init__(self, parent):
        super(MainMenu, self).__init__(parent)
        self.startbutton = Button(self, 'New Game')
        self.startbutton.setFixedWidth(150)
        
        self.loadbutton = Button(self, 'Load Game')
        self.loadbutton.setFixedWidth(150)

        self.quitbutton = Button(self, 'Quit')
        self.quitbutton.setFixedWidth(150)
        
        self.hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.vbox.addSpacing(250)
        self.vbox.addWidget(self.startbutton)
        self.vbox.addWidget(self.loadbutton)
        self.vbox.addWidget(self.quitbutton)
        self.vbox.addSpacing(250)
        self.hbox.addLayout(self.vbox)
        self.setLayout(self.hbox)
        
        
        
class StartMenu(QWidget):
    
    def __init__(self, parent):
        super(StartMenu, self).__init__(parent)
        
        self.tophbox = QHBoxLayout()
        self.hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()
        
        self.label = QLabel()
        self.label.setPixmap(QPixmap('img/new-game.png'))
        self.label.setScaledContents(True)
        self.label.setFixedSize(600, 200)
        self.tophbox.addWidget(self.label)
        
        self.startbutton = Button(self, 'Start')
        self.startbutton.setEnabled(False)
        self.startbutton.setFixedHeight(100)
        self.tophbox.addWidget(self.startbutton)
        
        self.playeramt_label = QLabel('Number of players:')
        self.playeramt_label.setFixedWidth(125)
        
        self.playeramount = QComboBox()
        self.playeramount.setStyleSheet('color: rgb(0, 0, 0)')
        self.playeramount.setFixedWidth(50)
        self.playeramount.addItems([str(i) for i in range(2, 13)])
        self.playeramount.setCurrentIndex(2)
        self.playeramount.setMaxVisibleItems(11)
        self.playeramount.currentTextChanged.connect(self.form_player_entries)
        
        self.score_label = QLabel('Score limit:')
        self.score_label.setFixedWidth(65)
        
        self.score_limit = QLineEdit()
        self.score_limit.setMaximumWidth(40)
        self.score_limit.setPalette(QPalette(Qt.white))
        self.score_limit.setText('16')
        
        self.mode_label = QLabel('Game Mode:')
        self.mode_label.setFixedWidth(85)
        
        self.mode_select = QComboBox()
        self.mode_select.addItems(['Deal-1', 'Deal-4'])
        self.mode_select.setPalette(QPalette(Qt.white))
        self.mode_select.setFixedWidth(100)
        self.mode_select.currentTextChanged.connect(self.update_playeramount)
            
        self.autofill_button = Button(self, 'Auto Fill')
        self.autofill_button.clicked.connect(self.auto_fill)
        self.clear_button = Button(self, 'Clear All')
        self.clear_button.clicked.connect(self.clear_all)
        
        self.player_entries = QVBoxLayout()
        
        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        self.hbox.addWidget(self.playeramt_label)
        self.hbox.addWidget(self.playeramount)
        self.hbox.addWidget(self.score_label)
        self.hbox.addWidget(self.score_limit)
        self.hbox.addWidget(self.mode_label)
        self.hbox.addWidget(self.mode_select)
        self.hbox.addWidget(self.autofill_button)
        self.hbox.addWidget(self.clear_button)
        
        self.vbox.addLayout(self.tophbox)
        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.player_entries)
        self.vbox.addItem(self.spacer)
        
        self.setLayout(self.vbox)
        
        self.form_player_entries() 


    def form_player_entries(self):
        amt = self.playeramount.currentIndex() + 2  #desired amount of player entries
        curr = self.player_entries.count()          #current amount of player entries
        dif = amt - self.player_entries.count()     #difference between desired and current entries
        
        if dif < 0:                                 #if too many entries currently 
            for i in range(curr-1, amt-1, -1):      #remove starting from last entry
                rm = self.player_entries.itemAt(i).widget()
                self.player_entries.removeWidget(rm)
                rm.setParent(None)
                
        
        else:                                       #if too few entries, add until desired amount reached
            for i in range(dif):
                new_entry = PlayerInfoField(self, self.player_entries.count())
                new_entry.name_field.textChanged.connect(self.check_filled)
                self.player_entries.addWidget(new_entry)
         
        self.check_filled()       
    
    
    def check_filled(self): #Enables start button when player fields are correctly filled
        ready = True
        
        for i in range(self.player_entries.count()):
            entry = self.player_entries.itemAt(i).widget()
            if entry.name_field.text() == '':
                ready = False
                break
            
        if ready:
            self.startbutton.setEnabled(True)
        else:
            self.startbutton.setEnabled(False)
            
                
    def auto_fill(self): #Generates fills the rest of the form automatically
        for i in range(self.player_entries.count()):
            entry = self.player_entries.itemAt(i).widget()
            if entry.name_field.text() == '':
                entry.generate_name()
                entry.AItoggle.setChecked(True)
                
    def clear_all(self):
        for i in range(self.player_entries.count()):
            entry = self.player_entries.itemAt(i).widget()
            entry.name_field.clear()
            entry.AItoggle.setChecked(False)
            
    def update_playeramount(self, mode):
        ind = self.playeramount.currentIndex()
        if mode == 'Deal-1': #Limit max players to 12
            self.playeramount.clear()
            self.playeramount.addItems([str(i) for i in range(2, 13)])
            self.playeramount.setCurrentIndex(ind)
            
        if mode == 'Deal-4': #Limit max players to 4
            self.playeramount.clear()
            self.playeramount.addItems([str(i) for i in range(2, 5)])
            self.playeramount.setCurrentIndex(min(2, ind))
            
        self.check_filled()
            
                
    def extract_info_and_init_game(self): #Creates a game object based on the info 
        pointlimit = int(self.score_limit.text())
        dealmode = self.mode_select.currentIndex()
        game = Game(pointlimit, dealmode)
        
        for i in range(self.player_entries.count()):
            entry = self.player_entries.itemAt(i).widget()
            name = entry.name_field.text()
            if entry.AItoggle.isChecked():
                difficulty = entry.AIdifficulty.currentIndex()
                game.add_player(name, difficulty)
            else:
                game.add_player(name, 5)
            
        return game


class PlayerInfoField(QWidget): #Widget for inputting player info. 
    names = ['Alex', 'Clifford', 'Tyrone', 'Ava', 'Ralph', 'Emily', 'Falcon', 'Giselle', 'Jaeger', 'Sally', 'Quentin', 'Lara']
    
    def __init__(self, parent, index):
        super(PlayerInfoField, self).__init__(parent)
        self.index = index
        
        self.layout = QHBoxLayout()
        
        self.auto_button = Button(self, 'Auto')
        self.auto_button.setFixedWidth(60)
        self.auto_button.clicked.connect(self.generate_name)
        self.layout.addWidget(self.auto_button)
        
        self.name_field = QLineEdit()
        self.name_field.setPalette(QPalette(Qt.white))
        self.name_field.setPlaceholderText('Name')
        self.name_field.setClearButtonEnabled(True)
        self.name_field.setFixedWidth(250)
        self.layout.addWidget(self.name_field)
        
        self.AItoggle = QCheckBox()
        self.AItoggle.setText('Computer')
        self.AItoggle.setFixedWidth(100)
        self.layout.addWidget(self.AItoggle)
        self.AItoggle.stateChanged.connect(self.AIToggled)
        
        self.AIdifficulty = QComboBox()
        self.AIdifficulty.setPalette(QPalette(Qt.white))
        self.AIdifficulty.setFixedWidth(100)
        self.AIdifficulty.addItems(['Braindead', 'Easy', 'Normal', 'Hard', 'HAL-9000'])
        self.AIdifficulty.setCurrentIndex(2)
        self.AIdifficulty.setDisabled(True)
        self.layout.addWidget(self.AIdifficulty)
        
        self.spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout.addItem(self.spacer)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.setLayout(self.layout)
        
        
    def generate_name(self):
        self.name_field.setText(PlayerInfoField.names[self.index])
     
    def AIToggled(self):
        if self.AItoggle.checkState() == Qt.Checked:
            self.AIdifficulty.setEnabled(True)
            
        else:
            self.AIdifficulty.setDisabled(True)
  
  
  
        
class EndMenu(QWidget): #Unused for now.
    
    def __init__(self, parent):
        super(EndMenu, self).__init__(parent)
        
        self.label = QLabel('End of game.')