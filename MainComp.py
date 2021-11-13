from PyQt5 import QtCore, QtGui, QtWidgets
import librosa
import librosa.display
from dtw import dtw
from python_speech_features import mfcc


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(662, 489)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(100)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(260, 50, 521, 21))
        self.label.setObjectName("Comparer deux enregistrements")

        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(255, 70, 165, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.boutton1 = QtWidgets.QPushButton(self.centralwidget)
        self.boutton1.setGeometry(QtCore.QRect(550, 170, 93, 28))
        self.boutton1.setObjectName("parcourir")

        self.chemin1 = QtWidgets.QLabel(self.centralwidget)
        self.chemin1.setGeometry(QtCore.QRect(20, 170, 521, 21))
        self.chemin1.setObjectName("chemin")

        self.chemin2 = QtWidgets.QLabel(self.centralwidget)
        self.chemin2.setGeometry(QtCore.QRect(20, 110, 521, 16))
        self.chemin2.setObjectName("chemin")

        self.boutton2 = QtWidgets.QPushButton(self.centralwidget)
        self.boutton2.setGeometry(QtCore.QRect(550, 110, 93, 28))
        self.boutton2.setObjectName("parcourir")

        self.resultat = QtWidgets.QLabel(self.centralwidget)
        self.resultat.setGeometry(QtCore.QRect(210, 320, 251, 61))
        self.resultat.setObjectName("Resultat")

        self.boutton3 = QtWidgets.QPushButton(self.centralwidget)
        self.boutton3.setGeometry(QtCore.QRect(210, 240, 241, 41))
        self.boutton3.setObjectName("comparer")
        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.dialog = QtWidgets.QFileDialog(self.centralwidget)
        self.dialog.setWindowTitle('Open wav File')
        self.dialog.setNameFilter('wav files (*.wav)')

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mini_Projet Traitement de parole: Ayah Barhrhouj "))
        MainWindow.setWindowIcon(QtGui.QIcon("icon.png"))
        self.label.setText(_translate("MainWindow", "Comparer deux enregistrements"))
        self.boutton1.setText(_translate("MainWindow", "Pacourir"))
        self.chemin1.setText(_translate("MainWindow", ""))
        self.chemin2.setText(_translate("MainWindow", ""))
        self.boutton2.setText(_translate("MainWindow", "Pacourir"))
        self.resultat.setText(_translate("MainWindow", ""))
        self.boutton3.setText(_translate("MainWindow", "Comparer"))
        self.boutton2.clicked.connect(self.selectWav1)
        self.boutton1.clicked.connect(self.selectWav2)
        self.boutton3.clicked.connect(self.Comparer)

    def selectWav1(self):
        self.dialog.setDirectory(QtCore.QDir.currentPath())
        self.dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        if self.dialog.exec_() == QtWidgets.QDialog.Accepted:
            chemin1_wav = str(self.dialog.selectedFiles()[0])

        else:
            return None
        self.chemin2.setText(chemin1_wav)
        self.path1 = chemin1_wav

    def selectWav2(self):
        self.dialog.setDirectory(QtCore.QDir.currentPath())
        self.dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        if self.dialog.exec_() == QtWidgets.QDialog.Accepted:
            chemin2_wav = str(self.dialog.selectedFiles()[0])

        else:
            return None
        self.chemin1.setText(chemin2_wav)
        self.path2 = chemin2_wav

    def Comparer(self):
        if self.path1 == '' or self.path2 == '':
            self.resultat.setText("Importer les audios SVP")
        else:
            audio1, sample_rate1 = librosa.load(self.path1)
            audio2, sample_rate2 = librosa.load(self.path2)
            mfcc_audio1 = librosa.feature.mfcc(audio1, sr=sample_rate1)
            mfcc_audio2 = librosa.feature.mfcc(audio2, sr=sample_rate2)
            n1, c1 = mfcc_audio1.shape
            n2, c2 = mfcc_audio2.shape

            # si les 2 vecteurs n'ont pas le meme shape
            if n1 != n2 or c1 != c2:
                mfcc_audio1 = mfcc_audio1.reshape(-1, 1)
                mfcc_audio2 = mfcc_audio2.reshape(-1, 1)
                matches, cost, mapping_1, mapping_2, matrix = dtw(mfcc_audio1, mfcc_audio2)
                if cost > 1000:
                    res = "les deux enregistrements  ne sont pas similaires"
                    self.resultat.setText("le coût = " + str(cost) + "\n" + res)
                elif cost == 0:
                    res1 = "les deux enregistrements sont similaires"
                    self.resultat.setText("le coût = " + str(cost) + "\n" + res1)
            else:
                matches, cost, mapping_1, mapping_2, matrix = dtw(mfcc_audio1, mfcc_audio2)
                if cost > 1000:
                    res = "les deux enregistrements ne sont pas similaires"
                    self.resultat.setText("le coût = " + str(cost) + "\n" + res)
                elif cost == 0:
                    res1 = "les deux enregistrements sont similaires"
                    self.resultat.setText("le coût = " + str(cost) + "\n" + res1)


if __name__ == "__main__":
    import sys


    app = QtWidgets.QApplication(sys.argv)
    ex = Ui_MainWindow()
    w = QtWidgets.QMainWindow()
    ex.setupUi(w)
    w.show()
    sys.exit(app.exec_())
