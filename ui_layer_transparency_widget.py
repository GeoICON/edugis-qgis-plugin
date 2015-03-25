# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_layer_transparency_widget.ui'
#
# Created: Sat Mar 14 06:11:09 2015
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_LayerTransparencyWidget(object):
    def setupUi(self, LayerTransparencyWidget):
        LayerTransparencyWidget.setObjectName(_fromUtf8("LayerTransparencyWidget"))
        LayerTransparencyWidget.resize(418, 70)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LayerTransparencyWidget.sizePolicy().hasHeightForWidth())
        LayerTransparencyWidget.setSizePolicy(sizePolicy)
        LayerTransparencyWidget.setMinimumSize(QtCore.QSize(0, 70))
        LayerTransparencyWidget.setMaximumSize(QtCore.QSize(16777215, 70))
        LayerTransparencyWidget.setStyleSheet(_fromUtf8(""))
        self.verticalLayout = QtGui.QVBoxLayout(LayerTransparencyWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtGui.QLabel(LayerTransparencyWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.transparencySlider = QtGui.QSlider(LayerTransparencyWidget)
        self.transparencySlider.setMaximum(100)
        self.transparencySlider.setOrientation(QtCore.Qt.Horizontal)
        self.transparencySlider.setObjectName(_fromUtf8("transparencySlider"))
        self.verticalLayout.addWidget(self.transparencySlider)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(LayerTransparencyWidget)
        QtCore.QMetaObject.connectSlotsByName(LayerTransparencyWidget)

    def retranslateUi(self, LayerTransparencyWidget):
        LayerTransparencyWidget.setWindowTitle(_translate("LayerTransparencyWidget", "Form", None))
        self.label.setText(_translate("LayerTransparencyWidget", "Layer transparency:", None))

