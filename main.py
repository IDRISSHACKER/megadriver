import sys, os
import webbrowser
from tkinter import W
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5 import QtCore, QtGui
from PyQt5.uic import loadUi
from api.Sync import Sync
from api.utils import Utils

class Worker(QObject):
    finished = pyqtSignal(bool)

    def __init__(self, folder):
        super(Worker, self).__init__()
        self.folder = folder
        self.clouad = Sync()
    
    def run(self):
        print("Upload...")
        self.clouad.upload(self.folder)
        self.finished.emit(True)

class Worker2(QObject):
    finished = pyqtSignal(bool)

    def __init__(self, email, password):
        super(Worker2, self).__init__()
        self.email = email
        self.password = password
        self.clouad = Sync()
    
    def run(self):
        print("Connexion...")
        if self.clouad.login(self.email, self.password):
            self.finished.emit(True)
        else:
            self.finished.emit(False)


count = 0
class Main(QtWidgets.QSystemTrayIcon):
    def __init__(self,):
        super(Main, self).__init__()
        self.clouad = Sync()

        self.main = loadUi("./gui/home.ui")
        self.login = loadUi("./gui/login.ui")
        self.sync = loadUi("./gui/synchro.ui")
        
        #self.login.show()
        
        self.login.setWindowTitle("Connexion")
        self.sync.setWindowTitle("Synchronisation")
        self.main.setWindowTitle("MegaDriver")
        self.login.setWindowIcon(QtGui.QIcon("./icon.png"))
        self.sync.setWindowIcon(QtGui.QIcon("./icon.png"))
        self.main.setWindowIcon(QtGui.QIcon("./icon.png"))

        self.pages = [
            {
                "title": "Home",
                "btn"  : self.main.compte,
                "page" : self.main.compteView,
            },
            {
                "title": "Dossier Synchroniser dans le clouad",
                "btn"  : self.main.dossier,
                "page" : self.main.dossierView,
            },
            {
                "title": "Vos Telechargements",
                "btn"  : self.main.offline,
                "page" : self.main.offlineView,
            },
            {
                "title": "settings",
                "btn"  : self.main.settings,
                "page" : self.main.settingsView,
            },
        ]
        self.setup_connection()
        self.modify_layout()

    def setup_connection(self):
        self.pages[0].get("btn").clicked.connect(self.showHomePage)
        self.pages[1].get("btn").clicked.connect(self.showFolderPage)
        self.pages[2].get("btn").clicked.connect(self.showOfflinePage)
        self.pages[3].get("btn").clicked.connect(self.showSettingsPage)

        self.login.submit.clicked.connect(self.connexion)
        self.sync.sync.clicked.connect(self.synchronize)
        self.sync.choose.clicked.connect(self.chooseFolder)
        self.login.goToMega.clicked.connect(self.openMega)
    
    def action(self):
        print("Background process started")

    def modify_layout(self):
        self.login.err.setVisible(False)
        self.sync.load.setVisible(False)
        self.util = Utils()
        if self.util.verfifyTrueCafeData()[1]:
            self.sync.path.setText(self.util.verfifyTrueCafeData()[0])

    def add_widget_to_layout(self):
        pass

    def setActivePage(self, index):
        self.main.pages.setCurrentWidget(self.pages[index].get("page"))
        self.main.setWindowTitle(self.pages[index].get("title"))
        self.main.title.setText(self.pages[index].get("title"))
           
    def showHomePage(self):
        self.setActivePage(0)
    
    def showFolderPage(self):
        self.setActivePage(1)
    
    def showOfflinePage(self):
        self.setActivePage(2)
    
    def showSettingsPage(self):
        self.setActivePage(3)
    
    def connexion(self):
        self.login.submit.setEnabled(False)
        self.login.submit.setText("Connexion en cour...")
        email = self.login.email.text()
        password = self.login.password.text()
        self.runLogin(email, password)

    def synchronize(self):
        self.sync.sync.setEnabled(False)
        self.sync.sync.setText("upload en cour...")
        path = self.sync.path.text()
        if path:
            self.sync.load.setVisible(True)
            self.sync.choose.setEnabled(False)
            self.sync.sync.setEnabled(False)
            self.runWorkers(path)
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.endWorker)
            self.timer.start(70000)

    def chooseFolder(self):
        select = QtWidgets.QFileDialog.getExistingDirectory(caption="Selectionner le dossier a synchroniser")
        file = select

        if file != "":
            self.sync.path.setText(file)

    def showMain(self):
        self.sync.close()
        self.main.show()

    def runWorkers(self, path):
        self.thread = QThread()
        self.worker = Worker(path)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.endWorker)
        self.thread.start()
    
    def runLogin(self, email, password):
        self.thread2 = QThread()
        self.worker2 = Worker2(email, password)
        self.worker2.moveToThread(self.thread2)
        self.thread2.started.connect(self.worker2.run)
        self.worker2.finished.connect(self.endRunLogin)
        self.thread2.start()

    def endWorker(self, status):
        self.sync.sync.setEnabled(True)
        self.sync.sync.setText("SYNCHRONISER")
        if status:
            self.showMain()
        else:
            print('err')
    
    def endRunLogin(self, status):
        self.login.submit.setEnabled(True)
        self.login.submit.setText("Connexion")
        print(status)
        if status:
            self.sync.show()
            self.login.close()
        else:
            self.login.err.setVisible(True)
        self.thread2.quit()

    def openMega(self):
        try:
            webbrowser.open_new_tab("mega.nz")
        except: 
            try:
                webbrowser.Mozilla("mega.nz")
            except:
                print("Aucun navigateur compatible")
        

app = QApplication(sys.argv)

tray = QtWidgets.QSystemTrayIcon(QtGui.QIcon("icon.png"), parent=app)
menu = QtWidgets.QMenu()
open_App = menu.addAction("Ouvrir")
open_App.setIcon(QtGui.QIcon("./icon.png"))
def show():
    window.login.show()
open_App.triggered.connect(show)
menu.addSeparator()
tray.setContextMenu(menu)
tray.setToolTip("MegaDriver")
tray.show()

window = Main()
window.action()
app.exec()
