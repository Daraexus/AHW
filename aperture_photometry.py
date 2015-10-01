from gPhoton.gAperture import gAperture

def lightcurve(skypos, filename, in_raduis, out_raduis=None, trange=None, stepsz=False):

	if out_raduis != None:
		annulus = [in_raduis, out_raduis]
		gAperture('NUV',skypos,in_raduis,csvfile=filename,annulus=annulus, stepsz=stepsz, trange=trange)
	else:
		gAperture('NUV',skypos,in_raduis,csvfile=filename, stepsz=stepsz, trange=trange)

if __name__ == '__main__':
	lightcurve([176.919525856024,0.255696872807351], 'lightcurve.csv', 0.03, 0.04)