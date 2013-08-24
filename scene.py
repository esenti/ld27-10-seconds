from game import Game
from menu import GameOver, Menu


class SceneManager(object):
	def __init__(self):

		self.scenes = {
			'game': Game(self),
			'gameover': GameOver(self),
			'menu': Menu(self)
		}

	def update(self, delta):
		for k, v in self.scenes.iteritems():
			v.update(delta)

	def event(self, event):
		for k, v in self.scenes.iteritems():
			r = v.event(event)
			if r:
		 		break

	def draw(self, screen):
		for k, v in self.scenes.iteritems():
			v.draw(screen)

	def set_scene(self, scene, **kwargs):
		for k, v in self.scenes.iteritems():
			if k != scene:
				v.leave()

		self.scenes[scene].enter(**kwargs)
