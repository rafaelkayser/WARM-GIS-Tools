# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 13:44:22 2022

@author: rafae
"""

import os, sys, datetime
import numpy as np
import matplotlib.pyplot as plt

from qgis.core import *

from qgis.PyQt.QtWidgets import QMessageBox

from PyQt5.QtWidgets import *

from csv import reader

import glob


########################################################################


class Quality_Model:
    

    
    
    def __init__ (self, lyr_drl, lyr_cat, lyr_efl, lyr_wit, lyr_res, path_par,scn_q_int, sim_dif):
        self.lyr_drl = lyr_drl
        self.lyr_cat = lyr_cat
        self.lyr_efl = lyr_efl
        self.lyr_wit = lyr_wit
        self.lyr_res = lyr_res
        self.path_par = path_par
        self.scn_q_int = scn_q_int
        self.sim_dif = sim_dif
        


    def read_parameters(self):
        
        nd =  self.lyr_drl.featureCount()
        
        self.d_subw= np.empty((0,0))
        features = self.lyr_drl.getFeatures()
        for feature in features:
            self.d_subw = np.append(self.d_subw, feature['SubWat'])
            

        
        # READ PARAMETERS FILE -------------------------------------------------------------------------
        
        list_input = []
        with open(self.path_par, 'r', encoding='utf-8') as read_obj:
            csv_reader = reader(read_obj, delimiter=';')
            header = next(csv_reader)
            # Check file as empty
            if header != None:
                # Iterate over each row after the header in the csv
                for row in csv_reader:
                    # row variable is a list that represents a row in csv
                    list_input.append(row)

        self.i_bod= float(list_input[0][1])
        self.i_do=float(list_input[1][1])
        self.i_col=float(list_input[2][1])
        self.i_po=float(list_input[3][1])
        self.i_pi=float(list_input[4][1])
        self.i_no=float(list_input[5][1])
        self.i_na=float(list_input[6][1])
        self.i_nn=float(list_input[7][1])
        self.i_satdo=float(list_input[8][1])
        self.i_temp=float(list_input[9][1])
        
        
        self.nb = int(list_input[10][1])
        
        self.red_bodp = []
        self.red_colp=[]
        self.red_ptp=[]
        self.red_ntp=[]
        self.red_bodd=[]
        self.red_cold=[]
        self.red_ptd=[]
        self.red_ntd=[]

        
        for ib in range(self.nb):
            self.red_bodp.append(float(list_input[24][ib+1]))
            self.red_colp.append(float(list_input[25][ib+1]))
            self.red_ptp.append(float(list_input[26][ib+1]))
            self.red_ntp.append(float(list_input[27][ib+1]))
            self.red_bodd.append(float(list_input[28][ib+1]))
            self.red_cold.append(float(list_input[29][ib+1]))
            self.red_ptd.append(float(list_input[30][ib+1]))
            self.red_ntd.append(float(list_input[31][ib+1]))    



  
        
    def read_input_files(self):
        
        
        # READ DRAINAGE LINE --------------------------------------------------------------------------------------        
        
        nd =  self.lyr_drl.featureCount()
        nt=1
        
        self.d_codbas= np.empty((0,0))
        self.d_codjus= np.empty((0,0))
        self.d_ord= np.empty((0,0))
        self.d_mini= np.empty((0,0))
        self.d_codres= np.empty((0,0))
        self.d_leng = np.empty((0,0))
        self.d_vel= np.empty((0,0))
        self.d_subw= np.empty((0,0))
        self.d_depth= np.empty((0,0))
        self.d_width= np.empty((0,0))
        self.d_qnat= np.empty((0,nt))
        
        self.d_kd=np.empty((0))
        self.d_ksmo=np.empty((0))
        self.d_kr=np.empty((0))
        self.d_ka=np.empty((0))
        self.d_kcol=np.empty((0))
        self.d_koi=np.empty((0))
        self.d_ksp=np.empty((0))        
        self.d_koa=np.empty((0))
        #self.d_kai=np.empty((0))
        #self.d_kin=np.empty((0))      
        self.d_temp=np.empty((0))
        self.d_vel=np.empty((0))        
        self.d_satdo=np.empty((0))
        
        self.d_kan=np.empty((0))
        self.d_kden=np.empty((0))
        
        
        
        features = self.lyr_drl.getFeatures()
        for feature in features:
            
            self.d_codbas = np.append(self.d_codbas, feature['CodBas_ID'])
            self.d_codjus = np.append(self.d_codjus, feature['CodDown_ID'])
            self.d_ord = np.append(self.d_ord, feature['Order_ID'])
            self.d_leng = np.append(self.d_leng, feature['Length_km'])
            self.d_width = np.append(self.d_width, feature['Width_m'])
            self.d_subw = np.append(self.d_subw, feature['SubWat'])
            self.d_depth = np.append(self.d_depth, feature['Depth_m'])
            self.d_mini = np.append(self.d_mini, feature['Mini_ID'])
            self.d_codres = np.append(self.d_codres, feature['Reserv_ID'])
            
            self.d_kd = np.append(self.d_kd, feature['Coef_Kd'])
            self.d_ksmo = np.append(self.d_ksmo, feature['Coef_Ksd'])
            self.d_ka = np.append(self.d_ka, feature['Coef_Ka'])
            self.d_kcol = np.append(self.d_kcol, feature['Coef_Kcol'])
            self.d_koi = np.append(self.d_koi, feature['Coef_Koi'])
            self.d_ksp = np.append(self.d_ksp, feature['Coef_Ksp'])                      
            self.d_koa = np.append(self.d_koa, feature['Coef_Koa'])
            #self.d_kai = np.append(self.d_kai, feature['Coef_Kai'])
            #self.d_kin = np.append(self.d_kin, feature['Coef_Kin'])
            self.d_kan = np.append(self.d_kan, feature['Coef_Kan'])
            self.d_kden = np.append(self.d_kden, feature['Coef_Kden'])
            self.d_vel = np.append(self.d_vel, feature['Vel_ms'])            
            #self.d_satdo = np.append(self.d_satdo, feature['DO_Sat'])
            
            

            self.d_qnat = np.append(self.d_qnat, feature['Q_Read_'+str(self.scn_q_int)]) 
            
            
        self.d_qnat.resize(nd,nt)
        self.d_kr = self.d_kd + self.d_ksmo
            
            
            #self.d_kr = np.append(self.d_kr, feature['Coef_Kd'])
            
        '''
            aux_qnat = np.empty((0,nt))
            for it in range(0,nt):
                #aux_qnat.append(feature['Q_Read_'+str(it+1)])
                aux_qnat = np.append(aux_qnat, feature['Q_Read_'+str(self.scn_q_int)])
                
            aux_qnat.resize(1,nt)
            self.d_qnat = np.append(self.d_qnat, aux_qnat, axis=0)
        '''
            

        
        
        
        
        # READ EFLUENTS  ----------------------------------------------------------------------------------------------
        ne =  self.lyr_efl.featureCount()
        nt=1
        
        self.e_codbas=np.empty((0))
        
        self.e_qefl= np.empty((0, nt))
        self.e_cbod= np.empty((0,nt))
        self.e_cdo= np.empty((0,nt))
        self.e_ccol= np.empty((0,nt))
        self.e_cpo= np.empty((0,nt))
        self.e_cpi= np.empty((0,nt))
        self.e_cno= np.empty((0,nt))
        self.e_cna= np.empty((0,nt))
        #self.e_cni= np.empty((0,nt))
        self.e_cnn= np.empty((0,nt))
        
        
        features = self.lyr_efl.getFeatures()

        for feature in features:
            
            self.e_codbas = np.append(self.e_codbas, feature['CodBas_ID'])
            
            for it in range(0,nt):
                
                self.e_qefl = np.append(self.e_qefl, feature['Q_Inflow'])
                self.e_cbod = np.append(self.e_cbod, feature['Conc_BOD'])
                self.e_cdo = np.append(self.e_cdo, feature['Conc_DO'])
                self.e_ccol = np.append(self.e_ccol, feature['Conc_Col'])
                self.e_cpi = np.append(self.e_cpi, feature['Conc_Pi'])
                self.e_cpo = np.append(self.e_cpo, feature['Conc_Po'])
                self.e_cno = np.append(self.e_cno, feature['Conc_No'])
                self.e_cna = np.append(self.e_cna, feature['Conc_Na'])
                #self.e_cni = np.append(self.e_cni, feature['Conc_Ni'])
                self.e_cnn = np.append(self.e_cnn, feature['Conc_Nn'])
                
                
        self.e_qefl.resize(ne,nt)
        self.e_cbod.resize(ne,nt)
        self.e_cdo.resize(ne,nt)
        self.e_ccol.resize(ne,nt)
        self.e_cpi.resize(ne,nt)
        self.e_cpo.resize(ne,nt)
        self.e_cno.resize(ne,nt)
        self.e_cna.resize(ne,nt)
        #self.e_cni.resize(ne,nt)
        self.e_cnn.resize(ne,nt)
    
        ########################################################################

        # ATRIBUIR CARGA POR TRECHO

        self.d_qefl=np.zeros((nd, nt))
        self.d_ebod=np.zeros((nd,nt))
        self.d_edo=np.zeros((nd,nt))
        self.d_ecol=np.zeros((nd,nt))
        self.d_epo=np.zeros((nd,nt))
        self.d_epi=np.zeros((nd,nt))
        self.d_eno=np.zeros((nd,nt))
        self.d_ena=np.zeros((nd,nt))
        #self.d_eni=np.zeros((nd,nt))
        self.d_enn=np.zeros((nd,nt))


        self.d_qwit=np.zeros((nd,nt))




        for idr in range(0,nd):
            for ie in range(0,ne):        
                if (self.d_codbas[idr]==self.e_codbas[ie]):
                    for it in range (0, nt):
                               
                        self.d_qefl[idr,it]= self.d_qefl[idr,it]+self.e_qefl[ie,it]               
                        self.d_ebod[idr,it] = ((self.e_cbod[ie,it] * self.e_qefl[ie,it]) + (self.d_ebod[idr,it] * self.d_qefl[idr,it])) / self.d_qefl[idr,it]
                        self.d_edo[idr,it] = ((self.e_cdo[ie,it] * self.e_qefl[ie,it]) + (self.d_edo[idr,it] * self.d_qefl[idr,it])) / self.d_qefl[idr,it]
                        self.d_ecol[idr,it] = ((self.e_ccol[ie,it] * self.e_qefl[ie,it]) + (self.d_ecol[idr,it] * self.d_qefl[idr,it])) / self.d_qefl[idr,it]
                        self.d_epo[idr,it] = ((self.e_cpo[ie,it] * self.e_qefl[ie,it]) + (self.d_epo[idr,it] * self.d_qefl[idr,it])) / self.d_qefl[idr,it]
                        self.d_epi[idr,it] = ((self.e_cpi[ie,it] * self.e_qefl[ie,it]) + (self.d_epi[idr,it] * self.d_qefl[idr,it])) / self.d_qefl[idr,it]
                        self.d_eno[idr,it] = ((self.e_cno[ie,it] * self.e_qefl[ie,it]) + (self.d_eno[idr,it] * self.d_qefl[idr,it])) / self.d_qefl[idr,it]
                        self.d_ena[idr,it] = ((self.e_cna[ie,it] * self.e_qefl[ie,it]) + (self.d_ena[idr,it] * self.d_qefl[idr,it])) / self.d_qefl[idr,it]
                        #self.d_eni[idr,it] = ((self.e_cni[ie,it] * self.e_qefl[ie,it]) + (self.d_eni[idr,it] * self.d_qefl[idr,it])) / self.d_qefl[idr,it]
                        self.d_enn[idr,it] = ((self.e_cnn[ie,it] * self.e_qefl[ie,it]) + (self.d_enn[idr,it] * self.d_qefl[idr,it])) / self.d_qefl[idr,it]
        
        
        #aplicar reduções de carga 
        for ib in range (self.nb):       
            for idr in range(nd):           
                if (self.d_subw[idr] == ib+1):                  
                    for it in range (0, nt):
                         self.d_ebod[idr,it] = self.d_ebod[idr,it] * (100- self.red_bodp[ib])/100
                         self.d_ecol[idr,it] = self.d_ecol[idr,it] * (100- self.red_colp[ib])/100
                         self.d_epo[idr,it] = self.d_epo[idr,it] * (100- self.red_ptp[ib])/100
                         self.d_epi[idr,it] = self.d_epi[idr,it] * (100- self.red_ptp[ib])/100
                         self.d_eno[idr,it] = self.d_eno[idr,it] * (100- self.red_ntp[ib])/100
                         self.d_ena[idr,it] = self.d_ena[idr,it] * (100- self.red_ntp[ib])/100
                         self.d_enn[idr,it] = self.d_enn[idr,it] * (100- self.red_ntp[ib])/100
                      
        
        #READ CATCHMENT #########################################################################################################
        
        
        if self.sim_dif ==1:
        
        
            nc =  self.lyr_cat.featureCount()

        
            c_codbas=np.empty((0))
        

            c_wbod= np.empty((0))
            c_wcol= np.empty((0))
            c_wpo= np.empty((0))
            c_wpi= np.empty((0))
            c_wno= np.empty((0))
            c_wna= np.empty((0))
            c_wnn= np.empty((0))


            self.d_wbod=np.zeros((nd))
            self.d_wcol=np.zeros((nd))
            self.d_wpo=np.zeros((nd))
            self.d_wpi=np.zeros((nd))
            self.d_wno=np.zeros((nd))
            self.d_wna=np.zeros((nd))
            self.d_wnn=np.zeros((nd))
      
        
            features = self.lyr_cat.getFeatures()

            for feature in features:
            
                c_codbas = np.append(c_codbas, feature['CodBas_ID'])
                c_wbod = np.append(c_wbod, feature['Load_BOD'])
                c_wcol = np.append(c_wcol, feature['Load_Col'])
                c_wpi = np.append(c_wpi, feature['Load_Pi'])
                c_wpo = np.append(c_wpo, feature['Load_Po'])
                c_wno = np.append(c_wno, feature['Load_No'])
                c_wna = np.append(c_wna, feature['Load_Na'])
                c_wnn = np.append(c_wnn, feature['Load_Nn'])


            for idr in range(nd):
                for ic in range(nc):        
                    if (self.d_codbas[idr]==c_codbas[ic]):

                        self.d_wbod[idr] = c_wbod[ic]
                        self.d_wcol[idr] = c_wcol[ic]
                        self.d_wpo[idr] = c_wpo[ic]
                        self.d_wpi[idr] = c_wpi[ic]
                        self.d_wno[idr] = c_wno[ic]
                        self.d_wna[idr] = c_wna[ic]
                        self.d_wnn[idr] = c_wnn[ic]


            #aplicar reduções de carga 
            for ib in range (self.nb):       
                for idr in range(nd):           
                    if (self.d_subw[idr] == ib+1):                  
                        for it in range (0, nt):
                            self.d_wbod[idr] = self.d_wbod[idr] * (100- self.red_bodd[ib])/100
                            self.d_wcol[idr] = self.d_wcol[idr] * (100- self.red_cold[ib])/100
                            self.d_wpo[idr] = self.d_wpo[idr] * (100- self.red_ptd[ib])/100
                            self.d_wpi[idr] = self.d_wpi[idr] * (100- self.red_ptd[ib])/100
                            self.d_wno[idr] = self.d_wno[idr] * (100- self.red_ntd[ib])/100
                            self.d_wna[idr] = self.d_wna[idr] * (100- self.red_ntd[ib])/100
                            self.d_wnn[idr] = self.d_wnn[idr] * (100- self.red_ntd[ib])/100


        # READ WITHDRAWALS  ----------------------------------------------------------------------------------------------
        nw =  self.lyr_wit.featureCount()
        nt=1
        
        self.w_codbas=np.empty((0))
        
        self.w_qwit= np.empty((0, nt))
     
        
        
        features = self.lyr_wit.getFeatures()

        for feature in features:
            
            
            # Append list as a column to the 2D Numpy array
            self.w_codbas = np.append(self.w_codbas, feature['CodBas_ID'])  #.transpose(), axis=1)
            
            if (1==1):
                aux_qwit = np.empty((0,nt))
                for it in range(0,nt):
                    aux_qwit = np.append(aux_qwit, feature['Q_Wit_1'])
                aux_qwit.resize(1,nt)
                self.w_qwit = np.append(self.w_qwit, aux_qwit, axis=0)
            
            
        #ATRIBUIR RETIRADAS NA MATRIZ DE DRENAGEM    
        
        self.d_qwit=np.zeros((nd,nt))
        
        for idr in range(0,nd):
            for iw in range(0,nw):        
                if (self.d_codbas[idr]==self.w_codbas[iw]):
                    for it in range (0, nt):
                        self.d_qwit[idr,it]=self.d_qwit[idr,it]+self.w_qwit[iw,it]

        
        # READ RESERVOIR  ----------------------------------------------------------------------------------------------
        nr =  self.lyr_res.featureCount()
    
    
        self.r_codres=np.empty((0))
        self.r_codbas=np.empty((0))
        
        self.r_qrel = np.empty((0, nt))
        self.r_qsubs = np.empty((0, nt))     
        
        
    
        
        if (nr>0):
        
          features = self.lyr_res.getFeatures()

          for feature in features:
            
            
            # Append list as a column to the 2D Numpy array
            self.r_codres = np.append(self.r_codres, feature['Res_ID'])
            self.r_codbas = np.append(self.r_codbas, feature['CodBas_ID'])
            
            
            aux_qrel = np.empty((0,nt))
            for it in range(0,nt):
                #aux_qwit = np.append(aux_qwit, feature['Q_Rel_'+str(it+1)])
                aux_qrel = np.append(aux_qrel, feature['Q_Rel_1'])
            aux_qrel.resize(1,nt)
            self.r_qrel = np.append(self.r_qrel, aux_qrel, axis=0)

            aux_qsubs = np.empty((0,nt))
            for it in range(0,nt):
                #aux_qwit = np.append(aux_qwit, feature['Q_Rel_'+str(it+1)])
                aux_qsubs = np.append(aux_qsubs, feature['Q_Subs_1'])
            aux_qsubs.resize(1,nt)
            self.r_qsubs = np.append(self.r_qsubs, aux_qsubs, axis=0)
        



    
  
    def run_model(self):
        
        
        
        
        nd = self.lyr_drl.featureCount()
        nt=1
        
        d_qmn=np.empty((nd, nt))
        d_qmr=np.empty((nd, nt))
        d_qmnr=np.empty((nd, nt))
        
        d_qmix=np.empty((nd, nt))
        d_qout_aux=np.empty((nd, nt))


        d_qcat=np.empty((nd, nt))
        self.d_qout=np.empty((nd, nt))
        self.d_wbal=np.empty((nd, nt))
        self.d_qnatres=np.empty((nd, nt))

        d_ibod=np.empty((nd, nt))
        d_mbod=np.empty((nd, nt))
        d_dbod=np.empty((nd, nt))
        self.d_obod=np.empty((nd, nt))

        d_ido=np.empty((nd, nt))
        d_mdo=np.empty((nd, nt))
        d_ddo=np.empty((nd, nt))
        self.d_odo=np.empty((nd, nt))

        d_icol=np.empty((nd, nt))
        d_mcol=np.empty((nd, nt))
        d_dcol=np.empty((nd, nt))
        self.d_ocol=np.empty((nd, nt))

        d_ipo=np.empty((nd, nt))
        d_mpo=np.empty((nd, nt))
        d_dpo=np.empty((nd, nt))
        self.d_opo=np.empty((nd, nt))

        d_ipi=np.empty((nd, nt))
        d_mpi=np.empty((nd, nt))
        d_dpi=np.empty((nd, nt))
        self.d_opi=np.empty((nd, nt))

        d_ino=np.empty((nd, nt))
        d_mno=np.empty((nd, nt))
        d_dno=np.empty((nd, nt))
        self.d_ono=np.empty((nd, nt))

        d_ina=np.empty((nd, nt))
        d_mna=np.empty((nd, nt))
        d_dna=np.empty((nd, nt))
        self.d_ona=np.empty((nd, nt))

        #d_ini=np.empty((nd, nt))
        #d_mni=np.empty((nd, nt))
        #d_dni=np.empty((nd, nt))
        #self.d_oni=np.empty((nd, nt))

        d_inn=np.empty((nd, nt))
        d_mnn=np.empty((nd, nt))
        d_dnn=np.empty((nd, nt))
        self.d_onn=np.empty((nd, nt))
        
        self.d_opt=np.empty((nd, nt))
        
        
        teste=np.empty((nd, nt))
        

        #carga difusa
        d_cbod=np.zeros((nd, nt))
        d_cdo=np.zeros((nd, nt))
        d_ccol=np.zeros((nd, nt))
        d_cpo=np.zeros((nd, nt))
        d_cpi=np.zeros((nd, nt))
        d_cno=np.zeros((nd, nt))
        d_cna=np.zeros((nd, nt))
        #d_cni=np.zeros((nd, nt))
        d_cnn=np.zeros((nd, nt))

        '''
        d_cbod=np.ones((nd, nt))* 2
        d_cdo=np.ones((nd, nt))*8.5
        d_ccol=np.ones((nd, nt))*50
        d_cpo=np.ones((nd, nt))*0.01
        d_cpi=np.ones((nd, nt))*0.01
        d_cno=np.ones((nd, nt))*0.1
        d_cna=np.ones((nd, nt))*0.1
        d_cni=np.ones((nd, nt))*0.01
        d_cnn=np.ones((nd, nt))*0.1
        '''

        d_minisort = np.arange(1,nd+1)

        # EXECUÇÃO DO MODELO 
        
        for ic in range(nd):
            
            ind = np.array(np.where(self.d_mini == d_minisort[ic])) #posiciona em ordem ascendente em relação ao Mini
            idr =ind[0][0]
        
    
            #1 - UPSTREAM CONCENTRATION 
            if self.d_ord[idr] ==1:
        
                for it in range(nt):
                    d_qmn[idr,it]= self.d_qnat[idr,it]*0.5  #montante - natural
                    d_qmr[idr,it]= self.d_qnat[idr,it]*0.5   #montante - remanescente
                    d_qmnr[idr,it]=self.d_qnat[idr,it]*0.5  #natural com reservatorios


                   

                    d_ibod[idr,it]=self.i_bod
                    d_ido[idr,it]=self.i_do
                    d_icol[idr,it]=self.i_col
                    d_ipo[idr,it]=self.i_po
                    d_ipi[idr,it]=self.i_pi
                    d_ino[idr,it]=self.i_no
                    d_ina[idr,it]=self.i_na
                    #d_ini[idr,it]=self.i_nn
                    d_inn[idr,it]=self.i_nn

                    
                    '''
                    d_ibod[idr,it]=2
                    d_ido[idr,it]=8.5
                    d_icol[idr,it]=50
                    d_ipo[idr,it]=0.01
                    d_ipi[idr,it]=0.01
                    d_ino[idr,it]=0.1
                    d_ina[idr,it]=0.1
                    d_ini[idr,it]=0.01
                    d_inn[idr,it]=0.1
                    '''

            
            
            else:
        
                ind_jus = np.array(np.where(self.d_codjus == self.d_codbas[idr]))
        
                if (ind_jus.size)==2:
            
                    for it in range(nt):
                
                        #upstream flow (natural)
                        qmn1 = self.d_qnat[ind_jus[0,0],it]
                        qmn2 = self.d_qnat[ind_jus[0,1],it]
                        d_qmn[idr,it] = qmn1+qmn2
                
                        #upstream flow (remaining)
                        qmr1 = self.d_qout[ind_jus[0,0],it]
                        qmr2 = self.d_qout[ind_jus[0,1],it]
                        d_qmr[idr,it] = qmr1+qmr2
                        
                        #upstream flow (natural with reservoirs)
                        qmnr1 = self.d_qnatres[ind_jus[0,0],it]
                        qmnr2 = self.d_qnatres[ind_jus[0,1],it]
                        d_qmnr[idr,it] = qmnr1+qmnr2 

                        #upstream bod
                        cm1 = self.d_obod[ind_jus[0,0],it]
                        cm2 = self.d_obod[ind_jus[0,1],it]
                        d_ibod[idr,it] = ((qmr1*cm1) + (qmr2*cm2))/d_qmr[idr,it]
                
                        #upstream do
                        cm1 = self.d_odo[ind_jus[0,0],it]
                        cm2 = self.d_odo[ind_jus[0,1],it]
                        d_ido[idr,it] = ((qmr1*cm1) + (qmr2*cm2))/d_qmr[idr,it]

                        #upstream col
                        cm1 = self.d_ocol[ind_jus[0,0],it]
                        cm2 = self.d_ocol[ind_jus[0,1],it]
                        d_icol[idr,it] = ((qmr1*cm1) + (qmr2*cm2))/d_qmr[idr,it]
                
                        #upstream po
                        cm1 = self.d_opo[ind_jus[0,0],it]
                        cm2 = self.d_opo[ind_jus[0,1],it]
                        d_ipo[idr,it] = ((qmr1*cm1) + (qmr2*cm2))/d_qmr[idr,it]
                
                        #upstream pi
                        cm1 = self.d_opi[ind_jus[0,0],it]
                        cm2 = self.d_opi[ind_jus[0,1],it]
                        d_ipi[idr,it] = ((qmr1*cm1) + (qmr2*cm2))/d_qmr[idr,it]
                
                        #upstream no
                        cm1 = self.d_ono[ind_jus[0,0],it]
                        cm2 = self.d_ono[ind_jus[0,1],it]
                        d_ino[idr,it] = ((qmr1*cm1) + (qmr2*cm2))/d_qmr[idr,it]
            
                        #upstream na
                        cm1 = self.d_ona[ind_jus[0,0],it]
                        cm2 = self.d_ona[ind_jus[0,1],it]
                        d_ina[idr,it] = ((qmr1*cm1) + (qmr2*cm2))/d_qmr[idr,it]
                
                        #upstream ni
                        #cm1 = self.d_oni[ind_jus[0,0],it]
                        #cm2 = self.d_oni[ind_jus[0,1],it]
                        #d_ini[idr,it] = ((qmr1*cm1) + (qmr2*cm2))/d_qmr[idr,it]

                        #upstream nn
                        cm1 = self.d_onn[ind_jus[0,0],it]
                        cm2 = self.d_onn[ind_jus[0,1],it]
                        d_inn[idr,it] = ((qmr1*cm1) + (qmr2*cm2))/d_qmr[idr,it]


                elif (ind_jus.size)==3:
            
                    for it in range(nt):
                
                        #upstream flow (natural)
                        qmn1 = self.d_qnat[ind_jus[0,0],it]
                        qmn2 = self.d_qnat[ind_jus[0,1],it]
                        qmn3 = self.d_qnat[ind_jus[0,2],it]
                        d_qmn[idr,it] = qmn1+qmn2+qmn3
            
                        #upstream flow (remaining)
                        qmr1 = self.d_qout[ind_jus[0,0],it]
                        qmr2 = self.d_qout[ind_jus[0,1],it]
                        qmr3 = self.d_qout[ind_jus[0,2],it]
                        d_qmr[idr,it] = qmr1+qmr2+qmr3

                        #upstream flow (natural with reservoirs)
                        qmnr1 = self.d_qnatres[ind_jus[0,0],it]
                        qmnr2 = self.d_qnatres[ind_jus[0,1],it]
                        qmnr3 = self.d_qnatres[ind_jus[0,2],it]
                        d_qmnr[idr,it] = qmnr1+qmnr2+qmnr3

                        
                        #upstream bod
                        cm1 = self.d_obod[ind_jus[0,0],it]
                        cm2 = self.d_obod[ind_jus[0,1],it]
                        cm3 = self.d_obod[ind_jus[0,2],it]
                        d_ibod[idr,it] = ((qmr1*cm1) + (qmr2*cm2) + (qmr3*cm3))/d_qmr[idr,it]
                
                        #upstream do
                        cm1 = self.d_odo[ind_jus[0,0],it]
                        cm2 = self.d_odo[ind_jus[0,1],it]
                        cm3 = self.d_odo[ind_jus[0,2],it]
                        d_ido[idr,it] = ((qmr1*cm1) + (qmr2*cm2) + (qmr3*cm3))/d_qmr[idr,it]                
                
                        #upstream col
                        cm1 = self.d_ocol[ind_jus[0,0],it]
                        cm2 = self.d_ocol[ind_jus[0,1],it]
                        cm3 = self.d_ocol[ind_jus[0,2],it]
                        d_icol[idr,it] = ((qmr1*cm1) + (qmr2*cm2) + (qmr3*cm3))/d_qmr[idr,it]                
                
                        #upstream po
                        cm1 = self.d_opo[ind_jus[0,0],it]
                        cm2 = self.d_opo[ind_jus[0,1],it]
                        cm3 = self.d_opo[ind_jus[0,2],it]
                        d_ipo[idr,it] = ((qmr1*cm1) + (qmr2*cm2) + (qmr3*cm3))/d_qmr[idr,it]                
                
                        #upstream pi
                        cm1 = self.d_opi[ind_jus[0,0],it]
                        cm2 = self.d_opi[ind_jus[0,1],it]
                        cm3 = self.d_opi[ind_jus[0,2],it]
                        d_ipi[idr,it] = ((qmr1*cm1) + (qmr2*cm2) + (qmr3*cm3))/d_qmr[idr,it]                

                        #upstream no
                        cm1 = self.d_ono[ind_jus[0,0],it]
                        cm2 = self.d_ono[ind_jus[0,1],it]
                        cm3 = self.d_ono[ind_jus[0,2],it]
                        d_ino[idr,it] = ((qmr1*cm1) + (qmr2*cm2) + (qmr3*cm3))/d_qmr[idr,it]

                        #upstream na
                        cm1 = self.d_ona[ind_jus[0,0],it]
                        cm2 = self.d_ona[ind_jus[0,1],it]
                        cm3 = self.d_ona[ind_jus[0,2],it]
                        d_ina[idr,it] = ((qmr1*cm1) + (qmr2*cm2) + (qmr3*cm3))/d_qmr[idr,it]

                        #upstream ni
                        #cm1 = self.d_oni[ind_jus[0,0],it]
                        #cm2 = self.d_oni[ind_jus[0,1],it]
                        #cm3 = self.d_oni[ind_jus[0,2],it]
                        #d_ini[idr,it] = ((qmr1*cm1) + (qmr2*cm2) + (qmr3*cm3))/d_qmr[idr,it]

                        #upstream nn
                        cm1 = self.d_onn[ind_jus[0,0],it]
                        cm2 = self.d_onn[ind_jus[0,1],it]
                        cm3 = self.d_onn[ind_jus[0,2],it]
                        d_inn[idr,it] = ((qmr1*cm1) + (qmr2*cm2) + (qmr3*cm3))/d_qmr[idr,it]


                elif (ind_jus.size)==4:
            
                    for it in range(nt):
                
                        #upstream flow (natural)
                        qmn1 = self.d_qnat[ind_jus[0,0],it]
                        qmn2 = self.d_qnat[ind_jus[0,1],it]
                        qmn3 = self.d_qnat[ind_jus[0,2],it]
                        qmn4 = self.d_qnat[ind_jus[0,3],it]
                        d_qmn[idr,it] = qmn1+qmn2+qmn3+qmn4
            
                        #upstream flow (remaining)
                        qmr1 = self.d_qout[ind_jus[0,0],it]
                        qmr2 = self.d_qout[ind_jus[0,1],it]
                        qmr3 = self.d_qout[ind_jus[0,2],it]
                        qmr4 = self.d_qout[ind_jus[0,3],it]
                        d_qmr[idr,it] = qmr1+qmr2+qmr3+qmr4

                        #upstream flow (natural with reservoirs)
                        qmnr1 = self.d_qnatres[ind_jus[0,0],it]
                        qmnr2 = self.d_qnatres[ind_jus[0,1],it]
                        qmnr3 = self.d_qnatres[ind_jus[0,2],it]
                        qmnr4 = self.d_qnatres[ind_jus[0,3],it]
                        d_qmnr[idr,it] = qmnr1+qmnr2+qmnr3+qmnr4

                        
                        #upstream bod
                        cm1 = self.d_obod[ind_jus[0,0],it]
                        cm2 = self.d_obod[ind_jus[0,1],it]
                        cm3 = self.d_obod[ind_jus[0,2],it]
                        cm4 = self.d_obod[ind_jus[0,3],it]
                        d_ibod[idr,it] = ((qmr1*cm1) + (qmr2*cm2) + (qmr3*cm3)+ (qmr4*cm4))/d_qmr[idr,it]
                
                        #upstream do
                        cm1 = self.d_odo[ind_jus[0,0],it]
                        cm2 = self.d_odo[ind_jus[0,1],it]
                        cm3 = self.d_odo[ind_jus[0,2],it]
                        cm4 = self.d_odo[ind_jus[0,3],it]
                        d_ido[idr,it] = ((qmr1*cm1) + (qmr2*cm2) + (qmr3*cm3)+ (qmr4*cm4))/d_qmr[idr,it]                
                
                        #upstream col
                        cm1 = self.d_ocol[ind_jus[0,0],it]
                        cm2 = self.d_ocol[ind_jus[0,1],it]
                        cm3 = self.d_ocol[ind_jus[0,2],it]
                        cm4 = self.d_ocol[ind_jus[0,3],it]
                        d_icol[idr,it] = ((qmr1*cm1) + (qmr2*cm2) + (qmr3*cm3)+ (qmr4*cm4))/d_qmr[idr,it]                
                
                        #upstream po
                        cm1 = self.d_opo[ind_jus[0,0],it]
                        cm2 = self.d_opo[ind_jus[0,1],it]
                        cm3 = self.d_opo[ind_jus[0,2],it]
                        cm4 = self.d_opo[ind_jus[0,3],it]
                        d_ipo[idr,it] = ((qmr1*cm1) + (qmr2*cm2) + (qmr3*cm3)+ (qmr4*cm4))/d_qmr[idr,it]                
                
                        #upstream pi
                        cm1 = self.d_opi[ind_jus[0,0],it]
                        cm2 = self.d_opi[ind_jus[0,1],it]
                        cm3 = self.d_opi[ind_jus[0,2],it]
                        cm4 = self.d_opi[ind_jus[0,3],it]
                        d_ipi[idr,it] = ((qmr1*cm1) + (qmr2*cm2) + (qmr3*cm3)+ (qmr4*cm4))/d_qmr[idr,it]                

                        #upstream no
                        cm1 = self.d_ono[ind_jus[0,0],it]
                        cm2 = self.d_ono[ind_jus[0,1],it]
                        cm3 = self.d_ono[ind_jus[0,2],it]
                        cm4 = self.d_ono[ind_jus[0,3],it]
                        d_ino[idr,it] = ((qmr1*cm1) + (qmr2*cm2) + (qmr3*cm3)+ (qmr4*cm4))/d_qmr[idr,it]

                        #upstream na
                        cm1 = self.d_ona[ind_jus[0,0],it]
                        cm2 = self.d_ona[ind_jus[0,1],it]
                        cm3 = self.d_ona[ind_jus[0,2],it]
                        cm4 = self.d_ona[ind_jus[0,3],it]
                        d_ina[idr,it] = ((qmr1*cm1) + (qmr2*cm2) + (qmr3*cm3)+ (qmr4*cm4))/d_qmr[idr,it]

                        #upstream ni
                        #cm1 = self.d_oni[ind_jus[0,0],it]
                        #cm2 = self.d_oni[ind_jus[0,1],it]
                        #cm3 = self.d_oni[ind_jus[0,2],it]
                        #d_ini[idr,it] = ((qmr1*cm1) + (qmr2*cm2) + (qmr3*cm3))/d_qmr[idr,it]

                        #upstream nn
                        cm1 = self.d_onn[ind_jus[0,0],it]
                        cm2 = self.d_onn[ind_jus[0,1],it]
                        cm3 = self.d_onn[ind_jus[0,2],it]
                        cm4 = self.d_onn[ind_jus[0,3],it]
                        d_inn[idr,it] = ((qmr1*cm1) + (qmr2*cm2) + (qmr3*cm3)+ (qmr4*cm4))/d_qmr[idr,it]


            
            # 2 - incremental streamflow
            for it in range(nt):
                d_qcat[idr,it] = self.d_qnat[idr,it] - d_qmn[idr,it]
    
    
            # 3 - Mistura do efluente com o trecho de rio
            for it in range(nt):
                
                #d_qmr[idr,it] = d_qmr[idr,it] - self.d_qwit[idr,it]
    
                d_qmix[idr,it] = (d_qmr[idr,it] + self.d_qefl[idr,it])

                if (self.d_qefl[idr,it]>0.00000001):
                    d_mbod[idr,it] = ((d_ibod[idr,it]*d_qmr[idr,it]) + (self.d_ebod[idr,it]*self.d_qefl[idr,it])) / (d_qmix[idr,it])
                    d_mdo[idr,it] = ((d_ido[idr,it]*d_qmr[idr,it]) + (self.d_edo[idr,it]*self.d_qefl[idr,it])) / (d_qmix[idr,it])
                    d_mcol[idr,it] = ((d_icol[idr,it]*d_qmr[idr,it]) + (self.d_ecol[idr,it]*self.d_qefl[idr,it])) / (d_qmix[idr,it])
                    d_mpo[idr,it] = ((d_ipo[idr,it]*d_qmr[idr,it]) + (self.d_epo[idr,it]*self.d_qefl[idr,it])) / (d_qmix[idr,it])
                    d_mpi[idr,it] = ((d_ipi[idr,it]*d_qmr[idr,it]) + (self.d_epi[idr,it]*self.d_qefl[idr,it])) / (d_qmix[idr,it])
                    d_mno[idr,it] = ((d_ino[idr,it]*d_qmr[idr,it]) + (self.d_eno[idr,it]*self.d_qefl[idr,it])) / (d_qmix[idr,it])
                    d_mna[idr,it] = ((d_ina[idr,it]*d_qmr[idr,it]) + (self.d_ena[idr,it]*self.d_qefl[idr,it])) / (d_qmix[idr,it])
                    #d_mni[idr,it] = ((d_ini[idr,it]*d_qmr[idr,it]) + (self.d_eni[idr,it]*self.d_qefl[idr,it])) / (d_qmr[idr,it] + self.d_qefl[idr,it])
                    d_mnn[idr,it] = ((d_inn[idr,it]*d_qmr[idr,it]) + (self.d_enn[idr,it]*self.d_qefl[idr,it])) / (d_qmix[idr,it])
                else:
                    d_mbod[idr,it] = d_ibod[idr,it]
                    d_mdo[idr,it] = d_ido[idr,it]
                    d_mcol[idr,it] = d_icol[idr,it]
                    d_mpo[idr,it] = d_ipo[idr,it]
                    d_mpi[idr,it] = d_ipi[idr,it]
                    d_mno[idr,it] = d_ino[idr,it] 
                    d_mna[idr,it] = d_ina[idr,it] 
                    #d_mni[idr,it] = d_ini[idr,it]
                    d_mnn[idr,it] = d_inn[idr,it]       


        
            # 4 - PROCESSOS DE TRANSFORMAÇÃO  --------------------------------------------------------------------
            for it in range(nt):
        
                time = (self.d_leng[idr]*1000) / (self.d_vel[idr]*86400)
        
                #BOD --------------------------------------------------------------------------------------------------------------------------
                d_dbod[idr,it] = d_mbod[idr,it] * np.exp(-1 * self.d_kr[idr] * time)
                
                
                #DISSOLVED OXIGEN -------------------------------------------------------------------------------------------------------------
                

                #DEFICIT DO
                def_do = (self.i_satdo- d_mdo[idr,it])* np.exp(-self.d_ka[idr] * time)


                #BOD PONTUAL
                
                if self.d_ka[idr] == self.d_kr[idr]:
                    self.d_ka[idr] = self.d_ka[idr] * 0.9

                def_bod = ((self.d_kd[idr] * d_mbod[idr,it]) / (self.d_ka[idr] - self.d_kr[idr])) * ((np.exp(-self.d_kr[idr] * time)) - (np.exp(-self.d_ka[idr] * time)))
                
                
                #NITRIFICAÇÃO

                RO2Namon = 4.57
                knitr=0.6
                fnitr = 1 - np.exp(-knitr* d_mdo[idr,it])
                
                kan_cor = self.d_kan[idr] * fnitr

                if (self.d_ka[idr] == kan_cor):
                    kan_cor = kan_cor*0.9
                    
                def_nitri = ((RO2Namon * kan_cor *d_mna[idr,it]) / (self.d_ka[idr] - kan_cor)) * (np.exp(-kan_cor * time) - np.exp(-self.d_ka[idr] * time))
                
                teste[idr,it]=fnitr
                
                
                #demanda de sedimento
                pSedUnit = 0.6
                pSed = pSedUnit /self.d_depth[idr]
                def_sed = pSed * (1 - np.exp(-self.d_ka[idr] * time))


                # DEFICIT TOTAL
                def_tot = def_do + def_bod + def_nitri #+ def_sed
                
                #FINAL CONCENTRATION
                d_ddo[idr,it] = self.i_satdo - def_tot

                
                #d_ddo[idr,it] =  self.d_satdo[idr] - (self.d_kd[idr] * d_mbod[idr,it] / 
                #     (self.d_ka[idr] - self.d_kd[idr]) * (np.exp(-self.d_kd[idr]*time) - np.exp(-self.d_ka[idr]*time)) + (self.d_satdo[idr] - d_mdo[idr,it]) * np.exp(-self.d_ka[idr]*time))
                
                #d_ddo_aux = d_ddo[idr,it]
                
                                
                # TRECHO EM ANAEOBIOSE ----------------------------------------------------------------------------------------------
                if (d_ddo[idr,it] < 0):
                     d_ddo[idr,it] = 0
                    
                        
                #COLIFORMS --------------------------------------------------------------------------------------------------------------------------
                d_dcol[idr,it] = (d_mcol[idr,it] * np.exp(-self.d_kcol[idr] * time))
        
        
                #PHOSPHORUS -------------------------------------------------------------------------------------------------------------------------
        
                d_dpo[idr,it] = d_mpo[idr,it] * np.exp(-1 * (self.d_koi[idr]+self.d_ksp[idr]) * time)
        
                #d_dpi[idr,it] = d_mpi[idr,it]+  (d_mpo[idr,it]* np.exp(-1 * self.d_kd[idr] * time))
                d_dpi[idr,it] = (d_mpi[idr,it] * np.exp(-self.d_ksp[idr] * time)) + (((self.d_koi[idr] * d_mpo[idr,it]) / 
                     (self.d_ksp[idr] - self.d_koi[idr])) * ((np.exp(-self.d_koi[idr] * time)) - (np.exp(-self.d_ksp[idr] * time))))
                
                
                #NITROGEN ----------------------------------------------------------------------------------------------------------------------------
        
                
                # NITROGENIO ORGANICO
                d_dno[idr,it] = d_mno[idr,it] * np.exp(-1 * self.d_koa[idr] * time)
        

                #NIT AMONIACAL
                
                if (self.d_kan[idr] == self.d_koa[idr]):
                    self.d_kan[idr] = self.d_kan[idr]*0.9
                
                d_dna[idr,it] = (d_mna[idr,it] * np.exp(-self.d_kan[idr] * time)) + (((self.d_koa[idr] * d_mno[idr,it]) /
                              (self.d_kan[idr] - self.d_koa[idr])) * ((np.exp(-self.d_koa[idr] * time)) - (np.exp(-self.d_kan[idr] * time))))
                
                               
                # NITRITO
                #NAUX_A = ((self.d_kai[idr] * d_mna[idr,it]) / (self.d_kin[idr] - self.d_kai[idr])) * (((np.exp(-self.d_kai[idr] * time)) - (np.exp(-self.d_kin[idr] * time))))
                #NAUX_B = ((self.d_kai[idr] * self.d_koa[idr] * d_mno[idr,it]) / (self.d_kai[idr] - self.d_koa[idr]))
                #NAUX_C = ((np.exp(-self.d_koa[idr] * time)) - (np.exp(-self.d_kin[idr] * time))) / (self.d_kin[idr] - self.d_koa[idr])
                #NAUX_D = ((np.exp(-self.d_kai[idr] * time)) - (np.exp(-self.d_kin[idr] * time))) / (self.d_kin[idr] - self.d_kai[idr])
                #d_dni[idr,it] = (d_mni[idr,it] * np.exp(-self.d_kin[idr] * time)) + (NAUX_A + (NAUX_B * (NAUX_C - NAUX_D)))


                # NITRATO
                #d_dnn[idr,it] = (d_mno[idr,it] - d_dno[idr,it]) + (d_mna[idr,it] - d_dna[idr,it]) + (d_mni[idr,it] - d_dni[idr,it]) + d_mnn[idr,it]
                d_dnn[idr,it] = (d_mna[idr,it]-d_dna[idr,it]+d_mnn[idr,it]) * np.exp(-self.d_kden[idr] * time)


        
            #5 - Entrada das cargas incrementais
            
            if self.sim_dif ==1:
                
                for it in range(nt):
                
                    d_cbod[idr,it] = (self.d_wbod[idr] / (d_qcat[idr,it])) * 0.01157
                    d_ccol[idr,it] = (self.d_wcol[idr] / (d_qcat[idr,it])) * (1 / 86400) * (1 / 10000)
                    d_cpo[idr,it] = (self.d_wpo[idr] / (d_qcat[idr,it])) * 0.01157
                    d_cpi[idr,it] = (self.d_wpi[idr] / (d_qcat[idr,it])) * 0.01157
                    d_cno[idr,it] = (self.d_wno[idr] / (d_qcat[idr,it])) * 0.01157
                    d_cna[idr,it] = (self.d_wna[idr] / (d_qcat[idr,it])) * 0.01157
                    #d_cni[idr,it] = (self.d_wnn[idr] / (d_qcat[idr,it])) * 0.01157
                    d_cnn[idr,it] = (self.d_wnn[idr] / (d_qcat[idr,it])) * 0.01157
                    d_cdo[idr,it] = self.i_do
                    
            else:
            
                    d_cbod[idr,it] = self.i_bod
                    d_ccol[idr,it] = self.i_col
                    d_cpo[idr,it] = self.i_po
                    d_cpi[idr,it] = self.i_pi
                    d_cno[idr,it] = self.i_no
                    d_cna[idr,it] = self.i_na
                    #d_cni[idr,it] = self.i_nn
                    d_cnn[idr,it] = self.i_nn
                    d_cdo[idr,it] = self.i_do
                    
                    
            for it in range(nt):
        
                 d_qout_aux[idr,it] = d_qmix[idr,it] + d_qcat[idr,it]
                
                 self.d_obod[idr,it] = ((d_dbod[idr,it]*d_qmix[idr,it]) + (d_cbod[idr,it]*d_qcat[idr,it])) / (d_qmix[idr,it] + d_qcat[idr,it])
                 self.d_odo[idr,it] = ((d_ddo[idr,it]*d_qmix[idr,it]) + (d_cdo[idr,it]*d_qcat[idr,it])) / (d_qmix[idr,it] + d_qcat[idr,it])
                 self.d_ocol[idr,it] = ((d_dcol[idr,it]*d_qmix[idr,it]) + (d_ccol[idr,it]*d_qcat[idr,it])) / (d_qmix[idr,it] + d_qcat[idr,it])
                 self.d_opo[idr,it] = ((d_dpo[idr,it]*d_qmix[idr,it]) + (d_cpo[idr,it]*d_qcat[idr,it])) / (d_qmix[idr,it] + d_qcat[idr,it])
                 self.d_opi[idr,it] = ((d_dpi[idr,it]*d_qmix[idr,it]) + (d_cpi[idr,it]*d_qcat[idr,it])) / (d_qmix[idr,it] + d_qcat[idr,it])
                 self.d_ono[idr,it] = ((d_dno[idr,it]*d_qmix[idr,it]) + (d_cno[idr,it]*d_qcat[idr,it])) / (d_qmix[idr,it] + d_qcat[idr,it])
                 self.d_ona[idr,it] = ((d_dna[idr,it]*d_qmix[idr,it]) + (d_cna[idr,it]*d_qcat[idr,it])) / (d_qmix[idr,it] + d_qcat[idr,it])
                 #self.d_oni[idr,it] = ((d_dni[idr,it]*d_qmix[idr,it]) + (d_cni[idr,it]*d_qcat[idr,it])) / (d_qmix[idr,it] + d_qcat[idr,it])
                 self.d_onn[idr,it] = ((d_dnn[idr,it]*d_qmix[idr,it]) + (d_cnn[idr,it]*d_qcat[idr,it])) / (d_qmix[idr,it] + d_qcat[idr,it])
                 self.d_opt[idr,it] = self.d_opo[idr,it] + self.d_opi[idr,it]
     

            #6 - Vazão final do trecho
            

            for it in range(nt):
                
                 self.d_qout[idr,it] = d_qmix[idr,it] + d_qcat[idr,it] - self.d_qwit[idr,it]
                 self.d_qnatres[idr,it] = d_qmnr[idr,it] + d_qcat[idr,it]
                 

                 if self.d_qout[idr,it]< (0.05*(d_qmix[idr,it] + d_qcat[idr,it])):
                    self.d_qout[idr,it] = 0.05*(d_qmix[idr,it] + d_qcat[idr,it])

                 self.d_obod[idr,it] = ((self.d_obod[idr,it]*d_qout_aux[idr,it])) / (self.d_qout[idr,it])
                 self.d_odo[idr,it] = ((self.d_odo[idr,it]*d_qout_aux[idr,it]) ) / (self.d_qout[idr,it])
                 self.d_ocol[idr,it] = ((self.d_ocol[idr,it]*d_qout_aux[idr,it]) ) / (self.d_qout[idr,it])
                 self.d_opo[idr,it] = ((self.d_opo[idr,it]*d_qout_aux[idr,it]) ) / (self.d_qout[idr,it])
                 self.d_opi[idr,it] = ((self.d_opi[idr,it]*d_qout_aux[idr,it]) ) / (self.d_qout[idr,it])
                 self.d_ono[idr,it] = ((self.d_ono[idr,it]*d_qout_aux[idr,it])) / (self.d_qout[idr,it])
                 self.d_ona[idr,it] = ((self.d_ona[idr,it]*d_qout_aux[idr,it]) ) / (self.d_qout[idr,it])
                 self.d_onn[idr,it] = ((self.d_onn[idr,it]*d_qout_aux[idr,it]) ) / (self.d_qout[idr,it])

             
            #7 - RESERVOIR MODULE
            
            #vazão substituída no espelho d'agua            
            if (self.d_codres[idr] >= 1):
                 
                 ind = np.array(np.where(self.r_codres == self.d_codres[idr]))
                 ir = ind[0][0]
                 
                 for it in range(nt):
                     
                     self.d_qout[idr,it] = self.r_qsubs[ir,it]
                     self.d_qnatres[idr,it] = self.r_qsubs[ir,it]

                     #concentrações nos trechos do barramento
                     self.d_obod[idr,it] = self.i_bod
                     self.d_odo[idr,it] = self.i_do
                     self.d_ocol[idr,it] = self.i_col
                     self.d_opo[idr,it] = self.i_opo
                     self.d_opi[idr,it] = self.i_opi
                     self.d_ono[idr,it] = self.i_ono
                     self.d_ona[idr,it] = self.i_ona
                     #self.d_oni[idr,it] = self.i_oni
                     self.d_onn[idr,it] = self.i_onn
                     self.d_opt[idr,it] = self.d_opo[idr,it] + self.d_opi[idr,it]
                     
                     
            #barramento
            ind_res = np.array(np.where(self.r_codbas == self.d_codbas[idr]))

            if (ind_res.size)==1:

                
                ir =ind_res[0][0]                
                for it in range(nt):
                    self.d_qout[idr,it] = self.r_qrel[ir,it]
                    self.d_qnatres[idr,it] = self.r_qrel[ir,it]


            #7 - water balance
            for it in range(nt):
                self.d_wbal[idr,it]= ((self.d_qnatres[idr,it]- self.d_qout[idr,it])/ self.d_qnatres[idr,it])*100
                
                if self.d_wbal[idr,it]<0:
                    self.d_wbal[idr,it]=0
                    

        return self.d_obod, self.d_odo, self.d_ocol,self.d_opo,self.d_opi, self.d_ono,self.d_ona, self.d_onn, self.d_opt, self.d_qout, self.d_wbal
        #return self.d_obod, self.d_odo, self.d_ocol,self.d_opo,self.d_opi, self.d_ono,self.d_ona, self.d_onn, self.d_opt, self.d_qout, d_qmix    
        
        
    def graph_profile(self, inp_codbas, inp_codjus, par, with_obs, with_enq, with_text, path_stations=None, path_obs=None):
        

        #READ OBSERVED DATA ############################################################################################   
        if with_obs == True:
            
            # READ OBSERVED FILE
            rows = []

            s_ids=[]
            s_codbas=[]
            
            with open(path_stations, 'r', encoding='utf-8') as read_obj:
                csv_reader = reader(read_obj, delimiter=';')
                header = next(csv_reader)
                if header != None:
                    for row in csv_reader:
                        rows.append(row)
                    
                    
            for i in range(len(rows)):
                s_ids.append(str(rows[i][0]))
                s_codbas.append(float(rows[i][1]))
                
                
            s_codbas = [int(m) for m in s_codbas]
                


            # READ OBSERVED FILE
            rows = []
        
            l_ids=[]
            l_bods=[]
            l_dos=[]
            l_cols=[]
            l_pts=[]
            l_nos=[]
            l_nas=[]
            l_nns=[]
    
            with open(path_obs, 'r', encoding='utf-8') as read_obj:
                csv_reader = reader(read_obj, delimiter=';')
                header = next(csv_reader)
                if header != None:
                    for row in csv_reader:
                        rows.append(row)
                    

            for i in range(len(rows)):
                l_ids.append(str(rows[i][0]))
                l_bods.append(str(rows[i][1]))
                l_dos.append(str(rows[i][2]))
                l_cols.append(str(rows[i][3]))
                l_pts.append(str(rows[i][4]))
                l_nos.append(str(rows[i][5]))
                l_nas.append(str(rows[i][6]))
                l_nns.append(str(rows[i][7]))
        



        #READ CALCULATED DATA  ############################################################################################        
        
        codjus=0
        l_profile=[]
        l_lengh=[]
        
        l_codbas=[]

        l_cod_trecho=[]
        l_bod_trecho=[]
        l_do_trecho=[]
        l_col_trecho=[]
        l_pt_trecho=[]
        l_no_trecho=[]
        l_na_trecho=[]
        l_nn_trecho=[]
        l_pos_trecho=[]        
        

        l_bod_tr_sim=[]
        l_do_tr_sim=[]
        l_col_tr_sim=[]
        l_pt_tr_sim=[]
        l_no_tr_sim=[]
        l_na_tr_sim=[]
        l_nn_tr_sim=[]

        
        
        i=0

        while (inp_codjus != codjus):


            ind = (np.where(self.d_codbas == inp_codbas))
            it=0
            
            l_bod_tr_sim.append(float(self.d_obod[ind,it]))
            l_do_tr_sim.append(float(self.d_odo[ind,it]))
            l_col_tr_sim.append(float(self.d_ocol[ind,it]))
            l_pt_tr_sim.append(float(self.d_opt[ind,it]))
            l_no_tr_sim.append(float(self.d_ono[ind,it]))
            l_na_tr_sim.append(float(self.d_ona[ind,it]))
            l_nn_tr_sim.append(float(self.d_onn[ind,it]))
            
            
            if (i==0):
                l_lengh.append(float(self.d_leng[ind]))
            else:
                l_lengh.append(float(self.d_leng[ind])+l_lengh[i-1])
                
            l_codbas.append(inp_codbas)
                
                
            ###################################################################################################    
            #inserir dados de monitoramento nos trechos ------------------------------------------------------
                
            if with_obs == True:
            
                #verifica se tem algum codbas com monitoramento 
                ind_cod = np.array(np.where(np.array(s_codbas) == int(inp_codbas)))
    
                if (ind_cod.size>0):
        
                    pos=ind_cod[0][0]
                    station = s_ids[pos]

                    ind_est = np.array(np.where(np.array(l_ids) == station))
                    
                    #QMessageBox.information(self.iface.mainWindow(), station)


                    l_bod_sel=[]
                    l_do_sel=[]
                    l_col_sel=[]
                    l_pt_sel=[]
                    l_no_sel=[]
                    l_na_sel=[]
                    l_nn_sel=[]


                    for j in range(ind_est.size):
    
                        l_bod_sel.append(l_bods[ind_est[0,j]])
                        l_do_sel.append(l_dos[ind_est[0,j]])
                        l_col_sel.append(l_cols[ind_est[0,j]])
                        l_pt_sel.append(l_pts[ind_est[0,j]])
                        l_no_sel.append(l_nos[ind_est[0,j]])
                        l_na_sel.append(l_nas[ind_est[0,j]])
                        l_nn_sel.append(l_nns[ind_est[0,j]])

        
                    l_bod_sel = list(filter(lambda x: str(x) != 'nan', l_bod_sel))
                    l_do_sel = list(filter(lambda x: str(x) != 'nan', l_do_sel))
                    l_col_sel = list(filter(lambda x: str(x) != 'nan', l_col_sel))
                    l_pt_sel = list(filter(lambda x: str(x) != 'nan', l_pt_sel))
                    l_no_sel = list(filter(lambda x: str(x) != 'nan', l_no_sel))
                    l_na_sel = list(filter(lambda x: str(x) != 'nan', l_na_sel))
                    l_nn_sel = list(filter(lambda x: str(x) != 'nan', l_nn_sel))


        
                    l_bod_sel = [float(m) for m in l_bod_sel]
                    l_do_sel = [float(m) for m in l_do_sel]
                    l_col_sel = [float(m) for m in l_col_sel]
                    l_pt_sel = [float(m) for m in l_pt_sel]
                    l_no_sel = [float(m) for m in l_no_sel]
                    l_na_sel = [float(m) for m in l_na_sel]
                    l_nn_sel = [float(m) for m in l_nn_sel]


                    l_cod_trecho.append(inp_codbas)
                    l_bod_trecho.append(l_bod_sel)
                    l_do_trecho.append(l_do_sel)
                    l_col_trecho.append(l_col_sel)
                    l_pt_trecho.append(l_pt_sel)
                    l_no_trecho.append(l_no_sel)    
                    l_na_trecho.append(l_na_sel)
                    l_nn_trecho.append(l_nn_sel)
                
                    l_pos_trecho.append(l_lengh[i])


            ####################################################################
            # atualiza p/ proximo trecho
            codjus = self.d_codjus[ind]
    
            indjus = (np.where(self.d_codbas == codjus))
            inp_codbas = self.d_codbas[indjus][0]
            
            
            i=i+1
        #FIM LOOP TRECHOS  #############################################################################
        
        
        # PLOT PROFILE
        f, ax = plt.subplots(1, figsize=(12, 6))

        if (len(l_bod_trecho)>0):
            

            def switch(case):
                if case == 'BOD':
                    return(l_bod_trecho)
                elif case == 'DO':                
                    return (l_do_trecho)
                elif case == 'Col':               
                    return (l_col_trecho)
                elif case == 'Pt':                
                    return (l_pt_trecho) 
                elif case == 'No':
                    return(l_no_trecho)
                elif case == 'Na':                
                    return (l_na_trecho)
                elif case == 'Nn':                
                    return (l_nn_trecho) 

            l_obs_select = switch(par)            
            
            ax.boxplot(l_obs_select, positions= l_pos_trecho, widths = 5, patch_artist = True, zorder=1)
        

        
        def switch(case):
            if case == 'BOD':
                return(l_bod_tr_sim)
            elif case == 'DO':                
                return (l_do_tr_sim)
            elif case == 'Col':               
                return (l_col_tr_sim)
            elif case == 'Pt':                
                return (l_pt_tr_sim) 
            elif case == 'No':
                return(l_no_tr_sim)
            elif case == 'Na':                
                return (l_na_tr_sim)
            elif case == 'Nn':                
                return (l_nn_tr_sim) 

        l_cal_select = switch(par)    
        

        ax.plot(l_lengh,l_cal_select, linestyle="-", color='black', zorder=3)
        ax.set_xticks([])
        
        
        if (par == 'Col'):
            ax.set_yscale('log')
            
            
            
        if with_enq == True:
            
            l_classe1=[]
            l_classe2=[]
            l_classe3=[]
            
            
            for k in range(len(l_lengh)):
            
                def switch_c1(case):
                    if case == 'BOD':
                        return(3)
                    elif case == 'DO':                
                        return (6)
                    elif case == 'Col':               
                        return (200)
                    elif case == 'Pt':                
                        return (0.1)
                    elif case == 'No':
                        return(10)
                    elif case == 'Na':                
                        return (3.7)
                    elif case == 'Nn':                
                        return (10)

                def switch_c2(case):
                    if case == 'BOD':
                        return(5)
                    elif case == 'DO':                
                        return (5)
                    elif case == 'Col':               
                        return (1000)
                    elif case == 'Pt':                
                        return (0.1)
                    elif case == 'No':
                        return(10)
                    elif case == 'Na':                
                        return (3.7)
                    elif case == 'Nn':                
                        return (10)

                def switch_c3(case):
                    if case == 'BOD':
                        return(10)
                    elif case == 'DO':                
                        return (4)
                    elif case == 'Col':               
                        return (2500)
                    elif case == 'Pt':                
                        return (0.15)
                    elif case == 'No':
                        return(10)
                    elif case == 'Na':                
                        return (13.3)
                    elif case == 'Nn':                
                        return (10)
                
            
                l_classe1.append(switch_c1(par))
                l_classe2.append(switch_c2(par))
                l_classe3.append(switch_c3(par))
            
            
            ax.plot(l_lengh, l_classe1, linestyle="--", color='blue', zorder=3)
            ax.plot(l_lengh, l_classe2, linestyle="--", color='green', zorder=3)
            ax.plot(l_lengh, l_classe3, linestyle="--", color='yellow', zorder=3)


        
        
        
        #start, end = ax.get_xlim()
        #ax.xaxis.set_ticks(np.arange(0, 350, 50))
        
        
        #plt.xticks(np.arange(0, l_lengh[i-1], 50))
        
        x_label = np.arange(0, l_lengh[i-1], int(l_lengh[i-1]/5))
        
        plt.xticks(x_label, x_label)
        
        
        ax.set_xlim(0, l_lengh[i-1])
        
        ax.grid(True)
        ax.grid('grid', linestyle="--", color='#E8E8E8')
        
        
        ax.set_ylabel("Concentration (mg/L)", fontsize=10)
        ax.set_xlabel("Distance from upstream to downstream basin (km)", fontsize=10)

        if (par == 'Col'):
            ax.set_ylabel("Concentration (org/100ml)", fontsize=10)
    
    
    
        ax.set_title("Longituginal concentration profile", fontsize=11)


        plt.show()
        
        
        if with_text== True:
            
            
            #WRITE INPUT FILE 

            name = QFileDialog.getSaveFileName(parent=None, caption='Save longitudinal profile', filter='.csv files (*.csv)')

            name = name[0]
            self.dir = os.path.dirname(name) + '/'
            for i in name:
                if i == '\\':
                    name = name.replace('\\', '/')


            file = open(str(name), 'w')

            file.write('Length; BOD; DO; Col; Pt; No; Na; Nn; \n')
            
            for i in range (len(l_bod_tr_sim)):
                file.write(str(l_lengh[i]) + ';' + str(l_bod_tr_sim[i]) + ';' + str(l_do_tr_sim[i]) + ';' + str(l_col_tr_sim[i]) + ';' + str(l_pt_tr_sim[i]) + ';' + str(l_no_tr_sim[i]) + ';' + str(l_na_tr_sim[i]) + ';' + str(l_nn_tr_sim[i]) + ';'  +  ' \n')
                #file.write(str(l_lengh[i]) + ';' + str(l_codbas[i]) +   ' \n')
                
           

            file.close()




















