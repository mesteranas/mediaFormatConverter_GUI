import sys
from custome_errors import *
sys.excepthook = my_excepthook
from moviepy.editor import VideoFileClip
import pydub
from PIL import Image
import update
import gui
import guiTools
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
language.init_translation()
class main (qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(app.name + _("version : ") + str(app.version))
        layout=qt.QVBoxLayout()
        self.audio_formats = [".mp3", ".wav", ".wma", ".aac", ".m4a", ".flac", ".ogg", ".opus", ".ape", ".mpga", ".alac", ".wv", ".mka", ".aiff", ".au", ".dss", ".iff", ".m4r", ".m4b", ".midi", ".mid", ".ac3", ".tta", ".m3u"]
        self.video_formats = [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".3gp", ".webm", ".rm", ".m2ts", ".vob", ".mts", ".mxf", ".SWF", ".AV1", ".VP9", ".MPG", ".M4V", ".WMV", ".ASF", ".mpeg", ".ogv", ".rmvb", ".divx", ".m2v"]
        self.image_formats = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".psd", ".ai", ".raw", ".svg", ".heic", ".webp", ".ps", ".EPS", ".PCT", ".TGA", ".FITS", ".JP2", ".EXR", ".PBM", ".ico", ".tif", ".tga", ".pcx", ".jif", ".hdr", ".dng", ".jxr", ".dib"]
        self.path=guiTools.QReadOnlyTextEdit()
        layout.addWidget(qt.QLabel(_("file path")))
        layout.addWidget(self.path)
        self.selectFile=guiTools.QPushButton(_("select file"))
        self.selectFile.clicked.connect(self.on_select_file)
        layout.addWidget(self.selectFile)
        self.format=qt.QComboBox()
        layout.addWidget(qt.QLabel(_("format")))
        layout.addWidget(self.format)
        self.outputDir=guiTools.QReadOnlyTextEdit()
        layout.addWidget(qt.QLabel(_("output folder")))
        layout.addWidget(self.outputDir)
        self.selectOutputDIR=guiTools.QPushButton(_("select folder"))
        self.selectOutputDIR.clicked.connect(self.on_select_output_folder)
        layout.addWidget(self.selectOutputDIR)
        self.startConvertion=guiTools.QPushButton(_("convert"))
        self.startConvertion.clicked.connect(lambda:gui.ConvertGUI(self,self.path.toPlainText(),self.outputDir.toPlainText(),self.format.currentText()).exec())
        layout.addWidget(self.startConvertion)
        self.setting=guiTools.QPushButton(_("settings"))
        self.setting.clicked.connect(lambda: settings(self).exec())
        layout.addWidget(self.setting)
        w=qt.QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)

        mb=self.menuBar()
        help=mb.addMenu(_("help"))
        helpFile=qt1.QAction(_("help file"),self)
        help.addAction(helpFile)
        helpFile.triggered.connect(lambda:guiTools.HelpFile())
        helpFile.setShortcut("f1")
        cus=help.addMenu(_("contact us"))
        telegram=qt1.QAction("telegram",self)
        cus.addAction(telegram)
        telegram.triggered.connect(lambda:guiTools.OpenLink(self,"https://t.me/mesteranasm"))
        telegramc=qt1.QAction(_("telegram channel"),self)
        cus.addAction(telegramc)
        telegramc.triggered.connect(lambda:guiTools.OpenLink(self,"https://t.me/tprogrammers"))
        githup=qt1.QAction(_("Github"),self)
        cus.addAction(githup)
        githup.triggered.connect(lambda: guiTools.OpenLink(self,"https://Github.com/mesteranas"))
        X=qt1.QAction(_("x"),self)
        cus.addAction(X)
        X.triggered.connect(lambda:guiTools.OpenLink(self,"https://x.com/mesteranasm"))
        email=qt1.QAction(_("email"),self)
        cus.addAction(email)
        email.triggered.connect(lambda: guiTools.sendEmail("anasformohammed@gmail.com","project_type=GUI app={} version={}".format(app.name,app.version),""))
        Github_project=qt1.QAction(_("visite project on Github"),self)
        help.addAction(Github_project)
        Github_project.triggered.connect(lambda:guiTools.OpenLink(self,"https://Github.com/mesteranas/{}".format(settings_handler.appName)))
        Checkupdate=qt1.QAction(_("check for update"),self)
        help.addAction(Checkupdate)
        Checkupdate.triggered.connect(lambda:update.check(self))
        licence=qt1.QAction(_("license"),self)
        help.addAction(licence)
        licence.triggered.connect(lambda: Licence(self))
        donate=qt1.QAction(_("donate"),self)
        help.addAction(donate)
        donate.triggered.connect(lambda:guiTools.OpenLink(self,"https://www.paypal.me/AMohammed231"))
        about=qt1.QAction(_("about"),self)
        help.addAction(about)
        about.triggered.connect(lambda:qt.QMessageBox.information(self,_("about"),_("{} version: {} description: {} developer: {}").format(app.name,str(app.version),app.description,app.creater)))
        self.setMenuBar(mb)
        if settings_handler.get("update","autoCheck")=="True":
            update.check(self,message=False)
    def closeEvent(self, event):
        if settings_handler.get("g","exitDialog")=="True":
            m=guiTools.ExitApp(self)
            m.exec()
            if m:
                event.ignore()
        else:
            self.close()
    def on_select_file(self):
        file=qt.QFileDialog(self)
        if file.exec()==file.DialogCode.Accepted:
            self.path.setText(file.selectedFiles()[0])
            self.format.clear()
            path=file.selectedFiles()[0]
            for audioFormat in self.audio_formats:
                if path.endswith(audioFormat):
                    self.format.addItems(self.audio_formats)
                    return
                continue
            for videoFormat in self.video_formats:
                if path.endswith(videoFormat):
                    self.format.addItems(self.video_formats)
                    return
                continue
            for imageFormat in self.image_formats:
                if path.endswith(imageFormat):
                    self.format.addItems(self.image_formats)
                    return
                continue
    def on_select_output_folder(self):
        folder=qt.QFileDialog()
        folder.setFileMode(folder.FileMode.Directory)
        if folder.exec()==folder.DialogCode.Accepted:
            self.outputDir.setText(folder.selectedFiles()[0])
App=qt.QApplication([])
w=main()
w.show()
App.setStyle('fusion')
App.exec()