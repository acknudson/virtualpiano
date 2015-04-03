class Position():

	def __init__(self):
		#position of fingers in each hand
		#[thumb, index, middle, ring, pinky]
		self.left = [Finger(),Finger(),Finger(),Finger(),Finger()]
		self.right = [Finger(),Finger(),Finger(),Finger(),Finger()]

	#hand is a string, "LEFT" or "RIGHT"
	#finger index in an interger, ranging from 0 to 4
	def update(self, hand, finger_index, x, y, z):
		if hand == "LEFT":
			self.left[finger_index].x = x
			self.left[finger_index].y = y
			self.left[finger_index].z = z
		if hand == "RIGHT":
			self.right[finger_index].x = x
			self.right[finger_index].y = y
			self.right[finger_index].z = z

class Finger():

	def __init__(self):
		self.x = 0
		self.y = 0
		self.z = 0