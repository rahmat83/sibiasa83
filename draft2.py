import sys
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QHBoxLayout,QLabel
from PyQt5 import QtCore
import pyautogui
import PIL
from pynput import mouse
import mss
import cv2
import numpy as np

class MousePosition():

    def __init__(self,location):
        self.screenlocation=location

    def on_move(x, y):
        print('Pointer moved to {0}'.format((x, y)))
    # def on_click(x, y, button, pressed):
    #     print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))
    #     if pressed:              
    #         self.screenlocation.append((x,y))
    #         print (self.screenlocation)
    #     if not pressed:
    #         # Stop listener
    #         return False
    def on_scroll(x, y, dx, dy):
        print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up',(x, y)))
    with mouse.Listener(
        on_move=on_move,
        #on_click=on_click,
        on_scroll=on_scroll) as listener:
        listener.join()

class ScreenSelected(QWidget):

    def __init__(self,location):
        super().__init__()
        self.setWindowTitle("screener")
        self.setGeometry(10, 10, 100, 100)
        self.location=location

        self.lines=[]
        with open('listing.txt', 'r') as csvfile:
            self.lines = csvfile.readlines()
            print (self.lines)
        

        try:
            self.left=self.location[0][0]
            self.top=self.location[0][1]
            self.width=self.location[1][0]-self.location[0][0]
            self.height=self.location[2][1]-self.location[0][1]
            self.monitor=monitor = {"top": self.top, "left": self.left, "width": self.width, "height": self.height}

            with mss.mss() as sct:
                sct_img = sct.grab(monitor)
                img=np.array(sct_img)
                cv2.namedWindow("opencv")
                cv2.imshow("opencv",img)
                cv2.waitKey(0)


            print(self.top,self.left,self.width,self.height)
        except IndexError:
            pass        
       
        layout = QHBoxLayout()
        self.label = QLabel("ScreenSelected")
        layout.addWidget(self.label)
        self.setLayout(layout)

class Front(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.screenlocation=[]
        j=MousePosition(self.screenlocation)


    def initUI(self):
        self.hbox = QHBoxLayout()
        self.btn1 = QPushButton(QIcon('exit.png'), 'Topleft', self)        
        self.btn1.clicked.connect(MousePosition(j.on_move()))
        self.btn2 = QPushButton(QIcon('exit.png'), 'Screen', self)
        self.btn2.clicked.connect(self.show_new_window)   
        self.hbox.addWidget(self.btn1)
        self.hbox.addWidget(self.btn2)
        self.setLayout(self.hbox)
        self.move(300, 300)
        self.setWindowTitle('KLSI Screener')
        
    # def MousePosition(self):
    #     def on_move(x, y):
    #         print('Pointer moved to {0}'.format((x, y)))
    #     def on_click(x, y, button, pressed):
    #         print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))
    #         if pressed:              
    #             self.screenlocation.append((x,y))
    #             print (self.screenlocation)
    #         if not pressed:
    #         # Stop listener
    #             return False
    #     def on_scroll(x, y, dx, dy):
    #         print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up',(x, y)))
    #     with mouse.Listener(
    #         on_move=on_move,
    #         on_click=on_click,
    #         on_scroll=on_scroll) as listener:
    #         listener.join()
    def show_new_window(self):
        self.w = ScreenSelected(self.screenlocation)
        self.w.move(400,400)
        self.w.show()


def main():
    app = QApplication(sys.argv)
    ex = Front()
    ex.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()     