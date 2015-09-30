import numpy as np
import sep
from astropy.io import fits
import matplotlib.path as mplpath
import pylab as plt

file = "VVDS22H_MOS05-05_NUV.fits"
hdulist = fits.open(file)
framecube = hdulist[0].data
#radii = [5.0, 15.0]

def extract_sources(data):
	data = data.byteswap(True).newbyteorder()
	bkg = sep.Background(data)
	back = bkg.back()
	data_woback = data-back
	thresh = 1.5 * bkg.globalrms
	objects = sep.extract(data_woback, thresh)
	return objects

def aperture_photometry(data, objects, radii):
	#TODO aperture corrected flux: take the ratio of the Flux in the bigger to the flux in the smaller, average them to find the correction, then multiply each of the smaller fluxes to the correction. Do the same thing for errors. Depending on what you set your GAIN to be, this is either background only or background and Poisson. If GAIN is set to 0 its only background error. http://www.galex.caltech.edu/researcher/techdoc-ch5.html Or you could use the apertures in Figure 1... The value for the correction shouldn't change much for GALEX since the PSF doesn't change across the CCDs.
	flux_min, fluxerr_min, flag_min = sep.sum_circle(data, objects[0], objects[1], min(radii))
	flux_max, fluxerr_max, flag_max = sep.sum_circle(data, objects[0], objects[1], max(radii))
	return flux_min

def point_in_rect(points,vertices):
	new_objects  = np.ones((len(vertices)), dtype=bool)
	for i in range(len(vertices)): #iterate through each of the new objects
		rect = mplpath.Path(vertices[i])	#draw the rectangle defining it
		inside = any(rect.contains_points(points)) #check if there is already a source there
		new_objects[i] = ~inside
	return new_objects

def vertices_of_pixels(xmins, xmaxs, ymins, ymaxs):
	verts = [[(xmins[i],ymins[i]), (xmaxs[i],ymins[i]), (xmaxs[i],ymaxs[i]), (xmins[i],ymaxs[i])] for i in range(len(xmaxs))]
	return verts
   
def plot_frame(data_array,known_objects,xs,ys,num):
	plt.figure(1)
	plt.imshow(data_array)
	for i in range(len(known_objects)):
		plt.plot(known_objects[i][0],known_objects[i][1],'ro')
	for i in range(len(xs)):
		plt.plot(xs[i],ys[i],'ko')
	plt.savefig('plot_frame_' + num + '.png')
	plt.clf()
	return

def find_all_objects(framecube):
	all_extracted_objects = np.array([])
	for i in range(framecube.shape[0] - 2):
		#print "frame number: ", i+2
		objects = extract_sources(framecube[i+2,:,:])
		plot_frame(framecube[i+2,:,:],all_extracted_objects,objects['x'],objects['y'],str(i+2))
		#print "number of objects: ", len(objects)
		if len(objects) > 0:
			if len(all_extracted_objects) > 0:
				vertices = vertices_of_pixels(objects['xmin'], objects['xmax'], objects['ymin'], objects['ymax'])
				new_objects = point_in_rect(all_extracted_objects,vertices) #returns array of True and False
				print new_objects
				all_extracted_objects = np.vstack((all_extracted_objects, np.asarray([objects['x'][new_objects],objects['y'][new_objects]]).T))
			else:
				all_extracted_objects = np.asarray([objects['x'],objects['y']]).T
		#print "total number of objects: ", len(all_extracted_objects)
	return unique_extracted_objects

def find_all_objects(framecube):
	for i in range(framecube.shape[0]):
		fluxes = aperture_photometry(framecube[i,:,:])