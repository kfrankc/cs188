import numpy as np

def mat_nonimplication(cur_frame, prev_frame):
	[rowMax, colMax] = cur_frame.shape
	ret_frame = np.ones((rowMax, colMax))
	for r in xrange(rowMax):
		for c in xrange(colMax):
			if cur_frame[r][c] == 1 and prev_frame[r][c] == 0:
				print "point: (%i, %i)" %(r, c)
				ret_frame[r][c] = 1
			else:
				ret_frame[r][c] = 0
	return ret_frame

A = np.array([[1, 1],[0, 0]], np.int32)
B = np.array([[1, 0],[0, 1]], np.int32)
C = mat_nonimplication(B, A)
print C