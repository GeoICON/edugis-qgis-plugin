# -*- coding: utf-8 -*-


from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *


class EduGisToolbar(object):


  def __init__(self, iface, config):
    self.__iface = iface
    self.__mw = self.__iface.mainWindow()
    self.__iconPathTemplate = ":/plugins/edugis/images/icons/%s"
    self.__config = config
    self.__name = config["name"]
    self.__actions = config["actions"]
    self.__color = config["color"]
    self.__toolbar = None


  def __getStyleSheet(self):
    return """
        QToolBar {
          background-color: %s;
          spacing: 2px;
          padding: 5px;
          border: none;
        }

        QToolButton {
          border-radius: 3px;          
          padding: 3px;
        }
        
        QToolButton:hover {
          background-color: #ff5426;
        }

        QToolButton:pressed  {
          background-color: #ff5426;
        }

        QToolButton:checked  {
          background-color: #ff5426;
        }

    """


  def widget(self):
    if self.__toolbar is None:
      self.__toolbar = QToolBar()
      self.__toolbar.setObjectName(self.__name)
      self.__toolbar.setIconSize(QSize(48,48))
      self.__toolbar.setFloatable(False)
      self.__toolbar.setMovable(False)
      styleSheet = self.__getStyleSheet() % self.__color
      self.__toolbar.setStyleSheet(styleSheet)
      for action in self.__actions:
        self.__toolbar.addAction(action)
    return self.__toolbar


  def name(self):
    return self.__name