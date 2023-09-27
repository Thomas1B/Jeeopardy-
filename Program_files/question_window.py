from PyQt5.QtWidgets import QMainWindow, QWidget, QSizePolicy
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt


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


class QuestionWindow(QMainWindow):
    '''
    Class to handle questions
    '''

    def __init__(self,  questionObj=None,  parent=None, clicked_btn=None):
        super(QuestionWindow, self).__init__(parent=parent)
        uic.loadUi('UI_Files/question_window.ui', self)
        self.showMaximized()


        # parent window
        self.parent = parent

        # if points have been added to the team.
        self.points_added = False

        # button that was clicked
        self.clicked_btn = clicked_btn

        # questionObj parameters
        self.questionObj = questionObj
        self.question = questionObj.get_question()
        self.answer = questionObj.get_answer()
        self.points = questionObj.get_points()

        self.team_frames = self.findChild(
            QtWidgets.QFrame, 'team_frames'
        )
        self.team_frame1 = self.findChild(
            QtWidgets.QFrame, 'team_frame_1'
        )
        self.team_frame2 = self.findChild(
            QtWidgets.QFrame, 'team_frame_2'
        )
        self.team_frame3 = self.findChild(
            QtWidgets.QFrame, 'team_frame_3'
        )
        self.team_frame4 = self.findChild(
            QtWidgets.QFrame, 'team_frame_4'
        )
        self.team_frame5 = self.findChild(
            QtWidgets.QFrame, 'team_frame_5'
        )
        self.team_frame6 = self.findChild(
            QtWidgets.QFrame, 'team_frame_6'
        )
        self.team_frame7 = self.findChild(
            QtWidgets.QFrame, 'team_frame_7'
        )
        self.team_frame8 = self.findChild(
            QtWidgets.QFrame, 'team_frame_8'
        )
        self.team_frame9 = self.findChild(
            QtWidgets.QFrame, 'team_frame_9'
        )
        self.team_frame10 = self.findChild(
            QtWidgets.QFrame, 'team_frame_10'
        )
        self.team_frames_list = [
            self.team_frame1, self.team_frame2, self.team_frame3, self.team_frame4, self.team_frame5, self.team_frame6, self.team_frame7, self.team_frame8, self.team_frame9, self.team_frame10]
        self.hide_frames(self.team_frames_list)

        self.findChild(
            QtWidgets.QPushButton, 'name_btn_1'
        ).clicked.connect(
            lambda: self.update_points(self.points)
        )
        self.findChild(
            QtWidgets.QPushButton, 'name_btn_2'
        ).clicked.connect(
            lambda: self.update_points(self.points)
        )
        self.findChild(
            QtWidgets.QPushButton, 'name_btn_3'
        ).clicked.connect(
            lambda: self.update_points(self.points)
        )
        self.findChild(
            QtWidgets.QPushButton, 'name_btn_4'
        ).clicked.connect(
            lambda: self.update_points(self.points)
        )
        self.findChild(
            QtWidgets.QPushButton, 'name_btn_5'
        ).clicked.connect(
            lambda: self.update_points(self.points)
        )
        self.findChild(
            QtWidgets.QPushButton, 'name_btn_6'
        ).clicked.connect(
            lambda: self.update_points(self.points)
        )
        self.findChild(
            QtWidgets.QPushButton, 'name_btn_7'
        ).clicked.connect(
            lambda: self.update_points(self.points)
        )
        self.findChild(
            QtWidgets.QPushButton, 'name_btn_8'
        ).clicked.connect(
            lambda: self.update_points(self.points)
        )
        self.findChild(
            QtWidgets.QPushButton, 'name_btn_9'
        ).clicked.connect(
            lambda: self.update_points(self.points)
        )
        self.findChild(
            QtWidgets.QPushButton, 'name_btn_10'
        ).clicked.connect(
            lambda: self.update_points(self.points)
        )
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

        # What frames to show
        self.frames_to_show = []
        for index, team_name in enumerate(parent.team_names):
            self.frames_to_show.append(self.team_frames_list[index])
        self.show_frames(self.frames_to_show)
        self.toggle_team_btns()

        # setting team frame info
        for index, frame in enumerate(self.frames_to_show):
            team = parent.team_objects[list(parent.team_objects)[index]]
            self.set_team_frame_info(
                frame=frame,
                name=team.get_name(),
                points=team.get_points()
            )

        # Styling
        self.header.setStyleSheet(
            '''
            QLabel {
                color: rgb(255, 170, 0);
                font-size: 75px;
            }
            '''
        )
        self.setStyleSheet(
            '''
            background-color: rgb(0, 0, 255);
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
        for frame in (self.team_frames_list):
            frame.setStyleSheet(
                '''
                QFrame {
                    border: 2px solid black;
                    padding: 10px;
                }

                QPushButton {
                    color: rgb(255, 170, 0);
                    font-size: 20px;
                    padding: 5px;
                }

                QLabel {
                    border: none;
                    font-size: 20px;
                    color: rgb(255, 170, 0);
                }
                '''
            )

        if self.questionObj.opened:
            self.show_answer()

    def closeEvent(self, event) -> None:
        if self.points_added:
            event.accept()
            self.parent.media_player.stop()

        else:
            # pop up telling user points haven't been added.
            event.ignore()
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Jeopardy! - Points Not Added")
            pixmapi = getattr(QtWidgets.QStyle, "SP_MessageBoxWarning")
            icon = self.style().standardIcon(pixmapi)
            msg.setWindowIcon(icon)
            text = 'Points not added to Team!'
            msg.setText(text)
            msg.setStandardButtons(
                QtWidgets.QMessageBox.Ok |
                QtWidgets.QMessageBox.Cancel
            )
            msg.setDefaultButton(QtWidgets.QMessageBox.Cancel)
            user = msg.exec_()

            match user:
                case QtWidgets.QMessageBox.Ok:
                    event.accept()
                    self.parent.media_player.stop()
                case _:
                    event.ignore()

    def show_frames(self, frames: list) -> None:
        '''
        Function to show team sub frames.

            Parameters:
                frames: list of frames to show.
        '''
        for frame in frames:
            frame.show()

    def hide_frames(self, frames: list) -> None:
        '''
        Function to hide team sub frames.

            Parameters:
                frames: list of frames to hide.
        '''
        for frame in frames:
            frame.hide()

    def toggle_team_btns(self, enabled=False):
        '''
        Function to toggle team pushbutton.

            Parameter:
                enabled: False - disabled button, True - enabled button.
        '''

        for frame in self.frames_to_show:
            btn = frame.findChildren(QtWidgets.QPushButton)[0]
            btn.setEnabled(enabled)

    def show_answer(self) -> None:
        '''
        Function to show the answer, when the button is clicked
        '''
        if self.questionObj.opened:
            self.toggle_team_btns(False)
        else:
            self.toggle_team_btns(True)

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
        self.parent.media_player.stop()

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

    def set_team_frame_info(self, frame: QtWidgets.QFrame, name: str, points: int | float) -> None:
        '''
        Function to set a team frame's name and points.

            Parameter:
                frame: what frame to look in.

            Returns: tuple
                name: str of team name.
                points: float of points.

        '''

        if type(points) == str:
            points = float(points)
            points = "Points: {:.0f}".format(points)
        else:
            points = "Points: {:.0f}".format(points)

        frame.findChild(QtWidgets.QPushButton).setText(name)
        frame.findChild(QtWidgets.QLabel).setText(points)

    def get_team_frame_info(self, frame: QtWidgets.QFrame) -> tuple:
        '''
        Function to get a team frame name and points.

            Parameter:
                frame: what frame to look in.

            Returns: tuple
                name: str of team name.
                points: float of points.

        '''
        name = frame.findChild(QtWidgets.QPushButton).text()
        points = frame.findChild(QtWidgets.QLabel).text()
        points = points.split(':')[-1]

        return name, float(points)

    def update_points(self, points: int | float) -> None:
        '''
        Function to update the team points

            Parameters:
                points: int or float of points.
        '''

        # getting the what team button was clicked
        sender = self.sender()
        sender_name = sender.objectName()
        btn = self.findChild(
            QtWidgets.QPushButton, sender_name
        )

        # going through team frames to find what team the clicked button belongs to:
        for frame in self.frames_to_show:
            if btn in frame.findChildren(QtWidgets.QPushButton):
                # updating QLabel:
                points_label = frame.findChildren(QtWidgets.QLabel)[0]
                prev_points = float(points_label.text().split(":")[-1])
                points_label.setText(
                    "Points: {:.0f}".format(self.points + prev_points)
                )

        # calling function in parent window to update points in the TeamWindow Class.
        self.points_added = True
        self.parent.team_window.points_changed(points)
