import argparse
from diff_image import diff_image
from source_extracting import find_all_objects
import numpy
import os

def find_transients(ifile, pngout, showplot=False):
    # Call diff_image to get the difference image frame and a numpy mask of
    # frames to ignore due to a lack of exposure time.
    diff_frame, bad_frames = diff_image(ifile, showplot=showplot)
    # The source extraction script wants a 3-D array of (nframes,height,width).
    diff_frame = numpy.expand_dims(diff_frame, axis=0)
    # Identify those transient objects that stand out in the difference frame.
    detected_sources = find_all_objects(diff_frame, bad_frames, pngout)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Given a gMap image cube,"
                                     " identify transients across the frames"
                                     " and measure initial photometry.")
    parser.add_argument("ifile", action="store", type=str, help="Name of gMap"
                        " FITS file to make the difference image out of.")
    parser.add_argument("-p", action="store_true", dest="show_plot", help="Plot"
                        " total flux per frame, showing cutoffs, within"
                        " diff_image?  Default = %(default)s.")
    parser.add_argument("-o", action="store", type=str, dest="png_outputfile",
                        default="", help="Output name of the plot showing"
                        " detected sources.  The default is to use the same"
                        " base name as the input FITS file + "
                        '"_detsources.png".')
    args=parser.parse_args()
    if args.png_outputfile == "":
        args.png_outputfile = (
            os.path.splitext(os.path.basename(args.ifile))[0] +
                             "_detsources.png")
    find_transients(args.ifile, args.png_outputfile, showplot=args.show_plot)
