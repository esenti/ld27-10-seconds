class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y


class Object(object):
	def __init__(self, sprites, rect):
		self.sprites = sprites
		self.rect = rect
		self.pos = Point(rect.x, rect.y)

	def move(self, x, y):
		self.pos.x += x
		self.pos.y += y
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y

	def current_sprite(self, time):
		return self.sprites[(time / 80) % len(self.sprites)]
