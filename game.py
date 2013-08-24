import pygame
from obj import Point, DrawableObject, Camera, Fly


class Game(object):
	def __init__(self, manager):

		self.manager = manager
		fly0 = pygame.image.load("assets/img/fly.png")
		fly1 = pygame.image.load("assets/img/fly1.png")
		fly2 = pygame.image.load("assets/img/fly2.png")
		fly3 = pygame.image.load("assets/img/fly3.png")
		plant_img = pygame.image.load("assets/img/plant.png")

		self.active = False
		self.objects = []

		self.player = DrawableObject(fly0.get_rect(), [fly0, fly1, fly2, fly3, fly2, fly1])

		self.objects.append(Fly(pygame.Rect(-40, -10, fly0.get_rect().width, fly0.get_rect().height), [fly0, fly1, fly2, fly3, fly2, fly1]))

		plant = DrawableObject(plant_img.get_rect(), [plant_img])
		plant.move(20, 30)
		self.objects.append(plant)

		self.font = pygame.font.Font('assets/font/Fleftex_M.ttf', 20)

		self.time_left = 10 * 1000
		self.current_time = 0

		info = pygame.display.Info()
		self.camera = Camera(0, 0, info.current_w, info.current_h)

	def enter(self):
		self.active = True

	def leave(self):
		self.active = False

	def update(self, delta):
		if self.active:
			self.time_left -= delta
			self.current_time += delta

			if self.time_left < 0:
				self.manager.set_scene('gameover')

			self.player.move(0.5 * delta * (int(pygame.key.get_pressed()[pygame.K_d]) - int(pygame.key.get_pressed()[pygame.K_a])),
							 0.5 * delta * (int(pygame.key.get_pressed()[pygame.K_s]) - int(pygame.key.get_pressed()[pygame.K_w])))

			self.camera.pos.x = self.player.rect.x + 16
			self.camera.pos.y = self.player.rect.y + 16


			for o in self.objects:
				o.update(delta)

				if self.player.rect.colliderect(o.rect):
					if isinstance(o, Fly):
						self.time_left = 9999
						self.objects.remove(o)


			# camera_pos.x += 0.1 * delta * (int(pygame.key.get_pressed()[pygame.K_RIGHT]) - int(pygame.key.get_pressed()[pygame.K_LEFT]))
			# camera_pos.y += 0.1 * delta * (int(pygame.key.get_pressed()[pygame.K_DOWN]) - int(pygame.key.get_pressed()[pygame.K_UP]))

	def draw(self, screen):
		if self.active:
			screen.blit(self.player.current_sprite(self.current_time), self.camera.apply(self.player.rect))

			for o in self.objects:
				screen.blit(o.current_sprite(self.current_time), self.camera.apply(o.rect))

			time_string = '{0}.{1:03d}'.format(self.time_left / 1000, self.time_left % 1000)
			t = self.font.render(time_string, False, (10, 10, 10))
			r = t.get_rect()
			r.x = (screen.get_rect().width - r.width) / 2
			r.y = 10
			screen.blit(t, r)

	def event(self, event):
		if self.active:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.manager.set_scene('menu')
