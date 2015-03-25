# -*- coding: utf-8 -*-

def classFactory(iface):
  from edugis_plugin import EduGisPlugin
  return EduGisPlugin(iface)
