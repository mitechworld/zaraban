# -*- coding: utf-8 -*-
############################################
###                 Zaraban              ### 
###             A python tools for       ###
###         analyzing echocardiograms    ### 
###              written by              ###
###  ----------- Milad Shiri ----------  ###
################## 2019 ####################

import numpy as np
from PIL import Image
import cv2
from matplotlib import pyplot as plt



def track_single_eulerian(im1, im2, WS, SS):
    ######
    ### track_single > applying block matching between two frames
    ###                to estimate speckles' displacement
    ### im1 = firt frame
    ### im2 = second frame
    ### WS = Window Size
    ### SS= Search Size
    #######
    
    if type(im1) != np.ndarray:
           print ('Error: Input image1 should be numpy.ndarray')
           return 0
    if type(im2) != np.ndarray:
           print ('Error: Input image2 should be numpy.ndarray')
           return 0
       
    f_size = im1.shape
    f_rows = f_size[0]
    f_cols = f_size[1]

    PD = WS + SS #Padding
    
    TH = 0  #Speckle Threshold
    
    vectx = np.zeros(f_size)
    vecty = np.zeros(f_size)
    score_std = np.zeros(f_size)
    score_mean = np.zeros(f_size)
    score_max = np.zeros(f_size)

    progress = 0
    for row in range(1+PD, f_rows-PD):
        for col in range(1+PD, f_cols-PD):
            progress += 1
            print('{:.3}'.format(progress/((f_rows-2*PD)*(f_cols-2*PD))*100))
            window = im1[row-WS:row+WS,col-WS:col+WS] 
            if np.mean(window) > TH:
                match_score = np.zeros((2*SS+1, 2*SS+1))
                cross_col = np.zeros((2*SS+1, 2*SS+1))
    
                for ii in range(-SS, SS+1):
                    for jj in range(-SS, SS+1):
                        patch = im2[row+ii-WS:row+ii+WS, col+jj-WS:col+jj+WS]
    #                    match_score[ii+SS, jj+SS] = np.sum(np.power(window-patch, 2))            
                        cross_col[ii+SS, jj+SS] = abs(np.mean((window-window.mean())*(patch-patch.mean()) / (window.std()*patch.std())))
                        match_score = cross_col
#                        print (cross_col[ii+SS, jj+SS])
                match_score = np.nan_to_num(match_score)
                score_std[row, col] = match_score.std()
                score_mean[row, col] = match_score.mean()
                score_max[row, col] = match_score.max()

                if match_score[SS, SS] == 1 or match_score[SS, SS] != match_score[SS, SS]:
                       vectx[row, col] = 0;
                       vecty[row, col] = 0; 
                else:
                    a, b = np.where(match_score == np.max(match_score))
                    vectx[row, col] = a[0] - (SS)
                    vecty[row, col] = b[0] - (SS)
         
    return vectx, vecty, score_std, score_mean, score_max
    

        
def track_point(im1, im2, markers, WS, SS):
    ######
    ### track_point > applying block matching to track a point between 
    ###               two frames.
    ### im1 = firt frame
    ### im2 = second frame
    ### markers = inpute initial points
    ### WS = Window Size
    ### SS= Search Size
    #######
    
    if type(im1) != np.ndarray:
           print ('Error: Input image1 should be numpy.ndarray')
           return 0
    if type(im2) != np.ndarray:
           print ('Error: Input image2 should be numpy.ndarray')
           return 0
       
    f_size = im1.shape
    f_rows = f_size[0]
    f_cols = f_size[1]
    counts = markers.shape[0]
    PD = WS + SS #Padding
    
    TH = 0  #Speckle Threshold
    
    vectx = np.zeros(f_size)
    vecty = np.zeros(f_size)
    progress = 0
    displacements = markers.copy()
    for i in range(0, counts):
        marker = markers[i]
        progress += 1
        print('{:.3}'.format(progress/(counts)*100))
        col = marker[0]
        row = marker[1]
        window = im1[row-WS:row+WS,col-WS:col+WS] 
        if np.mean(window) > TH:
            match_score = np.zeros((2*SS+1, 2*SS+1))
            cross_col = np.zeros((2*SS+1, 2*SS+1))

            for ii in range(-SS, SS+1):
                for jj in range(-SS, SS+1):
                    patch = im2[row+ii-WS:row+ii+WS, col+jj-WS:col+jj+WS]
#                    match_score[ii+SS, jj+SS] = np.sum(np.power(window-patch, 2))            
                    cross_col[ii+SS, jj+SS] = abs(np.mean((window-window.mean())*(patch-patch.mean()) / (window.std()*patch.std())))
                    match_score = cross_col
#                    print (cross_col[ii+SS, jj+SS])
            match_score = np.nan_to_num(match_score)
            print(match_score.std())
            print(match_score.mean())
            if match_score[SS, SS] == 1 or match_score[SS, SS] != match_score[SS, SS]:
               displacements[i, 0] = 0;
               displacements[i, 1] = 0;
            else:
                a, b = np.where(match_score == np.max(match_score))
                displacements[i, 0] = a[0] - (SS)
                displacements[i, 1] = b[0] - (SS)
     
    return displacements + markers
    
               
        
        
        