from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5 import QtWidgets, uic


class Question():
    '''
    Class to store question and answer.
    '''

    def __init__(self, question='', answer='', points=0):
        self.question = question
        self.answer = answer
        self.points = points
        self.opened = False  # if question has been opened.

    def set_question(self, question: str) -> None:
        '''
        Function to set the question.

            Parameter:
                question: question to ask
        '''
        self.question = question

    def set_answer(self, answer: str) -> None:
        '''
        Function to set the answer.

            Parameter: answer
        '''
        self.answer = answer

    def set_points(self, points: float) -> None:
        '''
        Function to set the points

            Parameter:
                points: how points.
        '''
        self.points = points

    def get_question(self) -> str:
        '''
        Function to get the question.

            Parameters: None

            Returns:
                question in a string.
        '''
        return self.question

    def get_answer(self) -> str:
        '''
        Function to get the answer.

            Parameters: None

            Returns:
                answer in a string.
        '''
        return self.answer

    def get_points(self) -> float:
        '''
        Function to get the amount of points the question is worth.

            Parameter:
                None

            Return:
                float
        '''
        return self.points


class Team():
    '''
    Team Class
    '''

    def __init__(self, name: str, points=0):
        self.name = name  # team name
        self.points = points  # points

    def get_name(self) -> str:
        '''
        Function to get team name.
        '''
        return self.name

    def get_points(self) -> float:
        '''
        Function to get points.
        '''
        return self.points

    def set_point(self, points: float) -> None:
        '''
        Function to set points.

            Parameter:
                points: how many points to set
        '''
        self.points = points

    def add_points(self, points: float) -> None:
        '''
        Function to add points.

            Parameter:
                points: how many points to add.
        '''
        self.points = self.points + points

    def remove_points(self, points: float) -> None:
        '''
        Function to remove points.

            Parameter:
                points: how many points to remove.
        '''
        self.points = self.points - points


class QuestionWindow(QMainWindow):
    '''
    Class to handle questions
    '''

    def __init__(self, questionObj=None, parent=None, clicked_btn=None):
        super(QuestionWindow, self).__init__(parent=parent)
        uic.loadUi('UI_Files/question_window.ui', self)
        self.resize(1500, 900)
        self.move(200, 50)

        # button that was clicked
        self.clicked_btn = clicked_btn

        # questionObj parameters
        self.questionObj = questionObj
        self.question = questionObj.get_question()
        self.answer = questionObj.get_answer()
        self.points = questionObj.get_points()

        # Finding Widgets
        self.header = self.findChild(
            QtWidgets.QLabel, 'header'
        )
        self.btn_question = self.findChild(
            QtWidgets.QPushButton
        )
        self.answer_label = self.findChild(
            QtWidgets.QLabel, 'answer_label'
        )

        # Attaching Functions and setting text
        self.btn_question.clicked.connect(self.show_answer)
        header_text = 'For {:.0f} Points'.format(self.points)
        self.header.setText(header_text)
        self.btn_question.setText(self.question)

        # Styling
        self.header.setStyleSheet(
            '''
            QLabel {
                color: rgb(255, 170, 0);
                font-size: 75px;
            }
            '''
        )
        self.btn_question.setStyleSheet(
            '''
            QPushButton {
                background-color: rgb(25, 25, 255);
                color: white;
                border: 2px solid black;
                font-size: 50px;
                margin: 20px 0px 20px 10px;
                padding: 15px;
            }

            QPushButton:hover {
                background-color: rgb(50, 50, 255);
            }
            '''
        )
        self.answer_label.setStyleSheet(
            '''
            QLabel {
                background-color: rgb(25, 25, 255);
                color: white;
                border: 2px solid black;
                font-size: 50px;
                padding: 20px;
                min-height: 200px;
            }
            '''
        )
        self.answer_label.hide()

        # Creating Widgets for add points to Team's
        # self.team_frame = self.findChild(
        #     QtWidgets.QFrame, 'team_frame'
        # )
        # self.layout_team_frame = QtWidgets.QVBoxLayout(self.team_frame)
        # frame = QtWidgets.QFrame()
        # layout = QtWidgets.QHBoxLayout(frame)
        # for team in parent.teams:
        #     team_name = parent.teams[team].name
        #     points = str(parent.teams[team].points)

        #     sub_frame = QtWidgets.QFrame()
        #     sub_layout = QtWidgets.QVBoxLayout(sub_frame)
        #     name_label = QtWidgets.QLabel(text=team_name)
        #     points_label = QtWidgets.QLabel(text=points)

        #     sub_layout.addWidget(name_label)
        #     sub_layout.addWidget(points_label)

        #     layout.addWidget(sub_frame)

        # self.layout_team_frame.addWidget(frame)

        if self.questionObj.opened:
            self.show_answer()

    def closeEvent(self, event) -> None:
        event.accept()

    def show_answer(self) -> None:
        '''
        Function to show the answer, when the button is clicked
        '''
        self.questionObj.opened = True
        self.btn_question.setEnabled(False)
        self.btn_question.setStyleSheet(
            '''
            QPushButton {
                background-color: rgb(50, 50, 255);
                color: white;
                font-size: 50px;
                margin: 20px 0px 20px 10px;
                padding: 15px;

            }
            '''
        )

        text = f'Answer:\n\n{self.answer}\n'
        self.answer_label.setText(text)
        self.answer_label.show()
        self.clicked_btn.setStyleSheet(
            '''
            QPushButton {
                color: rgb(255, 170, 0);
                background-color: rgb(50, 50, 255);
                text-decoration: line-through;
                font-size: 40px;

            }
            '''
        )


class GameWindow(QMainWindow):
    '''
    Class to handle the game window
    '''

    def __init__(self, team_names: list, category_names: list, questions: list, parent=None):
        super(GameWindow, self).__init__(parent=parent)
        uic.loadUi('UI_Files/game_window.ui', self)
        # self.showMaximized()

        # variables to store and keep track of things
        self.category_names = category_names
        self.all_questions = questions
        self.team_names = team_names
        self.teams = self.make_teams()
        self.question_window = None
        self.in_edit_mode = False

        # page title
        self.title = self.findChild(
            QtWidgets.QLabel, 'title'
        )
        self.title.hide()

        # Main Frame
        self.main_frame = self.findChild(QtWidgets.QFrame, 'main_frame')

        # Menu Actions
        self.edit_mode_action = self.findChild(
            QtWidgets.QAction, 'actionEdit_Mode'
        )

        # Column (Category) Headers
        self.category_header_1 = self.findChild(
            QtWidgets.QPushButton, 'category_header_1'
        )
        self.category_header_2 = self.findChild(
            QtWidgets.QPushButton, 'category_header_2'
        )
        self.category_header_3 = self.findChild(
            QtWidgets.QPushButton, 'category_header_3'
        )
        self.category_header_4 = self.findChild(
            QtWidgets.QPushButton, 'category_header_4'
        )
        self.category_header_5 = self.findChild(
            QtWidgets.QPushButton, 'category_header_5'
        )
        self.category_header_6 = self.findChild(
            QtWidgets.QPushButton, 'category_header_6'
        )
        self.category_headers = [
            self.category_header_1, self.category_header_2, self.category_header_3, self.category_header_4, self.category_header_5, self.category_header_6
        ]

        # Attaching functions
        self.edit_mode_action.triggered.connect(
            self.edit_mode
        )

        # styling
        self.title.setStyleSheet(
            '''
            QLabel {
                color: red;
                font-size: 40px;
            }
            '''
        )

        # setting buttons and headers
        self.set_up_buttons()
        self.set_category_names(category_names)
        self.show()

        self.team_window = TeamWindow(parent=self)
        self.team_window.show()

    def closeEvent(self, event) -> None:
        '''
        Function to handle close event.
        '''
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("Exiting Jeopardy!")
        msg.setText("Are you sure you want to quit?")
        msg.setStandardButtons(
            QtWidgets.QMessageBox.Yes |
            QtWidgets.QMessageBox.Cancel
        )
        msg.setDefaultButton(QtWidgets.QMessageBox.Yes)
        user = msg.exec_()
        if user == QtWidgets.QMessageBox.Yes:
            if self.parent().isVisible():
                self.parent().close()
            event.accept()
            if self.team_window.isVisible():
                self.team_window.close()
            event.accept()
        else:
            event.ignore()

    def toggle_header_btns(self, enabled=False):
        '''
        Function to toggle the header buttons

            Parameters:
                enabled: True -  button is activated.
        '''
        for cat in self.category_headers:
            cat.setEnabled(enabled)

    def set_category_names(self, names: list) -> None:
        '''
        Function set the  column (category) label text

            Parameters:
                names: list of names for each column (category).
        '''
        self.toggle_header_btns()
        for index, name in enumerate(names):
            self.category_headers[index].setText(name)

        for cat in self.category_headers:
            cat.setStyleSheet(
                '''
                QPushButton {
                    color: white;
                    font-size: 45px;
                    background-color: rgb(50, 50, 255);
                    padding: 5px;
                }
                '''
            )

    def set_up_buttons(self):
        '''
        Function to set up buttons and add styles.
        '''

        for btn in self.findChildren(QtWidgets.QPushButton):
            if btn not in self.category_headers:
                btn.setStyleSheet(
                    '''
                QPushButton {
                    background-color: rgb(50, 50, 255);
                    color: rgb(255, 170, 0);
                    font: Arial Bold;
                    font-size: 40px;
                }

                QPushButton:hover {
                    background-color: rgb(100, 100, 255);
                }

                '''
                )

        self.findChild(QtWidgets.QPushButton, 'question_1').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[0][0])
        )
        self.findChild(QtWidgets.QPushButton, 'question_2').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[0][1])
        )
        self.findChild(QtWidgets.QPushButton, 'question_3').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[0][2])
        )
        self.findChild(QtWidgets.QPushButton, 'question_4').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[0][3])
        )
        self.findChild(QtWidgets.QPushButton, 'question_5').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[0][4])
        )
        self.findChild(QtWidgets.QPushButton, 'question_6').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[0][5])
        )

        self.findChild(QtWidgets.QPushButton, 'question_7').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[1][0])
        )
        self.findChild(QtWidgets.QPushButton, 'question_8').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[1][1])
        )
        self.findChild(QtWidgets.QPushButton, 'question_9').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[1][2])
        )
        self.findChild(QtWidgets.QPushButton, 'question_10').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[1][3])
        )
        self.findChild(QtWidgets.QPushButton, 'question_11').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[1][4])
        )
        self.findChild(QtWidgets.QPushButton, 'question_12').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[1][5])
        )

        self.findChild(QtWidgets.QPushButton, 'question_13').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[2][0])
        )
        self.findChild(QtWidgets.QPushButton, 'question_14').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[2][1])
        )
        self.findChild(QtWidgets.QPushButton, 'question_15').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[2][2])
        )
        self.findChild(QtWidgets.QPushButton, 'question_16').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[2][3])
        )
        self.findChild(QtWidgets.QPushButton, 'question_17').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[2][4])
        )
        self.findChild(QtWidgets.QPushButton, 'question_18').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[2][5])
        )

        self.findChild(QtWidgets.QPushButton, 'question_19').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[3][0])
        )
        self.findChild(QtWidgets.QPushButton, 'question_20').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[3][1])
        )
        self.findChild(QtWidgets.QPushButton, 'question_21').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[3][2])
        )
        self.findChild(QtWidgets.QPushButton, 'question_22').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[3][3])
        )
        self.findChild(QtWidgets.QPushButton, 'question_23').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[3][4])
        )
        self.findChild(QtWidgets.QPushButton, 'question_24').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[3][5])
        )

        self.findChild(QtWidgets.QPushButton, 'question_25').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[4][0])
        )
        self.findChild(QtWidgets.QPushButton, 'question_26').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[4][1])
        )
        self.findChild(QtWidgets.QPushButton, 'question_27').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[4][2])
        )
        self.findChild(QtWidgets.QPushButton, 'question_28').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[4][3])
        )
        self.findChild(QtWidgets.QPushButton, 'question_29').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[4][4])
        )
        self.findChild(QtWidgets.QPushButton, 'question_30').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[4][5])
        )

        self.findChild(QtWidgets.QPushButton, 'question_31').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[5][0])
        )
        self.findChild(QtWidgets.QPushButton, 'question_32').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[5][1])
        )
        self.findChild(QtWidgets.QPushButton, 'question_33').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[5][2])
        )
        self.findChild(QtWidgets.QPushButton, 'question_34').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[5][3])
        )
        self.findChild(QtWidgets.QPushButton, 'question_35').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[5][4])
        )
        self.findChild(QtWidgets.QPushButton, 'question_36').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[5][5])
        )

    def make_teams(self):
        '''
        Function to make the teams
        '''
        teams = {}
        for name in self.team_names:
            teams[name] = Team(name)
        return teams

    def open_question_window(self, questionObj: Question):
        '''
        Function to open the question window
        '''
        btn = self.sender()
        btn_name = btn.objectName()
        clicked_btn = self.findChild(QtWidgets.QPushButton, btn_name)

        self.question_window = QuestionWindow(
            parent=self, questionObj=questionObj, clicked_btn=clicked_btn)
        self.question_window.show()

    def edit_mode(self):
        '''
        Function to put the program in edit mode.
        '''

        btns = [btn for btn in self.main_frame.findChildren(
            QtWidgets.QPushButton) if btn not in self.category_headers]
        if not self.in_edit_mode:
            self.in_edit_mode = True
            self.title.show()
            self.toggle_header_btns(enabled=True)
            for btn in btns:
                btn.disconnect()

            # attaching new edit functions
            self.category_header_1 = self.findChild(
                QtWidgets.QPushButton, 'category_header_1'
            ).clicked.connect(lambda: self.open_edit_window(self.category_headers[0]))
            self.category_header_2 = self.findChild(
                QtWidgets.QPushButton, 'category_header_2'
            ).clicked.connect(lambda: self.open_edit_window(self.category_headers[1]))
            self.category_header_3 = self.findChild(
                QtWidgets.QPushButton, 'category_header_3'
            ).clicked.connect(lambda: self.open_edit_window(self.category_headers[2]))
            self.category_header_4 = self.findChild(
                QtWidgets.QPushButton, 'category_header_4'
            ).clicked.connect(lambda: self.open_edit_window(self.category_headers[3]))
            self.category_header_5 = self.findChild(
                QtWidgets.QPushButton, 'category_header_5'
            ).clicked.connect(lambda: self.open_edit_window(self.category_headers[4]))
            self.category_header_6 = self.findChild(
                QtWidgets.QPushButton, 'category_header_6'
            ).clicked.connect(lambda: self.open_edit_window(self.category_headers[5]))
            self.findChild(QtWidgets.QPushButton, 'question_1').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[0][0])
            )
            self.findChild(QtWidgets.QPushButton, 'question_2').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[0][1])
            )
            self.findChild(QtWidgets.QPushButton, 'question_3').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[0][2])
            )
            self.findChild(QtWidgets.QPushButton, 'question_4').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[0][3])
            )
            self.findChild(QtWidgets.QPushButton, 'question_5').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[0][4])
            )
            self.findChild(QtWidgets.QPushButton, 'question_6').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[0][5])
            )

            self.findChild(QtWidgets.QPushButton, 'question_7').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[1][0])
            )
            self.findChild(QtWidgets.QPushButton, 'question_8').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[1][1])
            )
            self.findChild(QtWidgets.QPushButton, 'question_9').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[1][2])
            )
            self.findChild(QtWidgets.QPushButton, 'question_10').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[1][3])
            )
            self.findChild(QtWidgets.QPushButton, 'question_11').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[1][4])
            )
            self.findChild(QtWidgets.QPushButton, 'question_12').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[1][5])
            )

            self.findChild(QtWidgets.QPushButton, 'question_13').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[2][0])
            )
            self.findChild(QtWidgets.QPushButton, 'question_14').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[2][1])
            )
            self.findChild(QtWidgets.QPushButton, 'question_15').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[2][2])
            )
            self.findChild(QtWidgets.QPushButton, 'question_16').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[2][3])
            )
            self.findChild(QtWidgets.QPushButton, 'question_17').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[2][4])
            )
            self.findChild(QtWidgets.QPushButton, 'question_18').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[2][5])
            )

            self.findChild(QtWidgets.QPushButton, 'question_19').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[3][0])
            )
            self.findChild(QtWidgets.QPushButton, 'question_20').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[3][1])
            )
            self.findChild(QtWidgets.QPushButton, 'question_21').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[3][2])
            )
            self.findChild(QtWidgets.QPushButton, 'question_22').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[3][3])
            )
            self.findChild(QtWidgets.QPushButton, 'question_23').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[3][4])
            )
            self.findChild(QtWidgets.QPushButton, 'question_24').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[3][5])
            )

            self.findChild(QtWidgets.QPushButton, 'question_25').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[4][0])
            )
            self.findChild(QtWidgets.QPushButton, 'question_26').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[4][1])
            )
            self.findChild(QtWidgets.QPushButton, 'question_27').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[4][2])
            )
            self.findChild(QtWidgets.QPushButton, 'question_28').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[4][3])
            )
            self.findChild(QtWidgets.QPushButton, 'question_29').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[4][4])
            )
            self.findChild(QtWidgets.QPushButton, 'question_30').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[4][5])
            )

            self.findChild(QtWidgets.QPushButton, 'question_31').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[5][0])
            )
            self.findChild(QtWidgets.QPushButton, 'question_32').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[5][1])
            )
            self.findChild(QtWidgets.QPushButton, 'question_33').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[5][2])
            )
            self.findChild(QtWidgets.QPushButton, 'question_34').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[5][3])
            )
            self.findChild(QtWidgets.QPushButton, 'question_35').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[5][4])
            )
            self.findChild(QtWidgets.QPushButton, 'question_36').clicked.connect(
                lambda: self.open_edit_window(
                    self.all_questions[5][5])
            )

        else:
            self.title.hide()
            self.in_edit_mode = False
            for btn in btns:
                btn.disconnect()
            self.toggle_header_btns(enabled=False)
            self.set_up_buttons()

    def open_edit_window(self, questionObj: Question):
        '''
        Function to open the edit window
        '''
        # self.edit_window = EditQuestion(
        #     questionObj=questionObj, parent=self)
        # self.edit_window.show()
        self.edit_window = EditWindow(object_to_edit=questionObj, parent=self)
        self.edit_window.show()


class EditWindow(QtWidgets.QDialog):
    '''
    Pop up window to let user edit questions and column headers.
    '''

    def __init__(self, object_to_edit, parent=None):
        super(EditWindow, self).__init__(parent)
        self.setWindowTitle('Editting')

        self.passed_obj = object_to_edit  # passed object

        # Creating layout
        layout = QtWidgets.QVBoxLayout()
        self.header = QtWidgets.QLabel()
        self.line_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.header)
        layout.addWidget(self.line_edit)

        # if passed object is a Question
        if type(object_to_edit) == Question:
            # adding header text and creating plaintext edit for answer
            self.header.setText(f"For {self.passed_obj.get_points()} Points")
            self.plainEdit = QtWidgets.QPlainTextEdit()
            layout.addWidget(self.plainEdit)

            # adding placeholder text
            if len(self.passed_obj.get_question()) == 0:
                self.line_edit.setPlaceholderText("Question")
            if len(self.passed_obj.get_answer()) == 0:
                self.plainEdit.setPlaceholderText("Answer")

            # passing what is currently display in the Question.
            self.line_edit.setText(self.passed_obj.get_question())
            self.plainEdit.setPlainText(self.passed_obj.get_answer())
            self.plainEdit.setTabChangesFocus(True)
        else:
            # changing header text
            self.header.setText("Editing Column Header")
            # setting text for lineEdit
            self.line_edit.setText(self.passed_obj.text())
            if len(self.passed_obj.text()) == 0:
                self.line_edit.setPlaceholderText("Category")

        # Adding command buttons to pop up.
        ok_btn = QtWidgets.QPushButton('OK')
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(self.submit)
        cancel_btn = QtWidgets.QPushButton('Cancel')
        cancel_btn.clicked.connect(lambda: self.close())
        layout.addWidget(ok_btn)
        layout.addWidget(cancel_btn)

        # setting layout and styles
        self.setLayout(layout)
        self.setStyleSheet(
            '''
            QLabel { 
                font-size: 20px;
            }
            QLineEdit { 
                font-size: 12px;
            }
            QPlainTextEdit { 
                font-size: 12px;
            }
            '''
        )

    def submit(self):
        '''
        Function to update entries
        '''

        if type(self.passed_obj) == Question:
            self.passed_obj.set_question(self.line_edit.text())
            self.passed_obj.set_answer(self.plainEdit.toPlainText())
        else:
            self.passed_obj.setText(self.line_edit.text())

        self.close()


class TeamWindow(QMainWindow):
    '''
    Class to run the team window for add points
    '''

    def __init__(self, parent=None):
        super(TeamWindow, self).__init__(parent=parent)
        uic.loadUi('UI_Files/team_window.ui', self)
        self.resize(800, 500)

        self.team_frame_1 = self.findChild(
            QtWidgets.QFrame, "team_frame_1"
        )
        self.team_frame_2 = self.findChild(
            QtWidgets.QFrame, "team_frame_2"
        )
        self.team_frame_3 = self.findChild(
            QtWidgets.QFrame, "team_frame_3"
        )
        self.team_frame_4 = self.findChild(
            QtWidgets.QFrame, "team_frame_4"
        )
        self.team_frame_5 = self.findChild(
            QtWidgets.QFrame, "team_frame_5"
        )
        self.team_frame_6 = self.findChild(
            QtWidgets.QFrame, "team_frame_6"
        )
        self.team_frame_7 = self.findChild(
            QtWidgets.QFrame, "team_frame_7"
        )
        self.team_frame_8 = self.findChild(
            QtWidgets.QFrame, "team_frame_8"
        )
        self.team_frame_9 = self.findChild(
            QtWidgets.QFrame, "team_frame_9"
        )
        self.team_frame_10 = self.findChild(
            QtWidgets.QFrame, "team_frame_10"
        )
        self.team_frames = [self.team_frame_1, self.team_frame_2, self.team_frame_3,
                            self.team_frame_4, self.team_frame_5, self.team_frame_6, self.team_frame_7, self.team_frame_8, self.team_frame_9, self.team_frame_10]
        self.hide_frames(self.team_frames)

        self.frames_to_show = []
        for index, team_name in enumerate(parent.teams.keys()):
            self.frames_to_show.append(self.team_frames[index])

        self.show_frames(self.frames_to_show)
        self.set_team_names()

        # styling
        for frame in self.team_frames:
            frame.setStyleSheet(
                '''
                QFrame {
                    border: 1px solid;
                    background-color: white;
                }

                QLabel {
                    border: none;
                    padding: 5px;
                    font-size: 40px;
                    font-style: Times;
                }

                QSpinBox {
                    background-color: white;
                    padding: 5px;
                    font-size: 30px;
                }
                '''
            )
        self.setStyleSheet(
            '''
            background-color: rgb(100, 100, 250);
            '''
        )

        # showing window
        self.show()

    def closeEvent(self, event) -> None:
        '''
        Function to handle close event.
        '''
        user = self.parent().close()
        if user:
            event.accept()
        else:
            event.ignore()

    def hide_frames(self, frames: list):
        '''
        Function to hide team sub frames.

            Parameters:
                frames: list of frames to hide.
        '''
        for frame in frames:
            frame.hide()

    def show_frames(self, frames: list):
        '''
        Function to show team sub frames.

            Parameters:
                frames: list of frames to show.
        '''
        for frame in frames:
            frame.show()

    def set_team_names(self):
        '''
        Function to set labels with set names
        '''
        for frame, name, in zip(self.frames_to_show, self.parent().team_names):
            frame.findChildren(QtWidgets.QLabel)[0].setText(name)
            points = self.parent().teams[name].get_points()
            frame.findChildren(QtWidgets.QSpinBox)[0].setValue(points)