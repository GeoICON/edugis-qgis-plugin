# -*- coding: utf-8 -*-

import os
import re

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
from qgis.core import *

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

from ui_edugis_layers_dialog import Ui_EduGisLayersDialog


class EduGisLayersDialog(QtGui.QDialog):

    def __init__(self, data_root_dir):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_EduGisLayersDialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.__setConnections()
        self.__data_root_dir = data_root_dir
        self.__loadTree()

    def __add_leaf(self, name, path, parent_node):
        # Create tree node
        leaf_node = QTreeWidgetItem()
        leaf_node.setData(0, Qt.DisplayRole, name)
        leaf_node.setData(0, Qt.CheckStateRole, Qt.Unchecked)
        leaf_node.setData(0, Qt.UserRole + 0, name)
        leaf_node.setData(0, Qt.UserRole + 1, path)
        # Try to get description
        dpath = re.sub(pattern="\.qlr$", repl=".descr", string=path, flags=re.IGNORECASE)
        if os.path.isfile(dpath):
            file = open(dpath)
            descr = file.read()
            file.close()
            leaf_node.setToolTip(0, descr)
        # Add tree node to the parent node
        parent_node.addChild(leaf_node)

    def __traverse(self, path, name="UNNAMED", level=0, parent_node=None):
        res = os.listdir(path)
        # Filter and sort list of files
        files = [f for f in res if os.path.isfile(os.path.join(path, f))]
        files = [f for f in files if re.match("^.*\.qlr$", f, flags=re.IGNORECASE)]
        files.sort()
        # Filter and sort list of dirs
        dirs = [f for f in res if os.path.isdir(os.path.join(path, f))]
        dirs.sort()
        # Calculate conditions
        is_hidden = re.match("^\.", name)
        has_subdirs = len(dirs) > 0
        qlr_eq_one = len(files) == 1
        qlr_gt_one = len(files) > 1

        folder_node = None

        if level > 0 and not is_hidden and (has_subdirs or qlr_gt_one):
            # Add folder
            folder_node = QTreeWidgetItem()
            folder_node.setData(0, Qt.DisplayRole, name)
            if level == 1:
                self.ui.treeWidget.addTopLevelItem(folder_node)
            else:
                parent_node.addChild(folder_node)

        if not is_hidden and has_subdirs:
            for d in dirs:
                self.__traverse(os.path.join(path, d), d, level + 1, folder_node)

        if level > 0 and qlr_eq_one:
            # Add leaf
            leaf_path = os.path.join(path, files[0])
            self.__add_leaf(name, leaf_path, parent_node)

        if level > 0 and qlr_gt_one:
            for f in files:
                m = re.search("^(.*)\.qlr$", f,  flags=re.IGNORECASE)
                short_fname = m.group(1)
                leaf_path = os.path.join(path, f)
                # Add leaf in case of multiple qlr in one folder
                self.__add_leaf(short_fname, leaf_path, folder_node)

    def __loadTree(self):
        self.__traverse(self.__data_root_dir)

    def __setConnections(self):
        self.connect(self.ui.addButton, SIGNAL("clicked(bool)"), self.accept)
        self.connect(self.ui.cancelButton, SIGNAL("clicked(bool)"), self.reject)

    def __getCheckedItems(self):
        result = []
        topLevelItemCount = self.ui.treeWidget.topLevelItemCount()
        for i in range(topLevelItemCount):
            groupItem = self.ui.treeWidget.topLevelItem(i)
            childCount = groupItem.childCount()
            for j in range(childCount):
                treeItem = groupItem.child(j)
                checked = treeItem.data(0, Qt.CheckStateRole) == Qt.Checked
                if checked == True:
                    result.append(treeItem)
        return result

    def __uncheckAll(self):
        checkedItems = self.__getCheckedItems()
        for item in checkedItems:
            item.setData(0, Qt.CheckStateRole, Qt.Unchecked)

    def execute(self):
        self.__uncheckAll()
        self.show()

    def getSelectedLayers(self):
        result = []
        checkedItems = self.__getCheckedItems()
        for item in checkedItems:
            title = item.data(0, Qt.DisplayRole)
            name = item.data(0, Qt.UserRole + 0)
            path = item.data(0, Qt.UserRole + 1)
            layer_type = item.data(0, Qt.UserRole + 2)
            item = { "name": name, "title": title, "path": path, "layer_type": layer_type }
            result.append(item)
        return result