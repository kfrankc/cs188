class Segment(object):
	def __init__(self, seg_counter):
		# list of coordinates
		self.path = []
		self.junction = None
		self.parent = None
		self.children = None
		self.seg_id = seg_counter

	def add_to_path(self, r, c):
		self.path.append((r, c))

	def add_parent(self, segment):
		self.parent = segment

	def add_to_children(self, segment):
		if (self.children is None):
			self.children = [segment]
		else:
			self.children.append(segment)

	def add_junction(self, coord):
		self.junction = coord
