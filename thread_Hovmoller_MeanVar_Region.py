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

nut_list = ['sal']
#nut_list = ['nitrate', 'ammonium', 'phosphate', 'modn', 'smopn', 'lmopn',
#            'phosphate', 'modp', 'smopp', 'lmopp']

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
#    if fnmatch.fnmatch(our_file, '*se.nc'):  # modified to try on some files
    if fnmatch.fnmatch(our_file, '*01.nc'):  # modified to try on some files
        list_len.append(our_file)
        dates.append(our_file[0:4] + '/' + our_file[4:6] + '/' + our_file[6:8])

print 'list_len shape:', np.shape(list_len)
dates = to_datetime(dates, format='%Y/%m/%d')

vert_lev_list = ['ALL_LEV']
#vert_lev_list = ['SW', 'IW', 'DW']
#vert_lev_list = ['SW']

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
        
        if self.basin == 'ALB':
            y = [37.252960, 35.093681, 35, 37]
            x = [-2.159892, -0.690137, -5.5, -5.5]
        elif self.basin == 'ALG':
            y = [35.093681, 37.252960, 38.756497, 39.938244, 39.1284526, 36.93272338, 35.930524]
            x = [-0.690137, -2.159892, -0.162487, 4.159323, 8.92564455, 9.90934876, 3.994854]
        elif self.basin == 'GIB':
            y = [35.5, 36.5, 36.5, 35.5]
            x = [-5.5, -5.5, -5, -5]

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
    
        j = 0  # compteur
    
        for nutrient in nut_list:
            for vert_lev in vert_lev_list:
                vars()[nutrient + '_ALL_STOCK_' + self.basin + '_' + vert_lev] = np.zeros([43,len(list_len)])

        for o, fn in enumerate(list_len):
            our_file = list_len[o]
            print 'o:', o
            print 'our_file:', our_file

            # capturer la date
            date_file = our_file[0:8]
            f = Dataset(file_path + list_len[o], 'r')  # open netcdf file

            for nutrient in nut_list:
                print 'nutrient:', nutrient
                # Extracting data from files in file_list
                extracted_var = f.variables[nutrient][0, :, :, :]
                print 'shape extracted_var:', np.shape(extracted_var)
    
                lev_range = range(0, 43)     

                for z in lev_range:
                    print 'z:', z
                    temp_arr = extracted_var[z,:,:]
                    temp_arr2 = np.ma.masked_where(np.ma.getmask(new_bath), temp_arr)
                    temp_arr3 = np.ma.masked_where(indices_re == False, temp_arr2)

                    print 'indexing:',nutrient + '_ALL_STOCK_' + self.basin + '_' + vert_lev, z, o
                    vars()[nutrient + '_ALL_STOCK_' + self.basin + '_' + vert_lev][z,o] = np.mean(temp_arr3)
                    print 'np mean:', np.mean(temp_arr3)
                    #print 'np nanmean:', np.nanmean(temp_arr3)

            print 'before changing file'
            j += 1
            f.close()  # closing netcdf file
    
        print 'SECOND LOOP TO WRITE CSV FILES'
        
        for vert_lev in vert_lev_list:
            for nutrient in nut_list:
                print 'Creating variable:', nutrient + '_OUTPUT_' + self.basin + '_' + vert_lev
                       
                if nutrient in ('nitrate','ammonium', 'modn', 'smopn','lmopn','phosphate','modp', 'smopp','lmopp','sal'):
                    print nutrient
                    print nutrient + '_ALL_STOCK_' + self.basin + '_' + vert_lev
                    print 'shape Dataframe:', np.shape(vars()[nutrient + '_ALL_STOCK_' + self.basin + '_' + vert_lev])

                    vars()[nutrient + '_OUTPUT_' + self.basin + '_' + vert_lev] = DataFrame(vars()[nutrient + '_ALL_STOCK_' + self.basin + '_' + vert_lev])  
                    vars()[nutrient + '_OUTPUT_' + self.basin + '_' + vert_lev].to_csv(path_or_buf='/tmpdir/alex/PYTHON/FIGS/BestAjustRivE_BoostW_BOUCLE/' + nutrient + '_1DMEAN_'+ self.basin + '_' + vert_lev + '.csv')  
        
                else:
                    print 'Error nutrient'
            
        """Fin du code à exécuter."""

# boucle sur les regions pour repartir les threads
#basin_list = ['ALB', 'ALG']  
basin_list = ['GIB']  
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

