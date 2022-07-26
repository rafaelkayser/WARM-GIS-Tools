# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 13:44:22 2022

@author: Rafael Kayser
"""


import os, sys, datetime
import numpy as np
import matplotlib.pyplot as plt

from qgis.core import *

from qgis.PyQt.QtWidgets import QMessageBox

from PyQt5.QtWidgets import *



########################################################################


class Balance_Model:
    

    
    
    def __init__ (self, lyr_drl, lyr_wit, lyr_res, nt, scn_fix, scn_number):
        self.lyr_drl = lyr_drl
        self.lyr_wit = lyr_wit
        self.lyr_res = lyr_res
        self.nt = nt
        
        self.scn_fix = scn_fix
        self.scn_number = scn_number
        
        
        
    def read_files(self):


        # READ DRAINAGE LINE --------------------------------------------------------------------------------------        
        
        nd =  self.lyr_drl.featureCount()
        nt=self.nt
        
     
        self.d_codbas= np.empty((0,0))
        self.d_codjus= np.empty((0,0))
        self.d_ord= np.empty((0,0))
        self.d_mini= np.empty((0,0))
        self.d_codres= np.empty((0,0))
        self.d_leng = np.empty((0,0))
        self.d_vel= np.empty((0,0))
        self.d_subw= np.empty((0,0))
        self.d_depth= np.empty((0,0))
        self.d_qnat= np.empty((0,nt))
        

        features = self.lyr_drl.getFeatures()

        for feature in features:
            
            self.d_codbas = np.append(self.d_codbas, feature['CodBas_ID'])
            self.d_codjus = np.append(self.d_codjus, feature['CodDown_ID'])
            self.d_ord = np.append(self.d_ord, feature['Order_ID'])
            self.d_mini = np.append(self.d_mini, feature['Mini_ID'])
            self.d_codres = np.append(self.d_codres, feature['Reserv_ID'])
            self.d_leng = np.append(self.d_leng, feature['Length_km'])
            
            # cenario fixo de vazão
            if self.scn_fix == "str":
                aux_qnat = np.empty((0,nt))
                for it in range(0,nt):
                    aux_qnat = np.append(aux_qnat, feature['Q_Read_'+str(self.scn_number)])
                aux_qnat.resize(1,nt)
                self.d_qnat = np.append(self.d_qnat, aux_qnat, axis=0)
                    
            # cenario variavel de vazão
            elif self.scn_fix == "wit":
                aux_qnat = np.empty((0,nt))
                for it in range(0,nt):
                    aux_qnat = np.append(aux_qnat, feature['Q_Read_'+str(it+1)])                
                aux_qnat.resize(1,nt)
                self.d_qnat = np.append(self.d_qnat, aux_qnat, axis=0)                

            # ambos variaveis
            elif self.scn_fix == "var":
                aux_qnat = np.empty((0,nt))
                for it in range(0,nt):
                    aux_qnat = np.append(aux_qnat, feature['Q_Read_'+str(it+1)])                
                aux_qnat.resize(1,nt)
                self.d_qnat = np.append(self.d_qnat, aux_qnat, axis=0) 





            
        # READ WITHDRAWALS  ----------------------------------------------------------------------------------------------
        nw =  self.lyr_wit.featureCount()
        nt=self.nt
        
        self.w_codbas=np.empty((0))
        
        self.w_qwit= np.empty((0, nt))
     
        
        
        features = self.lyr_wit.getFeatures()

        for feature in features:
            
            
            # Append list as a column to the 2D Numpy array
            self.w_codbas = np.append(self.w_codbas, feature['CodBas_ID'])  #.transpose(), axis=1)
            
            
            # cenario fixo de demanda
            if self.scn_fix == "wit":            
                aux_qwit = np.empty((0,nt))
                for it in range(0,nt):
                    aux_qwit = np.append(aux_qwit, feature['Q_Wit_'+str(self.scn_number)])
                aux_qwit.resize(1,nt)
                self.w_qwit = np.append(self.w_qwit, aux_qwit, axis=0)
            
            # cenario variavel de demanda
            elif self.scn_fix == "str":
                aux_qwit = np.empty((0,nt))
                for it in range(0,nt):
                    aux_qwit = np.append(aux_qwit, feature['Q_Wit_'+str(it+1)])
                aux_qwit.resize(1,nt)
                self.w_qwit = np.append(self.w_qwit, aux_qwit, axis=0)


            # ambos variaveis
            elif self.scn_fix == "var":
                aux_qwit = np.empty((0,nt))
                for it in range(0,nt):
                    aux_qwit = np.append(aux_qwit, feature['Q_Wit_'+str(it+1)])
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
        self.r_fiodag=np.empty((0))
        
        self.r_qrel = np.empty((0, nt))
        self.r_qsubs = np.empty((0, nt))     
        
        if (nr>0):
        
          features = self.lyr_res.getFeatures()
          
          for feature in features:
            
            # Append list as a column to the 2D Numpy array
            self.r_codres = np.append(self.r_codres, feature['Res_ID'])
            self.r_codbas = np.append(self.r_codbas, feature['CodBas_ID'])
            self.r_fiodag = np.append(self.r_fiodag, feature['With_ROR'])
            
            #if self.r_fiodag[i] ==0:
            if (0==0):
            
                aux_qrel = np.empty((0,nt))
                for it in range(0,nt):
                    aux_qrel = np.append(aux_qrel, feature['Q_Rel_1'])
                aux_qrel.resize(1,nt)
                self.r_qrel = np.append(self.r_qrel, aux_qrel, axis=0)

                aux_qsubs = np.empty((0,nt))
                for it in range(0,nt):
                    aux_qsubs = np.append(aux_qsubs, feature['Q_Subs_1'])
                aux_qsubs.resize(1,nt)
                self.r_qsubs = np.append(self.r_qsubs, aux_qsubs, axis=0)
                
                
                
                
          for ir in range(nr):
                
                if self.r_fiodag[ir] ==1: 
                    for idr in range(0,nd):    
                        if (self.d_codbas[idr]==self.r_codbas[ir]):
                            for it in range (0, nt):
                                self.r_qrel[ir,it]= self.d_qnat[idr,it]
                                #self.r_qsubs[ir,it]= self.d_qnat[idr,it]
                




    def run_model(self):
        
        
        nd = self.lyr_drl.featureCount()
        nt=self.nt
        
        d_qmn=np.zeros((nd, nt))
        d_qmr=np.zeros((nd, nt))
        d_qmd=np.zeros((nd, nt))
        d_qmnr=np.zeros((nd, nt))
      
        d_qcat=np.zeros((nd, nt))
        self.d_qout=np.zeros((nd, nt))
        self.d_qdef=np.zeros((nd, nt))
        self.d_qdefacm=np.zeros((nd, nt))
        self.d_wbal=np.zeros((nd, nt))
        self.d_qnatres=np.zeros((nd, nt))
        
        
        d_minisort = np.arange(1,nd+1)

        # EXECUÇÃO DO MODELO 
        
        for ic in range(nd):
            
            ind = np.array(np.where(self.d_mini == d_minisort[ic]))
            idr =ind[0][0]

        #for idr in range(0,nd):
    
            #1 - UPSTREAM CONCENTRATION 
            if self.d_ord[idr] ==1:
        
                for it in range(nt):
                    
                     d_qmn[idr,it]=0  #montante - natural
                     d_qmr[idr,it]=0  #montante - remanescente                   
                     d_qmd[idr,it]=0  #deficit 
                     d_qmnr[idr,it]=0  #natural com reservatorios

            else:
        
                ind_jus = np.array(np.where(self.d_codjus == self.d_codbas[idr]))
        
                if (ind_jus.size)==2:
            
                    for it in range(nt):
                        
                        qmn1 = self.d_qnat[ind_jus[0,0],it]
                        qmn2 = self.d_qnat[ind_jus[0,1],it]
                        d_qmn[idr,it] = qmn1+qmn2
            
                        qmr1 = self.d_qout[ind_jus[0,0],it]
                        qmr2 = self.d_qout[ind_jus[0,1],it]
                        d_qmr[idr,it] = qmr1+qmr2 

                        qmd1 = self.d_qdefacm[ind_jus[0,0],it]
                        qmd2 = self.d_qdefacm[ind_jus[0,1],it]
                        d_qmd[idr,it] = qmd1+qmd2 

                        qmnr1 = self.d_qnatres[ind_jus[0,0],it]
                        qmnr2 = self.d_qnatres[ind_jus[0,1],it]
                        d_qmnr[idr,it] = qmnr1+qmnr2 



                elif (ind_jus.size)==3:
            
                    for it in range(nt):
                
                        qmn1 = self.d_qnat[ind_jus[0,0],it]
                        qmn2 = self.d_qnat[ind_jus[0,1],it]
                        qmn3 = self.d_qnat[ind_jus[0,2],it]
                        d_qmn[idr,it] = qmn1+qmn2+qmn3
            
                        qmr1 = self.d_qout[ind_jus[0,0],it]
                        qmr2 = self.d_qout[ind_jus[0,1],it]
                        qmr3 = self.d_qout[ind_jus[0,2],it]
                        d_qmr[idr,it] = qmr1+qmr2+qmr3
                        
                        qmd1 = self.d_qdefacm[ind_jus[0,0],it]
                        qmd2 = self.d_qdefacm[ind_jus[0,1],it]
                        qmd3 = self.d_qdefacm[ind_jus[0,2],it]
                        d_qmd[idr,it] = qmd1+qmd2+qmd3                        

                        qmnr1 = self.d_qnatres[ind_jus[0,0],it]
                        qmnr2 = self.d_qnatres[ind_jus[0,1],it]
                        qmnr3 = self.d_qnatres[ind_jus[0,2],it]
                        d_qmnr[idr,it] = qmnr1+qmnr2+qmnr3

                elif (ind_jus.size)==4:
            
                    for it in range(nt):
                
                        qmn1 = self.d_qnat[ind_jus[0,0],it]
                        qmn2 = self.d_qnat[ind_jus[0,1],it]
                        qmn3 = self.d_qnat[ind_jus[0,2],it]
                        qmn4 = self.d_qnat[ind_jus[0,3],it]
                        d_qmn[idr,it] = qmn1+qmn2+qmn3+qmn4
            
                        qmr1 = self.d_qout[ind_jus[0,0],it]
                        qmr2 = self.d_qout[ind_jus[0,1],it]
                        qmr3 = self.d_qout[ind_jus[0,2],it]
                        qmr4 = self.d_qout[ind_jus[0,3],it]
                        d_qmr[idr,it] = qmr1+qmr2+qmr3+qmr4
                        
                        qmd1 = self.d_qdefacm[ind_jus[0,0],it]
                        qmd2 = self.d_qdefacm[ind_jus[0,1],it]
                        qmd3 = self.d_qdefacm[ind_jus[0,2],it]
                        qmd4 = self.d_qdefacm[ind_jus[0,3],it]
                        d_qmd[idr,it] = qmd1+qmd2+qmd3+qmd4                     

                        qmnr1 = self.d_qnatres[ind_jus[0,0],it]
                        qmnr2 = self.d_qnatres[ind_jus[0,1],it]
                        qmnr3 = self.d_qnatres[ind_jus[0,2],it]
                        qmnr4 = self.d_qnatres[ind_jus[0,3],it]
                        d_qmnr[idr,it] = qmnr1+qmnr2+qmnr3+qmnr4


                elif (ind_jus.size)==5:
            
                    for it in range(nt):
                
                        qmn1 = self.d_qnat[ind_jus[0,0],it]
                        qmn2 = self.d_qnat[ind_jus[0,1],it]
                        qmn3 = self.d_qnat[ind_jus[0,2],it]
                        qmn4 = self.d_qnat[ind_jus[0,3],it]
                        qmn5 = self.d_qnat[ind_jus[0,4],it]
                        d_qmn[idr,it] = qmn1+qmn2+qmn3+qmn4+qmn5
            
                        qmr1 = self.d_qout[ind_jus[0,0],it]
                        qmr2 = self.d_qout[ind_jus[0,1],it]
                        qmr3 = self.d_qout[ind_jus[0,2],it]
                        qmr4 = self.d_qout[ind_jus[0,3],it]
                        qmr5 = self.d_qout[ind_jus[0,4],it]
                        d_qmr[idr,it] = qmr1+qmr2+qmr3+qmr4+qmr5
                        
                        qmd1 = self.d_qdefacm[ind_jus[0,0],it]
                        qmd2 = self.d_qdefacm[ind_jus[0,1],it]
                        qmd3 = self.d_qdefacm[ind_jus[0,2],it]
                        qmd4 = self.d_qdefacm[ind_jus[0,3],it]
                        qmd5 = self.d_qdefacm[ind_jus[0,4],it]
                        d_qmd[idr,it] = qmd1+qmd2+qmd3+qmd4+ qmd5                   

                        qmnr1 = self.d_qnatres[ind_jus[0,0],it]
                        qmnr2 = self.d_qnatres[ind_jus[0,1],it]
                        qmnr3 = self.d_qnatres[ind_jus[0,2],it]
                        qmnr4 = self.d_qnatres[ind_jus[0,3],it]
                        qmnr5 = self.d_qnatres[ind_jus[0,4],it]
                        d_qmnr[idr,it] = qmnr1+qmnr2+qmnr3+qmnr4+qmnr5


            
            # 2 - incremental streamflow
            for it in range(nt):
                d_qcat[idr,it] = self.d_qnat[idr,it] - d_qmn[idr,it]
                
    
    
            # 3 - WATER BALANCE 
            for it in range(nt):
    
                self.d_qout[idr,it] = (d_qmr[idr,it] + d_qcat[idr,it]-self.d_qwit[idr,it])
                self.d_qnatres[idr,it] = d_qmnr[idr,it] + d_qcat[idr,it]
                
                if (self.d_qout[idr,it] < 0):
                    
                    self.d_qout[idr,it] = 0
                    self.d_qdef[idr,it] = self.d_qwit[idr,it] -(d_qmr[idr,it] + d_qcat[idr,it])
                    

                    
            #5 - DEFICIT ACUMULADO
            for it in range(nt):
                self.d_qdefacm[idr,it]= d_qmd[idr,it] + self.d_qdef[idr,it]
                
            #6 - BALANCO HÍDRICO FINAL                    
            for it in range(nt):
                #self.d_wbal[idr,it]= ((self.d_qnat[idr,it]- self.d_qout[idr,it])/ self.d_qnat[idr,it])*100
                self.d_wbal[idr,it]= ((self.d_qnatres[idr,it]- self.d_qout[idr,it])/ self.d_qnatres[idr,it])*100
                
                if self.d_wbal[idr,it]==100:
                    self.d_wbal[idr,it]= (self.d_qwit[idr,it] / (self.d_qwit[idr,it] - self.d_qdef[idr,it]))*100

                    
            #4 - RESERVOIR MODULE
            
            #vazão substituída no espelho d'agua            
            if (self.d_codres[idr] >= 1):
                 
                 ind = np.array(np.where(self.r_codres == self.d_codres[idr]))
                 ir = ind[0][0]
                 
                 for it in range(nt):
                     
                     self.d_qout[idr,it] = self.r_qsubs[ir,it]
                     self.d_qnatres[idr,it] = self.r_qsubs[ir,it]
                     self.d_wbal[idr,it]= (self.d_qwit[idr,it] / self.r_qsubs[ir,it])*100
                     
                     if self.d_wbal[idr,it]<100:
                         self.d_qdef[idr,it] = 0
                     else:
                         self.d_qdef[idr,it] = self.d_qwit[idr,it] - self.r_qsubs[ir,it]
                     
            #barramento
            ind_res = np.array(np.where(self.r_codbas == self.d_codbas[idr]))

            if (ind_res.size)==1:

                
                ir =ind_res[0][0]                
                for it in range(nt):
                    self.d_qout[idr,it] = self.r_qrel[ir,it]
                    self.d_qnatres[idr,it] = self.r_qrel[ir,it]
                    
                    
        return self.d_qout, self.d_wbal, self.d_qdefacm, self.d_codbas
      #  return self.d_qout, self.d_wbal, self.d_qdef, self.d_codbas
    


    def graph_profile(self, inp_codbas, inp_codjus, cen, with_text):
    

        #READ CALCULATED DATA  ############################################################################################        
        
        codjus=0
        l_lengh=[]
        
        
        l_qrem=[]
        l_qnat=[]
        l_qdef=[]
        
        
        i=0

        while (inp_codjus != codjus):


            ind = (np.where(self.d_codbas == inp_codbas))
            it=cen-1
            
            
            l_qrem.append( float(self.d_qout[ind,it]))
            l_qnat.append( float(self.d_qnatres[ind,it]))
            l_qdef.append( float(self.d_qdefacm[ind,it]))
            

            if (i==0):
                l_lengh.append(float(self.d_leng[ind]))
            else:
                l_lengh.append(float(self.d_leng[ind])+l_lengh[i-1])
                
                
            # atualiza p/ proximo trecho
            codjus = self.d_codjus[ind]
    
            indjus = (np.where(self.d_codbas == codjus))
            inp_codbas = self.d_codbas[indjus]
            
            
            i=i+1
        #FIM LOOP TRECHOS
        
        
        f, ax = plt.subplots(1, figsize=(12, 6))

            
        ax.plot(l_lengh, l_qrem, linestyle="-", color='black', zorder=3, label = 'Remaining discharge')
        ax.plot(l_lengh, l_qnat, linestyle="-", color='blue', zorder=3, label = 'Natural discharge')
        ax.plot(l_lengh, l_qdef, linestyle="-", color='red', zorder=3, label = 'Accumulated water deficit')
        
        ax.set_xticks([])
        

        
        #plt.xticks(np.arange(0, l_lengh[i-1], 50))
        
        x_label = np.arange(0, l_lengh[i-1], int(l_lengh[i-1]/5))
        
        plt.xticks(x_label, x_label)
        
        
        ax.set_xlim(0, l_lengh[i-1])
        
        ax.grid(True)
        ax.grid('grid', linestyle="--", color='#E8E8E8')
        
        
        ax.set_ylabel("Discharge (m³/s)", fontsize=10)
    
    
        ax.set_title("Longituginal profile", fontsize=11)
        
        
        ax.legend(fontsize=9)


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

            file.write('Length; Qrem; Qnat; \n')
            
            for i in range (len(l_lengh)):
                file.write(str(l_lengh[i]) + ';' + str(l_qrem[i]) + ';' + str(l_qnat[i]) + '; \n')


        file.close()
            
            
        
        
        
        










