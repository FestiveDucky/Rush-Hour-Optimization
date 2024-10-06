import pygame.mouse

from constants import *
from simulation import Simulation

# TODO
# MAKE SURE THE GRAPH IS PLANAR (no edges overlap)
# create random pairs of vertices
# add saving to file and loading from file for graphs
# (for now seed the random number generator for pairs of vertices)
# Write dijkstra and run it for one vertex in each pair (if one of the vertices already has it ran, don't run it)
#       optimize # of dijkstra runs by taking the most occuring vertex in all the pairs and running dijkstra on that
#       then remove all of the pairs of that vertex from the frequency list and run dijkstra on the most frequent vertex again
#       Repeat until all vertices have a frequency of 0
# Calculate cost with just dijkstra runs
# Run modified A* from each vertex in the pair that does not have dijkstra run from it
# Repeat until no new paths are generated for every pair
# Return statistics on simulations (with matplotlib graphs)
#       Improvement of cost for every iteration over the minimum number (n pairs)
#       Histogram or something on possible percent improvement in travel time (need to relate traffic density to travel time)
#       Graph of average traffic density along the path and average length of the paths

# Proof of correctness / optimality of algorithm
# Runtime of algorithm
#      Expected number of iterations + worst case number of iterations

# ===============================
# KEYBINDS
# LEFT CLICK: places a new point
# r: removes the nearest point
# SPACE: manually updates the screen
# s: selects the nearest point
# ESC: clears the selected point
# e: adds an edge between the two selected points
# d: deletes the edge between the two selected points
# LEFT: Decrements the graph index and loads the new graph
# RIGHT: Increments the graph index and loads the new graph
# a: saves the graph manually
# f: finishes with graph editing
# ===============================

if __name__ == '__main__':

    # Titles the game
    pygame.display.set_caption('Traffic Distribution')
    clock = pygame.time.Clock()

    s = Simulation()
    s.loadGraphs()

    # TODO later change this to a number saved in the file
    graph_index = 0

    executing = True
    doneGraphEditing = False
    update = True
    # Starting the game loop
    while executing:
        print("Time between frames:", clock.tick(TPS), "ms")

        # Checking events
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                executing = False
            elif e.type == pygame.MOUSEBUTTONDOWN and not doneGraphEditing:
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
            elif e.type == pygame.MOUSEMOTION and not doneGraphEditing:
                update = s.getGraph(graph_index).movePoint(e.pos)
            elif e.type == pygame.MOUSEBUTTONUP and not doneGraphEditing:
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
                elif e.key == pygame.K_s and not doneGraphEditing:
                    s.getGraph(graph_index).selectPoint(pygame.mouse.get_pos())
                    update = True
                # Clear selected points
                elif e.key == pygame.K_ESCAPE and not doneGraphEditing:
                    s.getGraph(graph_index).clearSelectedPoints()
                    update = True
                # Adds an edge
                elif e.key == pygame.K_e and not doneGraphEditing:
                    s.getGraph(graph_index).addEdge()
                    update = True
                # Deletes the edge between the selected points
                elif e.key == pygame.K_d and not doneGraphEditing:
                    s.getGraph(graph_index).deleteEdge()
                    update = True
                elif e.key == pygame.K_LEFT and not doneGraphEditing:
                    graph_index -= 1
                    graph_index = max(0, graph_index)
                    s.saveGraphs()
                    update = True
                elif e.key == pygame.K_RIGHT and not doneGraphEditing:
                    graph_index += 1
                    s.saveGraphs()
                    update = True
                elif e.key == pygame.K_a:
                    s.saveGraphs()
                elif e.key == pygame.K_f:
                    s.getGraph(graph_index).clearSelectedPoints()
                    s.getGraph(graph_index).setMovingPoint(None)
                    doneGraphEditing = True
                    update = True
                    s.saveGraphs()

        s.tick()

        # Drawing to the screen
        if update:
            display.fill((14, 25, 36))

            s.getGraph(graph_index).updateEdges()
            s.getGraph(graph_index).updateTextBoxes()
            s.getGraph(graph_index).updatePoints()

            update = False

        # Updating the display
        pygame.display.update()
