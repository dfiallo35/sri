from PyQt5 import QtCore, QtGui, QtWidgets
from visual_actions import *

class Ui_SRI(object):
    def setupUi(self, SRI):
        SRI.setObjectName("SRI")
        SRI.resize(821, 682)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SRI.sizePolicy().hasHeightForWidth())
        SRI.setSizePolicy(sizePolicy)
        SRI.setTabShape(QtWidgets.QTabWidget.Rounded)
        SRI.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QtWidgets.QWidget(SRI)
        self.centralwidget.setObjectName("centralwidget")
        self.query = QtWidgets.QLineEdit(self.centralwidget)
        self.query.setGeometry(QtCore.QRect(30, 140, 391, 20))
        self.query.setObjectName("query")
        self.run = QtWidgets.QToolButton(self.centralwidget)
        self.run.setGeometry(QtCore.QRect(440, 140, 51, 19))
        self.run.setObjectName("run")
        self.sri_type = QtWidgets.QComboBox(self.centralwidget)
        self.sri_type.setGeometry(QtCore.QRect(30, 40, 201, 22))
        self.sri_type.setObjectName("sri_type")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 211, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 71, 16))
        self.label_2.setObjectName("label_2")
        self.lim = QtWidgets.QSpinBox(self.centralwidget)
        self.lim.setGeometry(QtCore.QRect(380, 30, 42, 22))
        self.lim.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.lim.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.lim.setObjectName("lim")
        self.umbral = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.umbral.setGeometry(QtCore.QRect(380, 60, 62, 22))
        self.umbral.setMaximum(1.0)
        self.umbral.setSingleStep(0.05)
        self.umbral.setObjectName("umbral")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(310, 30, 31, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(310, 60, 31, 16))
        self.label_4.setObjectName("label_4")
        self.limCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.limCheck.setGeometry(QtCore.QRect(350, 30, 16, 17))
        self.limCheck.setText("")
        self.limCheck.setObjectName("limCheck")
        self.umbralCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.umbralCheck.setGeometry(QtCore.QRect(350, 60, 16, 17))
        self.umbralCheck.setText("")
        self.umbralCheck.setObjectName("umbralCheck")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 200, 751, 451))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.output = QtWidgets.QListWidget(self.horizontalLayoutWidget)
        self.output.setObjectName("output")
        self.horizontalLayout.addWidget(self.output)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(310, 90, 31, 16))
        self.label_5.setObjectName("label_5")
        self.alphaCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.alphaCheck.setGeometry(QtCore.QRect(350, 90, 16, 17))
        self.alphaCheck.setText("")
        self.alphaCheck.setObjectName("alphaCheck")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(510, 30, 171, 16))
        self.label_6.setObjectName("label_6")
        self.alpha = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.alpha.setGeometry(QtCore.QRect(380, 90, 62, 22))
        self.alpha.setMaximum(1.0)
        self.alpha.setSingleStep(0.05)
        self.alpha.setObjectName("alpha")
        self.sensitive = QtWidgets.QCheckBox(self.centralwidget)
        self.sensitive.setGeometry(QtCore.QRect(680, 30, 16, 17))
        self.sensitive.setText("")
        self.sensitive.setObjectName("sensitive")
        self.dataset = QtWidgets.QComboBox(self.centralwidget)
        self.dataset.setGeometry(QtCore.QRect(30, 90, 201, 22))
        self.dataset.setObjectName("dataset")
        SRI.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(SRI)
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.statusbar.setFont(font)
        self.statusbar.setObjectName("statusbar")
        SRI.setStatusBar(self.statusbar)
        self.actionsave = QtWidgets.QAction(SRI)
        self.actionsave.setObjectName("actionsave")

        self.sri_type.addItem('Modelo Vectorial')
        self.dataset.addItem('cranfield')

        vectormodel= vector_model.VectorModel()

        self.models= {'VectorModel':vectormodel}

        self.run.clicked.connect(lambda: click_search(self.query,
                                            self.sri_type,
                                            self.dataset,
                                            self.umbral,
                                            self.umbralCheck,
                                            self.sensitive,
                                            self.alpha,
                                            self.alphaCheck,
                                            self.lim,
                                            self.limCheck,
                                            self.output,
                                            self.models))

        self.retranslateUi(SRI)
        QtCore.QMetaObject.connectSlotsByName(SRI)

    def retranslateUi(self, SRI):
        _translate = QtCore.QCoreApplication.translate
        SRI.setWindowTitle(_translate("SRI", "SRI"))
        self.run.setText(_translate("SRI", "Search"))
        self.label.setText(_translate("SRI", "Sistema de Recuperación de Información"))
        self.label_2.setText(_translate("SRI", "DataSet"))
        self.label_3.setText(_translate("SRI", "Limite"))
        self.label_4.setText(_translate("SRI", "Umbral"))
        self.label_5.setText(_translate("SRI", "alpha"))
        self.label_6.setText(_translate("SRI", "Busqueda sencible a mayusculas"))
        self.actionsave.setText(_translate("SRI", "save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SRI = QtWidgets.QMainWindow()
    ui = Ui_SRI()
    ui.setupUi(SRI)
    SRI.show()
    sys.exit(app.exec_())
