from pygame import Rect
from math import sin, sqrt
from random import random


class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y


class Vector(object):
	def __init__(self, start, end):
		self.x = end.x - start.x
		self.y = end.y - start.y

	def length(self):
		return sqrt(self.x**2 + self.y**2)

	def normalize(self):
		m = self.length()
		self.x = self.x / m
		self.y = self.y / m


class Object(object):
	def __init__(self, rect):
		self.alive_time = 0
		self.rect = rect
		self.pos = Point(rect.x, rect.y)
		self.expired = False

	def move(self, x, y):
		self.pos.x += x
		self.pos.y += y
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y

	def update(self, delta, **kwargs):
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
	def __init__(self, rect, sprites):
		self.speed = random() * 0.16 + 0.1
		super(Fly, self).__init__(rect, sprites)


class FriendlyFly(Fly):
	def update(self, delta, **kwargs):
		m = sin(self.alive_time / 100) * delta * self.speed
		self.move(m, m)
		super(FriendlyFly, self).update(delta, **kwargs)


class EnemyFly(Fly):
	def update(self, delta, player_pos):

		to_player = Vector(self.pos, player_pos)
		if to_player.length() < 512:
			to_player.normalize()
			self.move(to_player.x * delta * self.speed, to_player.y * delta * self.speed)
		else:
			m = sin(self.alive_time / 100) * delta * self.speed
			self.move(m, m)
		super(EnemyFly, self).update(delta)
