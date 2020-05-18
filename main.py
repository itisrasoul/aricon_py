#Import libs
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import os
import subprocess as sp
from ffmpeg_progress import start

#Multithreading support
class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.fn = fn
    @pyqtSlot()
    def run(self):
        self.fn()

#create the mainwindow class
class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__() #inherit from the QMainWindow
        self.setAcceptDrops(True) #Enable drag and drop

        self.initui() #call the initui function
    def initui(self):
        self.setStyleSheet("background-color: #2b2b2b;color: #B6BAB1;") #Dark mode for myself
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.menubar = self.menuBar() #create a menubar
        self.menubar_add() #call menubar_add func to add items to menubar
        self.main_vbox = QVBoxLayout() #add a layout for adding widgets
        self.main_widget.setLayout(self.main_vbox) #set it as the main layout of window
        self.main_lbl_welcome = QLabel("Welcome to Aricon!") #welcome label
        self.lbl_welcome_font = QFont() #add a font for welcome label
        self.lbl_welcome_font.setBold(True) #set bold 
        self.lbl_welcome_font.setPointSize(22) #set font size
        self.main_lbl_welcome.setFont(self.lbl_welcome_font) #set the label's font
        self.main_vbox.addWidget(self.main_lbl_welcome) #add the label
        self.main_vbox.setAlignment(self.main_lbl_welcome, Qt.AlignHCenter) #set the alignment of welcome label

        self.main_lbl_intro = QLabel("Aricon is a free, minimal, and open source video toolkit for linux.\nIt uses ffmpeg as the converter engine, which is fast and porwerful.\nThe first versions of Aricon were developed by my dearest friend, Hossein Heydari with bash script;\nSo I decided to continue developing it via Python and PyQt5.\n\nYou can Navigate through the menubar at the top to find the tool you're looking for.")
        self.main_vbox.addWidget(self.main_lbl_intro) #add introduction label
        self.main_vbox.setAlignment(self.main_lbl_intro, Qt.AlignHCenter) #set alignment

        self.setWindowTitle("Aricon 3.0") #set window title
        self.setWindowIcon(QIcon("icons/converter.png")) #set the window icon
        self.setMinimumSize(800,600) #set window min and max size
        self.setMaximumSize(800,600)
        self.show() #and FINALLY, show the window

    def menubar_add(self):
        self.file_menu = self.menubar.addMenu("File") #add file menu to menubar

        self.history_action = QAction("History") #set an action in file menu for history
        self.history_action.setIcon(QIcon("icons/about.svg")) #set action's icon
        self.history_action.triggered.connect(self.arihis) #sending the signal when action is triggered
        self.history_action.setShortcut("Ctrl+H") #set a shortcut for history
        self.file_menu.addAction(self.history_action) #add the action to file menu

        self.exit_action = QAction("Exit") #exit action in file menu
        self.exit_action.setIcon(QIcon("icons/remove.svg"))
        self.exit_action.triggered.connect(lambda: self.close()) ##sending the signal when action is triggered
        self.exit_action.setShortcut("Ctrl+Q") #set shortcut for the action
        self.file_menu.addAction(self.exit_action) #add the action to file menu

        self.sub_menu = self.menubar.addMenu("Subtitle Tools") #add subtitle menu to menubar

        self.sub_burn_action = QAction("Burn a .srt subtitle file into the video") #action for burning subtitles into a video
        self.sub_burn_action.setIcon(QIcon("icons/sub.png"))
        self.sub_burn_action.triggered.connect(self.burn_sub) ##sending the signal when action is triggered
        self.sub_burn_action.setShortcut("Shift+Ctrl+B") #set shortcut for the action
        self.sub_menu.addAction(self.sub_burn_action)

        self.video_tools_menu = self.menubar.addMenu("Video Tools") #Add a menu for video tools to menubar

        self.remove_video_action = QAction("Convert to audio file") #action for removing video
        self.remove_video_action.setIcon(QIcon("icons/play.svg")) #set icon for action
        self.remove_video_action.triggered.connect(self.novid_win) #sending the signal when action is triggered
        self.remove_video_action.setShortcut("Shift+Ctrl+A") #set shortcut for action
        self.video_tools_menu.addAction(self.remove_video_action)

        self.remove_audio_action = QAction("Mute the video")
        self.remove_audio_action.setIcon(QIcon("icons/play.svg"))
        self.remove_audio_action.triggered.connect(self.noaudio_win_)
        self.remove_audio_action.setShortcut("Shift+Ctrl+M")
        self.video_tools_menu.addAction(self.remove_audio_action)

        self.compress_video_action = QAction("Compress the video (Using X265 codec)")
        self.compress_video_action.setIcon(QIcon("icons/play.svg"))
        self.compress_video_action.triggered.connect(self.compress_win) #sending the signal when action is triggered
        self.compress_video_action.setShortcut("Shift+Ctrl+C") #set shortcut for the action
        self.video_tools_menu.addAction(self.compress_video_action)

        self.change_resolution_action = QAction("Change video's resolution") #action for changing the resolution of the video
        self.change_resolution_action.setIcon(QIcon("icons/play.svg")) #set action's icon
        self.change_resolution_action.triggered.connect(self.res_win) #sending the signal when action is triggered
        self.change_resolution_action.setShortcut("Shift+Ctrl+R") #set shortcut for the action
        self.video_tools_menu.addAction(self.change_resolution_action)

    def arihis(self): #history window function
        self.history_win = QDialog() #create the history window
        self.history_win.setStyleSheet("background-color: #2b2b2b;color: #B6BAB1;")
        self.history = open("arihis") #open the history file and read the data
        self.vbox_history = QVBoxLayout() #vertical layout 
        self.text_history = QTextEdit() #container widget for history data
        self.text_history.setReadOnly(True) #set readonly attribute for text container
        self.text_history.setText(self.history.read()) #set the history as a text
        self.history_win.setLayout(self.vbox_history) #set the main layout
        self.vbox_history.addWidget(self.text_history) #add widget
        self.close_btn_history = QPushButton("Close") #close button
        self.close_btn_history.setIcon(QIcon("icons/remove.svg")) #icon for close button
        self.close_btn_history.pressed.connect(lambda: self.history_win.close())
        self.refresh_btn_history = QPushButton("Refresh") #refresh button
        self.refresh_btn_history.setIcon(QIcon("icons/refresh.png")) #refresh button icon
        self.refresh_btn_history.pressed.connect(self.refresh_history)
        self.clear_btn_history = QPushButton("Clear") #clear button
        self.clear_btn_history.setIcon(QIcon("icons/multi_trash.svg"))
        self.clear_btn_history.pressed.connect(self.clear_history) #send signal when button is pressed and clear the history
        self.hbox_history = QHBoxLayout() #herizontal layout
        for i in [self.refresh_btn_history,self.clear_btn_history,self.close_btn_history,]: #add widgets
            self.hbox_history.addWidget(i)
        self.vbox_history.addLayout(self.hbox_history)
        self.vbox_history.setAlignment(self.hbox_history, Qt.AlignBottom | Qt.AlignRight)
        self.history_win.setMinimumSize(640,250) #set the window's max size
        self.history_win.setMaximumSize(640,250) #set the window's min size
        self.history_win.setWindowIcon(QIcon("icons/about.svg")) #history window icon
        self.history_win.setWindowTitle("History") #history window title
        self.history_win.show() #show the history window
    
    def burn_sub(self):
        self.vid_in = ""
        self.sub = ""
        self.vid_out = ""
        self.burn_win = QDialog() #dialog for burnning sub
        self.burn_win.setStyleSheet("background-color: #2b2b2b;color: #B6BAB1;") #dark style for myself
        self.vbox_burn = QVBoxLayout() #vertical layout
        self.burn_win.setLayout(self.vbox_burn)
        self.hbox_in_vid_burn = QHBoxLayout() #herizontal layout
        self.lbl_in_vid_burn = QLabel("Input Video: ")
        self.line_in_vid_burn = QLineEdit() #line edit for input
        self.btn_in_vid_burn = QToolButton() #button for browsing input
        self.btn_in_vid_burn.setText("...") #browse button text
        self.btn_in_vid_burn.pressed.connect(lambda: self.open("video_in_burn"))
        self.hbox_in_vid_burn.addWidget(self.lbl_in_vid_burn) #adding widgets
        self.hbox_in_vid_burn.addWidget(self.line_in_vid_burn)
        self.hbox_in_vid_burn.addWidget(self.btn_in_vid_burn)
        self.vbox_burn.addLayout(self.hbox_in_vid_burn)
        self.hbox_in_sub_burn = QHBoxLayout() #herizontal layout
        self.line_in_sub_burn = QLineEdit() #line edit for browsing sub file
        self.btn_in_sub_burn = QToolButton() #button for browsing sub file
        self.btn_in_sub_burn.setText("...") #text for button
        self.btn_in_sub_burn.pressed.connect(lambda: self.open("sub_in_burn"))
        self.lbl_in_sub_burn = QLabel("Input subtitle: ") #label for sub input
        for i in [self.lbl_in_sub_burn,self.line_in_sub_burn,self.btn_in_sub_burn]: #add widgets
            self.hbox_in_sub_burn.addWidget(i)
        self.vbox_burn.addLayout(self.hbox_in_sub_burn) #add layout
        self.hbox_out_burn = QHBoxLayout() #hbox layout
        self.lbl_out_burn = QLabel("Output Video: ") #label for video output
        self.line_out_burn = QLineEdit() #line edit for video output
        self.btn_out_burn = QToolButton() #button for video output browse
        self.btn_out_burn.setText("...") #button text
        self.btn_out_burn.pressed.connect(lambda: self.open("video_out_burn"))
        for i in [self.lbl_out_burn,self.line_out_burn,self.btn_out_burn]: #add widgets
            self.hbox_out_burn.addWidget(i)
        self.vbox_burn.addLayout(self.hbox_out_burn) #add layout
        self.start_burn = QPushButton("Start")
        self.start_burn.setIcon(QIcon("icons/sub.png"))
        self.start_burn.pressed.connect(lambda: self.start_("sub_burn"))
        self.cancel_burn = QPushButton("Cancel")
        self.cancel_burn.setIcon(QIcon("icons/remove.svg"))
        self.cancel_burn.pressed.connect(lambda: self.burn_win.close())
        self.hbox_burn_btn = QHBoxLayout()
        self.hbox_burn_btn.addWidget(self.start_burn)
        self.hbox_burn_btn.addWidget(self.cancel_burn)
        self.vbox_burn.addLayout(self.hbox_burn_btn)
        self.vbox_burn.setAlignment(self.hbox_burn_btn, Qt.AlignBottom | Qt.AlignRight)
        self.burn_win.setWindowTitle("Burn Subtitle") #set window title
        self.burn_win.setWindowIcon(QIcon("icons/sub.png"))
        self.burn_win.setMinimumSize(500,150)
        self.burn_win.setMaximumSize(500,150)
        self.burn_win.show() #show the window
    
    def noaudio_win_(self):
        self.noaudio_win = QDialog()
        self.noaudio_win.setStyleSheet("background-color: #2b2b2b;color: #B6BAB1;") #dark style for myself
        self.vbox_noaudio = QVBoxLayout()
        self.noaudio_win.setLayout(self.vbox_noaudio)
        self.hbox_in_noaudio = QHBoxLayout()
        self.line_in_noaudio = QLineEdit()
        self.btn_in_noaudio = QToolButton()
        self.btn_in_noaudio.setText("...")
        self.btn_in_noaudio.pressed.connect(lambda: self.open("vid_in_noaudio"))
        self.lbl_in_noaudio = QLabel("Video Input: ")
        for i in [self.lbl_in_noaudio, self.line_in_noaudio, self.btn_in_noaudio]:
            self.hbox_in_noaudio.addWidget(i)
        self.vbox_noaudio.addLayout(self.hbox_in_noaudio)
        self.hbox_out_noaudio = QHBoxLayout()
        self.line_out_noaudio = QLineEdit()
        self.btn_out_noaudio = QToolButton()
        self.btn_out_noaudio.setText("...")
        self.btn_out_noaudio.pressed.connect(lambda: self.open("vid_out_noaudio"))
        self.lbl_out_noaudio = QLabel("Video Output: ")
        for i in [self.lbl_out_noaudio, self.line_out_noaudio, self.btn_out_noaudio]:
            self.hbox_out_noaudio.addWidget(i)
        self.vbox_noaudio.addLayout(self.hbox_out_noaudio)
        self.hbox_btn_noaudio = QHBoxLayout()
        self.start_noaudio = QPushButton("Start")
        self.start_noaudio.setIcon(QIcon("icons/play.svg"))
        self.start_noaudio.pressed.connect(lambda: self.start_("noaudio"))
        self.cancel_noaudio = QPushButton("Cancel")
        self.cancel_noaudio.setIcon(QIcon("icons/remove.svg"))
        self.cancel_noaudio.pressed.connect(lambda: self.noaudio_win.close())
        self.hbox_btn_noaudio.addWidget(self.start_noaudio)
        self.hbox_btn_noaudio.addWidget(self.cancel_noaudio)
        self.vbox_noaudio.addLayout(self.hbox_btn_noaudio)
        self.vbox_noaudio.setAlignment(self.hbox_btn_noaudio, Qt.AlignBottom | Qt.AlignRight)
        self.noaudio_win.setMinimumSize(650,120)
        self.noaudio_win.setMaximumSize(650,120)
        self.noaudio_win.setWindowTitle("Mute the Video")
        self.noaudio_win.setWindowIcon(QIcon("icons/play.svg"))
        self.noaudio_win.show()

    def novid_win(self):
        self.novid_win = QDialog()
        self.novid_win.setStyleSheet("background-color: #2b2b2b;color: #B6BAB1;") #dark style for myself
        self.vbox_novid = QVBoxLayout()
        self.novid_win.setLayout(self.vbox_novid)
        self.hbox_in_novid = QHBoxLayout()
        self.line_in_novid = QLineEdit()
        self.btn_in_novid = QToolButton()
        self.btn_in_novid.setText("...")
        self.btn_in_novid.pressed.connect(lambda: self.open("vid_in_novid"))
        self.lbl_in_novid = QLabel("Video Input: ")
        self.hbox_in_novid.addWidget(self.lbl_in_novid)
        self.hbox_in_novid.addWidget(self.line_in_novid)
        self.hbox_in_novid.addWidget(self.btn_in_novid)
        self.vbox_novid.addLayout(self.hbox_in_novid)
        self.hbox_out_novid = QHBoxLayout()
        self.line_out_novid = QLineEdit()
        self.btn_out_novid = QToolButton()
        self.btn_out_novid.setText("...")
        self.btn_out_novid.pressed.connect(lambda: self.open("audio_out_novid"))
        self.lbl_out_novid = QLabel("Audio Output: ")
        self.hbox_out_novid.addWidget(self.lbl_out_novid)
        self.hbox_out_novid.addWidget(self.line_out_novid)
        self.hbox_out_novid.addWidget(self.btn_out_novid)
        self.vbox_novid.addLayout(self.hbox_out_novid)
        self.hbox_btn_novid = QHBoxLayout()
        self.start_novid = QPushButton("Start")
        self.start_novid.setIcon(QIcon("icons/play.svg"))
        #ffmpeg -i "$input" -vn -acodec libmp3lame "$remove_Format"[NEW].mp3
        self.start_novid.pressed.connect(lambda: self.start_("novid"))
        self.cancel_novid = QPushButton("Cancel")
        self.cancel_novid.setIcon(QIcon("icons/remove.svg"))
        self.cancel_novid.pressed.connect(lambda: self.novid_win.close())
        self.hbox_btn_novid.addWidget(self.start_novid)
        self.hbox_btn_novid.addWidget(self.cancel_novid)
        self.vbox_novid.addLayout(self.hbox_btn_novid)
        self.vbox_novid.setAlignment(self.hbox_btn_novid, Qt.AlignBottom | Qt.AlignRight)
        self.novid_win.setMinimumSize(650,120)
        self.novid_win.setMaximumSize(650,120)
        self.novid_win.setWindowTitle("Convert to audio")
        self.novid_win.setWindowIcon(QIcon("icons/play.svg"))
        self.novid_win.show()


    def compress_win(self):
        self.compress_win = QDialog()
        self.compress_win.setStyleSheet("background-color: #2b2b2b;color: #B6BAB1;") #dark style for myself
        self.vbox_compress = QVBoxLayout()
        self.compress_win.setLayout(self.vbox_compress)
        self.compress_win.setLayout(self.vbox_compress)
        self.line_in_compress = QLineEdit()
        self.btn_in_compress = QToolButton()
        self.btn_in_compress.setText("...")
        self.btn_in_compress.pressed.connect(lambda: self.open("vid_in_compress"))
        self.lbl_in_compress = QLabel("Video Input: ")
        self.hbox_in_compress = QHBoxLayout()
        self.hbox_in_compress.addWidget(self.lbl_in_compress)
        self.hbox_in_compress.addWidget(self.line_in_compress)
        self.hbox_in_compress.addWidget(self.btn_in_compress)
        self.hbox_out_compress = QHBoxLayout()
        self.line_out_compress = QLineEdit()
        self.btn_out_compress = QToolButton()
        self.btn_out_compress.setText("...")
        self.btn_out_compress.pressed.connect(lambda: self.open("vid_out_compress"))
        self.lbl_out_compress = QLabel("Video Output: ")
        self.hbox_out_compress.addWidget(self.lbl_out_compress)
        self.hbox_out_compress.addWidget(self.line_out_compress)
        self.hbox_out_compress.addWidget(self.btn_out_compress)
        self.vbox_compress.addLayout(self.hbox_in_compress)
        self.vbox_compress.addLayout(self.hbox_out_compress)
        self.hbox_btn_compress = QHBoxLayout()
        self.start_btn_compress = QPushButton("Start")
        self.start_btn_compress.setIcon(QIcon("icons/play.svg"))
        self.start_btn_compress.pressed.connect(lambda: self.start_("compress"))
        self.cancel_btn_compress = QPushButton("Cancel")
        self.cancel_btn_compress.setIcon(QIcon("icons/remove.svg"))
        self.cancel_btn_compress.pressed.connect(lambda: self.compress_win.close())
        self.hbox_btn_compress.addWidget(self.start_btn_compress)
        self.hbox_btn_compress.addWidget(self.cancel_btn_compress)
        self.vbox_compress.addLayout(self.hbox_btn_compress)
        self.vbox_compress.setAlignment(self.hbox_btn_compress, Qt.AlignBottom | Qt.AlignRight)
        self.compress_win.setWindowTitle("Compress Video")
        self.compress_win.setWindowIcon(QIcon("icons/play.svg"))
        self.compress_win.setMinimumSize(650,120)
        self.compress_win.setMaximumSize(650,120)
        self.compress_win.show()

    def res_win(self):
        self.res_win = QDialog()
        self.res_win.setStyleSheet("background-color: #2b2b2b;color: #B6BAB1;") #dark style for myself
        self.vbox_res = QVBoxLayout()
        self.res_win.setLayout(self.vbox_res)
        self.hbox_in_res = QHBoxLayout()
        self.lbl_in_res = QLabel("Video Input: ")
        self.line_in_res = QLineEdit()
        self.btn_in_res = QToolButton()
        self.btn_in_res.setText("...")
        self.btn_in_res.pressed.connect(lambda: self.open("vid_in_res"))
        self.hbox_in_res.addWidget(self.lbl_in_res)
        self.hbox_in_res.addWidget(self.line_in_res)
        self.hbox_in_res.addWidget(self.btn_in_res)
        self.vbox_res.addLayout(self.hbox_in_res)
        self.hbox_res = QHBoxLayout()
        self.line_res = QLineEdit()
        self.line_res.setPlaceholderText("Format: WidthxHeight; Example: 1360x768")
        self.lbl_res = QLabel("Resolution Input: ")
        self.hbox_res.addWidget(self.lbl_res)
        self.hbox_res.addWidget(self.line_res)
        self.vbox_res.addLayout(self.hbox_res)
        self.hbox_out_res = QHBoxLayout()
        self.line_out_res = QLineEdit()
        self.btn_out_res = QToolButton()
        self.btn_out_res.setText("...")
        self.btn_out_res.pressed.connect(lambda: self.open("vid_out_res"))
        self.lbl_out_res = QLabel("Video Output: ")
        self.hbox_out_res.addWidget(self.lbl_out_res)
        self.hbox_out_res.addWidget(self.line_out_res)
        self.hbox_out_res.addWidget(self.btn_out_res)
        self.vbox_res.addLayout(self.hbox_out_res)
        self.hbox_btn_res = QHBoxLayout()
        self.start_btn_res = QPushButton("Start")
        self.start_btn_res.pressed.connect(lambda: self.start_("resolution"))
        self.start_btn_res.setIcon(QIcon("icons/play.svg"))
        self.cancel_btn_res = QPushButton("Cancel")
        self.cancel_btn_res.setIcon(QIcon("icons/remove.svg"))
        self.cancel_btn_res.pressed.connect(lambda: self.res_win.close())
        self.hbox_btn_res.addWidget(self.start_btn_res)
        self.hbox_btn_res.addWidget(self.cancel_btn_res)
        self.vbox_res.addLayout(self.hbox_btn_res)
        self.vbox_res.setAlignment(self.hbox_btn_res, Qt.AlignBottom | Qt.AlignRight)
        self.res_win.setWindowIcon(QIcon("icons/play.svg"))
        self.res_win.setWindowTitle("Change Video Resolution")
        self.res_win.setMinimumSize(700,150)
        self.res_win.setMaximumSize(700,150)
        self.res_win.show()

    def start_(self,mode):
        if mode == "sub_burn":
            self.progress(['ffmpeg', '-nostats', '-i', self.vid_in_burn, '-vf', self.sub_burn, self.vid_out_burn], self.vid_in_burn, self.vid_out_burn, "Subtitle Burn")
            self.command = [ '-vf', self.sub_burn, self.vid_out_burn]

        if mode == "novid":
            self.progress(['ffmpeg', '-i', self.vid_in_novid, '-vn', '-acodec', 'libmp3lame', self.audio_out_novid], self.vid_in_novid, self.audio_out_novid, "Removed Video")
            self.command = [ '-vn', '-acodec', 'libmp3lame', self.audio_out_novid]

        if mode == "noaudio":
            self.progress(['ffmpeg', '-i', self.vid_in_noaudio, '-an', '-c', 'copy', self.vid_out_noaudio], self.vid_in_noaudio, self.vid_out_noaudio, "Removed the Audio Track")
            self.command = [ '-an', '-c', 'copy', self.vid_out_noaudio]

        if mode == "compress":
            self.progress(['ffmpeg', '-i', self.vid_in_compress, self.vid_out_compress], self.vid_in_compress, self.vid_out_compress, "Video Compression")
            self.command = [ self.vid_out_compress]

        if mode == "resolution":
            self.progress(['ffmpeg', '-i', self.vid_in_res, '-s', self.line_res.text(), self.vid_out_res], self.vid_in_res, self.vid_out_res, "Resolution Change")
            self.command = [ '-s', self.line_res.text(), self.vid_out_res]

    def refresh_history(self):
        self.history = open("arihis")
        self.text_history.clear()
        self.text_history.setText(self.history.read())

    def clear_history(self):
        self.history = open("arihis","w")
        self.history.write("")
        self.history.close()
        self.refresh_history()

    def create_history(self,file_name,edit_option):
        self.history = open("arihis","a")
        self.history.write("\n============================================\nFile Name: {}\nConversion Date: {}\nOperation: {}".format(file_name,self.date.toString(),edit_option))
        self.history.close()

    def progress(self,cmd,file_name,input_,edit_mode):
        self.progress_win = QDialog()
        self.progress_win.setStyleSheet("background-color: #2b2b2b;color: #B6BAB1;") #dark style for myself
        self.vbox_progress = QVBoxLayout()
        self.progress_win.setLayout(self.vbox_progress)
        self.lbl_filename = QLabel("File Name: {}".format(file_name))
        self.lbl_frcnt = QLabel()
        self.lbl_totalframes = QLabel()
        self.lbl_elapsed = QLabel()
        self.progressbar_ = QProgressBar()
        self.progressbar_.setRange(0,0)
        self.cancel_btn_progress = QPushButton("Cancel")
        self.cancel_btn_progress.setIcon(QIcon("icons/remove.svg"))
        for i in [self.lbl_filename,self.lbl_frcnt,self.lbl_totalframes,self.lbl_elapsed]:
            self.vbox_progress.addWidget(i)
            self.vbox_progress.setAlignment(i, Qt.AlignLeft)
        self.vbox_progress.addWidget(self.progressbar_)
        self.vbox_progress.addWidget(self.cancel_btn_progress)
        self.cancel_btn_progress.pressed.connect(lambda: self.cancel())
        self.vbox_progress.setAlignment(self.cancel_btn_progress, Qt.AlignBottom | Qt.AlignRight)

        self.progress_win.setWindowIcon(QIcon("icons/play.svg"))
        self.progress_win.setMinimumSize(700,200)
        self.progress_win.setMaximumSize(700,200)
        self.progress_win.show()
        self.cmd = cmd
        self.file_name = file_name
        self.input_ = input_
        self.edit_mode = edit_mode
        self.worker = Worker(self.progress_exec)
        self.threadpool = QThreadPool()
        self.threadpool.start(self.worker)

    def progress_exec(self):
        def ffmpeg_callback(infile: str, outfile: str, vstats_path: str):
            self.cmd = ['ffmpeg', '-nostats', 'loglevel', '0', '-y', '-vstats_file', vstats_path, '-i', infile]+self.command 
            return sp.Popen(['ffmpeg',
                            '-nostats',
                            '-loglevel', '0',
                            '-y',
                            '-vstats_file', vstats_path,
                            '-i', infile,
                            ]+self.command).pid

        def ffmpeg(infile: str, outfile: str, vstats_path: str):
            return sp.Popen(self.cmd).pid
        def on_message_handler(percent: float,
                            fr_cnt: int,
                            total_frames: int,
                            elapsed: float):
            self.lbl_frcnt.setText("Frame Count: {}".format(fr_cnt))
            self.lbl_totalframes.setText("Total Frames: {}".format(total_frames))
            #self.lbl_elapsed.setText("Elapsed Time: {}".format(round(elapsed)))
            #self.progressbar_.setValue(round(percent))
            self.progress_win.setWindowTitle("({}%){}".format(round(percent),self.input_))
        self.date = QDateTime.currentDateTime()
        start(self.file_name,
        self.input_,
        ffmpeg_callback,
        on_message=on_message_handler,
        on_done=None,
        wait_time=1)
        self.progressbar_.setValue(100)
        self.create_history(self.input_,self.edit_mode)
        #if os.path.isfile(download_path):
            #osCommands.xdgOpen(download_path, 'folder', 'file')
        self.progress_win.close()
        sp.Popen(["notify-send", "Operation Completed!", "--icon=$HOME/Aricon_python_git/icons/converter.svg"])
    
    def after_convert(self):
        sp.Popen(["notify-send", "Operation Completed!", "--icon=$HOME/Aricon_python_git/icons/converter.svg"])
        self.finish_dialog = QDialog()
        self.finish_dialog.setStyleSheet("background-color: #2b2b2b;color: #B6BAB1;") #dark style for myself
        self.vbox_finish = QVBoxLayout()
        self.finish_dialog.setLayout(self.vbox_finish)
        self.file_info = QTextEdit("Operation finished successfuly!\nFile Name: {}\nOperation: {}".format(self.input_,self.edit_mode))
        self.open_finish = QPushButton("Open")
        self.open_finish.setIcon(QIcon("icons/file.svg"))
        self.open_finish.pressed.connect(lambda: self.open_finish_func("file"))
        self.openf_finish = QPushButton("Open Containing Folder")
        self.openf_finish.setIcon(QIcon("icons/folder.svg"))
        self.openf_finish.pressed.connect(lambda: self.open_finish_func("folder"))
        self.close_finish = QPushButton("Close")
        self.close_finish.setIcon(QIcon("icons/remove.svg"))
        self.close_finish.pressed.connect(lambda: self.finish_dialog.close())
        self.vbox_finish.addWidget(self.file_info)
        self.hbox_finish = QHBoxLayout()
        for i in [self.open_finish,self.openf_finish,self.close_finish]:
            self.hbox_finish.addWidget(i)
        self.vbox_finish.addLayout(self.hbox_finish)
        self.vbox_finish.setAlignment(self.hbox_finish, Qt.AlignBottom | Qt.AlignRight)
        self.finish_dialog.setMinimumSize(640,250)
        self.finish_dialog.setMaximumSize(640,250)
        self.finish_dialog.setWindowTitle("Operation Completed!")
        self.finish_dialog.setWindowIcon(QIcon("icons/converter.png"))
        self.finish_dialog.show()

    def cancel(self):
        os.system("killall ffmpeg")
        self.progress_win.close()

    def open_finish_func(self,mode):
        if mode == "file":
                #sp.Popen(["xdg-open", self.input_])
                os.system("xdg-open {}".format(self.input_))
        if mode == "folder":
            path = path.split("/")
            path.pop()
            path.pop(0)
            for i in path:
                path = path+"/"+i
            path = path+"/"
            #sp.Popen(["xdg-open", path])
            os.system("xdg-open {}".format(path))

    def open(self,mode):
        if mode == "video_in_burn":
            vid=QFileDialog.getOpenFileName(self.burn_win,'Open the Video', "", '')
            self.vid_in_burn = ("{}".format(vid[0]))
            self.line_in_vid_burn.setText(self.vid_in_burn)
            self.vid_out_burn = ("{0}_{2}{1}".format(*os.path.splitext(vid[0]) + ('output',)))
            self.line_out_burn.setText(self.vid_out_burn)
            
        if mode == "video_out_burn":
            vid=QFileDialog.getSaveFileName(self.burn_win,'Save the Video', "", '')
            self.line_out_burn.setText(vid[0])
            self.vid_out_burn = ("{}".format(vid[0]))

        if mode == "sub_in_burn":
            sub=QFileDialog.getOpenFileName(self.burn_win,'Open the Subtitle', "", '')
            self.line_in_sub_burn.setText(sub[0])
            self.sub_burn = ("subtitles='{}'".format(sub[0]))

        if mode == "vid_in_novid":
            vid=QFileDialog.getOpenFileName(self.novid_win,'Open the Video', "", '')
            self.vid_in_novid = ("{}".format(vid[0]))
            self.line_in_novid.setText(self.vid_in_novid)
            self.audio_out_novid = ("{0}_{2}.mp3".format(*os.path.splitext(vid[0]) + ('output',)))
            self.line_out_novid.setText(self.audio_out_novid)

        if mode == "audio_out_novid":
            audio=QFileDialog.getSaveFileName(self.novid_win,'Save the Audio', "", '')
            self.audio_out_novid = ("{}".format(audio[0]))
            self.line_out_novid.setText(self.audio_out_novid)

        if mode == "vid_in_noaudio":
            vid=QFileDialog.getOpenFileName(self.noaudio_win,'Open the Video', "", '')
            self.vid_in_noaudio = ("{}".format(vid[0]))
            self.line_in_noaudio.setText(self.vid_in_noaudio)
            self.vid_out_noaudio = ("{0}_{2}{1}".format(*os.path.splitext(vid[0]) + ('output',)))
            self.line_out_noaudio.setText(elf.vid_out_noaudio)

        if mode == "vid_out_noaudio":
            vid=QFileDialog.getSaveFileName(self.noaudio_win,'Save the Video', "", '')
            self.vid_out_noaudio = ("{}".format(vid[0]))
            self.line_out_noaudio.setText(elf.vid_out_noaudio)

        if mode == "vid_in_compress":
            vid=QFileDialog.getOpenFileName(self.compress_win,'Open the Video', "", '')
            self.vid_in_compress = ("{}".format(vid[0]))
            self.line_in_compress.setText(self.vid_in_compress)
            self.vid_out_compress = ("{0}_{2}{1}".format(*os.path.splitext(vid[0]) + ('output',)))
            self.line_out_compress.setText(self.vid_out_compress)

        if mode == "vid_out_compress":
            vid=QFileDialog.getSaveFileName(self.compress_win,'Save the Video', "", '')
            self.vid_out_compress = ("{}".format(vid[0]))
            self.line_out_compress.setText(self.vid_out_compress)

        if mode == "vid_in_res":
            vid=QFileDialog.getOpenFileName(self.res_win,'Open the Video', "", '')
            self.vid_in_res = ("{}".format(vid[0]))
            self.line_in_res.setText(self.vid_in_res)
            self.vid_out_res = ("{0}_{2}{1}".format(*os.path.splitext(vid[0]) + ('output',)))
            self.line_out_res.setText(self.vid_out_res)

        if mode == "vid_out_res":
            vid=QFileDialog.getSaveFileName(self.res_win,'Save the Video', "", '')
            self.vid_out_res = ("{}".format(vid[0]))
            self.line_out_res.setText(self.vid_out_res)


if __name__ == "__main__":
    app = QApplication([])
    win = MainWindow()
    sys.exit(app.exec_())
