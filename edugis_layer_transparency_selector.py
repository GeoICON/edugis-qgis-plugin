# -*- coding: utf-8 -*-

import os.path

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
from qgis.core import *

from ui_layer_transparency_widget import Ui_LayerTransparencyWidget


class EduGisLayerTransparencySelector(object):
    def __init__(self, iface, plugin):
        self.__iface = iface
        self.__plugin = plugin
        self.__mainWindow = self.__iface.mainWindow()
        self.__dockwidget = None
        self.__oloWidget = None

    def __setDocWidget(self):
        self.__dockwidget = QDockWidget(self.__iface.mainWindow())
        self.__dockwidget.setObjectName("dwEduGisLayerTransparencySelector")
        self.__dockwidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.__titleWidget = QWidget(self.__dockwidget)
        self.__dockwidget.setTitleBarWidget(self.__titleWidget)
        widget = self.__widget = EduGisLayerTransparencyWidget(self.__iface, self.__dockwidget)
        self.__dockwidget.setWidget(widget)

    def __initGui(self):
        self.__cleanup()
        self.__setDocWidget()
        self.__iface.addDockWidget(Qt.LeftDockWidgetArea, self.__dockwidget)

    def __unload(self):
        self.__dockwidget.close()
        self.__iface.removeDockWidget(self.__dockwidget)
        del self.__widget
        self.__dockwidget = None

    def __cleanup(self):
        items = self.__mainWindow.findChildren(QDockWidget, "dwEduGisLayerTransparencySelector")
        for item in items:
            item.deleteLater()

    def setVisible(self, visible):
        if visible:
            if self.__dockwidget is None:
                self.__initGui()
        else:
            if not (self.__dockwidget is None):
                self.__unload()


class EduGisLayerTransparencyWidget(QWidget, Ui_LayerTransparencyWidget):

    def __init__(self, iface, dockwidget):
        QWidget.__init__(self)
        Ui_LayerTransparencyWidget.__init__(self)
        self.setupUi(self)
        self.__iface = iface
        self.__layer = None
        self.transparencySlider.setValue(0)
        self.setEnabled(False)
        self.transparencySlider.sliderReleased.connect(self._on_slider_released)
        self.__iface.currentLayerChanged.connect(self._on_current_layer_changed)

    @pyqtSlot(QgsMapLayer)
    def _on_slider_released(self):
        transparency = self.transparencySlider.value()
        self.update_layer_transparency(transparency)

    @pyqtSlot(QgsMapLayer)
    def _on_current_layer_changed(self, layer):
        if self.__layer.__class__ in [QgsVectorLayer, QgsRasterLayer]:
            try:
                # Disconnect handler from previously selected layer
                self.__layer.repaintRequested.disconnect(self._on_layer_repaint_requested)
            except Exception:
                pass

        self.__layer = layer

        if self.__layer.__class__ in [QgsVectorLayer, QgsRasterLayer]:
            # Connect handler to newly selected layer
            layer.repaintRequested.connect(self._on_layer_repaint_requested)

        self.__update_slider_view()

    @pyqtSlot()
    def _on_layer_repaint_requested(self):
        self.__update_slider_view()

    def __update_slider_view(self):
        layer = self.__layer
        transparency_is_applicable = False
        transparency = 0
        if layer.__class__ is QgsVectorLayer:
            transparency = layer.layerTransparency()
            transparency_is_applicable = True
        elif layer.__class__ is QgsRasterLayer:
            renderer = layer.renderer()
            opacity = renderer.opacity()
            transparency = 100 * (1.0 - opacity)
            transparency_is_applicable = True
        if not transparency_is_applicable:
            self.transparencySlider.setValue(0)
            self.setEnabled(False)
        else:
            self.transparencySlider.setValue(transparency)
            self.setEnabled(True)

    def update_layer_transparency(self, transparency):
        layer = self.__layer
        if layer.__class__ is QgsVectorLayer:
            layer.setLayerTransparency(transparency)
            layer.triggerRepaint()
        elif layer.__class__ is QgsRasterLayer:
            renderer = layer.renderer()
            renderer.setOpacity((100 - transparency) / 100.0)
            layer.triggerRepaint()

    @pyqtSlot(int)
    def _on_slider_value_changed(self, value):
        layer = self.__layer
        if layer.__class__ is QgsVectorLayer:
            layer.setLayerTransparency(value)
            layer.triggerRepaint()
        elif layer.__class__ is QgsRasterLayer:
            renderer = layer.renderer()
            renderer.setOpacity((100 - value) / 100.0)
            layer.triggerRepaint()