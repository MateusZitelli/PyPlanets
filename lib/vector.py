"""
This module implements the Vector object. Which has several of
2D vector features such dot product, adding, project and angle.
It also overloads many commom math operator
"""

import math

def _is_numeric(obj):
	"""
	Finds out if a variable is a numeric one
	"""
	if isinstance(obj, (int, long, float)):
		return True
	else:
		return False

class Vector(object):
	"""
	Vector class: Objects of this class have several of
	2D vector implementations such dot product, adding, project and angle.
	It also overloads many commom math operator
	"""

	def __init__(self, a=0, b=0 ):
		"""
		Creates a new vector
		"""
		if _is_numeric(a):
			#assume two numbers
			self.x = a
			self.y = b
		else:
			#assume Vectors/tuples
			self.x = b[0] - a[0]
			self.y = b[1] - a[1]

	def __getitem__(self, index):
		if index == 0:
			return self.x
		elif index == 1:
			return self.y
		else:
			raise IndexError
		
	def __add__(self, other):
		return Vector(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return Vector(self.x - other.x, self.y - other.y)

	def __mul__(self, other):
		try:
			other = other - 0
		except:
			raise TypeError, "Only scalar multiplication is supported."
		return Vector( other * self.x, other * self.y )

	def __rmul__(self, other):
		return self.__mul__(other)
		
	def __div__(self, other):
		return Vector( self.x / other, self.y / other )

	def __neg__(self):
		return Vector(-self.x, -self.y)

	def __abs__(self):
		return self.length()
	
	def __repr__(self):
		return '(%s, %s)' % (self.x, self.y)

	def __str__(self):
		return '(%s, %s)' % (self.x, self.y)

	def __pow__(self, y, z=None):
		return Vector(self.x.__pow__(y,z), self.y.__pow__(y,z))

	def dot(self, vector):
		"""
		Return the dot product of two vectors
		"""
		return self.x * vector.x + self.y * vector.y

	def cross(self, vector):
		"""
		Return the cross product of two vectors
		"""
		return self.x * vector.y - self.y * vector.x

	def length(self):
		"""
		Return the vector's length
		"""
		return math.sqrt( self.dot(self) )

	def perpendicular(self):
		"""
		Return the vector that is perpenticular of this
		"""
		return Vector(-self.y, self.x)

	def unit(self):
		"""
		Return the vector's unit(length one)
		"""
		return self / self.length()
	
	def projection(self, vector):
		"""
		Return the projection of this vector on another
		"""
		return self.dot(vector.unit()) * vector.unit()

	def angle(self, vector=None):
		"""
		Return the angle created by this vector and another of the vector
		(1,0) if given None
		"""
		if vector == None:
			vector = Vector(1,0)
		return math.acos((self.dot(vector))/(self.length() * vector.length()))

	def angle_in_degrees(self, vector=None):
		"""
		Return the angle created by this vector and another of the vector
		(1,0) if given None. Angle in degrees
		"""
		return (self.angle(vector) * 180) /math.pi


