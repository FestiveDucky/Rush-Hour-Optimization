import pygame.mouse

from constants import *
from simulation import Simulation

if __name__ == '__main__':
    # Titles the game
    pygame.display.set_caption('Rush Hour Traffic')
    clock = pygame.time.Clock()

    s = Simulation()
    executing = True
    update = True
    # Starting the game loop
    while executing:
        print("Time between frames:", clock.tick(TPS), "ms")

        # Checking events
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                executing = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                # Gets the points that the mouse clicked
                points_clicked = s.getGraph().getPointsClicked(e.pos)

                if len(points_clicked) == 0:
                    s.getGraph().addPoint(e.pos)
                    s.getGraph().clearSelectedPoints()
                else:
                    s.getGraph().setMovingPoint(points_clicked[0])

                update = True
            elif e.type == pygame.MOUSEMOTION:
                update = s.getGraph().movePoint(e.pos)
            elif e.type == pygame.MOUSEBUTTONUP:
                s.getGraph().setMovingPoint(None)
                update = True
            elif e.type == pygame.KEYDOWN:
                # Remove a point
                if e.key == pygame.K_r:
                    mouse_position = pygame.mouse.get_pos()
                    s.getGraph().removePoint(mouse_position)

                    update = True
                # Manual update
                elif e.key == pygame.K_SPACE:
                    update = True
                # Select a point
                elif e.key == pygame.K_s:
                    s.getGraph().selectPoint(pygame.mouse.get_pos())
                    update = True
                # Clear selected points
                elif e.key == pygame.K_ESCAPE:
                    s.getGraph().clearSelectedPoints()
                    update = True
                # Adds an edge
                elif e.key == pygame.K_e:
                    s.getGraph().addEdge()
                    update = True
                # Deletes the edge between the selected points
                elif e.key == pygame.K_d:
                    s.getGraph().deleteEdge()
                    update = True

        s.tick()

        # Drawing to the screen
        if update:
            display.fill((14, 25, 36))

            s.getGraph().drawEdges()
            s.getGraph().updatePoints()

            update = False

        # Updating the display
        pygame.display.update()
