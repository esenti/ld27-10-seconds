import pygame


class GameOver(object):
	def __init__(self, manager):

		self.manager = manager
		self.font = pygame.font.Font('assets/font/Fleftex_M.ttf', 24)

	def enter(self):
		self.active = True

	def leave(self):
		self.active = False

	def update(self, delta):
		pass

	def draw(self, screen):
		if self.active:

			string = 'You are dead.'
			t = self.font.render(string, False, (10, 10, 10))
			r = t.get_rect()
			r.x = (screen.get_rect().width - r.width) / 2
			r.y = (screen.get_rect().height - r.height) / 2
			screen.blit(t, r)

	def event(self, event):
		if self.active:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.manager.set_scene('menu')


class Menu(object):
	def __init__(self, manager):

		self.manager = manager
		self.font = pygame.font.Font('assets/font/Fleftex_M.ttf', 24)

	def enter(self):
		self.active = True

	def leave(self):
		self.active = False

	def update(self, delta):
		pass

	def draw(self, screen):
		if self.active:

			string = 'You\'re a fly.'
			t = self.font.render(string, False, (10, 10, 10))
			r = t.get_rect()
			r.x = (screen.get_rect().width - r.width) / 2
			r.y = (screen.get_rect().height - r.height) / 2
			screen.blit(t, r)

	def event(self, event):
		if self.active:
			if event.type == pygame.KEYDOWN:
				self.manager.set_scene('game')
