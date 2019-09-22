import threading
from datetime import datetime
from time import sleep

import requests
from PyQt5 import QtWidgets
import clientui


class ExampleApp(QtWidgets.QMainWindow, clientui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.send)

        threading.Thread(target=self.refresh).start()

    def send(self):
        text = self.lineEdit.text()
        username = self.lineEdit_2.text()
        password = self.lineEdit_3.text()

        try:
            response = requests.post('http://127.0.0.1:5000/login', json={
                'username': username,
                'password': password
            })
            print(response.text)

            response = requests.post('http://127.0.0.1:5000/send', json={
                'username': username,
                'password': password,
                'text': text
            })
            print(response.text)
        except requests.exceptions.ConnectionError:
            print('Сервер не доступен')
            return

        self.lineEdit.setText('')

    def refresh(self):
        last_time = 0
        while True:
            response = requests.get('http://127.0.0.1:5000/messages',
                                    params={'after': last_time})

            for message in response.json()['messages']:
                time_format = datetime.fromtimestamp(message['time'])
                time_format = time_format.strftime('%Y-%m-%d %H:%M:%S')
                self.textBrowser.append(message['username'] + ' в ' + str(time_format))
                self.textBrowser.append(message['text'])
                self.textBrowser.append('')


                last_time = message['time']

            sleep(1)





if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = ExampleApp()
    window.show()
    app.exec_()
