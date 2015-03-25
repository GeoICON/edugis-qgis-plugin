# -*- coding: utf-8 -*-

import os.path

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import qgis.utils

from edugis_layer_transparency_selector import EduGisLayerTransparencySelector
from edugis_action_manager import EduGisActionManager
from edugis_toolbar import EduGisToolbar


class EduGisPlugin:

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self._mw = iface.mainWindow()

        self._layerTransparencySelector = EduGisLayerTransparencySelector(iface, self)
        self._actionManager = EduGisActionManager(iface, self)
        self._toolbars = {}

        self._pluginTitle = "EduGIS"

    def __describeToolbars(self):
        self.__toolbar_items = [
            {"name": "gi_layers_toolbar", "color": "#fbeca0", "position": "top"},
            {"name": "gi_navigation_toolbar", "color": "#a6e2df", "position": "top"},
            {"name": "gi_selection_toolbar", "color": "#aac0f2", "position": "top"},
            {"name": "gi_attributes_toolbar", "color": "#f8afba", "position": "top"},
            {"name": "gi_processing_toolbar", "color": "#c89de6", "position": "right"},
            {"name": "gi_print_toolbar", "color": "#c1c7cc", "position": "right"},
        ]


    def __fixUi(self):
        widgets = self._mw.findChildren(QDockWidget, "Layers")
        if len(widgets) > 0:
            layersWidget = widgets[0]
            layersWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
            treeWidget = layersWidget.findChildren(qgis._gui.QgsLayerTreeView, "theLayerTreeView")
            if len(treeWidget) > 0:
                treeWidget = treeWidget[0]
                treeWidget.setStyleSheet("#theLayerTreeView { border: 1px solid #ddd; margin: 0 0 0 2px; }")

        canvas = self.iface.mapCanvas()
        canvas.setStyleSheet("QgsMapCanvas { border: 1px solid #dddddd; margin: 2px 2px 0 0; }")

        widgets = self._mw.findChildren(QStatusBar, "statusbar")
        if len(widgets) > 0:
            sbWidget = widgets[0]
            sbWidget.setStyleSheet("QLineEdit, QComboBox { border: none; }")

        widgets = self._mw.findChildren(QDockWidget, "Browser")
        for widget in widgets:
            widget.deleteLater()

    def initGui(self):
        self._layerTransparencySelector.setVisible(True)
        self.__describeToolbars()
        self.__setupToolbars()
        self.__fixUi()

    def unload(self):
        pass

    def __uiCleanUp(self, objectName):
        items = self._mw.findChildren(QToolBar, objectName)
        for item in items:
            item.deleteLater()

    def __setupToolbars(self):
        for item in self.__toolbar_items:
            toolbarName = item["name"]
            toolbar = EduGisToolbar(self.iface, {
                "name": toolbarName,
                "actions": self._actionManager.getToolbarActions(toolbarName),
                "color": item["color"]
            })
            self._toolbars[toolbarName] = toolbar
            self.__uiCleanUp(toolbarName)
            position = Qt.TopToolBarArea
            if item["position"] == "right":
                position = Qt.RightToolBarArea
            self._mw.addToolBar(position, toolbar.widget())