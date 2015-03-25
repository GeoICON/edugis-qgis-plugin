# -*- coding: utf-8 -*-

from qgis.core import *


class EduGisLogger(object):

  def __init__(self, iface):
    self.__iface = iface


  def log(self, message):
    QgsMessageLog.logMessage(message, "EduGIS", QgsMessageLog.INFO)