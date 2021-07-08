import asyncio
import os
from getpass import getuser
import sys
import gc
from PyQt5 import uic, QtCore, QtWidgets
import time
import gd
from PySide2 import QtXml
import win32api
import win32con
import ctypes
from PyQt5.QtWidgets import QMainWindow, QApplication
from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

class MainCode():
    try:
        def GDIn():
            class Interfaz(QMainWindow):
                def __init__(self):
                    super().__init__()
                    self.AbrirUI()
                    self.Debug.setText("Iniciando Programa")
                    self.LowMode.clicked.connect(self.LowText)
                    self.TimerC()
                    self.showPB.clicked.connect(self.ShowPBar)
                    self.showS.clicked.connect(self.ShowSong)
                    self.showID.clicked.connect(self.ShowIDLevel)
                    self.showA.clicked.connect(self.ShowAttempts)
                    self.showBestP.clicked.connect(self.ShowBestPor)
                    self.showNL.clicked.connect(self.ShowNameLevel)
                    self.showPor.clicked.connect(self.ShowPorcentaje)
                    self.StreamStatus.clicked.connect(self.StreamMode)

                def TimerC(self):
                    self.repaint()
                    self.Debug.setText("Actualizando pantalla en 0.1seg")
                    self.timer = QtCore.QTimer()
                    self.timer1 = QtCore.QTimer()
                    self.timer.timeout.connect(self.Update)
                    self.timer.start(100)

                def Update(self):
                    self.Debug.setText("Enviando peticiones")
                    self.repaint()
                    self.Clase()
            
                def AbrirUI(self):
                    print("Ejecutando interfaz")
                    Dir = r'C:/ProyectsMM/GD Tool' 
                    File = r'/UIGDT.ui'
                    DirFile = Dir + File
                    print("Optimizando programa al jugar un nivel en GD")
                    uic.loadUi(DirFile,self)

                def Clase(self):
                    self.Debug.setText("Obteniendo peticiones")
                    try:
                        memory = gd.memory.get_memory()
                    except:
                        print("Error: GD No running")
                        self.BsoD()
                        return
                    if memory.is_in_level() and self.Playing.isChecked()==True:
                            self.RunAppUpdates()
                    else:
                        self.Playing.setChecked(True)
                        if memory.is_in_level():
                            self.RunAppStatic()
                        else:
                            self.InMenuGD()


                def InMenuGD(self):
                    if self.StreamStatus.isChecked()==True:
                        Attempts = open(r"C:/ProyectsMM/GD Tool/TextStreams/Attempts.txt","w+")
                        Attempts.write(f"")
                        Attempts.close()
                        Porcentaje = open(r"C:/ProyectsMM/GD Tool/TextStreams/Porcentage.txt","w+")
                        Porcentaje.write(f"")
                        Porcentaje.close()
                        BestPor = open(r"C:/ProyectsMM/GD Tool/TextStreams/BestPorcentage.txt","w+")
                        BestPor.write(f"")
                        BestPor.close()
                        IDlvl = open(r"C:/ProyectsMM/GD Tool/TextStreams/IDLevel.txt","w+")
                        IDlvl.write(f"")
                        IDlvl.close()
                        LevelName = open(r"C:/ProyectsMM/GD Tool/TextStreams/LevelName.txt","w+")
                        LevelName.write(f"")
                        LevelName.close()
                    else:
                        self.progressBar.setValue(0)
                        self.textp.setText("...")
                        self.gdstatus.setText("")
                        self.levelinfo.setText("In menu")
                        self.idlevel.setText("")
                        self.songinfo.setText("")
                        self.bestPinfo.setText("")
                        self.progressBar.setHidden(True)
                        self.TimerC()
                    Song = open(r"C:/ProyectsMM/GD Tool/TextStreams/Song.txt","w+")
                    Song.write("")
                    Song.close()
                    self.Playing.setChecked(False)
                
                def RunAppUpdates(self):
                    memory = gd.memory.get_memory()
                    Intentos = memory.get_attempts()
                    BestPorc = memory.get_normal_percent()
                    b = memory.get_percent()
                    ANT = int(b)
                    porF = str(ANT)
                    if self.StreamStatus.isChecked()==True:
                        Attempts = open(r"C:/ProyectsMM/GD Tool/TextStreams/Attempts.txt","w+")
                        Attempts.write(f"Attempts: {Intentos}")
                        Attempts.close()
                        Porcentaje = open(r"C:/ProyectsMM/GD Tool/TextStreams/Porcentage.txt","w+")
                        Porcentaje.write(f"{porF}%")
                        Porcentaje.close()
                        BestPor = open(r"C:/ProyectsMM/GD Tool/TextStreams/BestPorcentage.txt","w+")
                        BestPor.write(f"{BestPorc}%")
                        BestPor.close()
                    else:
                        self.gdstatus.setText(f"Attempts: {Intentos}")
                        self.ShowPBar()
                        self.TimerC()
                        self.bestPinfo.setText(f"Best: {BestPorc}%")
                        self.progressBar.setValue(ANT)
                        self.textp.setText(f"{porF}%")

                def RunAppStatic(self):
                    memory = gd.memory.get_memory()
                    LevelName = memory.get_level_name()
                    IDL = memory.get_level_id()
                    if self.StreamStatus.isChecked()==True:
                        Lvl = open(r"C:/ProyectsMM/GD Tool/TextStreams/LevelName.txt","w+")
                        Lvl.write(f"{LevelName}")
                        Lvl.close()
                        if IDL >= 22 or IDL == 0:
                            if IDL == 0:
                                IDlvl = open(r"C:/ProyectsMM/GD Tool/TextStreams/IDLevel.txt","w+")
                                IDlvl.write(f"No ID available")
                                IDlvl.close()
                            else:
                                IDlvl = open(r"C:/ProyectsMM/GD Tool/TextStreams/IDLevel.txt","w+")
                                IDlvl.write(f"ID: {IDL}")
                                IDlvl.close()
                        else:
                            IDlvl = open(r"C:/ProyectsMM/GD Tool/TextStreams/IDLevel.txt","w+")
                            IDlvl.write(f"Official level")
                            IDlvl.close()
                    else:
                        self.levelinfo.setText(f"{LevelName}")
                        if IDL >= 22 or IDL == 0:
                            if IDL == 0:
                                self.idlevel.setText("ID: Not available")
                            else:
                                self.idlevel.setText(f"ID: {IDL}")
                        else:
                            self.idlevel.setText("Official robtop level")
                    self.GetNameSong()
                    return
                
                def StreamMode(self):
                    if self.StreamStatus.isChecked()==True:
                        self.showPB.setChecked(False)
                        self.showS.setChecked(False)
                        self.showID.setChecked(False)
                        self.showA.setChecked(False)
                        self.showBestP.setChecked(False)
                        self.showPor.setChecked(False)
                        self.showNL.setChecked(False)
                    else:
                        self.showPB.setChecked(True)
                        self.showS.setChecked(True)
                        self.showID.setChecked(True)
                        self.showA.setChecked(True)
                        self.showBestP.setChecked(True)
                        self.showPor.setChecked(True)
                        self.showNL.setChecked(True)
                    self.ShowPBar()
                    self.ShowPorcentaje()
                    self.ShowAttempts()
                    self.ShowIDLevel()
                    self.ShowBestPor()
                    self.ShowSong()
                    self.ShowNameLevel()

                def InstallFont(self):
                    ctypes.windll.gdi32.AddFontResourceA("C:/ProyectosPY/GD Tool Beta 1.2/PUSAB___.otf")
                    win32api.SendMessage(win32con.HWND_BROADCAST, win32con.WM_FONTCHANGE)

                ##def BGcolor(self):
                    ##BGC = self.typeBG.currentText()
                    ##Blue = "Backgroond Blue"
                    ##Green = "Background Green"
                    ##if Blue == BGC:
                        ##self.WidgetMain.setStyleSheet('''background-color: rgb(0, 0, 255); ''')
                    ##if Green == BGC:
                        ##self.WidgetMain.setStyleSheet('''background-color: rgb(85, 255, 0); ''')

                def ShowPBar(self):
                    if self.showPB.isChecked()==True:
                        self.progressBar.setHidden(False)
                    else:
                        self.progressBar.setHidden(True)

                def ShowSong(self):
                    if self.showS.isChecked()==True:
                        self.songinfo.setHidden(False)
                    else:
                        self.songinfo.setHidden(True)

                def ShowAttempts(self):
                    if self.showA.isChecked()==True:
                        self.gdstatus.setHidden(False)
                    else:
                        self.gdstatus.setHidden(True)
                
                def ShowIDLevel(self):
                    if self.showID.isChecked()==True:
                        self.idlevel.setHidden(False)
                    else:
                        self.idlevel.setHidden(True)

                def ShowBestPor(self):
                    if self.showBestP.isChecked()==True:
                        self.bestPinfo.setHidden(False)
                    else:
                        self.bestPinfo.setHidden(True)

                def ShowPorcentaje(self):
                    if self.showPor.isChecked()==True:
                        self.textp.setHidden(False)
                    else:
                        self.textp.setHidden(True)

                def ShowNameLevel(self):
                    if self.showNL.isChecked()==True:
                        self.levelinfo.setHidden(False)
                    else:
                        self.levelinfo.setHidden(True)

                def LowText(self):
                    if self.LowMode.isChecked()==True:
                        print("Texto pequeño ON")
                        self.textp.setStyleSheet('''color:rgb(255, 255, 255); font-size: 18px; ''')
                        self.textp.setGeometry(10,10,71,21)
                        self.bestPinfo.setStyleSheet('''color:rgb(255, 255, 255); font-size: 18px; ''')
                        self.bestPinfo.setGeometry(240,10,151,21)
                        self.levelinfo.setStyleSheet('''color:rgb(255, 255, 255); font-size: 18px; ''')
                        self.levelinfo.setGeometry(10,40,441,31)
                        self.idlevel.setStyleSheet('''color:rgb(255, 255, 255); font-size: 18px; ''')
                        self.idlevel.setGeometry(10,70,381,31)
                        self.songinfo.setStyleSheet('''color:rgb(255, 255, 255); font-size: 18px; ''')
                        self.songinfo.setGeometry(10,100,441,31)
                        self.gdstatus.setStyleSheet('''color:rgb(255, 255, 255); font-size: 18px; ''')
                        self.gdstatus.setGeometry(10,130,381,31)
                        self.progressBar.setGeometry(80,10,151,22)
                    else:
                        print("Texto grande ON")
                        self.textp.setStyleSheet('''color:rgb(255, 255, 255);''')
                        self.textp.setGeometry(10,0,141,51)
                        self.bestPinfo.setStyleSheet('''color:rgb(255, 255, 255); ''')
                        self.bestPinfo.setGeometry(440,10,291,41)
                        self.levelinfo.setStyleSheet('''color:rgb(255, 255, 255); ''')
                        self.levelinfo.setGeometry(10,70,801,31)
                        self.idlevel.setStyleSheet('''color:rgb(255, 255, 255); ''')
                        self.idlevel.setGeometry(10,120,791,31)
                        self.songinfo.setStyleSheet('''color:rgb(255, 255, 255); ''')
                        self.songinfo.setGeometry(10,170,801,31)
                        self.gdstatus.setStyleSheet('''color:rgb(255, 255, 255); ''')
                        self.gdstatus.setGeometry(10,220,801,31)
                        self.progressBar.setGeometry(160,10,271,41)


                def GetNameSong(self):
                    try:
                        client = gd.Client()
                        memory = gd.memory.get_memory()
                        IDsong = memory.get_song_id()                        
                    except:
                        self.BsoD()
                        return
                    if IDsong >= 30:
                        Song = open(r"C:/ProyectsMM/GD Tool/TextStreams/Song.txt","w+")
                        self.songinfo.setText("NONG Level/Layout")
                        Song.write("NONG Level/Layout")
                        Song.close()
                    if IDsong == 0:
                        Song = open(r"C:/ProyectsMM/GD Tool/TextStreams/Song.txt","w+")
                        self.songinfo.setText("")
                        Song.write("")
                        Song.close()
                    else:
                        Song = open(r"C:/ProyectsMM/GD Tool/TextStreams/Song.txt","w+")
                        print(f"IDSONG:{IDsong}")
                        async def getns():
                            IDsong = memory.get_song_id()
                            song = await client.get_song(IDsong)
                            NameSong = str(song)
                            self.songinfo.setText(f"Song: {NameSong}")
                            Song.write(f"Song: {NameSong}")
                    try:
                        client.run(getns())
                        Song.close()
                    except:
                        return
                    
                def BsoD(self):
                    self.levelinfo.setText("GD No Running")
                    self.bestPinfo.setText("")
                    self.idlevel.setText("")
                    self.songinfo.setText("")
                    self.gdstatus.setText("Try...")
                    self.Debug.setText("Reiniciando en 0.1 seg")
                    return


            def main():
                app = QApplication(sys.argv)
                GUI = Interfaz()
                GUI.show()
                sys.exit(app.exec_())

            if __name__ == '__main__':
                main()
        GDIn()

    except:
        class InterfazError(QMainWindow):
            def __init__(self):
                super().__init__()
                uic.loadUi("thxu.ui", self)
                self.Debug.setText("Thx u!")
                self.Ohno()
                print("Gracias por usarlo! <3")
                
                
            def Ohno(self):
                self.Debug.setText("Thx u! <3")

        if __name__ == '__main__':          
            app = QApplication.instance()
            if app == None:
                app = QApplication([])
            GUI = InterfazError()
            GUI.show()
            sys.exit(app.exec_())
