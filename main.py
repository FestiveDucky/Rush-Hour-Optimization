import pygame.mouse

from constants import *
from simulation import Simulation

# TODO
# add saving to file and loading from file
# Add button to swap into simulation mode which prevents graph editing
# create vehicles with start locations and destinations
# Write A* for vehicle pathing
# Create vehicle movement and timing/scoring for vehicles
# Add delays based on traffic density
# Return statistics on simulations (with matplotlib graphs)

# Start ACO and other algorithms


if __name__ == '__main__':
    # Titles the game
    pygame.display.set_caption('Rush Hour Traffic')
    clock = pygame.time.Clock()

    s = Simulation()
    s.loadGraphs()

    # TODO later change this to a number saved in the file
    graph_index = 0

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
                # First prioritize clicks on text boxes
                textboxes_clicked = s.getGraph(graph_index).getTextBoxesClicked(e.pos)
                if len(textboxes_clicked) != 0:
                    textboxes_clicked[0].typing(True)
                else:
                    # Gets the points that the mouse clicked
                    points_clicked = s.getGraph(graph_index).getPointsClicked(e.pos)

                    if len(points_clicked) == 0:
                        s.getGraph(graph_index).addPoint(e.pos)
                        s.getGraph(graph_index).clearSelectedPoints()
                    else:
                        s.getGraph(graph_index).setMovingPoint(points_clicked[0])

                update = True
            elif e.type == pygame.MOUSEMOTION:
                update = s.getGraph(graph_index).movePoint(e.pos)
            elif e.type == pygame.MOUSEBUTTONUP:
                s.getGraph(graph_index).setMovingPoint(None)
                update = True
            elif e.type == pygame.KEYDOWN:
                # Remove a point
                if e.key == pygame.K_r:
                    mouse_position = pygame.mouse.get_pos()
                    s.getGraph(graph_index).removePoint(mouse_position)

                    update = True
                # Manual update
                elif e.key == pygame.K_SPACE:
                    update = True
                # Select a point
                elif e.key == pygame.K_s:
                    s.getGraph(graph_index).selectPoint(pygame.mouse.get_pos())
                    update = True
                # Clear selected points
                elif e.key == pygame.K_ESCAPE:
                    s.getGraph(graph_index).clearSelectedPoints()
                    update = True
                # Adds an edge
                elif e.key == pygame.K_e:
                    s.getGraph(graph_index).addEdge()
                    update = True
                # Deletes the edge between the selected points
                elif e.key == pygame.K_d:
                    s.getGraph(graph_index).deleteEdge()
                    update = True
                elif e.key == pygame.K_LEFT:
                    graph_index -= 1
                    graph_index = max(0, graph_index)
                    update = True
                elif e.key == pygame.K_RIGHT:
                    graph_index += 1
                    update = True

        s.tick()

        # Drawing to the screen
        if update:
            display.fill((14, 25, 36))

            s.getGraph(graph_index).drawEdges()
            s.getGraph(graph_index).updateTextBoxes()
            s.getGraph(graph_index).updatePoints()

            update = False

        # Updating the display
        pygame.display.update()
