class NotFoundError(Exception):

	def __init__(self, value = None):
		self.value = value

	def __str__(self):
		return repr(self.value)

class NotCreated(Exception):

	def __init__(self, value = None):
		self.value = value

	def __str__(self):
		return repr(self.value)