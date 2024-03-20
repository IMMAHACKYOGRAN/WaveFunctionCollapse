import pygame
from WaveFunctionCollapse import WFCGenerator

WIDTH = 800
HEIGHT = 800

if __name__ == "__main__":
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Wave Function Collapse For Wagot")
	clock = pygame.time.Clock()

	# ------------- Create Wave Function Collapse ------------- #
	gen = WFCGenerator(5, 5)
	gen.LoadImages(pygame.image.load)
	gen.Collapse()
	# --------------------------------------------------------- #

	running = True
	while running:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				
		screen.fill((0,0,0))
		
		# ---------------------- Render Grid ---------------------- #
		w = WIDTH/gen.Cols
		h = HEIGHT/gen.Rows

		for x in range(gen.Cols):
			for y in range(gen.Rows):
				tile = gen.Grid[x + y * gen.Rows]
				screen.blit(pygame.transform.scale(gen.Images[tile.Options[0]], (w, h)), (x*w, y*h))
		# --------------------------------------------------------- #

		pygame.display.flip()

	pygame.quit()