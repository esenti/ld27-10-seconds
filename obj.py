from pygame import Rect
from math import sin

class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y


class Object(object):
	def __init__(self, rect):
		self.alive_time = 0
		self.rect = rect
		self.pos = Point(rect.x, rect.y)

	def move(self, x, y):
		self.pos.x += x
		self.pos.y += y
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y

	def update(self, delta):
		self.alive_time += delta


class DrawableObject(Object):
	def __init__(self, rect, sprites):
		self.sprites = sprites
		super(DrawableObject, self).__init__(rect)

	def current_sprite(self, time):
		return self.sprites[(time / 80) % len(self.sprites)]


class Camera(Object):
	def __init__(self, x, y, w, h):
		self.w = w
		self.h = h
		super(Camera, self).__init__(Rect(x, y, 0, 0))

	def apply(self, rect):
		return Rect(rect.x + self.w / 2 - self.pos.x, rect.y + self.h / 2 - self.pos.y, rect.width, rect.height)


class Fly(DrawableObject):
	def update(self, delta):
		m = sin(self.alive_time / 100) * delta * 0.04
		self.move(m, m)
		super(Fly, self).update(delta)
