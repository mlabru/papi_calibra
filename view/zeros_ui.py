

    def setupUi(self, Form):

        font = QtGui.QFont()
        assert font

        font.setBold(True)
        font.setWeight(75)

        self.frame = QtGui.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(60, 120, 91, 171))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)


        self.lbl_dst = QtGui.QLabel(self.frame)
        self.lbl_dst.setFont(font)

        self.dsb_dst = QtGui.QDoubleSpinBox(self.frame)

        self.lbl_zero = QtGui.QLabel(self.frame)
        self.lbl_zero.setFont(font)

        self.lbl_lat = QtGui.QLabel(self.frame)
        self.lbl_lng = QtGui.QLabel(self.frame)
        self.lbl_alt = QtGui.QLabel(self.frame)

        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        assert self.verticalLayout

        self.verticalLayout.addWidget(self.lbl_dst)
        self.verticalLayout.addWidget(self.dsb_dst)
        self.verticalLayout.addWidget(self.lbl_zero)
        self.verticalLayout.addWidget(self.lbl_lat)
        self.verticalLayout.addWidget(self.lbl_lng)
        self.verticalLayout.addWidget(self.lbl_alt)

