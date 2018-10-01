from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from PyQt5.Qt import QMainWindow, QUrl, QFileDialog,\
    QPalette, QIcon, QStackedWidget, QStatusBar, \
    QAction, QMenuBar, QActionGroup, QDir
from menu import StartMenu, MainMenu
from play_widget import PlayWidget
from save_load import save, load

    

    
class MainWindow(QMainWindow):
    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.app = app
        print('window created')
        self.setWindowIcon(QIcon('img/icon.png'))
        self.setWindowTitle('Kasino')
        self.setPalette(QPalette(Qt.darkGreen))
        self.setup_music()
        
        self.statusbar = QStatusBar(self)
        self.statusbar.setStyleSheet('background: white')
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage('Welcome to the Cassino game!')
        
        self.menubar = QMenuBar(self)
        self.optionsMenu = self.menubar.addMenu('Options')
        self.music_toggle = QAction()
        self.music_toggle.setText('Music')
        self.music_toggle.setShortcut('Ctrl+m')
        self.music_toggle.setCheckable(True)
        self.music_toggle.setChecked(True)
        self.optionsMenu.addAction(self.music_toggle)
        self.music_toggle.triggered.connect(self.toggle_music)
        
        self.speedGroup = QActionGroup(self)
        self.speedGroup.triggered.connect(self.set_speed)
        
        self.slow_speed = QAction('Slow', self.speedGroup)
        self.slow_speed.setCheckable(True)
        self.normal_speed = QAction('Normal', self.speedGroup)
        self.normal_speed.setCheckable(True)
        self.fast_speed = QAction('Fast', self.speedGroup)
        self.fast_speed.setCheckable(True)
        self.vfast_speed = QAction('Very Fast', self.speedGroup)
        self.vfast_speed.setCheckable(True)
        self.normal_speed.setChecked(True)
        
        self.speed_menu = self.optionsMenu.addMenu('Speed')
        self.speed_menu.addActions(self.speedGroup.actions())
        self.menubar.setMouseTracking(False)
        self.setMenuBar(self.menubar)
        
        self.play_widget = PlayWidget(self)
        self.main_menu = MainMenu(self)
        self.start_menu = StartMenu(self)
        self.widgets = QStackedWidget(self)
        self.widgets.addWidget(self.play_widget)
        self.widgets.addWidget(self.main_menu)
        self.widgets.addWidget(self.start_menu)
        self.widgets.setCurrentWidget(self.main_menu)
        
        self.setCentralWidget(self.widgets)
        self.setGeometry(25, 50, 1028, 720)
        
        self.main_menu.startbutton.clicked.connect(self.init_game)
        self.main_menu.loadbutton.clicked.connect(self.load_game)
        self.main_menu.quitbutton.clicked.connect(self.quit)
        self.play_widget.quit_button.clicked.connect(self.quit_to_menu)
        self.play_widget.save_button.clicked.connect(self.save_game)
        self.start_menu.startbutton.clicked.connect(self.start_game)
        
        
    def setup_music(self):
        self.music = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        file_name = "sound/bg.mp3"
        self.media = QMediaContent(QUrl.fromLocalFile(file_name))
        self.playlist.addMedia(self.media)
        self.music.setPlaylist(self.playlist)
        self.music.setVolume(20)
        self.music.play()
    
    def toggle_music(self):
        if self.music.isMuted():
            self.music.setMuted(False)
            self.statusbar.showMessage('Music on', 5000)
        else:
            self.music.setMuted(True)
            self.statusbar.showMessage('Music off', 5000)
            
            
    def set_speed(self, action):
        if action == self.slow_speed:
            self.play_widget.speed = 1
        elif action == self.normal_speed:
            self.play_widget.speed = 3
        elif action == self.fast_speed:
            self.play_widget.speed = 4
        else:
            self.play_widget.speed = 6
    
    def start_game(self):
        self.play_widget.init_game(self.start_menu.extract_info_and_init_game())
        self.widgets.setCurrentWidget(self.play_widget)
        self.statusbar.showMessage('Game launched', 2000)
        
    def load_game(self):
        path = QFileDialog.getOpenFileName(self, 'Open save file', QDir.currentPath() + '/sav')[0]
        if path != '':
            game, msg, count = load(path)
            self.play_widget.resume_from_save(game, msg, count)
            self.widgets.setCurrentWidget(self.play_widget)
            self.statusbar.showMessage('Loaded save file', 5000)
        
        
    def save_game(self):
        path = QFileDialog.getSaveFileName(self, 'Create save file', QDir.currentPath()+'/sav')[0]
        if path != '':
            save(path, self.play_widget.game, self.play_widget.export_log(), self.play_widget.move_count)
            self.statusbar.showMessage('Game saved', 5000)    
        
    def init_game(self):
        self.widgets.setCurrentWidget(self.start_menu)
        self.statusbar.showMessage('Starting new game')
        
    def quit_to_menu(self):
        #Reset playwidget
        self.widgets.removeWidget(self.play_widget)
        speed = self.play_widget.speed
        self.play_widget.setParent(None)
        self.play_widget = PlayWidget(self)
        self.play_widget.speed = speed
        self.widgets.addWidget(self.play_widget)
        self.play_widget.quit_button.clicked.connect(self.quit_to_menu)
        self.play_widget.save_button.clicked.connect(self.save_game)
        
        self.widgets.setCurrentWidget(self.main_menu)
        
    def closeEvent(self, *args, **kwargs): #for handling closing from 'x' button
        self.quit()
    
    def quit(self):
        print('Exited game. Thanks for playing!\n')
        self.app.exit()