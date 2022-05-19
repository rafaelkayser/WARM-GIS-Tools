# -*- coding: utf-8 -*-
"""
 ***************************************************************************
    MBG

    Processing
                             -------------------
        begin                : 2017-07-01
        updated              : 2019-10-28 by Leonardo Laipelt
        copyright            : (C) 2017 by HGE-IPH
        email                : martinbiancho@hotmail.com
 ***************************************************************************

 ***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************
"""

import os

from PyQt5 import QtGui, uic
from PyQt5.QtCore import pyqtSignal


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'WARMGIS_Tools_dockwidget_base.ui'))

FORM_CLASS2, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'wid_open_project.ui'))

FORM_CLASS_BAL, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'wid_run_balance.ui'))

FORM_CLASS_ins_wit_pon, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'wid_ins_wit_pon.ui'))

FORM_CLASS_ins_wit_tab, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'wid_ins_wit_tab.ui'))

FORM_CLASS_ins_stream_data, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'wid_ins_stream_data.ui'))

FORM_CLASS_ins_lan_pon, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'wid_ins_lan_pon.ui'))

FORM_CLASS_ins_lan_tab, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'wid_ins_lan_tab.ui'))

FORM_CLASS_qual_par, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'wid_qual_par.ui'))

FORM_CLASS_ins_res_pon, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'wid_ins_res_pon.ui'))

FORM_CLASS_qual_obs, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'wid_qual_obs.ui'))

FORM_CLASS_RUN_QUAL, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'wid_run_qual.ui'))


from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from qgis.core import QgsProject

class Widget(QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.setupUi(self)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()



class wid_open_proj(QDialog, FORM_CLASS2):
    def __init__(self, parent=None):
        """Constructor."""
        super(wid_open_proj, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

class wid_ins_stream_data(QDialog, FORM_CLASS_ins_stream_data):
    def __init__(self, parent=None):
        """Constructor."""
        super(wid_ins_stream_data, self).__init__(parent)
        self.setupUi(self)


class wid_run_balance(QDialog, FORM_CLASS_BAL):
    def __init__(self, parent=None):
        """Constructor."""
        super(wid_run_balance, self).__init__(parent)
        self.setupUi(self)


class wid_run_qual(QDialog, FORM_CLASS_RUN_QUAL):
    def __init__(self, parent=None):
        """Constructor."""
        super(wid_run_qual, self).__init__(parent)
        self.setupUi(self)


class wid_ins_wit_pon(QDialog, FORM_CLASS_ins_wit_pon):
    def __init__(self, parent=None):
        """Constructor."""
        super(wid_ins_wit_pon, self).__init__(parent)
        self.setupUi(self)
        
class wid_ins_wit_tab(QDialog, FORM_CLASS_ins_wit_tab):
    def __init__(self, parent=None):
        """Constructor."""
        super(wid_ins_wit_tab, self).__init__(parent)
        self.setupUi(self)        
        
        

class wid_ins_lan_pon(QDialog, FORM_CLASS_ins_lan_pon):
    def __init__(self, parent=None):
        """Constructor."""
        super(wid_ins_lan_pon, self).__init__(parent)
        self.setupUi(self)

class wid_ins_lan_tab(QDialog, FORM_CLASS_ins_lan_tab):
    def __init__(self, parent=None):
        """Constructor."""
        super(wid_ins_lan_tab, self).__init__(parent)
        self.setupUi(self)


class wid_ins_res_pon(QDialog, FORM_CLASS_ins_res_pon):
    def __init__(self, parent=None):
        """Constructor."""
        super(wid_ins_res_pon, self).__init__(parent)
        self.setupUi(self)




class wid_qual_par(QDialog, FORM_CLASS_qual_par):
    def __init__(self, parent=None):
        """Constructor."""
        super(wid_qual_par, self).__init__(parent)
        self.setupUi(self)


class wid_qual_obs(QDialog, FORM_CLASS_qual_obs):
    def __init__(self, parent=None):
        """Constructor."""
        super(wid_qual_obs, self).__init__(parent)
        self.setupUi(self)

