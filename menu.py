import pygame


class GameOver(object):
	def __init__(self, manager):

		self.manager = manager
		self.select_sound = pygame.mixer.Sound('assets/sound/select.wav')
		self.font = pygame.font.Font('assets/font/Fleftex_M.ttf', 24)
		self.font_small = pygame.font.Font('assets/font/Fleftex_M.ttf', 16)
		self.font_tiny = pygame.font.Font('assets/font/Fleftex_M.ttf', 10)

	def enter(self, time_survived):
		self.time_survived = time_survived
		self.active = True

	def leave(self):
		self.active = False

	def update(self, delta):
		pass

	def draw(self, screen):
		if self.active:

			string = 'It\'s over.'
			t = self.font.render(string, False, (10, 10, 10))
			r = t.get_rect()
			r.x = (screen.get_rect().width - r.width) / 2
			r.y = (screen.get_rect().height - r.height) / 2
			screen.blit(t, r)

			survived_string = 'You have survived for {0}.{1:03d} seconds.'.format(self.time_survived / 1000, self.time_survived % 1000)
			t = self.font_small.render(survived_string, False, (10, 10, 10))
			r = t.get_rect()
			r.x = (screen.get_rect().width - r.width) / 2
			r.y = (screen.get_rect().height - r.height) / 2 + 50
			screen.blit(t, r)

			menu_string = '[ space to continue ]'
			t = self.font_tiny.render(menu_string, False, (10, 10, 10))
			r = t.get_rect()
			r.x = (screen.get_rect().width - r.width) / 2
			r.y = (screen.get_rect().height - r.height) / 2 + 200
			screen.blit(t, r)

	def event(self, event):
		if self.active:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					self.select_sound.play()
					self.manager.set_scene('menu')

					return True


class Menu(object):
	def __init__(self, manager):

		self.manager = manager
		self.select_sound = pygame.mixer.Sound('assets/sound/select.wav')
		self.font = pygame.font.Font('assets/font/Fleftex_M.ttf', 30)
		self.font_small = pygame.font.Font('assets/font/Fleftex_M.ttf', 16)
		self.font_tiny = pygame.font.Font('assets/font/Fleftex_M.ttf', 14)
		self.current_time = 0

	def enter(self):
		self.active = True
		self.select_sound.play()
		self.current_time = 0

	def leave(self):
		self.active = False

	def update(self, delta):
		self.current_time += delta

	def draw(self, screen):
		if self.active:

			string = 'You\'re a fly.'
			t = self.font.render(string, False, (10, 10, 10))
			r = t.get_rect()
			r.x = (screen.get_rect().width - r.width) / 2
			r.y = 200
			screen.blit(t, r)

			if self.current_time % 1000 < 500:
				string = '[ any key to start ]'
				t = self.font_tiny.render(string, False, (10, 10, 10))
				r = t.get_rect()
				r.x = (screen.get_rect().width - r.width) / 2
				r.y = screen.get_rect().height - 100
				screen.blit(t, r)

	def event(self, event):
		if self.active:
			if event.type == pygame.KEYDOWN:
				self.select_sound.play()
				self.manager.set_scene('game')

			return True
