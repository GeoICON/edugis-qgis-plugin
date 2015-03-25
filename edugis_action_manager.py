# -*- coding: utf-8 -*-

import os.path

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import QDomDocument

from qgis.core import *

try:
    from PyQt4.QtCore import QString
except ImportError:
    QString = str

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

import resources_rc

from edugis_layers_dialog import EduGisLayersDialog


class EduGisActionManager(object):
    def __init__(self, iface, plugin):
        self.__iface = iface
        self.__plugin = plugin
        self.__mw = self.__iface.mainWindow()
        self.__iconPathTemplate = ":/plugins/edugis/images/icons/%s"
        self.__describeItems()
        self.__groups = {}
        self.__toolbars = {}
        self.__actions = {}
        self.__buildActions()
        self.__assignHandlers()

        plugin_dir = os.path.dirname(__file__)
        data_root_dir = plugin_dir + "/data"
        self.__layersDialog = EduGisLayersDialog(data_root_dir)
        QObject.connect(self.__layersDialog, SIGNAL("accepted()"), self.__on_layers_dialog_accepted)
        self.__layerPathTemplate = ":/plugins/edugis/images/icons/%s"


    def log(self, message):
        QgsMessageLog.logMessage(message, "EduGIS", QgsMessageLog.INFO)


    def __describeItems(self):

        self.__action_items = [

            { "name": "gi_add_edugis_layer"          , "group": None          , "toolbar": "gi_layers_toolbar"     , "icon": "gi_add_edugis_layer.png"          , "checkable": False  , "bindTo": None                        , "toolTip": "Add EduGIS Layer"     },
            { "name": "gi_remove_layers"             , "group": None          , "toolbar": "gi_layers_toolbar"     , "icon": "gi_remove_layers.png"             , "checkable": False  , "bindTo": "mActionRemoveLayer"        , "toolTip": "Remove Layers(s)"     },
            { "name": "gi_open_project"              , "group": None          , "toolbar": "gi_layers_toolbar"     , "icon": "gi_open_project.png"              , "checkable": False  , "bindTo": "mActionOpenProject"        , "toolTip": "Open Project"         },
            { "name": "gi_save_project"              , "group": None          , "toolbar": "gi_layers_toolbar"     , "icon": "gi_save_project.png"              , "checkable": False  , "bindTo": "mActionSaveProject"        , "toolTip": "Save Project"         },
            { "name": "gi_add_vector_layer"          , "group": None          , "toolbar": "gi_layers_toolbar"     , "icon": "gi_add_vector_layer.png"          , "checkable": False  , "bindTo": None                        , "toolTip": "Add Vector Layer"     },
            { "name": "gi_add_raster_layer"          , "group": None          , "toolbar": "gi_layers_toolbar"     , "icon": "gi_add_raster_layer.png"          , "checkable": False  , "bindTo": "mActionAddRasterLayer"     , "toolTip": "Add Raster Layer"     },

            { "name": "gi_pan"                       , "group": "gi_map_tool" , "toolbar": "gi_navigation_toolbar" , "icon": "gi_pan.png"                       , "checkable": True   , "bindTo": "mActionPan"                , "toolTip": "Pan Map"           },
            { "name": "gi_zoom_in"                   , "group": "gi_map_tool" , "toolbar": "gi_navigation_toolbar" , "icon": "gi_zoom_in.png"                   , "checkable": True   , "bindTo": "mActionZoomIn"             , "toolTip": "Zoom In"           },
            { "name": "gi_zoom_out"                  , "group": "gi_map_tool" , "toolbar": "gi_navigation_toolbar" , "icon": "gi_zoom_out.png"                  , "checkable": True   , "bindTo": "mActionZoomOut"            , "toolTip": "Zoom Out"          },
            { "name": "gi_zoom_full"                 , "group": None          , "toolbar": "gi_navigation_toolbar" , "icon": "gi_zoom_full.png"                 , "checkable": False  , "bindTo": "mActionZoomFullExtent"     , "toolTip": "Zoom Full"         },

            { "name": "gi_zoom_to_selection"         , "group": None          , "toolbar": "gi_selection_toolbar"  , "icon": "gi_zoom_to_selection.png"         , "checkable": False  , "bindTo": "mActionZoomToSelected"     , "toolTip": "Zoom to Selection" },
            { "name": "gi_select_single"             , "group": "gi_map_tool" , "toolbar": "gi_selection_toolbar"  , "icon": "gi_select_single.png"             , "checkable": True   , "bindTo": "mActionSelectFeatures"     , "toolTip": "Select Single Feature"             },
            { "name": "gi_select_polygon"            , "group": "gi_map_tool" , "toolbar": "gi_selection_toolbar"  , "icon": "gi_select_polygon.png"            , "checkable": True   , "bindTo": "mActionSelectPolygon"      , "toolTip": "Select Features by Polygon"        },
            { "name": "gi_select_radius"             , "group": "gi_map_tool" , "toolbar": "gi_selection_toolbar"  , "icon": "gi_select_radius.png"             , "checkable": True   , "bindTo": "mActionSelectRadius"       , "toolTip": "Select Features by Radius"         },
            { "name": "gi_deselect_all"              , "group": None          , "toolbar": "gi_selection_toolbar"  , "icon": "gi_deselect_all.png"              , "checkable": False  , "bindTo": "mActionDeselectAll"        , "toolTip": "Deselect Features from All Layers" },

            { "name": "gi_identify"                  , "group": "gi_map_tool" , "toolbar": "gi_attributes_toolbar" , "icon": "gi_identify.png"                  , "checkable": True   , "bindTo": "mActionIdentify"           , "toolTip": "Identify Features"    },
            { "name": "gi_layer_properties"          , "group": None          , "toolbar": "gi_attributes_toolbar" , "icon": "gi_layer_properties.png"          , "checkable": False  , "bindTo": "mActionLayerProperties"    , "toolTip": "Layer Properties"     },
            { "name": "gi_open_table"                , "group": None          , "toolbar": "gi_attributes_toolbar" , "icon": "gi_open_table.png"                , "checkable": False  , "bindTo": "mActionOpenTable"          , "toolTip": "Open Attribute Table" },
            { "name": "gi_measure_line"              , "group": "gi_map_tool" , "toolbar": "gi_attributes_toolbar" , "icon": "gi_measure_line.png"              , "checkable": True   , "bindTo": "mActionMeasure"            , "toolTip": "Measure Line"         },
            { "name": "gi_measure_area"              , "group": "gi_map_tool" , "toolbar": "gi_attributes_toolbar" , "icon": "gi_measure_area.png"              , "checkable": True   , "bindTo": "mActionMeasureArea"        , "toolTip": "Measure Area"         },
            { "name": "gi_measure_angle"             , "group": "gi_map_tool" , "toolbar": "gi_attributes_toolbar" , "icon": "gi_measure_angle.png"             , "checkable": True   , "bindTo": "mActionMeasureAngle"       , "toolTip": "Measure Angle"        },

            { "name": "gi_query"                     , "group": None          , "toolbar": "gi_processing_toolbar" , "icon": "gi_query.png"                     , "checkable": False  , "bindTo": "mActionLayerSubsetString"  , "toolTip": "Query"                    },
            { "name": "gi_fixed_distance_buffer"     , "group": None          , "toolbar": "gi_processing_toolbar" , "icon": "gi_fixed_distance_buffer.png"     , "checkable": False  , "bindTo": None                        , "toolTip": "Create Buffers"           },
            { "name": "gi_spatial_query"             , "group": None          , "toolbar": "gi_processing_toolbar" , "icon": "gi_spatial_query.png"             , "checkable": False  , "bindTo": "mSpatialQueryAction"       , "toolTip": "Spatial Query"            },

            { "name": "gi_print"                     , "group": None          , "toolbar": "gi_print_toolbar"      , "icon": "gi_print.png"                     , "checkable": False  , "bindTo": "mActionNewPrintComposer"   , "toolTip": "New Print Composer"   },
            { "name": "gi_new_bookmark"              , "group": None          , "toolbar": "gi_print_toolbar"      , "icon": "gi_new_bookmark.png"              , "checkable": False  , "bindTo": "mActionNewBookmark"        , "toolTip": "New Bookmark"         },
            { "name": "gi_show_bookmarks"            , "group": None          , "toolbar": "gi_print_toolbar"      , "icon": "gi_show_bookmarks.png"            , "checkable": False  , "bindTo": "mActionShowBookmarks"      , "toolTip": "Show Bookmarks"       }

        ]

        
    def __buildActions(self):        
        for item in self.__action_items:
            actionName = item["name"]
            icon = QIcon()
            icon.addPixmap(QPixmap(_fromUtf8(self.__iconPathTemplate % item["icon"])), QIcon.Normal, QIcon.Off)
            action = QAction(icon, None, self.__mw)
            action.setObjectName(actionName)
            if "toolTip" in item and not item["toolTip"] is None:
                action.setToolTip(item["toolTip"])
            self.__actions[actionName] = action
            action.setCheckable(item["checkable"])

            groupName = item["group"]
            if not groupName is None:
                if not groupName in self.__groups:
                    group = QActionGroup(self.__mw)
                    group.setObjectName(groupName)
                    self.__groups[groupName] = group
                else:
                    group = self.__groups[groupName]
                group.addAction(action)

            toolbarName = item["toolbar"]
            if not toolbarName is None:
                if not toolbarName in self.__toolbars:
                    self.__toolbars[toolbarName] = []
                self.__toolbars[toolbarName].append(action)
                
            # Binding to native action
            if "bindTo" in item and not item['bindTo'] is None:
                nativeAction = None
                bindTo = item['bindTo']
                actions = self.__mw.findChildren(QAction, bindTo)
                if len(actions) > 0:
                    nativeAction = actions[0]
                if not nativeAction is None:
                    QObject.connect(nativeAction, SIGNAL("toggled(bool)"), action, SLOT("setChecked(bool)"))
                    QObject.connect(action, SIGNAL("toggled(bool)"), nativeAction, SLOT("setChecked(bool)"))
                    QObject.connect(action, SIGNAL("triggered(bool)"), nativeAction, SLOT("trigger()"))                    
                    nativeAction.changed.connect(lambda me=self, src=nativeAction, dst=action : me.__onActionChanged(src, dst))
                    self.__onActionChanged(nativeAction, action)

    def __onActionChanged(self, nativeAction, action):
        action.setEnabled(nativeAction.isEnabled())

    def __assignHandlers(self):
        a = self.__actions
        QObject.connect(a["gi_add_edugis_layer"], SIGNAL("triggered(bool)"), self.__onAddEduGisLayer)
        QObject.connect(a["gi_add_vector_layer"], SIGNAL("triggered(bool)"), self.__onAddVectorLayer)
        QObject.connect(a["gi_fixed_distance_buffer"], SIGNAL("triggered(bool)"), self.__onFixedDistanceBuffer)

    def __onAddEduGisLayer(self):
        self.__layersDialog.execute()

    def __onAddVectorLayer(self):
        path = QFileDialog.getOpenFileName(None, "Open Vector File", None, "Shapefile (*.shp)")
        if not path:
            return
        caption = os.path.basename(path)
        caption = os.path.splitext(caption)[0]
        self.__iface.addVectorLayer(path, caption, "ogr")

    def __onFixedDistanceBuffer(self):
        actions = self.__mw.findChildren(QAction)
        createBuffersAction = None
        for action in actions:
            if action.text() == "Create Buffers" and action.toolTip() == "Create Buffers":
                createBuffersAction = action
                break
        createBuffersAction.trigger()

    def getAction(self, actionName):
        if actionName in self.__actions:
            return self.__actions[actionName]
        else:
            return None

    def getToolbarActions(self, toolbarName):
        if toolbarName in self.__toolbars:
            return self.__toolbars[toolbarName]
        else:
            return []

    def __on_layers_dialog_accepted(self):
        items = self.__layersDialog.getSelectedLayers()
        for item in items:
            self.__loadqlr(item["path"])

    def __loadqlr(self, path):
        # Load xml data into DOM
        with open(path, 'r') as f:
            content = f.read()
        doc = QDomDocument()
        doc.setContent(content)
        # Hacky workaround. We had issue with relative datastores.
        # Transform datastore string from relative to absolute.
        qlr_dir = os.path.dirname(path)
        ds_elements = doc.elementsByTagName('datasource')
        for i in xrange(0, ds_elements.length()):
            ds_element = ds_elements.at(i)
            text_node = ds_element.firstChild()
            rel_path = text_node.nodeValue()
            abs_path = os.path.join(qlr_dir, rel_path)
            text_node.setNodeValue(abs_path)
        # Create layers from qlr DOM
        layers = QgsMapLayer.fromLayerDefinition(doc)
        # Add layers to the map
        QgsMapLayerRegistry.instance().addMapLayers(layers)