#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 13:26:03 2023

@author: bob
"""

import os
import paramiko
from configparser import ConfigParser

# Read the basic paths from the config file
config = ConfigParser()
config.read('config_bd_s2s.ini')

#Set the directories from the config file
direc = config['paths']['data_dir'] + 'input_bmd_gridded_data/'

if not os.path.exists(direc):
    os.makedirs(direc)

host = "114.31.28.234"
username = "rimes"
password = "inflamedwarrior666"

base_dir = "/home/rimes/BMD_GRIDDED_DATA/"

# Set the URL to the ENACTS data
rr_folder = base_dir + "BMD_grd_Rainfall/Daily_Rainfall/"
tmax_folder = base_dir + "BMD_grd_Tmax/Daily_Tmax/"
tmin_folder = base_dir + "BMD_grd_Tmin/Daily_Tmin/"

# Connect to 
proxy = None
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=username, password=password, sock=proxy)
sftp = ssh.open_sftp()

# Define the available years
years = range(1981,2023)

# Loop over all available years
for year in years:
    
    # Download rainfall, maximum and minimum temperature
    if not os.path.exists(direc + f'merge_rr_{year}.nc'):
        sftp.get(rr_folder + f'merge_rr_{year}.nc', direc + f'merge_rr_{year}.nc')
    if not os.path.exists(direc + f'merge_tmin_{year}.nc'):
        sftp.get(tmin_folder + f'merge_tmin_{year}.nc', direc + f'merge_tmin_{year}.nc')
    if not os.path.exists(direc + f'merge_tmax_{year}.nc'):
        sftp.get(tmax_folder + f'merge_tmax_{year}.nc', direc + f'merge_tmax_{year}.nc')
    
sftp.close()
ssh.close()
