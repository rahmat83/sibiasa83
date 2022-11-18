import sys
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QHBoxLayout,QLabel,QFileDialog,QVBoxLayout,QTextEdit,QGridLayout
from PyQt5 import QtCore
from PyQt5.QtCore import QDir,QProcess
import pyautogui
import PIL
from pynput import mouse
import mss
import cv2
import numpy as np
import time




class ScreenSelected(QWidget):

    def __init__(self,location):
        super().__init__()
        self.setWindowTitle("screener")
        self.setGeometry(10, 10, 100, 100)
        self.location=location

        self.lines=[]
        with open('listing.txt', 'r') as csvfile:
            self.lines = csvfile.readlines()
              
        try:
            self.left=self.location[0][0]
            self.top=self.location[0][1]
            self.width=self.location[1][0]-self.location[0][0]
            self.height=self.location[2][1]-self.location[0][1]
            self.monitor = {"top": self.top, "left": self.left, "width": self.width, "height": self.height}

            with mss.mss() as sct:                      

                self.sct_img = sct.grab(self.monitor)
                self.img=np.array(self.sct_img)
                cv2.namedWindow("ROI")
                cv2.imshow("ROI",self.img)          
      
        except IndexError:
            pass        
            
        self.layout = QGridLayout()
        self.textEdit = QTextEdit()       
        self.btn4 = QPushButton(QIcon('exit.png'), 'SelectKonterlist', self)
        self.btn4.clicked.connect(self.openFileNameDialog)
        self.btn5 = QPushButton(QIcon('exit.png'), 'Runscreen', self)        
        self.btn5.clicked.connect(self.runScreen)
        self.btn6 = QPushButton(QIcon('exit.png'), 'Clear', self)
        self.btn6.clicked.connect(self.clearScreen)       
        self.layout.addWidget(self.btn4)
        self.layout.addWidget(self.btn5)
        self.layout.addWidget(self.btn6)
        self.layout.addWidget(self.textEdit)
        self.setLayout(self.layout)


    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Choose File", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            with open(fileName, 'r') as csvfile:
                listing = csvfile.readlines()
                self.lines = [x.replace('\n', '') for x in listing]
            
        else:
            print ("No file selected")
    
    def runScreen(self):
        kontercoor=[self.location[3][0], self.location[3][1]]
        for i in range(0,len(self.lines)-47): 
            self.textEdit.append('screening konter'+str(self.lines[i]))
            pyautogui.click(x=kontercoor[0] , y=kontercoor[1])
            pyautogui.typewrite(self.lines[i])
            pyautogui.press('enter')
            time.sleep(2)
            with mss.mss() as sct:

                self.sct_img1 = sct.grab(self.monitor)
            img=np.array(self.sct_img1)        
            hsv=cv2.cvtColor(img, cv2.cv2.COLOR_BGR2HSV)
            dst = cv2.inRange(hsv, (36, 25, 25), (70, 255,255))
            no_green = cv2.countNonZero(dst)
            self.textEdit.append('The number of green pixels is: ' + str(no_green))
            QApplication.processEvents()

            if no_green>10:
                print(self.lines[i])
                output = "{}_{}_".format(self.lines[i][4:],no_green)+"sct-{top}x{left}_{width}x{height}.png".format(**self.monitor)
                print (output)                
                mss.tools.to_png(self.sct_img1.rgb, self.sct_img1.size, output=output)
    
    def clearScreen(self):
    	self.textEdit.clear()
 
class Front(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.screenlocation=[]

    def initUI(self):

        
        self.hbox = QGridLayout()
        self.textEdit = QTextEdit()
        
        self.btn1 = QPushButton(QIcon('exit.png'), 'GetCoordinate', self)
        self.btn1.clicked.connect(self.MousePosition)
        self.btn2 = QPushButton(QIcon('exit.png'), 'Screen', self)
        self.btn2.clicked.connect(self.show_new_window)   
        self.btn3 = QPushButton(QIcon('exit.png'), 'Reset Coordinate', self)
        self.btn3.clicked.connect(self.resetcoordinate)
        
        self.hbox.addWidget(self.btn1)
        self.hbox.addWidget(self.btn2)
        self.hbox.addWidget(self.btn3)
        self.hbox.addWidget(self.textEdit)
       
       
        self.setLayout(self.hbox)
        self.move(300, 300)
        self.setWindowTitle('KLSI Screener')
        
    def MousePosition(self):
        def on_move(x, y):
            print('Pointer moved to {0}'.format((x, y)))
        def on_click(x, y, button, pressed):
            print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))
            if pressed:              
                self.screenlocation.append((x,y))
                if len(self.screenlocation)>2:
                    print ("this is for screen")
                print (self.screenlocation)
            if not pressed:
            # Stop listener
                return False
        def on_scroll(x, y, dx, dy):
            print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up',(x, y)))
        with mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll) as listener:
            listener.join()
    def show_new_window(self):

        if self.screenlocation ==[]:
            self.textEdit.append('No coordinate select')
        else:
            try:
                self.textEdit.append('area of selection is {}'.format(self.screenlocation[:3]))
                self.textEdit.append('Search coordinates {}'.format(self.screenlocation[3]))
                self.w = ScreenSelected(self.screenlocation)
                self.w.move(400,400)
                self.w.show()
            except IndexError:
                pass

    def resetcoordinate(self):
        try:
            self.screenlocation.clear()
            print(self.screenlocation)
            self.textEdit.append('coordinate has been reset')          
        except IndexError:
            pass


def main():
    app = QApplication(sys.argv)
    ex = Front()
    ex.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()     