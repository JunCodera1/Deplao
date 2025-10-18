# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QFrame
from PySide6.QtCore import QMetaObject, QCoreApplication

################################################################################
## Form generated from reading UI file 'designerJwUKpQ.ui'
## Created by: Qt User Interface Compiler version 6.10.0
################################################################################

class Ui_Frame(object):
    def setupUi(self, Frame):
        if not Frame.objectName():
            Frame.setObjectName(u"Frame")
        Frame.resize(400, 300)

        self.retranslateUi(Frame)
        QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    frame = QFrame()

    ui = Ui_Frame()
    ui.setupUi(frame)

    frame.show()

    sys.exit(app.exec())
