'''
Platform for playing the game
'''
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.Qt import QSizePolicy, QHBoxLayout, QWidget, QUrl, QVBoxLayout,\
    QPalette, QSpacerItem, QPlainTextEdit, QPixmap, QTimer, QLabel
from button import Button
from player import AIPlayer
from card_view import CardView, HandCardView
       
class PlayWidget(QWidget):
    def __init__(self, parent):
        super(PlayWidget, self).__init__(parent)
        self.setAutoFillBackground(True)
        self.hlayout = QHBoxLayout(self)
        
        
        
        self.table_view = CardView(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_view.sizePolicy().hasHeightForWidth())
        self.table_view.setSizePolicy(sizePolicy)
        self.table_view.setMinimumHeight(200)
        self.table_view.setBackgroundBrush(Qt.darkGreen)
        self.table_view.setGeometry(0,0,1028,200)
        
        self.hand_view = HandCardView(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hand_view.sizePolicy().hasHeightForWidth())
        self.hand_view.setSizePolicy(sizePolicy)
        self.hand_view.setMinimumHeight(200)
        self.hand_view.setBackgroundBrush(Qt.darkGreen)
        self.hand_view.setGeometry(0,0,1028,200)
        
        self.show_button = Button(self, 'Show Hand')
        self.show_button.setText("Show hand")
        self.show_button.clicked.connect(self.hand_view.show_cards)
        self.show_button.hide()
        
        self.move_button = Button(self, 'Make Move')
        self.move_button.setMinimumSize(300, 100)
        self.move_button.clicked.connect(self.attempt_move)
        self.move_button.hide()
        
        self.start_button = Button(self, 'Start Round')
        self.start_button.setMinimumHeight(100)
        self.start_button.clicked.connect(self.start_round)
        
        
        self.next_button = Button(self, 'Continue')
        self.next_button.setMinimumHeight(100)
        self.next_button.clicked.connect(self.goto_next_round)
        self.next_button.hide()
        
        self.quit_button = Button(self, 'Quit to menu')
        
        self.save_button = Button(self, 'Save')
        
        self.show_button.setMaximumWidth(150)
        self.move_button.setMaximumWidth(150)
        self.quit_button.setMaximumWidth(150)
        
        self.btnlayout = QHBoxLayout()
        self.btnlayout.addWidget(self.start_button)
        
        self.btn2layout = QHBoxLayout()
        self.btn2layout.addWidget(self.save_button)
        self.btn2layout.addWidget(self.quit_button)
        
        self.playlayout = QVBoxLayout()
        self.playlayout.addWidget(self.table_view)
        self.playlayout.addLayout(self.btnlayout)
        self.playlayout.addWidget(self.hand_view)
        self.playlayout.addLayout(self.btn2layout)
        self.hlayout.addLayout(self.playlayout)
        
        self.sidelayout = QVBoxLayout()
        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setPalette(QPalette(Qt.white))
        self.log.setMaximumWidth(300)
        self.log.setMaximumHeight(200)
        self.sidelayout.addWidget(self.log)
        
        self.playerinfolayout = QVBoxLayout()
        self.sidelayout.addLayout(self.playerinfolayout)
        
        self.sidelayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        
        self.hlayout.addLayout(self.sidelayout)
        
        self.setup_sound()
        
        self.move_count = 0
        self.speed = 3
        self.game = None    
        
    
    def init_game(self, game):
        self.game = game
        self.game.logSignal.connect(self.update_log)
        self.game.sweepSignal.connect(self.sweep_sound.play)
        
        self.game.new_round()
        self.shuffle_sound.play()
        self.game.initial_deal()

        self.move_count = 0
        
        for player in self.game.players:
            self.playerinfolayout.addWidget(PlayerInfo(self, player))
    
    def start_round(self):
        self.btnlayout.removeWidget(self.start_button)
        self.btnlayout.insertWidget(0, self.show_button)
        self.btnlayout.insertWidget(1, self.move_button)
        self.start_button.hide()
        self.show_button.show()
        self.move_button.show()
        
        self.table_view.update_scene(self.game.table)
        self.hand_view.update_scene(self.game.current_player.hand)
            
        self.hand_view.hide_cards()
        
        if type(self.game.current_player) is not AIPlayer and self.game.one_human:
            self.hand_view.show_cards()
            
        self.playerinfolayout.itemAt(self.game.players.index(self.game.current_player)).widget().set_active()
        self.update_log('\n----------\n{}\'s turn\n'.format(self.game.current_player))
            
        if type(self.game.current_player) is AIPlayer:
            self.move_button.setDisabled(True)
            self.show_button.setDisabled(True)
            self.save_button.setDisabled(True)
            self.make_ai_move()
    
    
    def resume_from_save(self, game, logmsg, movecount):
        self.game = game
        self.game.logSignal.connect(self.update_log)
        self.game.sweepSignal.connect(self.sweep_sound.play)
        
        self.log.insertPlainText(logmsg)
        self.log.insertPlainText('\n----------------\n    Resuming from save\n----------------\n\n')
        
        self.move_count = movecount
        
        for player in self.game.players:
            self.playerinfolayout.addWidget(PlayerInfo(self, player))
        
        self.playerinfolayout.itemAt(self.game.players.index(self.game.current_player)).widget().set_active()
        
    def make_ai_move(self):
        self.game.select_move_for_ai()
        QTimer.singleShot(1500//self.speed, self.show_ai_move)
        
    def show_ai_move(self):
        self.hand_view.auto_select()
        self.table_view.auto_select()
        self.card_sound.play()
        self.game.do_action()
        QTimer.singleShot(3000//self.speed, self.after_ai_move_done)
    
    def after_ai_move_done(self):
        self.move_sound.play()
        self.playerinfolayout.itemAt(self.game.players.index(self.game.current_player)).widget().update_info()
        self.game.deal()
        self.table_view.update_scene(self.game.table)
        self.hand_view.update_scene(self.game.current_player.hand)
        self.hand_view.hide_cards()
        QTimer.singleShot(3000//self.speed, self.end_turn)
        
                
    def attempt_move(self):
        if self.game.do_action():
            self.move_sound.play()
            self.playerinfolayout.itemAt(self.game.players.index(self.game.current_player)).widget().update_info()
            self.move_button.setDisabled(True)
            self.table_view.update_scene(self.game.table)
            self.hand_view.update_scene(self.game.current_player.hand)
            QTimer.singleShot(1800//self.speed, self.after_move_done)
            
        else:
            self.error_sound.play()
            
    def after_move_done(self):
        self.game.deal()
        self.hand_view.update_scene(self.game.current_player.hand)
        QTimer.singleShot(3000//self.speed, self.end_turn)
            
    def end_turn(self):
        self.playerinfolayout.itemAt(self.game.players.index(self.game.current_player)).widget().set_inactive()
        self.game.next_player()
        self.playerinfolayout.itemAt(self.game.players.index(self.game.current_player)).widget().set_active()
        
        self.move_button.setDisabled(False)
        self.show_button.setDisabled(False)
        self.table_view.deselect_all()
        
        self.move_count += 1
        if self.move_count == 48:
            self.end_round()
            return
        
        self.update_log('\n----------\n{}\'s turn\n'.format(self.game.current_player))
        self.hand_view.update_scene(self.game.current_player.hand)
        self.hand_view.hide_cards()
        
        #if there is only one human player, his/her cards are shown automatically
        if type(self.game.current_player) is not AIPlayer and self.game.one_human:
            self.hand_view.show_cards()
            self.alert_sound.play()
        
        
        if type(self.game.current_player) is AIPlayer:
            self.move_button.setDisabled(True)
            self.show_button.setDisabled(True)
            self.save_button.setDisabled(True)
            self.make_ai_move()
            return
        
        self.save_button.setDisabled(False)
    
    def end_round(self):
        self.save_button.setDisabled(True)
        self.playerinfolayout.itemAt(self.game.players.index(self.game.current_player)).widget().set_inactive()
        self.end_sound.play()
        game_ended = self.game.end_round()
        for i in range(self.playerinfolayout.count()):
            self.playerinfolayout.itemAt(i).widget().update_info()
            self.playerinfolayout.itemAt(i).widget().update_score()
            
        self.table_view.update_scene(self.game.table)
        
        self.btnlayout.removeWidget(self.show_button)
        self.btnlayout.removeWidget(self.move_button)
        self.btnlayout.insertWidget(0, self.next_button)
        self.next_button.show()
        self.show_button.hide()
        self.move_button.hide()
        if game_ended:
            self.next_button.setDisabled(True)
        
        
    def goto_next_round(self):
        self.save_button.setDisabled(False)
        self.btnlayout.removeWidget(self.next_button)
        self.btnlayout.insertWidget(0, self.start_button)
        self.start_button.show()
        self.next_button.hide()
        
        #rotate playerinfo
        mov = self.playerinfolayout.itemAt(0).widget()
        self.playerinfolayout.removeWidget(mov)
        self.playerinfolayout.addWidget(mov)
        
        self.game.new_round()
        self.shuffle_sound.play()
        
        for i in range(self.playerinfolayout.count()):
            self.playerinfolayout.itemAt(i).widget().update_info()
            
        self.game.new_round()
        self.game.initial_deal()

        self.move_count = 0
        
        
    def setup_sound(self):
        self.shuffle_sound = QSoundEffect()
        self.shuffle_sound.setSource(QUrl.fromLocalFile('sound/shuffle.wav'))
        
        self.error_sound = QSoundEffect()
        self.error_sound.setSource(QUrl.fromLocalFile('sound/error.wav'))
        
        self.move_sound = QSoundEffect()
        self.move_sound.setSource(QUrl.fromLocalFile('sound/draw.wav'))
        
        self.card_sound = QSoundEffect()
        self.card_sound.setSource(QUrl.fromLocalFile('sound/playcard.wav'))
        
        self.sweep_sound = QSoundEffect()
        self.sweep_sound.setSource(QUrl.fromLocalFile('sound/sweep.wav'))
        
        self.alert_sound = QSoundEffect()
        self.alert_sound.setSource(QUrl.fromLocalFile('sound/alert.wav'))
        
        self.end_sound = QSoundEffect()
        self.end_sound.setSource(QUrl.fromLocalFile('sound/endturn.wav'))
        
    def reset(self):
        self.game = None    
            
    def update_log(self, msg):
        self.log.insertPlainText(msg)
        self.log.ensureCursorVisible() #auto-scrolls to bottom of log
        
    def export_log(self):
        return self.log.toPlainText()


class PlayerInfo(QWidget):
    
    def __init__(self, parent, player):
        super(PlayerInfo, self).__init__(parent)
        self.setMaximumWidth(300)
        self.player = player
        
        self.mainlayout = QHBoxLayout()
        
        self.active_icon = QLabel()
        self.active_icon.setPixmap(QPixmap('img/arrow.png'))
        self.active_icon.setScaledContents(True)
        self.active_icon.setFixedSize(30,20)
        
        self.type_icon = QLabel()
        if type(player) == AIPlayer:
            self.type_icon.setPixmap(QPixmap('img/robot.png'))
        else:
            self.type_icon.setPixmap(QPixmap('img/human.png'))
        self.type_icon.setScaledContents(True)
        self.type_icon.setFixedSize(20,20)
        self.mainlayout.addWidget(self.type_icon)
        
        self.name_label = QLabel(player.name + ': ')
        self.score_label = QLabel(str(player.score))
        self.mainlayout.addWidget(self.name_label)
        self.mainlayout.addWidget(self.score_label)
        self.mainlayout.addItem(QSpacerItem(40,20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.cards_icon = QLabel()
        self.cards_icon.setPixmap(QPixmap('img/red_back.png'))
        self.cards_icon.setScaledContents(True)
        self.cards_icon.setFixedSize(20,30)
        self.mainlayout.addWidget(self.cards_icon)
        
        self.cards_label = QLabel(str(len(player.deck)))
        self.mainlayout.addWidget(self.cards_label)
        
        self.spades_icon = QLabel()
        self.spades_icon.setPixmap(QPixmap('img/spade2.png'))
        self.spades_icon.setScaledContents(True)
        self.spades_icon.setFixedSize(20,20)
        self.mainlayout.addWidget(self.spades_icon)
        
        self.spades_label = QLabel(str(len(player.deck)))
        self.mainlayout.addWidget(self.spades_label)
        
        self.sweeps_icon = QLabel()
        self.sweeps_icon.setPixmap(QPixmap('img/empty.png'))
        self.sweeps_icon.setScaledContents(True)
        self.sweeps_icon.setFixedSize(20,30)
        self.mainlayout.addWidget(self.sweeps_icon)
        
        self.sweeps_label = QLabel(str(player.sweeps))
        self.mainlayout.addWidget(self.sweeps_label)
        
        self.mainlayout.setContentsMargins(1, 1, 1, 1)
        self.setLayout(self.mainlayout)
        
    def set_active(self):
        self.mainlayout.insertWidget(1, self.active_icon)
        self.active_icon.show()
        
    def set_inactive(self):
        self.mainlayout.removeWidget(self.active_icon)
        self.active_icon.hide()
        
    def update_info(self):
        self.cards_label.setText((str(len(self.player.deck))))
        self.spades_label.setText((str(len([c for c in self.player.deck if c.suit == 'Spades']))))
        self.sweeps_label.setText(str(self.player.sweeps))
        
    def update_score(self):
        self.score_label.setText(str(self.player.score))
                                  
        
