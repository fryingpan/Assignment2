
class IceCream(Enemy):
	IMAGE = None
	def __init__(self, speed):
		Enemy.__init__(speed)
		if not IceCream.Image:
			IceCream.Image = None
		self.health = 1
		self.puddle_image = None
		self.rect.x = 0
		self.rect.y = 0
		self.face = None



	def is_alive(self):
		if self.health == 0:
			#then the enemy is dead
			pass

	def attack(self):




	def load_images(self):
        Enemy.IMAGES_RIGHT = []
        Enemy.IMAGES_LEFT = []
        Enemy.IMAGES_FRONT = []
        Enemy.IMAGES_BACK = []
        sheetR = PI.load("FPGraphics/Food/IceCreamWalkRight.png").convert_alpha()
        sheetL = PI.load("FPGraphics/Food/IceCreamWalkLeft.png").convert_alpha()
        sheetF = PI.load("FPGraphics/Food/IceCreamWalkFront.png").convert_alpha()
        sheetB = PI.load("FPGraphics/Food/IceCreamWalkBack.png").convert_alpha()
        Enemy.IMAGES_RIGHT = self.load_images_helper(Enemy.IMAGES_RIGHT, sheetR)
        Enemy.IMAGES_LEFT = self.load_images_helper(Enemy.IMAGES_LEFT, sheetL)
        Enemy.IMAGES_FRONT = self.load_images_helper(Enemy.IMAGES_FRONT, sheetF)
        Enemy.IMAGES_BACK = self.load_images_helper(Enemy.IMAGES_BACK, sheetB)

    def update_image(self, imageArray):
        try:
            self.image = imageArray[self.frame].convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.center = (self.WIDTH/2, self.HEIGHT/2)
        except IndexError:
			self.face = list(self.face)[0]

