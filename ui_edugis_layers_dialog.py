# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_edugis_layers_dialog.ui'
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

class Ui_EduGisLayersDialog(object):
    def setupUi(self, EduGisLayersDialog):
        EduGisLayersDialog.setObjectName(_fromUtf8("EduGisLayersDialog"))
        EduGisLayersDialog.resize(480, 600)
        EduGisLayersDialog.setMinimumSize(QtCore.QSize(400, 400))
        self.verticalLayout = QtGui.QVBoxLayout(EduGisLayersDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.treeWidget = QtGui.QTreeWidget(EduGisLayersDialog)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.treeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.treeWidget.header().setVisible(False)
        self.verticalLayout.addWidget(self.treeWidget)
        self.widget = QtGui.QWidget(EduGisLayersDialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.addButton = QtGui.QPushButton(self.widget)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.horizontalLayout.addWidget(self.addButton)
        self.cancelButton = QtGui.QPushButton(self.widget)
        self.cancelButton.setDefault(False)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(EduGisLayersDialog)
        QtCore.QMetaObject.connectSlotsByName(EduGisLayersDialog)

    def retranslateUi(self, EduGisLayersDialog):
        EduGisLayersDialog.setWindowTitle(_translate("EduGisLayersDialog", "Add EduGIS Layers", None))
        self.addButton.setText(_translate("EduGisLayersDialog", "Add", None))
        self.cancelButton.setText(_translate("EduGisLayersDialog", "Cancel", None))

