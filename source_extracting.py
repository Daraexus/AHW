import numpy as np
import sep
from astropy.io import fits
import matplotlib.path as mplpath
import pylab as plt
import os

radii = [5.0, 15.0]
match_radius = 10

def extract_sources(data):
	try:
		bkg = sep.Background(data)
	except ValueError:
		data = data.byteswap(True).newbyteorder()
		bkg = sep.Background(data)
	back = bkg.back()
	data_woback = data-back
	thresh = 3.0 * bkg.globalrms
	objects = sep.extract(data_woback, thresh)
	return objects

def aperture_photometry(data, objects, radii):
	#TODO aperture corrected flux: take the ratio of the Flux in the bigger to the flux in the smaller, average them to find the correction, then multiply each of the smaller fluxes to the correction. Do the same thing for errors. Depending on what you set your GAIN to be, this is either background only or background and Poisson. If GAIN is set to 0 its only background error. http://www.galex.caltech.edu/researcher/techdoc-ch5.html Or you could use the apertures in Figure 1... The value for the correction shouldn't change much for GALEX since the PSF doesn't change across the CCDs.
	flux_min, fluxerr_min, flag_min = sep.sum_circle(data, objects[0], objects[1], min(radii))
	flux_max, fluxerr_max, flag_max = sep.sum_circle(data, objects[0], objects[1], max(radii))
	return flux_min

def point_within_distance(existing_points, new_points):
	new_objects = np.asarray([False]*len(new_points))
	for i, point in enumerate(new_points):
		distances = ((existing_points[:,0]-point[0])**2.0 + (existing_points[:,1]-point[1])**2.0)**0.5 
		if np.all(distances > match_radius):
			new_objects[i] = True
	return new_objects
   
def plot_frame(data_array,known_objects,xs,ys,num,ifile,pngout=""):
	# If not specified, "pngout" = "", so make a default.
	if pngout == "":
		pngout = (os.path.splitext(os.path.basename(ifile))[0] +
			"_detsources.png")
	plt.figure(1)
	plt.imshow(data_array)
	for i in range(len(known_objects)):
		plt.plot(known_objects[i][0],known_objects[i][1],'ro')
	for i in range(len(xs)):
		plt.plot(xs[i],ys[i],'ko')
	plt.savefig(os.path.splitext(pngout)[0] + "_" + num + ".png")
	plt.clf()
	return

def find_all_objects(framecube, bad_frame_mask, frame_wcs, pngout, ifile):
	all_extracted_objects = np.array([])
	for i in range(framecube.shape[0]):
		objects = extract_sources(framecube[i,:,:])
		plot_frame(framecube[i,:,:],all_extracted_objects,objects['x'],objects['y'],str(i),ifile,pngout=pngout)
		if len(objects) > 0:
			if len(all_extracted_objects) > 0:
				new_objects = point_within_distance(all_extracted_objects,np.asarray([objects['x'],objects['y']]).T) #returns array of True and False
				all_extracted_objects = np.vstack((all_extracted_objects, np.asarray([objects['x'][new_objects],objects['y'][new_objects]]).T))
			else:
				all_extracted_objects = np.asarray([objects['x'],objects['y']]).T
		#print "total number of objects: ", len(all_extracted_objects)
	return all_extracted_objects
