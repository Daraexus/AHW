import argparse
from diff_image import diff_image
import matplotlib
import random
from photutils import CircularAperture
import matplotlib.pyplot as plt

def plot_light_curves(diff_cube, unique_extracted_objects):
    
    frame_data = [i for i in range(len(diff_cube))]
    colors = [(random.uniform(0.5, 1),random.uniform(0.5, 1),random.uniform(0.5,1)) for i in range(len(unique_extracted_objects))]


    plt.figure(figsize=(20,10))


    for i, extracted_obj in enumerate(unique_extracted_objects):
        ap_data=[]
        plt.figure(i, figsize=(10, 12))
        for frame in diff_cube:
            diff_cube_test = frame.copy()
            flux, fluxerr, flag = sep.sum_ellipse(diff_cube_test, x=extracted_obj[0], y=extracted_obj[1], a=extracted_obj[2], b=extracted_obj[3], theta=extracted_obj[4])
            #flux /= diff_cube_test.sum()
            ap_data.append(flux)

  
        plt.ylim((0,800))
        plt.plot(frame_data, ap_data, '-o', color=colors[i],linewidth=5.0, )

    plt.show()

    plt.figure(2, figsize=(10, 12))

    plt.imshow(diff_cube[1], cmap='gray', vmin=1, vmax=12)
    plt.colorbar()

    for i, extracted_obj in enumerate(unique_extracted_objects):
        positions = (extracted_obj[0], extracted_obj[1])
        apertures = CircularAperture(positions, r=5.)
        apertures.plot(color=colors[i], linewidth=10.0, lw=2.5, alpha=0.5)

