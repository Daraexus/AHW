import argparse
from diff_image import diff_image
from source_extracting import find_all_objects
import numpy
import os
from astropy import wcs

def find_transients(ifile, pngout, showplot=False, diffonly=False):
    # Call diff_image to get the difference image frame and a numpy mask of
    # frames to ignore due to a lack of exposure time.
    diff_frame, bad_frames, frame_wcs = diff_image(ifile, showplot=showplot,
                                                   diffonly=diffonly)
    # The source extraction script wants a 3-D array of (nframes,height,width).
    # If diffonly then need to add back in the "number of frames" as 1.
    if diffonly:
        diff_frame = numpy.expand_dims(diff_frame, axis=0)
    # Identify those transient objects that stand out in the difference frame.
    detected_sources_pix = find_all_objects(diff_frame, bad_frames, frame_wcs,
                                        pngout, ifile)
    # The WCS in the frame is 3D, but the 3rd dimension is useless, so just
    # stick zeroes everywhere.
    detected_sources_coords = frame_wcs.wcs_pix2world(
        numpy.insert(detected_sources_pix,2,0.,axis=1),1)[:,0:2]

    print "Sources Found: (xpix, ypix, RA, DEC)"
    for pix,coord in zip(detected_sources_pix,detected_sources_coords):
        print pix[0], pix[1], coord[0], coord[1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Given a gMap image cube,"
                                     " identify transients across the frames"
                                     " and measure initial photometry.")
    parser.add_argument("ifile", action="store", type=str, help="Name of gMap"
                        " FITS file to make the difference image out of.")
    parser.add_argument("-d", action="store_true", dest="diff_only", help="Get"
                        " all frames + bad frame mask, or return only diff."
                        " image frame + bad frame mask?  Default ="
                        " %(default)s = All Frames + Mask.")
    parser.add_argument("-p", action="store_true", dest="show_plot", help="Plot"
                        " total flux per frame, showing cutoffs, within"
                        " diff_image?  Default = %(default)s.")
    parser.add_argument("-o", action="store", type=str, dest="png_outputfile",
                        default="", help="Output name of the plot showing"
                        " detected sources.  The default is to use the same"
                        " base name as the input FITS file + "
                        '"_detsources.png".')
    args=parser.parse_args()
    find_transients(args.ifile, args.png_outputfile, showplot=args.show_plot,
                    diffonly=args.diff_only)
