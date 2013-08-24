#!/usr/bin/env python

import pygame
import sys

pygame.init()
pygame.mixer.init(frequency=44100, channels=1)

size = width, height = 640, 480
bg_color = 245, 245, 245

pygame.display.set_caption('LD27 - 10 seconds')
screen = pygame.display.set_mode(size)

prev_time = pygame.time.get_ticks()
fly0 = pygame.image.load("assets/img/fly.png")
fly1 = pygame.image.load("assets/img/fly1.png")
fly2 = pygame.image.load("assets/img/fly2.png")
fly3 = pygame.image.load("assets/img/fly3.png")
plant_img = pygame.image.load("assets/img/plant.png")

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


player = Object([fly0, fly1, fly2, fly3, fly2, fly1], fly0.get_rect())
asdf = Object([fly0, fly1, fly2, fly3, fly2, fly1], fly0.get_rect())

plant = Object([plant_img], plant_img.get_rect())
plant.move(20, 30)

camera_pos = Point(0, 0)

font = pygame.font.Font('assets/font/Fipps-Regular.otf', 20)

def apply_camera(rect):
	return pygame.Rect(rect.x + width / 2 - camera_pos.x, rect.y + height / 2 - camera_pos.y, rect.width, rect.height)

time_left = 10 * 1000

while 1:

	curr_time = pygame.time.get_ticks()
	delta = curr_time - prev_time
	prev_time = curr_time

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	time_left -= delta

	if time_left < 0:
		bg_color = 245, 45, 45

	player.move(0.5 * delta * (int(pygame.key.get_pressed()[pygame.K_d]) - int(pygame.key.get_pressed()[pygame.K_a])),
				0.5 * delta * (int(pygame.key.get_pressed()[pygame.K_s]) - int(pygame.key.get_pressed()[pygame.K_w])))

	camera_pos.x = player.rect.x + 16
	camera_pos.y = player.rect.y + 16

	# camera_pos.x += 0.1 * delta * (int(pygame.key.get_pressed()[pygame.K_RIGHT]) - int(pygame.key.get_pressed()[pygame.K_LEFT]))
	# camera_pos.y += 0.1 * delta * (int(pygame.key.get_pressed()[pygame.K_DOWN]) - int(pygame.key.get_pressed()[pygame.K_UP]))

	# Drawing
	screen.fill(bg_color)
	screen.blit(player.current_sprite(curr_time), apply_camera(player.rect))
	screen.blit(asdf.current_sprite(curr_time), apply_camera(asdf.rect))
	screen.blit(plant.current_sprite(curr_time), apply_camera(plant.rect))

	time_string = '{0}.{1:03d}'.format(time_left / 1000, time_left % 1000)
	t = font.render(time_string, False, (10, 10, 10))
	screen.blit(t, t.get_rect())

	pygame.display.flip()
