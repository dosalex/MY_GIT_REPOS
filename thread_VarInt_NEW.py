# coding: utf-8

# -rwx------ 1 dosa users     6389  3 mars  20:27 thread_VarInt_NEW.py

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

nut_list = ['ppb', 'netppb', 'chl_tot', 'export_nit_sw', 'export_pho_sw', 'export_doc200', 'export_poc200'] 

# #### IMPORTANT ##### IMPORTANT #### IMPORTANT #####

#file_path = '/tmpdir/alex/BASSIN_3D/MED8_JO/GRAPHIQUES/ALEX_TESTS_RECENT/BestAjustRivE_BoostW/'
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
#        list_len.append(our_file)
#        dates.append(our_file[0:4] + '/' + our_file[4:6] + '/' + our_file[6:8])
        if our_file != '19700615_121001.ECO3M-S.LA.tlse.nc': # problem with 1st file
            list_len.append(our_file)
            dates.append(our_file[0:4] + '/' + our_file[4:6] + '/' + our_file[6:8])

dates = to_datetime(dates, format='%Y/%m/%d')

# vert_lev_list = ['SW', 'IW', 'DW']

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

#        if self.basin == 'NWE':
#            y = [40,40,45,45];
#            x = [0,9,9,0];
#        elif self.basin == 'SWE':
#            y = [40,40,35,35];
#            x = [1.5,9,9,1.5];
#        elif self.basin == 'ION':
#            y = [30,38,38,40,40,30];
#            x = [15,15,16,16,22.5,22.5];
#        elif self.basin == 'LEV':
#            y = [30,35,35,39,39,30];
#            x = [22.5,22.5,28,28,37,37];
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
    
        for nutrient in nut_list:
            for basin in basin_list:
                vars()['all_mean_'+nutrient+'_'+self.basin] = np.empty([len(list_len)])
                
        #print list_len

        for o, fn in enumerate(list_len):
            our_file = list_len[o]
            # capturer la date
            date_file = our_file[0:8]
            f = Dataset(file_path + list_len[o], 'r')  # open netcdf file

            for nutrient in nut_list:
                # Extracting data from files in file_list
                extracted_var = f.variables[nutrient][:]
                extracted_nut = extracted_var  # pourquoi cette étape est-elle utile???
    
                # Modif Alex 20/05/2018 for 2D variables    
                if nutrient == 'chl_tot':
                   nut = extracted_nut[0, 42, :, :]
                else:
                   nut = extracted_nut[0, :, :]
                # On applique notre masque au nouveau jeu de données
                new_nut = np.ma.masked_where(np.ma.getmask(new_bath), nut)
        
                vars()['all_mean_'+nutrient+'_'+self.basin][o] = np.nanmean(np.ma.masked_array(new_nut, indices_re == False))

                extracted_var = [] # TEST ALEX 01/11 18h15
                new_nut = []
                nut = []
                extracted_nut = []

            f.close()  # closing netcdf file
    
        print 'SECOND LOOP TO WRITE CSV FILES'
            
#        for vert_lev in vert_lev_list:

        for nutrient in nut_list:
            print 'Creating variable:', 'all_mean_'+nutrient+'_'+self.basin
                       
            vars()[nutrient + '_2D_' + self.basin] = DataFrame(dates, columns=['date'])
            vars()[nutrient + '_2D_' + self.basin]['var'] = vars()['all_mean_'+nutrient+'_'+self.basin]
            vars()[nutrient + '_2D_' + self.basin].to_csv(path_or_buf='/tmpdir/alex/PYTHON/FIGS/BestAjustRivE_BoostW_BOUCLE/' + nutrient + '_2D_'+ self.basin + '.csv')  

        """Fin du code à exécuter."""

# boucle sur les regions pour repartir les threads
#basin_list = ['NWE', 'SWE', 'ION', 'LEV']  
basin_list = ['ALB_W', 'ALB_C', 'ALB_E', 'ALG_W']

thread_count = 1 

for basin in basin_list: 
    print 'thread_count = ', thread_count 
    
    # Création des threads
    vars()['thread_' + str(thread_count)] = Compute_Stock(basin) 
 
    # Lancement des threads
    vars()['thread_' + str(thread_count)].start()

    # iterating count
    thread_count += 1

print ' '
print 'END OF COMPUTING'
print ' '

