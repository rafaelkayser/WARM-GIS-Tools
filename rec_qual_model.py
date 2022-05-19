# -*- coding: utf-8 -*-
"""
Created on Thu May  5 20:14:46 2022

@author: rafae
"""

       # READ PARAMETERS FILE -------------------------------------------------------------------------
        
        list_input = []
        with open(self.path_par, 'r') as read_obj:
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
        self.i_ni=float(list_input[7][1])
        self.i_nn=float(list_input[8][1])        
        
        nb = int(list_input[9][1])
        
        kdd = []
        kds=[]
        ksmo=[]
        ka=[]
        kcol=[]
        koi=[]
        ksp=[]
        koa=[]
        kai=[]
        kin=[]
        temp=[]
        vel=[]
        
        
        for ib in range(nb):
            kdd.append(float(list_input[11][ib+1]))
            kds.append(float(list_input[12][ib+1]))
            ksmo.append(float(list_input[13][ib+1]))
            ka.append(float(list_input[14][ib+1]))
            kcol.append(float(list_input[15][ib+1]))
            koi.append(float(list_input[16][ib+1]))
            ksp.append(float(list_input[17][ib+1]))
            koa.append(float(list_input[18][ib+1]))
            kai.append(float(list_input[19][ib+1]))
            kin.append(float(list_input[20][ib+1]))        
            temp.append(float(list_input[21][ib+1]))
            vel.append(float(list_input[22][ib+1]))
            
            
        #atribuir nos trechos da rede de drenagem    
        
        self.d_kd=np.empty((nd))
        self.d_ksmo=np.empty((nd))
        self.d_kr=np.empty((nd))
        self.d_ka=np.empty((nd))
        self.d_kcol=np.empty((nd))
        self.d_koi=np.empty((nd))
        self.d_ksp=np.empty((nd))        
        self.d_koa=np.empty((nd))
        self.d_kai=np.empty((nd))
        self.d_kin=np.empty((nd))      
        self.d_temp=np.empty((nd))
        self.d_vel=np.empty((nd))        
        self.d_satdo=np.empty((nd))
        
        
        for ib in range (nb):
        
            for idr in range(nd):
            
                if (self.d_subw[idr] == ib+1):
              
                    self.d_kd[idr] = kdd[ib]
                    self.d_ksmo[idr] = ksmo[ib]
                    self.d_ka[idr] = ka[ib]
                    self.d_kcol[idr] = kcol[ib]
                    self.d_koi[idr] = koi[ib]
                    self.d_ksp[idr] = ksp[ib]
                    self.d_koa[idr] = koa[ib]
                    self.d_kai[idr] = kai[ib]
                    self.d_kin[idr] = kin[ib]
                    self.d_temp[idr] = temp[ib]
                    self.d_vel[idr] = vel[ib]
              
                    self.d_kr[idr]= self.d_kd[idr] +self.d_ksmo[idr]
              
                    #(Popel, 1979)
                    self.d_satdo[idr] =  14.652 - (4.1022 * 1e-1 * self.d_temp[idr]) + (7.991 * 1e-3 * self.d_temp[idr] ** 2) -(7.7774 * 1e-5 * self.d_temp[idr] ** 3)

        #write shapefile
        features = self.lyr_drl.getFeatures()
        self.lyr_drl.startEditing()
        

        i = 0
        for feat in features:
            
            self.lyr_drl.changeAttributeValue(feat.id(), self.lyr_drl.fields().indexFromName('Coef_Kd'), float(self.d_kd[i]))
            self.lyr_drl.changeAttributeValue(feat.id(), self.lyr_drl.fields().indexFromName('Coef_Ksd'), float(self.d_ksmo[i]))
            self.lyr_drl.changeAttributeValue(feat.id(), self.lyr_drl.fields().indexFromName('Coef_Ka'), float(self.d_ka[i]))
            self.lyr_drl.changeAttributeValue(feat.id(), self.lyr_drl.fields().indexFromName('Coef_Kcol'), float(self.d_kcol[i]))
            self.lyr_drl.changeAttributeValue(feat.id(), self.lyr_drl.fields().indexFromName('Coef_Koi'), float(self.d_koi[i]))
            self.lyr_drl.changeAttributeValue(feat.id(), self.lyr_drl.fields().indexFromName('Coef_Ksp'), float( self.d_ksp[i]))
            self.lyr_drl.changeAttributeValue(feat.id(), self.lyr_drl.fields().indexFromName('Coef_Koa'), float(self.d_koa[i]))
            self.lyr_drl.changeAttributeValue(feat.id(), self.lyr_drl.fields().indexFromName('Coef_Kai'), float(self.d_kai[i]))
            self.lyr_drl.changeAttributeValue(feat.id(), self.lyr_drl.fields().indexFromName('Coef_Kin'), float(self.d_kin[i]))
            self.lyr_drl.changeAttributeValue(feat.id(), self.lyr_drl.fields().indexFromName('Vel_ms'), float(self.d_vel[i]))
            self.lyr_drl.changeAttributeValue(feat.id(), self.lyr_drl.fields().indexFromName('DO_Sat'), float(self.d_satdo[i]))
            i = i + 1

        self.lyr_drl.commitChanges()
        self.lyr_drl.updateFields() 
        
        
        
        
        
                        '''
                    if self.d_ord[idr] ==1:
                        d_odcrit[idr,it]=1
                    else:
                        ind_jus = np.array(np.where(self.d_codjus == self.d_codbas[idr]))
                        
                        if (ind_jus.size)==2:
                            d_odcrit[idr,it]=d_odcrit[ind_jus[0,0],it]+d_odcrit[ind_jus[0,1],it]+1
                        if (ind_jus.size)==3:
                            d_odcrit[idr,it]=d_odcrit[ind_jus[0,0],it]+d_odcrit[ind_jus[0,1],it]+d_odcrit[ind_jus[0,2],it]+1

                # IDENTIFICA PRIMEIRO TRECHO CRITICO
                if (d_odcrit[idr,it] == 1):

                    #DURAÇÃO DO TEMPO CRITICO
                    d_tdur[idr,it] = (d_mbod[idr,it] / (self.d_ka[idr] *self.d_satdo[idr])) - (1 / self.d_kd[idr])
                    
                    d_tc[idr,it]=time

                    d_ddo[idr,it] = 0
                    #d_dbod[idr,it] =d_mbod[idr,it] - (self.d_ka[idr] * self.d_satdo[idr] * (d_tc[idr,it] - time))
                    
                else:
                    
                    if self.d_ord[idr] >1:
                        
                        if (ind_jus.size)==2:                            
                            d_tc[idr,it] = d_tc[ind_jus[0,0],it] + d_tc[ind_jus[0,1],it] + time 
                            d_tdur[idr,it] = max( d_tdur[ind_jus[0,0],it], d_tdur[ind_jus[0,1],it])
                            
                            d_ddo[idr,it] = 0
                            #d_dbod[idr,it] =d_mbod[idr,it] - (self.d_ka[idr] * self.d_satdo[idr] * (d_tc[idr,it] - time))
                            

                        if (ind_jus.size)==3:                            
                            d_tc[idr,it] = d_tc[ind_jus[0,0],it] + d_tc[ind_jus[0,1],it] + d_tc[ind_jus[0,2],it] + time 
                            d_tdur[idr,it] = max( d_tdur[ind_jus[0,0],it], d_tdur[ind_jus[0,1],it],  d_tdur[ind_jus[0,2],it])
                            
                            d_ddo[idr,it] = 0
                            #d_dbod[idr,it] =d_mbod[idr,it] - (self.d_ka[idr] * self.d_satdo[idr] * (d_tc[idr,it] - time))
                            

                        #'!VERIFICA SE O TEMPO CRITICO É MAIOR QUE A DURACAO TOTAL EM ANAEROBIOSE
                        if (d_tc[idr,it] > d_tdur[idr,it]):

                            d_ddo[idr,it] = d_ddo_aux

                            # ZERA VARIAVEIS
                            d_odcrit[idr,it] = 0
                            d_tc[idr,it] = 0
                            d_tdur[idr,it] = 0
                '''
                        
                        
        
        
        
        
        
        
        
        
        
        
        
        