import argparse
from diff_image import diff_image
import matplotlib
import random
from photutils import CircularAperture
import matplotlib.pyplot as plt
import sep
import numpy as np


def plot_light_curves(diff_cube, unique_extracted_objects):
    #The diff_cube has to be byte swapped BEFORE being sent as parameter (diff_cube.byteswap(True).newbyteorder()), otherwise the method is not goint to work. Unique_extracted_objects only work for elliptic-shapped apertures
    
    #We get the number of frames from the cube
    frame_data = [i for i in range(len(diff_cube))]
    #Random colours array
    colours = [(random.uniform(0.5, 1),random.uniform(0.5, 1),random.uniform(0.5,1)) for i in range(len(unique_extracted_objects))]
    
    maxVal = 0
    minVal = float("inf")
    
    plt.figure(2, figsize=(10, 12))
    
    #Bonus: Show the image with the sources on the same colour than the plots.
    if len(diff_cube) == 1:
        plt.imshow(diff_cube[0], cmap='gray', vmin=1, vmax=12)
    else:
        plt.imshow(diff_cube[1], cmap='gray', vmin=1, vmax=12)
    plt.colorbar()
    for i, extracted_obj in enumerate(unique_extracted_objects):
        positions = (extracted_obj[0], extracted_obj[1])
        apertures = CircularAperture(positions, r=5.)
        apertures.plot(color=colours[i], linewidth=10.0, lw=2.5, alpha=0.5)
    #For every object we are going to calculate the aperture
    plt.figure(1, figsize=(20, 12))
    for i, extracted_obj in enumerate(unique_extracted_objects):
        ap_data=[]
        #The standard size of each independent figure
        #plt.figure(i, figsize=(10, 12))
        #For every frame...
        for frame in diff_cube:
            diff_cube_test = frame.copy()
            #The parameters passed in order are x, y, a, b and theta
            flux, fluxerr, flag = sep.sum_ellipse(diff_cube_test, x=extracted_obj[0], y=extracted_obj[1], a=extracted_obj[2], b=extracted_obj[3], theta=extracted_obj[4])
            
            
            ap_data.append(flux)
        maxVal = np.maximum(maxVal,np.max(ap_data))
        minVal = np.minimum(minVal,np.min(ap_data))
        #Hard-coded value!!! ALERT!!!
        
        #Plot every curve as a dotted line with the points visible
        plt.plot(frame_data, ap_data, '-o', color=colours[i],linewidth=5.0, )
    plt.ylim((minVal*1.1,maxVal*0.9))
    #Voila
    plt.show()

