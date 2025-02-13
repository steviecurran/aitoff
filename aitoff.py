#!/usr/bin/python3  
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os 
import sys 
import pandas as pd
from astropy.coordinates import SkyCoord  # High-level coordinates
from astropy.coordinates import ICRS, Galactic, FK4, FK5  # Low-level frames
from astropy.coordinates import Angle, Latitude, Longitude  # Angles
import astropy.units as units
from matplotlib  import cm
from matplotlib.colors import LogNorm
from scipy.stats import gaussian_kde 

pi = np.pi

D = pd.read_csv("DESI_trun.csv");
D = D[['TARGET_RA','TARGET_DEC','Z']]; 
D.rename({'TARGET_RA': 'RA', 'TARGET_DEC': 'dec', 'Z':'z'}, axis=1, inplace=True)

S = pd.read_csv('~/CATALOGUES/SDSS/QSOs_1st_100k.dat', sep = ' ', index_col = False, header = None); 
S.columns = ['ct','blah1','NED1','NED2','RA','dec','type','z_NED','blah2','RA2','dec2','class','z','ez']
S = S[['NED1','NED2','RA','dec','z']]

def deg2rad(df):
    ra = df['RA']; dec = df['dec']
    return ra*pi/180 - pi, dec*pi/180
    
def update_ticks(z, pos):
    return "%1.0f" %(z)

cmap = plt.cm.rainbow;
font = 10
plt.rcParams.update({'font.size': font})
fig = plt.figure(figsize=(6,3),dpi=150)
ax = fig.add_subplot(111, projection="aitoff")

def plots(data,grid,name):

    RA,DEC = deg2rad(data)

    h = plt.hexbin(RA, DEC, gridsize=grid, cmap=cmap,norm=LogNorm(),zorder=1)#,alpha = 0.1) # 596 K
    cbar = plt.colorbar(h,ax=ax, shrink=0.7,label = 'Number of %s sources' %(name),
                        aspect=24, pad=0.05,format=ticker.FuncFormatter(update_ticks))
    
    cbar.ax.tick_params(axis='y', direction='out',length=4, width=1, which = 'major')
    cbar.ax.tick_params(axis='y', direction='out',length=2, width=1, which = 'minor')

    plt.xlabel('R.A.', size= font); plt.ylabel('Declination.', size=font)
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("%s_aitoff_%d.png" %(name,grid))
    plt.show()

plots(D,200,'DESI')
#plots(S,500,'SDSS')
