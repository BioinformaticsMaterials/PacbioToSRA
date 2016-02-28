#!/usr/bin/env python

###############################################################################
# Copyright (c) 2011-2013, Pacific Biosciences of California, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of Pacific Biosciences nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY
# THIS LICENSE.  THIS SOFTWARE IS PROVIDED BY PACIFIC BIOSCIENCES AND ITS
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT
# NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL PACIFIC BIOSCIENCES OR
# ITS CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###############################################################################



__author__ = 'jlandolin'
__email__ = 'jlandolin@pacificbiosciences.com'


# This script is deprecated. The new script is bin_send_to_ncbi.py
values_to_continue = set(['y', 'yes'])
values_to_stop = set(['n', 'no'])
all_values = values_to_continue.union(values_to_stop)

print "This script will be DEPRECATED. Please use the following script instead: bin/send_to_ncbi.py"
response = None

while response not in all_values:
    response = str(raw_input("Would you still like to continue? (Y)es/(No): ")).lower()
    if response in values_to_continue:
        break
    elif response in values_to_stop:
        import sys
        sys.exit()


import os
import csv
import argparse
#import subprocess
import xml.etree.ElementTree as ET

from argparse import RawTextHelpFormatter
from subprocess import PIPE, Popen


###################################################
# global variables
###################################################
#dictionary containing files and levels relative to data directory
file_formats = {'metadata.xml':-1, 'bas.h5':0, '1.bax.h5':0, '2.bax.h5':0, '3.bax.h5':0}
nfiles = len(file_formats)
data_dirs = {}
pbns = {'metadata' : '{http://pacificbiosciences.com/PAP/Metadata.xsd}',}



##################################################
#functions
##################################################
def fofn2fodn(fofn_filename):

    #read in fofn file, and make fodn.
    #Assume fofn file points to files within Analysis_Results directory
    f = open(fofn_filename, "r")
    for line in f.readlines():
        path=os.path.dirname(line)
        if path in data_dirs.keys():
            data_dirs[path] = data_dirs[path] + 1
           #print 'inside if: ', path, data_dirs[path]
        else:
            data_dirs[path] = 1
            #print 'inside else:', path, data_dirs[path]

    return data_dirs
    f.close()





def get_library_info(d,f):
    a = [1,2,3,4]
    return a


#def get_file_info(dir, filetype, level):
def get_file_info(dir, fileformats, fileobject1, fileobject2):

    nfiles = len(fileformats)
    fileinfo = [0,0,0,0]
    sorted_keys = reversed(sorted(fileformats.keys())) #make sure metadata file goes first
    for filetype in sorted_keys:
        level = fileformats[filetype]
        currentdir = dir

        cds = range(0,level,-1)  #change directory to appropriate level
        if cds:
            for i in range(0,level,-1):
                currentdir = os.path.dirname(currentdir)
                #print "   get_file_info: current level", i, dir


        cmd = "ls -1 " + currentdir + "/*" + filetype + "*"
        fullpathfilename = cmdline(cmd)
        fullpathfilename = fullpathfilename.rstrip('\n')
        #print "   get_file_info: fullpathfilename = ", fullpathfilename

        #get samplename
        if filetype == "metadata.xml":
            root = ET.parse(fullpathfilename).getroot()
            #for child in root:
            #print child.tag

            #samplename = s.find('metadata:Name', pbns).text
            #cellname = s.find('metadata:PlateId', pbns).text + "_" + s.find('metadata:WellName', pbns).text

            # alternatively, a worse way to do this is:
            samplename =  root[4][0].text
            cellname = root[4][1].text + "_" + root[4][2].text
            runname = os.path.basename(currentdir)


        #get md5sum
        filename = os.path.basename(fullpathfilename)
        cmd = "md5sum " + fullpathfilename + "| awk \'{print $1}\'"
        md5sum = cmdline(cmd)
        md5sum = md5sum.rstrip('\n')
        #md5sum = "placeholder"
        # print "   get_file_info: ", samplename, cellname, filename, md5sum
        print "   ", filename


        fileobject1.write(fullpathfilename + "\n")
        fileinfo = [samplename,cellname,filename,md5sum]

        fileobject2.write("\t".join(fileinfo))
        fileobject2.write("\n")
        #fileobject2.write(matrix_fileinfo)


        #print "   get_file_info:"
        #print "   get_file_info: k = ", k
        #print "   get_file_info: samplename = ", samplename
        #print "   get_file_info: cellname = ", cellname
        #print "   get_file_info: filename = ", filename
        #print "   get_file_info: md5sum = ", md5sum
        #print "   get_file_info: matrix_fileinfo = ", matrix_fileinfo

    return samplename






def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

###################################################
# main
###################################################
help_text = ["Given a PacBio input.fofn file (file of filenames), create necessary files for data submission at NCBI SRA. Output files are:",
        "  1. sra_data.txt - sample information (from metadata.xml)",
        "  2. file_info.csv - md5sums of all files that need to be uploaded",
        "  3. aspera.fofn - full path of all files that need to be uploaded to NCBI SRA"]

parser = argparse.ArgumentParser(description= '\n'.join(help_text), formatter_class = RawTextHelpFormatter)
parser.add_argument("input_fofn", help="path to input.fofn file")
args = parser.parse_args()
# first convert the file of file names (fofn) to a file of directory names (fodn)
dirs = fofn2fodn(args.input_fofn)



unique_samples={}

f1 = open("aspera.fofn",'w')
f2 = open("file_info.csv",'w')
f2.write("\t".join(['Library_ID', 'Run_ID', 'Filename', 'md5sum']))
f2.write("\n")

#loop through smrtcell directories and file_formats for each directory
sorted_keys = reversed(sorted(dirs.keys())) #sort alphabetically
for d in sorted_keys:
    print "working on ", d
    samplename = get_file_info(d,file_formats, f1, f2)
    if samplename in unique_samples.keys():
        unique_samples[samplename]=unique_samples[samplename] + 1
    else:
        unique_samples[samplename] = 0

    print ""
    print ""


f1.close()
f2.close()


#write sra_data
f3 = open("sra_data.txt",'w')
for k in unique_samples.keys():
    f3.write(k)
    f3.write("\n")
f3.close()


