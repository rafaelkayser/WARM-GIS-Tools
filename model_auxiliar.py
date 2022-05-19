# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 13:47:10 2022

@author: rafae
"""

from . import shapefile

import numpy as np
import matplotlib.pyplot as plt

from qgis.core import *

from qgis.PyQt.QtWidgets import QMessageBox
from PyQt5.QtWidgets import *
from csv import reader

from qgis.PyQt.QtCore import *


def create_drl_from_iph(self, lyr_drl, lyr_cat, module):
    
    
        inputmini= self.wid_open_proj.lin_path_mini.text()


        miniarq = open(inputmini, 'r')
        minidata = miniarq.read()
        miniarq.close()
        mini = minidata.split('\n')

        #shp = shapefile.Reader(str(path_shape))

        attbs = list()
        catchs = list()
        minis = list()
        xs = list()
        ys = list()
        subs = list()
        areas = list()
        uareas = list()
        rlens = list()
        rslos = list()
        alens = list()
        aslos = list()
        minijuss = list()
        orders = list()
        
        hdrs = list()
        widths = list()
        depth = list()



        #for i in shp.shapeRecords():
        #    attbs.append(i.record[0])

        lenght = len(attbs)

        auxxs = [0]*lenght
        auxys = [0]*lenght
        auxsubs = [0]*lenght
        auxareas = [0]*lenght
        auxuareas = [0]*lenght
        auxrlens = [0]*lenght
        auxrslos = [0]*lenght
        auxalens = [0]*lenght
        auxaslos = [0]*lenght
        auxminijuss = [0]*lenght
        auxorders = [0]*lenght

        for i in range(1, len(mini)-1):
            catchs.append(int(mini[i][:8]))

        for i in range(1, len(mini)-1):
            minis.append(int(mini[i][8:16])) #era mini[i][10:16]

        for i in range(1, len(mini)-1):
            xs.append(float(mini[i][16:31]))

        for i in range(1, len(mini)-1):
            ys.append(float(mini[i][31:46]))

        for i in range(1, len(mini)-1):
            subs.append(int(mini[i][46:54]))

        for i in range(1, len(mini)-1):
            areas.append(float(mini[i][54:69]))

        for i in range(1, len(mini)-1):
            uareas.append(float(mini[i][69:84]))

        for i in range(1, len(mini)-1):
            rlens.append(float(mini[i][84:99]))

        for i in range(1, len(mini)-1):
            rslos.append(float(mini[i][99:114]))

        for i in range(1, len(mini)-1):
            alens.append(float(mini[i][114:129]))

        for i in range(1, len(mini)-1):
            aslos.append(float(mini[i][129:144]))

        for i in range(1, len(mini)-1):
            minijuss.append(int(mini[i][144:152]))

        for i in range(1, len(mini)-1):
            orders.append(int(mini[i][152:160]))


        for i in range(1, len(mini)-1):
            hdrs.append(int(mini[i][160:165]))

        for i in range(1, len(mini)-1):
            widths.append(float(mini[i][165:175]))

        for i in range(1, len(mini)-1):
            depth.append(float(mini[i][175:185]))





        # aux = 0
        if 0 in attbs:
            # attbs.pop(0) # o primeiro valor é '0', ver se é sempre assim
            attbs[attbs.index(0)] = 1
            # aux = 1
        else:
            pass
        
        
        #DRAINAGE LINE  ############################################################################
        
        
        #add columns 
        
        if not (lyr_drl.fields().indexFromName('CodDown_ID') >= 0):
        
        
            if module == 'bal':
                lyr_drl = add_columns_drl_bal(lyr_drl)
            
            if module == 'qual':
                lyr_drl = add_columns_drl_qual(lyr_drl)
            
            
        id_shape=[]
        features = lyr_drl.getFeatures()
        for feat in features:
                id_shape.append(feat.attribute("ID"))
        
        
        #write shapefile
        lyr_drl.startEditing()
        
        
        i = 0
        for i in range(len(catchs)):
            
             a_ind = np.array(np.where(np.array(id_shape) == catchs[i]))
             ind=a_ind[0][0]
            
             lyr_drl.changeAttributeValue(ind, lyr_drl.fields().indexFromName('CodBas_ID'), float(minis[i]))
             lyr_drl.changeAttributeValue(ind, lyr_drl.fields().indexFromName('CodDown_ID'), float(minijuss[i]))
             lyr_drl.changeAttributeValue(ind, lyr_drl.fields().indexFromName('Order_ID'), float(orders[i]))
             lyr_drl.changeAttributeValue(ind, lyr_drl.fields().indexFromName('Mini_ID'), float(minis[i]))
             lyr_drl.changeAttributeValue(ind, lyr_drl.fields().indexFromName('Reserv_ID'), 0)
             lyr_drl.changeAttributeValue(ind, lyr_drl.fields().indexFromName('Length_km'), float(rlens[i]))
             
             if module == 'qual':
             #if (1==1):
                 
                 lyr_drl.changeAttributeValue(ind, lyr_drl.fields().indexFromName('SubWat'), 1)
                 lyr_drl.changeAttributeValue(ind, lyr_drl.fields().indexFromName('Area_km2'), float(areas[i]))
                 lyr_drl.changeAttributeValue(ind, lyr_drl.fields().indexFromName('AreaUp_km2'), float(uareas[i]))
                 lyr_drl.changeAttributeValue(ind, lyr_drl.fields().indexFromName('Slope'), float(rslos[i]/1000))
                 lyr_drl.changeAttributeValue(ind, lyr_drl.fields().indexFromName('Depth_m'), float(depth[i]))
                 lyr_drl.changeAttributeValue(ind, lyr_drl.fields().indexFromName('Width_m'), float(widths[i]))
                 lyr_drl.changeAttributeValue(ind, lyr_drl.fields().indexFromName('Vel_ms'), 0)
        
        
        lyr_drl.commitChanges()
        lyr_drl.updateFields()
        
        
        
        
        # CATCHMENT ######################################################################################
        
        id_shape=[]
        features = lyr_cat.getFeatures()
        for feat in features:
                id_shape.append(feat.attribute("ID"))
        
        
        if not (lyr_cat.fields().indexFromName('CodBas_ID') >= 0):
        
            layer_provider1=lyr_cat.dataProvider()
            layer_provider1.addAttributes([QgsField("CodBas_ID",QVariant.Int)])
        
        
            layer_provider1.addAttributes([QgsField("Load_BOD",QVariant.Double)])        
            layer_provider1.addAttributes([QgsField("Load_Col",QVariant.Double)])
            layer_provider1.addAttributes([QgsField("Load_Po",QVariant.Double)])
            layer_provider1.addAttributes([QgsField("Load_Pi",QVariant.Double)])
            layer_provider1.addAttributes([QgsField("Load_No",QVariant.Double)]) 
            layer_provider1.addAttributes([QgsField("Load_Na",QVariant.Double)])
            layer_provider1.addAttributes([QgsField("Load_Nn",QVariant.Double)])

            lyr_cat.updateFields()
        
        
        
        #write shapefile
        lyr_cat.startEditing()
        
        
        for i in range(len(catchs)):
            
             a_ind = np.array(np.where(np.array(id_shape) == catchs[i]))
             ind=a_ind[0][0]
             lyr_cat.changeAttributeValue(ind, lyr_cat.fields().indexFromName('CodBas_ID'), float(minis[i]))
           
        lyr_cat.commitChanges()
        lyr_cat.updateFields()

        
        return lyr_drl, lyr_cat
    
    


def add_columns_drl_bal(lyr_drl):
    
        layer_provider=lyr_drl.dataProvider()
        layer_provider.addAttributes([QgsField("CodBas_ID",QVariant.Int)])
        layer_provider.addAttributes([QgsField("CodDown_ID",QVariant.Int)])
        layer_provider.addAttributes([QgsField("Order_ID",QVariant.Int)])
        layer_provider.addAttributes([QgsField("Mini_ID",QVariant.Int)])
        layer_provider.addAttributes([QgsField("Reserv_ID",QVariant.Int)])
        layer_provider.addAttributes([QgsField("Length_km",QVariant.Double)])

        
        layer_provider.addAttributes([QgsField("Q_Read_1",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Read_2",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Read_3",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Read_4",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Read_5",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Read_6",QVariant.Double, 'double', 8, 4)])        
        layer_provider.addAttributes([QgsField("Q_Read_7",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Read_8",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Read_9",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Read_10",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Read_11",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Read_12",QVariant.Double, 'double', 8, 4)]) 

        layer_provider.addAttributes([QgsField("Q_Rem_1",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Rem_2",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Rem_3",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Rem_4",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Rem_5",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Rem_6",QVariant.Double, 'double', 8, 4)])        
        layer_provider.addAttributes([QgsField("Q_Rem_7",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Rem_8",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Rem_9",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Rem_10",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Rem_11",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Rem_12",QVariant.Double, 'double', 8, 4)]) 

        layer_provider.addAttributes([QgsField("Q_Def_1",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Def_2",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Def_3",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Def_4",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Def_5",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Def_6",QVariant.Double, 'double', 8, 4)])        
        layer_provider.addAttributes([QgsField("Q_Def_7",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Def_8",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Def_9",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Def_10",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Def_11",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Def_12",QVariant.Double, 'double', 8, 4)]) 

        layer_provider.addAttributes([QgsField("W_Bal_1",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("W_Bal_2",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("W_Bal_3",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("W_Bal_4",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("W_Bal_5",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("W_Bal_6",QVariant.Double, 'double', 8, 4)])        
        layer_provider.addAttributes([QgsField("W_Bal_7",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("W_Bal_8",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("W_Bal_9",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("W_Bal_10",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("W_Bal_11",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("W_Bal_12",QVariant.Double, 'double', 8, 4)]) 


        lyr_drl.updateFields()
        
        return lyr_drl
    
    
def add_columns_drl_qual(lyr_drl):


        layer_provider=lyr_drl.dataProvider()
        layer_provider.addAttributes([QgsField("CodBas_ID",QVariant.Int)])
        layer_provider.addAttributes([QgsField("CodDown_ID",QVariant.Int)])
        layer_provider.addAttributes([QgsField("Order_ID",QVariant.Int)])
        layer_provider.addAttributes([QgsField("Mini_ID",QVariant.Int)])
        layer_provider.addAttributes([QgsField("Reserv_ID",QVariant.Int)])    
        layer_provider.addAttributes([QgsField("SubWat",QVariant.Int)])
        
        layer_provider.addAttributes([QgsField("Area_km2",QVariant.Double)])
        layer_provider.addAttributes([QgsField("AreaUp_km2",QVariant.Double)])
        layer_provider.addAttributes([QgsField("Length_km",QVariant.Double)])
        layer_provider.addAttributes([QgsField("Slope",QVariant.Double)])   
        layer_provider.addAttributes([QgsField("Depth_m",QVariant.Double)])
        layer_provider.addAttributes([QgsField("Width_m",QVariant.Double)])

        layer_provider.addAttributes([QgsField("Q_Read_1",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Read_2",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Read_3",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Read_4",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Read_5",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Read_6",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Read_7",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Read_8",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Read_9",QVariant.Double, 'double', 8, 4)])        
        layer_provider.addAttributes([QgsField("Q_Read_10",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Read_11",QVariant.Double, 'double', 8, 4)])
        layer_provider.addAttributes([QgsField("Q_Read_12",QVariant.Double, 'double', 8, 4)])   
        
        
        
        layer_provider.addAttributes([QgsField("Coef_Kd",QVariant.Double, 'double', 10, 4)])
        layer_provider.addAttributes([QgsField("Coef_Ksd",QVariant.Double, 'double', 10, 4)])
        layer_provider.addAttributes([QgsField("Coef_Ka",QVariant.Double, 'double', 10, 4)])
        layer_provider.addAttributes([QgsField("Coef_Kcol",QVariant.Double, 'double', 10, 4)])   
        layer_provider.addAttributes([QgsField("Coef_Koi",QVariant.Double, 'double', 10, 4)])
        layer_provider.addAttributes([QgsField("Coef_Ksp",QVariant.Double, 'double', 10, 4)])
        layer_provider.addAttributes([QgsField("Coef_Koa",QVariant.Double, 'double', 10, 4)])     
        layer_provider.addAttributes([QgsField("Coef_Kan",QVariant.Double, 'double', 10, 4)])   
        layer_provider.addAttributes([QgsField("Coef_Kden",QVariant.Double, 'double', 10, 4)])
        layer_provider.addAttributes([QgsField("Vel_ms",QVariant.Double, 'double', 10, 4)])
        #layer_provider.addAttributes([QgsField("DO_Sat",QVariant.Double)])
    
    
     
        layer_provider.addAttributes([QgsField("Q_Rem_1",QVariant.Double, 'double', 10, 4)])        
        layer_provider.addAttributes([QgsField("W_Bal_1",QVariant.Double, 'double', 10, 4)]) 
        
        layer_provider.addAttributes([QgsField("Conc_BOD",QVariant.Double, 'double', 10, 4)])        
        layer_provider.addAttributes([QgsField("Conc_DO",QVariant.Double, 'double', 10, 4)])
        layer_provider.addAttributes([QgsField("Conc_Col",QVariant.Double, 'double', 20, 4)])
        layer_provider.addAttributes([QgsField("Conc_Po",QVariant.Double, 'double', 10, 4)])
        layer_provider.addAttributes([QgsField("Conc_Pi",QVariant.Double, 'double', 10, 4)])
        layer_provider.addAttributes([QgsField("Conc_Pt",QVariant.Double, 'double', 10, 4)])
        layer_provider.addAttributes([QgsField("Conc_No",QVariant.Double, 'double', 10, 4)]) 
        layer_provider.addAttributes([QgsField("Conc_Na",QVariant.Double, 'double', 10, 4)])
        #layer_provider.addAttributes([QgsField("Conc_Ni",QVariant.Double)])
        layer_provider.addAttributes([QgsField("Conc_Nn",QVariant.Double, 'double', 10, 4)])
        
        
        layer_provider.addAttributes([QgsField("Enq_BOD",QVariant.Int, 'integer', 2, 1)])
        layer_provider.addAttributes([QgsField("Enq_DO",QVariant.Int, 'integer', 2, 1)])
        layer_provider.addAttributes([QgsField("Enq_Col",QVariant.Int, 'integer', 2, 1)])        
        layer_provider.addAttributes([QgsField("Enq_Pt",QVariant.Int, 'integer', 2, 1)])
        layer_provider.addAttributes([QgsField("Enq_Na",QVariant.Int, 'integer', 2, 1)])
        layer_provider.addAttributes([QgsField("Enq_Tot",QVariant.Int, 'integer', 2, 1)])
        
        
        return lyr_drl


def create_fields_wit(fields):
    
    fields.append(QgsField("CodBas_ID", QVariant.Int))
    
    fields.append(QgsField("Name", QVariant.String))
    fields.append(QgsField("Wit_ID", QVariant.Int))
    fields.append(QgsField("Q_Wit_1", QVariant.Double))
    fields.append(QgsField("Q_Wit_2", QVariant.Double))
    fields.append(QgsField("Q_Wit_3", QVariant.Double))
    fields.append(QgsField("Q_Wit_4", QVariant.Double))
    fields.append(QgsField("Q_Wit_5", QVariant.Double))
    fields.append(QgsField("Q_Wit_6", QVariant.Double))
    
    fields.append(QgsField("Q_Wit_7", QVariant.Double))
    fields.append(QgsField("Q_Wit_8", QVariant.Double))
    fields.append(QgsField("Q_Wit_9", QVariant.Double))
    fields.append(QgsField("Q_Wit_10", QVariant.Double))
    fields.append(QgsField("Q_Wit_11", QVariant.Double))
    fields.append(QgsField("Q_Wit_12", QVariant.Double))
    
    return fields
    
    
def create_fields_efl(fields):

    fields.append(QgsField("CodBas_ID", QVariant.Int))
    
    fields.append(QgsField("Name", QVariant.String))
    fields.append(QgsField("Efl_ID", QVariant.Int))
    fields.append(QgsField("Q_Inflow", QVariant.Double))
    fields.append(QgsField("Conc_BOD", QVariant.Double))
    fields.append(QgsField("Conc_DO", QVariant.Double))
    fields.append(QgsField("Conc_Col", QVariant.Double))
    fields.append(QgsField("Conc_Po", QVariant.Double))
    fields.append(QgsField("Conc_Pi", QVariant.Double))
    fields.append(QgsField("Conc_No", QVariant.Double))
    fields.append(QgsField("Conc_Na", QVariant.Double))
    #fields.append(QgsField("Conc_Ni", QVariant.Double))
    fields.append(QgsField("Conc_Nn", QVariant.Double))
    
    return fields


def create_fields_res(fields):

    fields.append(QgsField("Name", QVariant.String))
    fields.append(QgsField("Res_ID", QVariant.Int))
    fields.append(QgsField("CodBas_ID", QVariant.Int))
    fields.append(QgsField("Q_Rel_1", QVariant.Double))
    fields.append(QgsField("Q_Subs_1", QVariant.Double))
    
    return fields


#############################################################################################################################################################

def read_streamflow_file(self):
    
    path = self.wid_ins_stream_data.lin_path_str.text()
    
    if self.wid_ins_stream_data.rbt_str_siaqua.isChecked()==True:
    
        miniarq = open(path, 'r')
        minidata = miniarq.read()
        miniarq.close()
        mini = minidata.split('\n')

        #shp = shapefile.Reader(str(path_shape))

        minis = list()
        q50s = list()
        q70s = list()
        q90s = list()
        q95s = list()
        qmeans = list()
        qmins = list()


        for i in range(1, len(mini)-1):
            minis.append(float(mini[i][:10]))

        for i in range(1, len(mini)-1):
            q50s.append(float(mini[i][40:50]))

        for i in range(1, len(mini)-1):
            q70s.append(float(mini[i][50:60]))

        for i in range(1, len(mini)-1):
            q90s.append(float(mini[i][60:70]))

        for i in range(1, len(mini)-1):
            q95s.append(float(mini[i][70:80]))

        for i in range(1, len(mini)-1):
            qmeans.append(float(mini[i][140:150]))

        for i in range(1, len(mini)-1):
            qmins.append(float(mini[i][160:170]))
            
            

    if self.wid_ins_stream_data.rbt_str_month.isChecked()==True:

        miniarq = open(path, 'r')
        minidata = miniarq.read()
        miniarq.close()
        mini = minidata.split('\n')

        #shp = shapefile.Reader(str(path_shape))

        minis = list()
        qjan = list()
        qfeb = list()
        qmar = list()
        qapr = list()
        qmay = list()
        qjun = list()
        qjul = list()
        qaug = list()
        qsep = list()
        qoct = list()
        qnov = list()
        qdec = list()



        for i in range(0, len(mini)-1):
            minis.append(int(mini[i][:6]))

        for i in range(0, len(mini)-1):
            qjan.append(float(mini[i][6:16]))
        for i in range(0, len(mini)-1):
            qfeb.append(float(mini[i][16:26]))
        for i in range(0, len(mini)-1):
            qmar.append(float(mini[i][26:36]))
        for i in range(0, len(mini)-1):
            qapr.append(float(mini[i][36:46]))
        for i in range(0, len(mini)-1):
            qmay.append(float(mini[i][46:56]))
        for i in range(0, len(mini)-1):
            qjun.append(float(mini[i][56:66]))

        for i in range(0, len(mini)-1):
            qjul.append(float(mini[i][66:76]))
        for i in range(0, len(mini)-1):
            qaug.append(float(mini[i][76:86]))
        for i in range(0, len(mini)-1):
            qsep.append(float(mini[i][86:96]))
        for i in range(0, len(mini)-1):
            qoct.append(float(mini[i][96:106]))
        for i in range(0, len(mini)-1):
            qnov.append(float(mini[i][106:116]))
        for i in range(0, len(mini)-1):
            qdec.append(float(mini[i][116:126]))
            
            
    #fim condicional tipo de arquivo    #########################################################3        
            
            
    def  switch(case):
        if case == 'Q50':
            return q50s
        if case == 'Q70':
            return q70s                
        if case == 'Q90':
            return q90s            
        if case == 'Q95':
            return q95s             
        if case == 'Qmean':
            return qmeans             
        if case == 'Qmin':
            return qmins
                
        if case == 'Qjan':
            return qjan
        if case == 'Qfeb':
            return qfeb                
        if case == 'Qmar':
            return qmar            
        if case == 'Qapr':
            return qapr             
        if case == 'Qmay':
            return qmay             
        if case == 'Qjun':
            return qjun

        if case == 'Qjul':
            return qjul
        if case == 'Qaug':
            return qaug                
        if case == 'Qsep':
            return qsep            
        if case == 'Qoct':
            return qoct             
        if case == 'Qnov':
            return qnov             
        if case == 'Qdec':
            return qdec


                
    id_shape=[]
    features = self.lyr_drl.getFeatures()
    for feat in features:
        id_shape.append(feat.attribute("Mini_ID"))
                
                
    ncen = int(self.wid_ins_stream_data.cbx_str_ncen.currentText())
        
        
    list_=[self.wid_ins_stream_data.cbx_str_1.currentText(),
               self.wid_ins_stream_data.cbx_str_2.currentText(),
               self.wid_ins_stream_data.cbx_str_3.currentText(),
               self.wid_ins_stream_data.cbx_str_4.currentText(),
               self.wid_ins_stream_data.cbx_str_5.currentText(),
               self.wid_ins_stream_data.cbx_str_6.currentText(),
               self.wid_ins_stream_data.cbx_str_7.currentText(),
               self.wid_ins_stream_data.cbx_str_8.currentText(),
               self.wid_ins_stream_data.cbx_str_9.currentText(),
               self.wid_ins_stream_data.cbx_str_10.currentText(),
               self.wid_ins_stream_data.cbx_str_11.currentText(),
               self.wid_ins_stream_data.cbx_str_12.currentText()]

        
    #write shapefile
    self.lyr_drl.startEditing()
        
    for i in range(len(minis)):
        a_ind = np.array(np.where(np.array(id_shape) == minis[i]))
        ind=a_ind[0][0]
            
        for ic in range(ncen):
            qinput = switch(str(list_[ic]))
            self.lyr_drl.changeAttributeValue(ind, self.lyr_drl.fields().indexFromName('Q_Read_'+str(ic+1)), float(qinput[i]))
            

    self.lyr_drl.commitChanges()
    self.lyr_drl.updateFields()   

    return self.lyr_drl




def conf_drl_bho(self, lyr_drl, lyr_cat, module):
       
        #lyr_drl = QgsVectorLayer('C:/Users/rafae/OneDrive/10_warm_gis/teste_bho/teste_bho_psh_v1.shp', 'Drainage Line', 'ogr')  
        nd = lyr_drl.featureCount()
        
        
        #read variables 
        aTdr_cur=np.empty((0))
        aCodJusID_C=np.empty((0))      
        aCodID_C=np.empty((0))
        pDistFoz=np.empty((0))

        areas=np.empty((0))      
        upareas=np.empty((0))
        rlens=np.empty((0))
        d_cobacia=np.empty((0))
        
        
        aComCab=np.zeros((nd))     
        aCodMini=np.zeros((nd))
        aOrdem=np.zeros((nd))
        simula=np.zeros((nd))
        
        #depths=np.zeros((nd))
        #widths=np.zeros((nd))
        
        pSomaMini=0
        
        
        features = lyr_drl.getFeatures()
        for feature in features:
            
            aTdr_cur = np.append(aTdr_cur, feature['cocursodag'])               
            aCodJusID_C = np.append(aCodJusID_C, feature['nodestino'])
            aCodID_C = np.append(aCodID_C, feature['noorigem'])  
            pDistFoz = np.append(pDistFoz, feature['nudistcdag'])
            d_cobacia = np.append(d_cobacia, feature['cobacia'])
            
            
            
            
            
            areas = np.append(areas, feature['nuareacont'])
            upareas = np.append(upareas, feature['nuareamont'])   
            rlens = np.append(rlens, feature['nucomptrec'])          
            
        
        
        
        depths = 1.03 * (upareas**0.3)
        widths = 0.95 * (upareas**0.5)
        
        #for idr in range(nd):
        #    depths[idr] = 1.03 * (upareas[idr]^0.3)
        #    widths[idr] = 0.95 * (upareas[idr]^0.5)
            



        #LOCALIZAR OS TRECHOS DE CABECEIRA 

            
        aCodTr_unique = np.unique(aTdr_cur)
        
        for i in range (len(aCodTr_unique)):
            
            ind_ = np.array(np.where(aTdr_cur == aCodTr_unique[i]))
            
            if (ind_.size==1):
                
                 ind=ind_[0,0]
                 aComCab[ind] = 1
                 pSomaMini = pSomaMini + 1
                 aCodMini[ind] = pSomaMini
                 aOrdem[ind] = 1
                 
            else:
                
                 pDistMax = -1
                 for it in range(ind_.size):
                     
                     ind=ind_[0,it]
                     
                     dist=pDistFoz[ind]
                      
                     if dist > pDistMax:
                          pDistMax = dist
                          pIDMont = ind
                          
                     simula[ind]=1
                      
                      
                 aComCab[pIDMont] = 1
                 pSomaMini = pSomaMini + 1
                 aCodMini[pIDMont] = pSomaMini
                 aOrdem[pIDMont] = 1
                 
                 
        #ROTINA P/ CALCULAR O CAMPO ORDEM
        
        for idr in range(nd):
            
            if (aComCab[idr]==1):
                
                pNextDownID = aCodJusID_C[idr]              
                
                while (np.array(np.where(aCodID_C == pNextDownID)).size>0):
                    ind_ = np.array(np.where(aCodID_C == pNextDownID))
                    ind=ind_[0,0]
                    pNextDownID = aCodJusID_C[ind]
                    aOrdem[ind] = aOrdem[ind] + 1

                    
                    
        #ROTINA P/ COMPLETAR O CAMPO MINI
        
        ord_unique = np.unique(aOrdem)        
        #ord_unique = ord_unique.sort()
        
        for i in range(1,len(ord_unique)):
            
            ind_ = np.array(np.where(aOrdem == ord_unique[i]))
            
            mini_max = max(aCodMini)
            
            for it in range(ind_.size):
                     
                     ind=ind_[0,it]
                     aCodMini[ind] = mini_max + it + 1
                    
                    

        #--------------------------------------------------------------------------------------------------------------------
        
        #module = 'qual'
        
        
        
        #ADICIONAR COLUNAS 
        if module == 'bal':
            lyr_drl = add_columns_drl_bal(lyr_drl)
            
        if module == 'qual':
            lyr_drl = add_columns_drl_qual(lyr_drl)

        
        #SALVAR NO SHAPEFILE 
        
        features = lyr_drl.getFeatures()
        lyr_drl.startEditing()        

      
        i = 0
        for feat in features:           

             lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('Order_ID'), int(aOrdem[i]))             
             lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('Mini_ID'), int(aCodMini[i]))
             lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('CodBas_ID'), int(aCodID_C[i]))
             lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('CodDown_ID'), int(aCodJusID_C[i]))
             lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('Reserv_ID'), 0)
             lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('Length_km'), float(rlens[i]))
             
             if module == 'qual':

                 lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('SubWat'), 1)
                 lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('Area_km2'), float(areas[i]))
                 lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('AreaUp_km2'), float(upareas[i]))
                 lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('Depth_m'), float(depths[i]))
                 lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('Width_m'), float(widths[i]))
                 lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('Vel_ms'), 0)            
                 lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('Slope'), 0)            
            

             i = i + 1

        lyr_drl.commitChanges()
        lyr_drl.updateFields()
            
            
            
        # CATCHMENT ######################################################################################
        
        nc = lyr_cat.featureCount()
        c_cobacia=np.empty((0))
        
        c_codbas=np.zeros((nc))
        

        features = lyr_cat.getFeatures()
        for feature in features:
            c_cobacia = np.append(c_cobacia, feature['cobacia'])
            
            
            
        
        for ic in range(nc):
            for idr in range(nd):
                if (d_cobacia[idr]==c_cobacia[ic]):
                    c_codbas[ic]= aCodID_C[idr]
        
        
        #add coluna
        
        layer_provider1=lyr_cat.dataProvider()
        layer_provider1.addAttributes([QgsField("CodBas_ID",QVariant.Int)])
        
        
        layer_provider1.addAttributes([QgsField("Load_BOD",QVariant.Double)])        
        layer_provider1.addAttributes([QgsField("Load_Col",QVariant.Double)])
        layer_provider1.addAttributes([QgsField("Load_Po",QVariant.Double)])
        layer_provider1.addAttributes([QgsField("Load_Pi",QVariant.Double)])
        layer_provider1.addAttributes([QgsField("Load_No",QVariant.Double)]) 
        layer_provider1.addAttributes([QgsField("Load_Na",QVariant.Double)])
        layer_provider1.addAttributes([QgsField("Load_Nn",QVariant.Double)])

        
        lyr_cat.updateFields()
        

        #write shapefile
        lyr_cat.startEditing()
        features = lyr_cat.getFeatures()
        
        
        i = 0
        for feat in features: 
            
             lyr_cat.changeAttributeValue(feat.id(), lyr_cat.fields().indexFromName('CodBas_ID'), int(c_codbas[i]))
             i = i + 1

           
        lyr_cat.commitChanges()
        lyr_cat.updateFields()

        
        return lyr_drl, lyr_cat
        
########################################################################################################        
    
def save_parameters_drl(self, lyr_drl):
    
    
    nd =  lyr_drl.featureCount()
    
    
    d_codbas=np.empty(0)
    d_subw= np.empty((0))
    d_depth= np.empty((0))
    d_width= np.empty((0))
    d_slope= np.empty((0))
    #self.d_qefl=np.zeros((nd))
    d_qnat= np.empty((0))
    d_uparea= np.empty((0))
    
    features = lyr_drl.getFeatures()
    for feature in features:
            d_codbas = np.append(d_codbas, feature['CodBas_ID'])
            d_subw = np.append(d_subw, feature['SubWat'])
            d_depth = np.append(d_depth, feature['Depth_m'])
            d_width = np.append(d_width, feature['Width_m'])
            d_slope = np.append(d_slope, feature['Slope'])
            d_uparea = np.append(d_uparea, feature['AreaUp_km2'])
            
            d_qnat = np.append(d_qnat, feature['Q_Read_'+str(self.q_scn)])
            
    


 
    
    '''
    ###########################
    ne =  lyr_efl.featureCount()

        
    self.e_codbas=np.empty(0) 
    self.e_qefl= np.empty((0))
    
    features = lyr_efl.getFeatures()
    for feature in features:
            
        self.e_codbas = np.append(self.e_codbas, feature['CodBas_ID'])
        self.e_qefl = np.append(self.e_qefl, feature['Q_Inflow'])
            
    
      
    
        ########################################################################

        # ATRIBUIR CARGA POR TRECHO
        #self.d_qefl=np.zeros((nd, nt))
     
        for idr in range(nd):
            for ie in range(ne):        
                if (self.d_codbas[idr]==self.e_codbas[ie]):
                        self.d_qefl[idr]= self.d_qefl[idr]+self.e_qefl[ie] 
    '''
                        
   


    #####################################################################

    
    nb = len(self.kds1s)

    
    d_kd=np.empty((nd))
    d_ksmo=np.empty((nd))
    d_ka=np.empty((nd))
    d_kcol=np.empty((nd))
    d_koi=np.empty((nd))
    d_ksp=np.empty((nd))        
    d_koa=np.empty((nd))
    #d_kai=np.empty((nd))
    d_kan=np.empty((nd))      
    d_vel=np.empty((nd))        
    #d_satdo=np.empty((nd))
    
    d_kden=np.empty((nd)) 
    
    

    
    rh=np.empty((nd))
    
    
    
    #parametros hidraulicos 
    
    
    if self.geo_option ==2:
        
        for idr in range(nd):
            d_width[idr] = self.w_a * (d_uparea[idr]** self.w_b)
            d_depth[idr] = self.d_c * (d_uparea[idr]** self.d_d)
        

    
    #calculo da velocidade  ---------------------------------------------------------------
    
    if self.vel_option ==1: #subbasin
        
         for ib in range (nb):      
             for idr in range(nd):                
                 if (d_subw[idr] == ib+1):
                     d_vel[idr] = self.vels[ib]        
    
    elif self.vel_option ==2: #manning 
        
        for idr in range(nd):
            
            a = ((2* d_width[idr] + (2*2* d_depth[idr]))*d_depth[idr])/2
            p = d_width[idr] + 2 * (d_depth[idr]**2 + (2*d_depth[idr]))**(1/2)
            
            rh[idr]=a/p
            
            #rh[idr] = (d_depth[idr] *  d_width[idr]) / (d_width[idr] + (2* d_depth[idr]))      
            d_vel[idr] = (rh[idr]**(2/3) * d_slope[idr]**(1/2)) / 0.03
            
    elif self.vel_option == 3:  #reg
        
        for idr in range(nd):
            d_vel[idr] = self.vel_reg_a * (d_qnat[idr]** self.vel_reg_b)


    elif self.vel_option == 4:  #continuidade
        
        for idr in range(nd):
            d_vel[idr] =  (d_qnat[idr] / d_depth[idr] *  d_width[idr])


            
            
    # calculo do ka
    
    if self.ka_option == 1:  #sub-basin
    
        for ib in range (nb):      
             for idr in range(nd):                
                 if (d_subw[idr] == ib+1):
                     d_ka[idr] = self.kas[ib]

    
    elif self.ka_option == 2: 
        
        
        for idr in range(nd):
            
            if d_depth[idr] < 0.6:
                d_ka[idr] = (5.3 * (d_vel[idr] ** 0.67)) * (d_depth[idr] ** (-1.85))  #'Owens
            elif d_depth[idr] >= 0.6:
                
                if d_vel[idr] < 0.8:
                    d_ka[idr] = (3.93 * (d_vel[idr] ** 0.5)) * (d_depth[idr] ** (-1.5))  #'O'Connor & Dobbins
                else:
                    d_ka[idr] = (5.0 * (d_vel[idr] ** 0.97)) * (d_depth[idr] ** (-1.67))  #CHURCHILL
                    
                    
    elif self.ka_option == 3: #tsivoglou
        
        for idr in range(nd):
            d_ka[idr] = 15.4 * d_slope[idr] * 1000 * d_vel[idr]
            
            
    elif self.ka_option == 4: #melching e flores 
        
        
        if d_qnat[idr] < 0.556:  
            d_ka[idr] = 517 * (d_slope[idr] * d_vel[idr])**0.524 * (d_qnat[idr])**(-0.242)
        else:
            d_ka[idr] = 596 * (d_slope[idr] * d_vel[idr])**0.528 * (d_qnat[idr])**(-0.136)
        




        
    #parametros fixos por subbacia 
    for ib in range (nb):
        
            for idr in range(nd):
            
                if (d_subw[idr] == ib+1):
                    
                    #kd
                    if (d_depth[idr]<1.5):
                        #if (self.d_qefl[idr]<0.001):
                            d_kd[idr] = self.kds1s[ib]
                        #else:
                        #    d_kd[idr] = self.kds2s[ib]
                    else:
                        #if (self.d_qefl[idr]<0.001):
                            d_kd[idr] = self.kdd1s[ib]
                        #else:
                          #  d_kd[idr] = self.kdd2s[ib]
                            
                            
                    #ksmo
                    d_ksmo[idr]= self.vsmos[ib]/d_depth[idr]
                    if d_ksmo[idr]>0.5:
                        d_ksmo[idr]=0.5
                        
                    #ksp
                    d_ksp[idr]= self.vsps[ib]/d_depth[idr]
                    if d_ksp[idr]>0.5:
                        d_ksp[idr]=0.5                    
                    
                    
                    
                    d_kcol[idr] = self.kcols[ib]
                    d_koi[idr] = self.kois[ib]
                    d_koa[idr] = self.koas[ib]
                    d_kan[idr] = self.kans[ib]
                    d_kden[idr] = self.kdens[ib]
                    
                    
                    #d_vel[idr] = self.vels[ib]
              

                    #(Popel, 1979)
                    #self.d_satdo[idr] =  14.652 - (4.1022 * 1e-1 * self.d_temp[idr]) + (7.991 * 1e-3 * self.d_temp[idr] ** 2) -(7.7774 * 1e-5 * self.d_temp[idr] ** 3)

    #write shapefile
    features = lyr_drl.getFeatures()
    lyr_drl.startEditing()
        

    i = 0
    for feat in features:
            
            lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('Coef_Kd'), float(d_kd[i]))
            lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('Coef_Ksd'), float(d_ksmo[i]))
            lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('Coef_Ka'), float(d_ka[i]))
            lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('Coef_Kcol'), float(d_kcol[i]))
            lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('Coef_Koi'), float(d_koi[i]))
            lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('Coef_Ksp'), float(d_ksp[i]))
            lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('Coef_Koa'), float(d_koa[i]))
            lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('Coef_Kan'), float(d_kan[i]))
            lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('Coef_Kden'), float(d_kden[i]))
            
            lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('Vel_ms'), float(d_vel[i]))
            
            lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('Width_m'), float(d_width[i]))
            lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('Depth_m'), float(d_depth[i]))
         
            
            
            
            #lyr_drl.changeAttributeValue(feat.id(), lyr_drl.fields().indexFromName('DO_Sat'), float(d_satdo[i]))
            i = i + 1

    lyr_drl.commitChanges()
    lyr_drl.updateFields()
    
    
    return lyr_drl
        
        
        
        
        
        
        
        
        
    


