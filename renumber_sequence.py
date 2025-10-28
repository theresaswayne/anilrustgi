# -*- coding: utf-8 -*-
"""
Script to rename files containing a number in a specific pattern
The number meeting the pattern criteria is replaced with 
the next consecutive number
E.g. files numbered 0 through 3 would be re-numbered 1 through 4.

Sample filenames: A1_max_m1_t000_c001.tif or A1_M1_t001_z001_c001.tif

Written by Theresa Swayne with initial code generation by Kota Miura and MS365 Copilot
"""
# https://docs.python.org/3/library/re.html
# https://docs.python.org/3/howto/regex.html#regex-howto

# ---- Setup ----

import os
#import math
#import io
#import string
import re
import shutil

# ---- Variables -- update these as needed! ----

inDir = "/Users/tcs6/Desktop/input"
outDir = "/Users/tcs6/Desktop/input"
image_extension = ".tif"
containString =  "D1" # string that must be in the filename

# ---- functions ----

def increment_filename(filename):
            
    # 1. increment a number within a filename (filename)
    # find the number in the correct position
    # A1_max_m1_t000_c001.tif or A1_M1_t001_z001_c001.tif
    
    # Extract the base name and extension
    base, ext = os.path.splitext(filename)

    # Search for the timepoint number in the base name: t plus 3 digits, surrounded by underscores
    match = re.search('_t(\d{3})_', base)
    if match:
        # if match routine -- convert the string to a number, add 1, convert back to a string with padding to 3 digits
        # use str(int(number)+1)
        number = match.group(1)
        print("Found a number", number)
        incremented = str(int(number) + 1).zfill(3)
        # Replace the old number with the incremented one
        # construct the new file name using match and return it
        new_base = base[:match.start()] + "_t" + incremented + "_" + base[match.end():]
        return new_base + ext
    else:
        raise ValueError("No number found in filename.")
        

def rename_files_in_directory(inputdir, outputdir):
    files = os.listdir(inputdir)
    files = sorted(files, reverse=True) # sort the file names in reverse -- this is important to avoid overwriting
    for filename in files:
        if filename.startswith("."): # avoid dotfiles that have the extension and filename filter
        	continue
        if filename.endswith(image_extension):
            if containString not in filename:
                continue
            old_path = os.path.join(inputdir, filename)
            if os.path.isfile(old_path):
                print("Processing", filename)
                new_filename = increment_filename(filename)
                #if new_filename and filename != new_filename:
                new_path = os.path.join(outputdir, new_filename)
                # shutil.copy(old_path, new_path) # safer than os.rename
                os.rename(old_path, new_path) # careful, this replaces the old file! 

                print("Renamed ",filename," -> ",new_filename)
    return
 
# ---- running ----


rename_files_in_directory(inDir, outDir)  # Replace '.' with your target directory path


