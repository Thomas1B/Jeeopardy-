from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, uic
from .game_window import GameWindow


class MenuWindow(QMainWindow):
    '''
    Class to handle the main window
    '''

    def __init__(self, questions: list, category_names: list):
        super(MenuWindow, self).__init__()
        uic.loadUi("UI_Files/jeopardy_menu_window.ui", self)

        self.category_names = category_names
        self.all_questions = questions

        # Variables to keep track of states
        self.team_count = 2

        ''' Defining widgets '''
        self.title = self.findChild(
            QtWidgets.QLabel, 'title'
        )
        self.spinBox_num_teams = self.findChild(
            QtWidgets.QSpinBox, 'how_many_teams_spinBox'
        )
        self.team_name_frame = self.findChild(
            QtWidgets.QFrame, 'team_name_frame'
        )
        self.layout_team_frame = QtWidgets.QVBoxLayout(self.team_name_frame)
        self.team_name_frame.setLayout(self.layout_team_frame)
        self.btn_play = self.findChild(
            QtWidgets.QPushButton, 'btn_play'
        )

        ''' Connecting Widgets to functions '''
        self.spinBox_num_teams.valueChanged.connect(
            self.show_lineEdits
        )
        self.btn_play.clicked.connect(self.open_game_window)

        ''' Styling '''
        self.title.setStyleSheet(
            '''
            QLabel {
                font-size: 40px;
                padding: 15px;
            }
            '''
        )
        self.spinBox_num_teams.setStyleSheet(
            '''
            QSpinBox {
                background-color: white;
                max-width: 100px;
            }
            '''
        )
        self.team_name_frame.setStyleSheet(
            '''
            QLineEdit {
                background-color: white;
                padding: 5px;
                font-size: 16px;
            }
            '''
        )
        self.btn_play.setStyleSheet(
            '''
            QPushButton:focus {
                border: 1px solid blue;
            }
            QPushButton:hover {
                border: 1px solid blue;
            }
            '''
        )

        for num in range(self.team_count):
            lineEdit = QtWidgets.QLineEdit(self)
            lineEdit.setPlaceholderText("Team Name...")
            self.layout_team_frame.addWidget(
                lineEdit
            )

        # adjusting tab order
        self.setTabOrder(self.spinBox_num_teams, self.team_name_frame)
        self.setTabOrder(self.team_name_frame, self.btn_play)
        self.setTabOrder(self.btn_play, self.spinBox_num_teams)
        self.show()

    def show_lineEdits(self) -> None:
        '''
        Function to show N number of line edits.
            Triggered by spinBox itemChanged.
        '''

        lineEdit = QtWidgets.QLineEdit()
        lineEdit.setPlaceholderText("Team Name...")

        previous = self.team_count
        current = self.spinBox_num_teams.value()

        if current > previous:
            self.layout_team_frame.addWidget(lineEdit)
        else:
            last = self.layout_team_frame.itemAt(
                self.layout_team_frame.count() - 1).widget()
            last.deleteLater()

        self.team_count = current

    def get_team_names(self):
        '''
        Function to get team names from the lineEdits.
        '''
        team_names = []
        for lineEdit in self.team_name_frame.findChildren(QtWidgets.QLineEdit):
            team_names.append(lineEdit.text())

        if any(name == '' for name in team_names):
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Jeopardy! - Blank Team Names")
            pixmapi = getattr(QtWidgets.QStyle, "SP_MessageBoxWarning")
            icon = self.style().standardIcon(pixmapi)
            msg.setWindowIcon(icon)
            msg.setText("\nAll Team entries must be filled!\n")
            msg.setStandardButtons(
                QtWidgets.QMessageBox.Ok
            )
            msg.exec_()
        else:
            return team_names

    def open_game_window(self):
        '''
        Function to open the game window
        '''
        team_names = self.get_team_names()
        if team_names:
            self.btn_play.setEnabled(False)
            self.game_window = GameWindow(
                parent=self,
                team_names=team_names,
                category_names=self.category_names,
                questions=self.all_questions,
            )
