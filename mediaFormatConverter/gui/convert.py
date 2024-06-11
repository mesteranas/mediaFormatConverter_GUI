from moviepy.editor import VideoFileClip
import  soundfile
from PIL import Image
import guiTools
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class Thread(qt2.QThread):
    finished=qt2.pyqtSignal(bool)
    def __init__(self,p,path,outputFolder,format):
        super().__init__()
        self.p=p
        self.path=path
        self.outputDIR=outputFolder
        self.format=format
    def run(self):
        OutputPath=self.outputDIR + "/" + self.path.split("/")[-1].split(".")[0] + self.format
        for imageFormat in self.p.image_formats:
            if self.path.endswith(imageFormat):
                try:
                    img=Image.open(self.path)
                    if self.format.lower() in [".jpg", ".jpeg"] and img.mode == "P":
                        img = img.convert("RGB")
                    img.save(OutputPath)
                    self.finished.emit(True)
                except Exception as error:
                    self.finished.emit(False)
                return
            continue
        for audioFormat in self.p.audio_formats:
            if self.path.endswith(audioFormat):
                try:
                    data,sampleRate=soundfile.read(self.path)
                    soundfile.write(OutputPath,data,sampleRate)
                    self.finished.emit(True)
                except Exception as error:
                    self.finished.emit(False)
                return
            continue
        for videoFormat in self.p.video_formats:
            if self.path.endswith(videoFormat):
                try:
                    video=VideoFileClip(self.path)
                    video.write_videofile(OutputPath,codec='libx264' if self.format.lower() in ['.mp4', '.mkv'] else None)
                    self.finished.emit(True)
                except Exception as error:
                    self.finished.emit(False)
                return
            continue

class ConvertGUI(qt.QDialog):
    def __init__(self,p,path,outputFolder,format):
        super().__init__(p)
        self.setWindowTitle(_("converting ..."))
        self.thread=Thread(p,path,outputFolder,format)
        layout=qt.QVBoxLayout(self)
        self.cancel=guiTools.QPushButton(_("cancel"))
        self.cancel.clicked.connect(self.thread.terminate)
        layout.addWidget(self.cancel)
        self.thread.finished.connect(self.on_finish)
        self.thread.start()
    def on_finish(self,state):
        if state:
            qt.QMessageBox.information(self,_("done"),_("converted"))
        else:
            qt.QMessageBox.warning(self,_("error"),"")
        self.close()