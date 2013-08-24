import pygame
from obj import Point, DrawableObject, Camera, FriendlyFly, EnemyFly, Fly
import random


class Game(object):
	def __init__(self, manager):

		self.manager = manager

		self.collect_sound = pygame.mixer.Sound('assets/sound/collect.wav')
		self.die_sound = pygame.mixer.Sound('assets/sound/die.wav')

		self.fly_imgs = [pygame.image.load("assets/img/fly{}.png".format(x)) for x in range(4)]


		plant_img = pygame.image.load("assets/img/plant.png")

		self.font = pygame.font.Font('assets/font/Fleftex_M.ttf', 20)
		self.font_tiny = pygame.font.Font('assets/font/Fleftex_M.ttf', 10)

		self.active = False
		self.objects = []

		self.fly_anim = [self.fly_imgs[0], self.fly_imgs[1], self.fly_imgs[2], self.fly_imgs[3], self.fly_imgs[2], self.fly_imgs[1]]

		self.player = DrawableObject(self.fly_imgs[0].get_rect(), self.fly_anim)

		for i in range(12):
			self.objects.append(FriendlyFly(pygame.Rect(random.randint(-1000, 1000), random.randint(-1000, 1000), self.fly_imgs[0].get_rect().width, self.fly_imgs[0].get_rect().height), self.fly_anim))
			self.objects.append(EnemyFly(pygame.Rect(random.randint(-1000, 1000), random.randint(-1000, 1000), self.fly_imgs[0].get_rect().width, self.fly_imgs[0].get_rect().height), self.fly_anim))
			self.objects.append(DrawableObject(pygame.Rect(random.randint(-1000, 1000), random.randint(-1000, 1000), plant_img.get_rect().width, plant_img.get_rect().height), [plant_img]))

		self.time_left = 10 * 1000
		self.current_time = 0

		info = pygame.display.Info()
		self.camera = Camera(0, 0, info.current_w, info.current_h)

	def enter(self):
		self.__init__(self.manager)
		self.active = True

	def leave(self):
		self.active = False

	def update(self, delta):
		if self.active:
			self.time_left -= delta
			self.current_time += delta

			if self.time_left < 0:
				self.manager.set_scene('gameover', time_survived=self.current_time)

			self.player.move(0.5 * delta * (int(pygame.key.get_pressed()[pygame.K_d]) - int(pygame.key.get_pressed()[pygame.K_a])),
							 0.5 * delta * (int(pygame.key.get_pressed()[pygame.K_s]) - int(pygame.key.get_pressed()[pygame.K_w])))

			self.camera.pos.x = self.player.rect.x + 16
			self.camera.pos.y = self.player.rect.y + 16


			for o in self.objects:
				o.update(delta, player_pos=self.player.pos)

				if self.player.rect.colliderect(o.rect):
					if isinstance(o, EnemyFly):
						self.die_sound.play()
						self.manager.set_scene('gameover', time_survived=self.current_time)
					elif isinstance(o, FriendlyFly):
						self.collect_sound.play()
						self.time_left = 9999
						self.objects.remove(o)
						self.objects.append(FriendlyFly(pygame.Rect(random.randint(-1000, 1000), random.randint(-1000, 1000), self.fly_imgs[0].get_rect().width, self.fly_imgs[0].get_rect().height), self.fly_anim))


			# camera_pos.x += 0.1 * delta * (int(pygame.key.get_pressed()[pygame.K_RIGHT]) - int(pygame.key.get_pressed()[pygame.K_LEFT]))
			# camera_pos.y += 0.1 * delta * (int(pygame.key.get_pressed()[pygame.K_DOWN]) - int(pygame.key.get_pressed()[pygame.K_UP]))

	def draw(self, screen):
		if self.active:
			screen.blit(self.player.current_sprite(self.current_time), self.camera.apply(self.player.rect))

			for o in self.objects:
				screen.blit(o.current_sprite(self.current_time), self.camera.apply(o.rect))
				# if isinstance(o, Fly):
				# 	string = '{0:3f}'.format(o.speed)
				# 	t = self.font_tiny.render(string, False, (10, 10, 10))
				# 	r = t.get_rect()
				# 	r.x = o.rect.x
				# 	r.y = o.rect.y
				# 	screen.blit(t, self.camera.apply(r))

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
