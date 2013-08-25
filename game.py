import pygame
from obj import Point, DrawableObject, Camera, FriendlyFly, EnemyFly, Fly, Animation
import random


class Game(object):
	def __init__(self, manager):

		self.manager = manager

		self.collect_sound = pygame.mixer.Sound('assets/sound/collect.wav')
		self.die_sound = pygame.mixer.Sound('assets/sound/die.wav')

		fly_imgs = [pygame.image.load("assets/img/fly{}.png".format(x)) for x in range(4)]
		self.fly_anim = [fly_imgs[0], fly_imgs[1], fly_imgs[2], fly_imgs[3], fly_imgs[2], fly_imgs[1]]

		enemy_imgs = [pygame.image.load("assets/img/enemy{}.png".format(x)) for x in range(4)]
		self.enemy_anim = [enemy_imgs[0], enemy_imgs[1], enemy_imgs[2], enemy_imgs[3], enemy_imgs[2], enemy_imgs[1]]

		anim = [pygame.image.load("assets/img/anim{}.png".format(x)) for x in range(4)]
		self.anim = [anim[0], anim[1], anim[2], anim[3]]

		plant_img = pygame.image.load("assets/img/plant.png")

		self.font = pygame.font.Font('assets/font/Fleftex_M.ttf', 20)
		self.font_tiny = pygame.font.Font('assets/font/Fleftex_M.ttf', 10)

		self.active = False
		self.objects = []


		self.player = DrawableObject(fly_imgs[0].get_rect(), self.fly_anim)
		self.info = pygame.display.Info()

		for i in range(15):
			self.spawn(FriendlyFly, self.fly_anim)
			self.spawn(EnemyFly, self.enemy_anim)

			self.objects.append(DrawableObject(pygame.Rect(random.randint(-1000, 1000), random.randint(-1000, 1000), plant_img.get_rect().width, plant_img.get_rect().height), [plant_img]))

		self.time_left = 10 * 1000
		self.current_time = 0

		self.camera = Camera(0, 0, self.info.current_w, self.info.current_h)
		self.dx = 0
		self.dy = 0

	def enter(self):
		self.__init__(self.manager)
		self.active = True

	def leave(self):
		self.active = False

	def spawn(self, class_, anim):
		ranges = [
			((self.player.rect.x + self.info.current_w / 2 + 20, self.player.rect.x + self.info.current_w / 2 + 500), (self.player.rect.y - 500, self.player.rect.y + 500)),
			((self.player.rect.x - self.info.current_w / 2 - 500, self.player.rect.x - self.info.current_w / 2 - 20), (self.player.rect.y - 500, self.player.rect.y + 500)),
			((self.player.rect.x - 500, self.player.rect.x + 500), (self.player.rect.y - self.info.current_h - 500, self.player.rect.y - self.info.current_h - 20)),
			((self.player.rect.x - 500, self.player.rect.x + 500), (self.player.rect.y + self.info.current_h + 20, self.player.rect.y + self.info.current_h + 500)),
		]

		r = random.choice(ranges)

		self.objects.append(class_(pygame.Rect(random.randint(*r[0]), random.randint(*r[1]), anim[0].get_rect().width, anim[0].get_rect().height), anim))


	def update(self, delta):
		if self.active:
			self.time_left -= delta
			self.current_time += delta

			if self.time_left < 0:
				self.manager.set_scene('gameover', time_survived=self.current_time)

			if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_a]:
				self.dx = 0.4 * (int(pygame.key.get_pressed()[pygame.K_d]) - int(pygame.key.get_pressed()[pygame.K_a]))
			else:
				if self.dx > 0:
					self.dx -= delta * 0.002
					self.dx = self.dx if self.dx > 0 else 0
				elif self.dx < 0:
					self.dx += delta * 0.002
					self.dx = self.dx if self.dx < 0 else 0


			if pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_w]:
				self.dy = 0.4 * (int(pygame.key.get_pressed()[pygame.K_s]) - int(pygame.key.get_pressed()[pygame.K_w]))
			else:
				if self.dy > 0:
					self.dy -= delta * 0.002
					self.dy = self.dy if self.dy > 0 else 0
				elif self.dy < 0:
					self.dy += delta * 0.002
					self.dy = self.dy if self.dy < 0 else 0

			self.player.move(delta * self.dx, delta * self.dy)

			self.camera.pos.x = self.player.rect.x + 16
			self.camera.pos.y = self.player.rect.y + 16


			for o in self.objects:
				o.update(delta, player_pos=self.player.pos)
				if o.expired:
					self.objects.remove(o)
				elif self.player.rect.colliderect(o.rect):
					if isinstance(o, EnemyFly):
						self.die_sound.play()
						self.manager.set_scene('gameover', time_survived=self.current_time)
					elif isinstance(o, FriendlyFly):
						self.objects.append(Animation(pygame.Rect(self.player.rect.x, self.player.rect.y, self.anim[0].get_rect().width, self.anim[0].get_rect().height), self.anim))
						self.collect_sound.play()
						self.time_left = 9999
						self.objects.remove(o)
						self.spawn(FriendlyFly, self.fly_anim)
						self.spawn(EnemyFly, self.enemy_anim)

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
