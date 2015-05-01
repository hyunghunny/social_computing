# coding=UTF-8
##
# transpose CSV data
#
#
from itertools import izip
from csv import reader, writer
import os

##
# Pivot TSV file
# source snippet from http://stackoverflow.com/questions/4869189/how-to-pivot-data-in-a-csv-file
#
def transpose(src, dest):

    with open(src, "rb") as f:
        with open(dest, "wb") as fw:
            transposed = izip(*reader(f, delimiter='\t'))
            writer(fw, delimiter='\t').writerows(transposed)

