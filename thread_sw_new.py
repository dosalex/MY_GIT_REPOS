# coding: utf-8

import fnmatch
# Loading libraries
import os.path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pandas import read_csv, to_datetime, DataFrame
from matplotlib.path import Path
from netCDF4 import Dataset

import random
import sys
from threading import Thread
import time

nut_list = ['nitrate', 'ammonium', 'phosphate', 'modn', 'smopn', 'lmopn', 'nanon', 'dian', 'zoonanoc', 
            'zoomicroc', 'zoomesoc', 'synen', 'bactc', 'silice', 'smopsi', 'lmopsi', 'diasi']

# #### IMPORTANT ##### IMPORTANT #### IMPORTANT #####

file_path = '/tmpdir/alex/BASSIN_3D/MED8_JO/GRAPHIQUES/BestAjustRivE_BoostW_BOUCLE/'
# HERE THAT YOU GIVE THE PATH TO YOUR FOLDER CONTAINING MEAN NC FILES !!!

# #### IMPORTANT ##### IMPORTANT #### IMPORTANT #####

full_list = os.listdir(file_path)
full_list.sort()

# LOADING GRID FILE AND VARIABLES
grid_file = '../grille.nc'
print 'file exist:', os.path.isfile(grid_file)

f = Dataset(grid_file)  # open netcdf
# extracting variables
lon_t = f.variables['longitude_t'][:]  # extracting lon data
lat_t = f.variables['latitude_t'][:]  # extracting lat data
depth_t = f.variables['depth_t'][:]
bathy = f.variables['h_w'][:]
print 'Bathy :', np.shape(bathy), 'max :', np.max(bathy), 'min :', np.min(bathy)
print ' '

# Creating a mask according to the depth (to suppress shallow cells)
new_bath = np.ma.masked_where(bathy < 200, bathy)

# Creating a list of all files to be treated
list_len = list()  # here we preallocate an empty list
dates = []

for our_file in full_list:
    if fnmatch.fnmatch(our_file, '*se.nc'):  # modified to try on some files
        list_len.append(our_file)
        dates.append(our_file[0:4] + '/' + our_file[4:6] + '/' + our_file[6:8])

dates = to_datetime(dates, format='%Y/%m/%d')

#vert_lev_list = ['SW', 'IW', 'DW']
vert_lev_list = ['SW']

print ' '
print ' -- '
print ' END OF INTRODUCTION - BEFORE LOOP '
print ' -- '
print ' '

class Compute_Stock(Thread):

    """Thread chargé simplement d'afficher une lettre dans la console."""

    def __init__(self, basin):
        Thread.__init__(self)
        self.basin = basin

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        

        if self.basin == 'ALB_W':
            y = [37,37,34,34]
            x = [-6,-4.5,-4.5,-6]
        elif self.basin == 'ALB_C':
            y = [37,34,34,37]
            x = [-4.5,-4.5,-3,-3]
        elif self.basin == 'ALB_E':
            y = [34,37,37,34]
            x = [-2.5,-2.5,-1,-1]
        elif self.basin == 'ALG_W':
            y = [35, 38, 39, 35]
            x = [-0.6, -0.6, 1, 1]

#        if self.basin == 'ALL_MED':
#            y = [37,35,35,30.5,30.5,38,46,45,44];
#            x = [-5.5,-5.5,10,10,36.5,36.5,13.5,10,3];
#        elif self.basin == 'W':
#            y = [37, 35, 35, 36.4, 37.8, 38, 38.5, 39.5, 45, 44]
#            x = [-5.5, -5.5, 10, 10, 12.8, 15, 16.5, 16.5, 10, 3]
#        elif self.basin == 'E':
#            y = [36.4, 37.8, 38, 38.5, 39.5, 45, 46, 38, 30.5, 30.5]
#            x = [10, 12.8, 15, 16.5, 16.5, 10, 13.5, 36.5, 36.5, 10]
#        elif self.basin == 'GOL':
#            y = [43.44829732432269, 42.97458858683228, 43.0604306783546, 42.96837802751135, 41.96306909843022,
#                 41.43113753799402, 41.16267859938984, 40.91067143551019, 39.12845260900497, 39.938244, 38.756497,
#                 39.247095, 46.4938123, 44.4124705]
#            x = [11.68790444824612, 10.82516607380484, 9.82460045736472, 9.409248985801327, 9.294900137395576,
#                 9.198952404436941, 9.339783959671131, 9.097279040223231, 8.925644550468935, 4.159323, -0.162487,
#                 -1.17747, 5.2446879, 10.1001797]
#        elif self.basin == 'ALB':
#            y = [37.252960, 35.093681, 35, 37]
#            x = [-2.159892, -0.690137, -5.5, -5.5]
#        elif self.basin == 'ALG':
#            y = [35.093681, 37.252960, 38.756497, 39.938244, 39.1284526, 36.93272338, 35.930524]
#            x = [-0.690137, -2.159892, -0.162487, 4.159323, 8.92564455, 9.90934876, 3.994854]
#        elif self.basin == 'TYR':
#            y = [39.12845260900497, 37.88508389278273, 38.03532811253486, 38.19020427258793, 38.206530069008,
#                 38.49522011750975, 39.25645461354518, 40.44930918149475, 43.44829732432269, 42.97458858683228,
#                 43.0604306783546, 42.96837802751135, 41.96306909843022, 41.43113753799402, 41.16267859938984,
#                 40.91067143551019]
#            x = [8.925644550468935, 13.3111744311976, 15.29159159227882, 15.48719160249115, 15.74199259491107,
#                 16.21860737848962, 16.43223864162354, 16.01437911440215, 11.68790444824612, 10.82516607380484,
#                 9.824600457364721, 9.409248985801327, 9.294900137395576, 9.198952404436941, 9.339783959671131,
#                 9.097279040223231]
#        elif self.basin == 'CMED':
#            y = [39.12845260900497, 37.88508389278273, 37.001816, 31.924008, 33.259229, 36.93272338]
#            x = [8.925644550468935, 13.3111744311976, 15.084801, 15.081913, 7.954713, 9.90934876]
#        elif self.basin == 'ION':
#            y = [37.88508389278273, 38.03532811253486, 38.19020427258793, 38.206530069008, 38.49522011750975,
#                 39.25645461354518, 40.44930918149475, 40.857014, 40.138887, 39.74605, 38.155586, 37.503355,
#                 29.658354, 30.941890, 31.924008, 37.001816]
#            x = [13.3111744311976, 15.29159159227882, 15.48719160249115, 15.74199259491107, 16.21860737848962,
#                 16.43223864162354, 16.01437911440215, 16.854632, 18.343058, 20.052826, 23.556638, 21.936077,
#                 20.090485, 15.297679, 15.081913, 15.084801]
#        elif self.basin == 'ADR':
#            y = [45.123088, 46.248509, 42.990612, 41.876774, 39.746050, 40.138887, 40.857014, 41.497860]
#            x = [10.040714, 14.099647, 17.690915, 20.079333, 20.052826, 18.343058, 16.854632, 15.316464]
#        elif self.basin == 'AEG':
#            y = [39.746050, 38.155586, 37.503355, 35.335479, 35.045582, 35.478996, 36.113327, 40.879240, 42.000219,
#                 41.876774]
#            x = [20.052826, 23.556638, 21.936077, 23.620988, 26.217209, 27.159167, 28.006273, 30.504893, 23.493337,
#                 20.079333]
#        elif self.basin == 'LEV':
#            y = [37.503355, 35.335479, 35.045582, 35.478996, 36.113327, 40.879240, 37.180585, 30.329515, 29.658354]
#            x = [21.936077, 23.620988, 26.217209, 27.159167, 28.006273, 30.504893, 37.441401, 35.238352, 20.090485]
        else:
            print 'Les coordonnées pour : ', self.basin, ' ne sont pas définies ici'
    
        print 'Basin :', self.basin
        print ' '
       
        # Selecting the data
        vertices = np.array([np.hstack((x, 0)), np.hstack((y, 0))], float).transpose()
        path = Path(vertices, codes=None, closed=True)
        indices = path.contains_points(
            np.array([np.reshape(lon_t, (np.size(lon_t))), np.reshape(lat_t, (np.size(lat_t)))]).T, transform=None,
            radius=0.0)
        indices_re = np.reshape(indices, np.shape(lon_t))  # this our mask for the zone
    
        vol_levels = read_csv('../vol_lev_' + self.basin + '.csv')

        j = 0  # compteur
    
        for nutrient in nut_list:
            for vert_lev in vert_lev_list:
                vars()[nutrient + '_ALL_STOCK_' + self.basin + '_' + vert_lev] = np.zeros([len(list_len)])
                vars()[nutrient + '_SUMM_' + self.basin] = np.zeros([len(list_len)])

        for o, fn in enumerate(list_len):
            our_file = list_len[o]
            # capturer la date
            date_file = our_file[0:8]
            f = Dataset(file_path + list_len[o], 'r')  # open netcdf file

            for nutrient in nut_list:
                # Extracting data from files in file_list
                extracted_var = f.variables[nutrient][:]
                extracted_nut = extracted_var  # pourquoi cette étape est-elle utile???
    
                for vert_lev in vert_lev_list:
		    if vert_lev in ('SW'):
                        #lev_range = range(30, 43)     
                        lev_range = range(31, 43)     
                        #vars()[nutrient + '_' + self.basin + '_' + vert_lev + '_' + date_file] = np.zeros([14])
                        vars()[nutrient + '_' + self.basin + '_' + vert_lev + '_' + date_file] = np.zeros([13])
                    elif vert_lev in ('IW'):
                        lev_range = range(23, 30)     
                        vars()[nutrient + '_' + self.basin + '_' + vert_lev + '_' + date_file] = np.zeros([8])
                    elif vert_lev in ('DW'):
                        lev_range = range(0, 23)     
                        vars()[nutrient + '_' + self.basin + '_' + vert_lev + '_' + date_file] = np.zeros([23])
                    else:
                        print 'Error vertical levels'

                    for z in lev_range:
                        curr_ind = len(lev_range) - ((lev_range[len(lev_range)-1]+1) - z)
                        nut = extracted_nut[0, z, :, :]
                        # On applique notre masque au nouveau jeu de données
                        new_nut = np.ma.masked_where(np.ma.getmask(new_bath), nut)
        
                        vars()[nutrient + '_' + self.basin + '_' + vert_lev + '_' + date_file][curr_ind] = np.nansum(np.ma.masked_array(new_nut, indices_re == False)) * vol_levels.vol_m3[z]
        
                    # tous les niveaux faits
                    # sum le tout = stock sur tous les niveaux à date en question
        
                    vars()[nutrient + '_ALL_STOCK_' + self.basin + '_' + vert_lev][j] = np.nansum(vars()[nutrient + '_' + self.basin + '_' + vert_lev + '_' + date_file])

#                vars()[nutrient + '_SUMM_' + self.basin][j] = (vars()[nutrient + '_ALL_STOCK_' + self.basin + '_SW'][j] + vars()[nutrient + '_ALL_STOCK_' + self.basin + '_IW'][j] 
#                                                              + vars()[nutrient + '_ALL_STOCK_' + self.basin + '_DW'][j])
                vars()[nutrient + '_SUMM_' + self.basin][j] = vars()[nutrient + '_ALL_STOCK_' + self.basin + '_SW'][j] 

                extracted_var = [] # TEST ALEX 01/11 18h15
        
            j += 1
            f.close()  # closing netcdf file
    
        print 'SECOND LOOP TO WRITE CSV FILES'
            
        for vert_lev in vert_lev_list:
            for nutrient in nut_list:
                print 'Creating variable:', nutrient + '_ALL_STOCK_' + self.basin + '_' + vert_lev
                       
                if nutrient in ('nitrate','ammonium', 'modn', 'smopn','lmopn','nanon', 'dian', 'synen', 'silice', 'smopsi','lmopsi', 'diasi', 'phosphate'):
                    vars()[nutrient + '_STOCK_' + self.basin + '_' + vert_lev] = DataFrame(dates, columns=['date'])
                    vars()[nutrient + '_STOCK_' + self.basin + '_' + vert_lev]['var'] = vars()[nutrient + '_ALL_STOCK_' + self.basin + '_' + vert_lev]
                    vars()[nutrient + '_STOCK_' + self.basin + '_' + vert_lev].to_csv(path_or_buf='/tmpdir/alex/PYTHON/FIGS/BestAjustRivE_BoostW_BOUCLE/' + nutrient + '_STOCK_'+ self.basin + '_' + vert_lev + '.csv')  
        
                elif nutrient in ('zoonanoc', 'zoomicroc', 'zoomesoc'):
                    vars()[nutrient + '_N_ALL_STOCK_' + self.basin + '_' + vert_lev] = vars()[nutrient + '_ALL_STOCK_' + self.basin + '_' + vert_lev] * 0.18
                    vars()[nutrient + '_N_STOCK_' + self.basin + '_' + vert_lev] = DataFrame(dates, columns=['date'])
                    vars()[nutrient + '_N_STOCK_' + self.basin + '_' + vert_lev]['var'] = vars()[nutrient + '_N_ALL_STOCK_' + self.basin + '_' + vert_lev] # final results seem ok
                    vars()[nutrient + '_N_STOCK_' + self.basin + '_' + vert_lev].to_csv(path_or_buf='/tmpdir/alex/PYTHON/FIGS/BestAjustRivE_BoostW_BOUCLE/' + nutrient + '_N_STOCK_' + self.basin + '_' + vert_lev + '.csv') # nécessite pd.DataFrame 
        
                elif nutrient in ('bactc'):
                    vars()[nutrient + '_N_ALL_STOCK_' + self.basin + '_' + vert_lev] = vars()[nutrient + '_ALL_STOCK_' + self.basin + '_' + vert_lev] * 0.232
                    vars()['bactn_STOCK_' + self.basin + '_' + vert_lev] = DataFrame(dates, columns=['date'])
                    vars()['bactn_STOCK_' + self.basin + '_' + vert_lev]['var'] = vars()[nutrient + '_N_ALL_STOCK_' + self.basin + '_' + vert_lev] # final results seem ok
                    vars()['bactn_STOCK_' + self.basin + '_' + vert_lev].to_csv(path_or_buf='/tmpdir/alex/PYTHON/FIGS/BestAjustRivE_BoostW_BOUCLE/bactn_STOCK_' + self.basin + '_' + vert_lev + '.csv') # nécessite pd.DataFrame 
                  
                else:
                    print 'Error nutrient'
            
            vars()['allzoo_ALL_STOCK_' + self.basin + '_' + vert_lev] = ( vars()['zoonanoc_N_ALL_STOCK_' + self.basin + '_' + vert_lev] + vars()['zoomicroc_N_ALL_STOCK_' + self.basin + '_' + vert_lev] 
                                                                        + vars()['zoomesoc_N_ALL_STOCK_' + self.basin + '_' + vert_lev] )
            vars()['allphy_ALL_STOCK_' + self.basin + '_' + vert_lev] = ( vars()['synen_ALL_STOCK_' + self.basin + '_' + vert_lev] + vars()['nanon_ALL_STOCK_' + self.basin + '_' + vert_lev]
                                                                        + vars()['dian_ALL_STOCK_' + self.basin + '_' + vert_lev] )
                
            vars()['allzoo_STOCK_' + self.basin + '_' + vert_lev] = DataFrame(dates, columns=['date'])
            vars()['allzoo_STOCK_' + self.basin + '_' + vert_lev]['var'] = vars()['allzoo_ALL_STOCK_' + self.basin + '_' + vert_lev] # final results seem ok
            vars()['allzoo_STOCK_' + self.basin + '_' + vert_lev].to_csv(path_or_buf='/tmpdir/alex/PYTHON/FIGS/BestAjustRivE_BoostW_BOUCLE/allzoo_STOCK_' + self.basin + '_' + vert_lev + '.csv') # nécessite pd.DataFrame
               
            vars()['allphy_STOCK_' + self.basin + '_' + vert_lev] = DataFrame(dates, columns=['date'])
            vars()['allphy_STOCK_' + self.basin + '_' + vert_lev]['var'] = vars()['allphy_ALL_STOCK_' + self.basin + '_' + vert_lev] # final results seem ok
            vars()['allphy_STOCK_' + self.basin + '_' + vert_lev].to_csv(path_or_buf='/tmpdir/alex/PYTHON/FIGS/BestAjustRivE_BoostW_BOUCLE/allphy_STOCK_' + self.basin + '_' + vert_lev + '.csv') # nécessite pd.DataFrame 

            vars()['DIN_ALL_STOCK_' + self.basin + '_' + vert_lev] = ( vars()['nitrate_ALL_STOCK_' + self.basin + '_' + vert_lev] + vars()['ammonium_ALL_STOCK_' + self.basin + '_' + vert_lev] )
                
            vars()['DIN_STOCK_' + self.basin + '_' + vert_lev] = DataFrame(dates, columns=['date'])
            vars()['DIN_STOCK_' + self.basin + '_' + vert_lev]['var'] = vars()['DIN_ALL_STOCK_' + self.basin + '_' + vert_lev] # final results seem ok
            vars()['DIN_STOCK_' + self.basin + '_' + vert_lev].to_csv(path_or_buf='/tmpdir/alex/PYTHON/FIGS/BestAjustRivE_BoostW_BOUCLE/DIN_STOCK_' + self.basin + '_' + vert_lev + '.csv') # nécessite pd.DataFrame
               
            vars()['DIN_DIP_ALL_STOCK_' + self.basin + '_' + vert_lev] = ( vars()['DIN_ALL_STOCK_' + self.basin + '_' + vert_lev] / vars()['phosphate_ALL_STOCK_' + self.basin + '_' + vert_lev] )

            vars()['DIN_DIP_STOCK_' + self.basin + '_' + vert_lev] = DataFrame(dates, columns=['date'])
            vars()['DIN_DIP_STOCK_' + self.basin + '_' + vert_lev]['var'] = vars()['DIN_DIP_ALL_STOCK_' + self.basin + '_' + vert_lev] # final results seem ok
            vars()['DIN_DIP_STOCK_' + self.basin + '_' + vert_lev].to_csv(path_or_buf='/tmpdir/alex/PYTHON/FIGS/BestAjustRivE_BoostW_BOUCLE/DIN_DIP_STOCK_' + self.basin + '_' + vert_lev + '.csv') # nécessite pd.DataFrame 
   
        vars()['allzoo_SUMM_' + self.basin] = vars()['allzoo_ALL_STOCK_' + self.basin + '_SW'] 
#        vars()['allzoo_SUMM_' + self.basin] = (vars()['allzoo_ALL_STOCK_' + self.basin + '_SW'] + vars()['allzoo_ALL_STOCK_' + self.basin + '_IW'] 
#                                              + vars()['allzoo_ALL_STOCK_' + self.basin + '_DW']) 
        vars()['allphy_SUMM_' + self.basin] = vars()['allphy_ALL_STOCK_' + self.basin + '_SW']
#        vars()['allphy_SUMM_' + self.basin] = (vars()['allphy_ALL_STOCK_' + self.basin + '_SW'] + vars()['allphy_ALL_STOCK_' + self.basin + '_IW'] 
#                                              + vars()['allphy_ALL_STOCK_' + self.basin + '_DW']) 
        vars()['bactn_SUMM_' + self.basin] = vars()['bactc_N_ALL_STOCK_' + self.basin + '_SW'] 
#        vars()['bactn_SUMM_' + self.basin] = (vars()['bactc_N_ALL_STOCK_' + self.basin + '_SW'] + vars()['bactc_N_ALL_STOCK_' + self.basin + '_IW'] 
#                                              + vars()['bactc_N_ALL_STOCK_' + self.basin + '_DW']) 

        vars()['synen_SUMM_' + self.basin] = vars()['synen_ALL_STOCK_' + self.basin + '_SW'] 
        vars()['nanon_SUMM_' + self.basin] = vars()['nanon_ALL_STOCK_' + self.basin + '_SW'] 
        vars()['dian_SUMM_' + self.basin] = vars()['dian_ALL_STOCK_' + self.basin + '_SW'] 
#        vars()['synen_SUMM_' + self.basin] = (vars()['synen_ALL_STOCK_' + self.basin + '_SW'] + vars()['synen_ALL_STOCK_' + self.basin + '_IW'] 
#                                              + vars()['synen_ALL_STOCK_' + self.basin + '_DW']) 
#        vars()['nanon_SUMM_' + self.basin] = (vars()['nanon_ALL_STOCK_' + self.basin + '_SW'] + vars()['nanon_ALL_STOCK_' + self.basin + '_IW'] 
#                                              + vars()['nanon_ALL_STOCK_' + self.basin + '_DW']) 
#        vars()['dian_SUMM_' + self.basin] = (vars()['dian_ALL_STOCK_' + self.basin + '_SW'] + vars()['dian_ALL_STOCK_' + self.basin + '_IW'] 
#                                              + vars()['dian_ALL_STOCK_' + self.basin + '_DW']) 

	vars()['diasi_SUMM_' + self.basin] = vars()['diasi_ALL_STOCK_' + self.basin + '_SW']
#	vars()['diasi_SUMM_' + self.basin] = (vars()['diasi_ALL_STOCK_' + self.basin + '_SW'] + vars()['diasi_ALL_STOCK_' + self.basin + '_IW']
#                                              + vars()['diasi_ALL_STOCK_' + self.basin + '_DW'])

        vars()['zoonanon_SUMM_' + self.basin] = vars()['zoonanoc_N_ALL_STOCK_' + self.basin + '_SW'] 
        vars()['zoomicron_SUMM_' + self.basin] = vars()['zoomicroc_N_ALL_STOCK_' + self.basin + '_SW'] 
        vars()['zoomeson_SUMM_' + self.basin] = vars()['zoomesoc_N_ALL_STOCK_' + self.basin + '_SW'] 
#        vars()['zoonanon_SUMM_' + self.basin] = (vars()['zoonanoc_N_ALL_STOCK_' + self.basin + '_SW'] + vars()['zoonanoc_N_ALL_STOCK_' + self.basin + '_IW'] 
#                                              + vars()['zoonanoc_N_ALL_STOCK_' + self.basin + '_DW']) 
#        vars()['zoomicron_SUMM_' + self.basin] = (vars()['zoomicroc_N_ALL_STOCK_' + self.basin + '_SW'] + vars()['zoomicroc_N_ALL_STOCK_' + self.basin + '_IW'] 
#                                              + vars()['zoomicroc_N_ALL_STOCK_' + self.basin + '_DW']) 
#        vars()['zoomeson_SUMM_' + self.basin] = (vars()['zoomesoc_N_ALL_STOCK_' + self.basin + '_SW'] + vars()['zoomesoc_N_ALL_STOCK_' + self.basin + '_IW'] 
#                                              + vars()['zoomesoc_N_ALL_STOCK_' + self.basin + '_DW']) 

        vars()['DIN_SUMM_' + self.basin] = vars()['DIN_ALL_STOCK_' + self.basin + '_SW'] 
        vars()['DIN_DIP_SUMM_' + self.basin] = vars()['DIN_DIP_ALL_STOCK_' + self.basin + '_SW'] 
#        vars()['DIN_SUMM_' + self.basin] = (vars()['DIN_ALL_STOCK_' + self.basin + '_SW'] + vars()['DIN_ALL_STOCK_' + self.basin + '_IW'] 
#                                              + vars()['DIN_ALL_STOCK_' + self.basin + '_DW']) 
#        vars()['DIN_DIP_SUMM_' + self.basin] = ((vars()['DIN_DIP_ALL_STOCK_' + self.basin + '_SW']*13 + vars()['DIN_DIP_ALL_STOCK_' + self.basin + '_IW']*7 
#                                              + vars()['DIN_DIP_ALL_STOCK_' + self.basin + '_DW']*23)/43) # Moyenne par nombre de niveaux 
        # attention ici DIN_DIP_SUMM est en fait une moyenne sur la colonne d'eau et pas une SUMM (notation conservee pour simplifier le code)

        for nutrient in ('nitrate','ammonium', 'modn', 'smopn','lmopn', 'allphy', 'allzoo', 'bactn', 'synen', 'nanon', 'dian', 'zoonanon', 'zoomicron', 'zoomeson', 'silice', 'smopsi','lmopsi', 'diasi', 'phosphate', 'DIN', 'DIN_DIP'):
            vars()[nutrient + '_SUM_' + self.basin] = DataFrame(dates, columns=['date'])
            vars()[nutrient + '_SUM_' + self.basin]['var'] = vars()[nutrient + '_SUMM_' + self.basin]
            vars()[nutrient + '_SUM_' + self.basin].to_csv(path_or_buf='/tmpdir/alex/PYTHON/FIGS/BestAjustRivE_BoostW_BOUCLE/' + nutrient + '_SUM_'+ self.basin + '.csv')  

        """Fin du code à exécuter."""

# boucle sur les regions pour repartir les threads
# basin_list = ['ALL_MED', 'W', 'E', 'GOL', 'ALB', 'ALG', 'TYR', 'CMED', 'ADR', 'ION', 'AEG', 'LEV']  
basin_list = ['ALB_W', 'ALB_C', 'ALB_E', 'ALG_W']  
thread_count = 1 

for basin in basin_list: 
    print 'thread_count = ', thread_count 
    
    # Création des threads
    vars()['thread_' + str(thread_count)] = Compute_Stock(basin) 
 
    # Lancement des threads
    vars()['thread_' + str(thread_count)].start()

    # Attend que les threads se terminent
#    vars()['thread_' + str(thread_count)].join()
    
    # iterating count
    thread_count += 1

print ' '
print 'END OF COMPUTING'
print ' '

