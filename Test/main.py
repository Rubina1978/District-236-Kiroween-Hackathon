
import asyncio
import pygame

async def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygbag Test")

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 100, 160))

        pygame.draw.circle(screen, (255, 220, 50), (400, 300), 70)

        pygame.display.flip()

        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())