# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './pc_wnd_main.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_wndMain(object):
    def setupUi(self, wndMain):
        wndMain.setObjectName(_fromUtf8("wndMain"))
        wndMain.resize(1218, 893)
        self.centralwidget = QtGui.QWidget(wndMain)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        wndMain.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(wndMain)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1218, 28))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuProcess = QtGui.QMenu(self.menubar)
        self.menuProcess.setObjectName(_fromUtf8("menuProcess"))
        self.menu_Help = QtGui.QMenu(self.menubar)
        self.menu_Help.setObjectName(_fromUtf8("menu_Help"))
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName(_fromUtf8("menuView"))
        wndMain.setMenuBar(self.menubar)
        self.mainToolBar = QtGui.QToolBar(wndMain)
        self.mainToolBar.setMovable(False)
        self.mainToolBar.setAllowedAreas(QtCore.Qt.TopToolBarArea)
        self.mainToolBar.setFloatable(False)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        wndMain.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusbar = QtGui.QStatusBar(wndMain)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        wndMain.setStatusBar(self.statusbar)
        self.actionAbout_Qt = QtGui.QAction(wndMain)
        self.actionAbout_Qt.setObjectName(_fromUtf8("actionAbout_Qt"))
        self.actionAbout = QtGui.QAction(wndMain)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.act_select_TTY_port = QtGui.QAction(wndMain)
        self.act_select_TTY_port.setObjectName(_fromUtf8("act_select_TTY_port"))
        self.actionStart_Monitor = QtGui.QAction(wndMain)
        self.actionStart_Monitor.setObjectName(_fromUtf8("actionStart_Monitor"))
        self.actionStop_Monitor = QtGui.QAction(wndMain)
        self.actionStop_Monitor.setObjectName(_fromUtf8("actionStop_Monitor"))
        self.actionNew = QtGui.QAction(wndMain)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionOpen = QtGui.QAction(wndMain)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionSave = QtGui.QAction(wndMain)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSave_as = QtGui.QAction(wndMain)
        self.actionSave_as.setObjectName(_fromUtf8("actionSave_as"))
        self.actionExit = QtGui.QAction(wndMain)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionRun = QtGui.QAction(wndMain)
        self.actionRun.setObjectName(_fromUtf8("actionRun"))
        self.actionStop = QtGui.QAction(wndMain)
        self.actionStop.setObjectName(_fromUtf8("actionStop"))
        self.actionToolbar = QtGui.QAction(wndMain)
        self.actionToolbar.setObjectName(_fromUtf8("actionToolbar"))
        self.actionConfiguration = QtGui.QAction(wndMain)
        self.actionConfiguration.setObjectName(_fromUtf8("actionConfiguration"))
        self.actionChart = QtGui.QAction(wndMain)
        self.actionChart.setObjectName(_fromUtf8("actionChart"))
        self.actionAbout_Qt_2 = QtGui.QAction(wndMain)
        self.actionAbout_Qt_2.setObjectName(_fromUtf8("actionAbout_Qt_2"))
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuProcess.addAction(self.actionRun)
        self.menuProcess.addAction(self.actionStop)
        self.menu_Help.addAction(self.actionAbout)
        self.menu_Help.addAction(self.actionAbout_Qt_2)
        self.menuView.addAction(self.actionToolbar)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionChart)
        self.menuView.addAction(self.actionConfiguration)
        self.menuView.addSeparator()
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuProcess.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.mainToolBar.addSeparator()

        self.retranslateUi(wndMain)
        QtCore.QMetaObject.connectSlotsByName(wndMain)

    def retranslateUi(self, wndMain):
        wndMain.setWindowTitle(_translate("wndMain", "PAPI Calibra v.0.1", None))
        self.menuFile.setTitle(_translate("wndMain", "&File", None))
        self.menuProcess.setTitle(_translate("wndMain", "Process", None))
        self.menu_Help.setTitle(_translate("wndMain", "&Help", None))
        self.menuView.setTitle(_translate("wndMain", "View", None))
        self.mainToolBar.setWindowTitle(_translate("wndMain", "Toolbar", None))
        self.actionAbout_Qt.setText(_translate("wndMain", "About Qt", None))
        self.actionAbout.setText(_translate("wndMain", "About", None))
        self.act_select_TTY_port.setText(_translate("wndMain", "Select TTY Port", None))
        self.actionStart_Monitor.setText(_translate("wndMain", "Start Monitor", None))
        self.actionStop_Monitor.setText(_translate("wndMain", "Stop Monitor", None))
        self.actionNew.setText(_translate("wndMain", "new", None))
        self.actionOpen.setText(_translate("wndMain", "open", None))
        self.actionSave.setText(_translate("wndMain", "save", None))
        self.actionSave_as.setText(_translate("wndMain", "save as", None))
        self.actionExit.setText(_translate("wndMain", "exit", None))
        self.actionRun.setText(_translate("wndMain", "run", None))
        self.actionStop.setText(_translate("wndMain", "stop", None))
        self.actionToolbar.setText(_translate("wndMain", "toolbar", None))
        self.actionConfiguration.setText(_translate("wndMain", "configuration", None))
        self.actionChart.setText(_translate("wndMain", "chart", None))
        self.actionAbout_Qt_2.setText(_translate("wndMain", "About Qt", None))

