#! /usr/bin/env python

import dicom
import pylab

ds = dicom.read_file("2d_angiogram.dcm")

for frame in ds.pixel_array:
	pylab.imshow(frame, cmap=pylab.cm.bone)
	pylab.pause(.1)
	pylab.draw()
