from pygame import Rect, font
from math import sin, sqrt
from random import random


class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y


class Vector(object):
	def __init__(self, start, end):
		if isinstance(start, Point) and isinstance(end, Point):
			self.x = end.x - start.x
			self.y = end.y - start.y
		else:
			self.x = start
			self.y = end

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

	def current_sprite(self):
		return self.sprites[(self.alive_time / 80) % len(self.sprites)]


class TextAnimation(DrawableObject):
	def __init__(self, rect, text):
		super(TextAnimation, self).__init__(rect, None)
		self.font = font.Font('assets/font/Fleftex_M.ttf', 12)
		self.text_sprite = self.font.render(text, False, (50, 50, 50))
		self.rect.width = self.text_sprite.get_rect().width
		self.rect.height = self.text_sprite.get_rect().height

	def current_sprite(self):
		return self.text_sprite

	def update(self, delta, **kwargs):
		if self.alive_time > 800:
			self.expired = True
		else:
			self.move(0, delta * -0.1)
		super(TextAnimation, self).update(delta, **kwargs)

class Animation(DrawableObject):
	def current_sprite(self):
		i = self.alive_time / 80
		if i > len(self.sprites) - 1:
			self.expired = True
			i -= 1
		return self.sprites[i]


class Camera(Object):
	def __init__(self, x, y, w, h):
		self.w = w
		self.h = h
		self.vel = [(0, 0)] * 30
		super(Camera, self).__init__(Rect(x, y, 0, 0))

	def move(self, x, y):
		self.vel.append((x, y))
		p = self.vel.pop(0)

		# self.pos.x += p[0]
		# self.pos.y += p[1]
		self.pos.x += x
		self.pos.y += y
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y

	def apply(self, rect):
		return Rect(rect.x + self.w / 2 - self.pos.x, rect.y + self.h / 2 - self.pos.y, rect.width, rect.height)


class BackgroundObject(DrawableObject):
	pass


class Fly(DrawableObject):
	def __init__(self, rect, sprites):
		self.speed = random() * 0.16 + 0.1
		super(Fly, self).__init__(rect, sprites)


class FriendlyFly(Fly):
	def __init__(self, rect, sprites):
		self.dir = Vector(random() * 2.0 - 1.0, random() * 2.0 - 1.0)
		self.dir.normalize()
		super(FriendlyFly, self).__init__(rect, sprites)

	def update(self, delta, **kwargs):

		if self.alive_time % 1000 > 990:
			self.dir = Vector(random() * 2.0 - 1.0, random() * 2.0 - 1.0)
			self.dir.normalize()
		self.move(self.dir.x * self.speed, self.dir.y * self.speed)
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
