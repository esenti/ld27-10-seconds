import pygame
from obj import Point, Object

camera_pos = Point(0, 0)

def apply_camera(rect):
	info = pygame.display.Info()
	return pygame.Rect(rect.x + info.current_w / 2 - camera_pos.x, rect.y + info.current_h / 2 - camera_pos.y, rect.width, rect.height)


class Game(object):
	def __init__(self, manager):

		self.manager = manager
		fly0 = pygame.image.load("assets/img/fly.png")
		fly1 = pygame.image.load("assets/img/fly1.png")
		fly2 = pygame.image.load("assets/img/fly2.png")
		fly3 = pygame.image.load("assets/img/fly3.png")
		plant_img = pygame.image.load("assets/img/plant.png")

		self.active = False


		self.player = Object([fly0, fly1, fly2, fly3, fly2, fly1], fly0.get_rect())
		self.asdf = Object([fly0, fly1, fly2, fly3, fly2, fly1], fly0.get_rect())

		self.plant = Object([plant_img], plant_img.get_rect())
		self.plant.move(20, 30)

		self.font = pygame.font.Font('assets/font/Fipps-Regular.otf', 20)

		self.time_left = 10 * 1000
		self.current_time = 0


	def enter(self):

		self.active = True

	def leave(self):
		self.active = False


	def update(self, delta):
		if self.active:
			self.player.move(0.5 * delta * (int(pygame.key.get_pressed()[pygame.K_d]) - int(pygame.key.get_pressed()[pygame.K_a])),
						0.5 * delta * (int(pygame.key.get_pressed()[pygame.K_s]) - int(pygame.key.get_pressed()[pygame.K_w])))

			camera_pos.x = self.player.rect.x + 16
			camera_pos.y = self.player.rect.y + 16

			self.time_left -= delta
			self.current_time += delta

			# camera_pos.x += 0.1 * delta * (int(pygame.key.get_pressed()[pygame.K_RIGHT]) - int(pygame.key.get_pressed()[pygame.K_LEFT]))
			# camera_pos.y += 0.1 * delta * (int(pygame.key.get_pressed()[pygame.K_DOWN]) - int(pygame.key.get_pressed()[pygame.K_UP]))


	def draw(self, screen):
		if self.active:
			screen.blit(self.player.current_sprite(self.current_time), apply_camera(self.player.rect))
			screen.blit(self.asdf.current_sprite(self.current_time), apply_camera(self.asdf.rect))
			screen.blit(self.plant.current_sprite(self.current_time), apply_camera(self.plant.rect))

			time_string = '{0}.{1:03d}'.format(self.time_left / 1000, self.time_left % 1000)
			t = self.font.render(time_string, False, (10, 10, 10))
			screen.blit(t, t.get_rect())


	def event(self, event):
		if self.active:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.manager.set_scene('menu')
