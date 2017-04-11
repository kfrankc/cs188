#! /usr/bin/env python

import dicom
import pylab

ds = dicom.read_file("2d_angiogram.dcm")

frames = len(ds.pixel_array[:,1,1])
for i in xrange(frames):
	pixel_array_2d = ds.pixel_array[i,:,:]
	pylab.imshow(pixel_array_2d, cmap=pylab.cm.bone)
	pylab.pause(.1)
	pylab.draw()
