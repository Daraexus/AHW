import argparse
import os
from astropy.io import fits
import ipdb
import matplotlib.pyplot as pyp
import numpy

def diff_image(ifile,showplot=False):
    with fits.open(ifile) as hdulist:
        frame_cube = hdulist[0].data
        # Parameters of the cube are (n_frames, height, width) when calling
        # ".shape" on the object.
        n_frames = frame_cube.shape[0]
        # These are the sum of all the flux across each frame.
        tot_counts = numpy.asarray([frame_cube[x].sum() for x in
                                    xrange(n_frames)])
        median_tot_counts = numpy.median(tot_counts)
        mean_tot_counts = numpy.mean(tot_counts)

        # Play around with using the Median Absolute Deviation to define the
        # base level.  Note that in order to translate the MAD into an
        # approximation for sigma, one must use a scale factor.  For Gaussian
        # distributions this is ~1.4826, for uniform distributions this is
        # ~1.1547.  This is really only true for LARGE samples from a uniform
        # distribution, but maybe it doesn't impact the outlier identification
        # when the samples are a few 10s of frames.
        scale_factor = 1.1547
        mad_value = scale_factor*numpy.median(numpy.absolute(
                tot_counts - median_tot_counts))

        # Only consider those frames with reasonable total counts, to ignore
        # frames with very little exposure for their bin.
        bad_frames = numpy.asarray([x < median_tot_counts-3.*mad_value for x in
                              tot_counts])

        # Plot the total flux counts for each frame and where the cutoffs are.
        if showplot:
            pyp.plot(range(n_frames), tot_counts, 'ko')
            pyp.axhline(median_tot_counts, color='b')
            pyp.axhline(median_tot_counts-3*mad_value, color='g')
            pyp.axhline(median_tot_counts+3*mad_value, color='g')
            pyp.plot(numpy.asarray(range(n_frames))[bad_frames],
                     tot_counts[bad_frames], 'ro')
            pyp.xlim([-2.,n_frames+2])
            pyp.show()

        # This will compute the difference between the max. flux and the min.
        # flux for each pixel across all frames in the cube, ignoring frames
        # identified as having low exposure time.
        diff_image = (numpy.max(frame_cube[~bad_frames],axis=0) -
                      numpy.median(frame_cube[~bad_frames],axis=0))

        # Write the difference image to a FITS file.
        file_splits = os.path.splitext(ifile)
        output_file_name = file_splits[0] + "_diff" + file_splits[1]
        new_hdu = fits.PrimaryHDU(diff_image)
        new_hdulist = fits.HDUList([new_hdu])
        new_hdulist.writeto(output_file_name, clobber=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Makes a difference image"
                                     " across all frames for a gPhoton cube."
                                     "  Difference is defined as (for each"
                                     " pixel) max(pix)-median(pix) across all"
                                     " frames.")
    parser.add_argument("ifile", action="store", type=str, help="Name of gMap"
                        " FITS file to make the difference image out of.")
    parser.add_argument("-p", action="store_true", dest="show_plot", help="Plot"
                        " total flux per frame, showing cutoffs?  Default = "
                        "%(default)s.")
    args=parser.parse_args()
    diff_image(args.ifile,showplot=args.show_plot)
