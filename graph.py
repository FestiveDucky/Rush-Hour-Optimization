import pygame.sprite

from constants import *
from point import Point


class UndirectedGraph:
    def __init__(self):
        self.adjacency_list = {}
        self.points = []
        self.point_group = pygame.sprite.LayeredUpdates()
        # Point that is going to be moved by the user
        self.moving_point = None

        # Points for creating edges between points
        self.selected_point1 = None
        self.selected_point2 = None

    def addPoint(self, location):
        self.points.append(Point(location, self.point_group))
        self.adjacency_list[self.points[-1]] = set()

    def removePoint(self, location):
        if len(self.points) == 0:
            return

        # Search for nearest point to the location and delete it
        closest_point = self.points.pop(self.getNearestPointIndex(location))

        # Remove the edge from all locations in the adjacency list
        for other_point in self.adjacency_list[closest_point]:
            self.adjacency_list[other_point].remove(closest_point)

        self.adjacency_list.pop(closest_point)
        closest_point.kill()

        # Just in case this point is selected, to prevent errors:
        self.clearSelectedPoints()

    def movePoint(self, new_location):
        if self.moving_point is None:
            return False

        # Make sure that the movement is within the width of the screen
        # (Line thickness is to make points not phase through side of the screen)
        x = max(min(WIDTH - LINE_THICKNESS * 2, new_location[0]), LINE_THICKNESS * 2)
        y = max(min(HEIGHT - LINE_THICKNESS * 2, new_location[1]), LINE_THICKNESS * 2)

        self.moving_point.setCoords((x, y))
        return True

    def setMovingPoint(self, point):
        self.moving_point = point

    def getPointsClicked(self, location):
        return self.point_group.get_sprites_at(location)

    def addEdge(self):
        if self.selected_point2 is None or self.selected_point1 in self.adjacency_list[self.selected_point1]:
            return

        self.adjacency_list[self.selected_point1].add(self.selected_point2)
        self.adjacency_list[self.selected_point2].add(self.selected_point1)

    def deleteEdge(self):
        self.adjacency_list[self.selected_point1].remove(self.selected_point2)
        self.adjacency_list[self.selected_point2].remove(self.selected_point1)

    def updatePoints(self):
        self.point_group.update()

    def getNearestPointIndex(self, location):
        # Searches for the nearest point to the location
        closest_point = 0
        for i in range(1, len(self.points)):
            if dist(self.points[i].getCoords(), location) < dist(self.points[closest_point].getCoords(), location):
                closest_point = i
        return closest_point

    def selectPoint(self, location):
        if len(self.points) == 0:
            return

        p = self.points[self.getNearestPointIndex(location)]
        p.setColor(ORANGE)

        if self.selected_point1 is None:
            self.selected_point1 = p
        elif p != self.selected_point1:
            if self.selected_point2 not in [None, p]:
                self.selected_point2.setColor(WHITE)
            self.selected_point2 = p

    def clearSelectedPoints(self):
        if self.selected_point1 is not None:
            self.selected_point1.setColor(WHITE)
            self.selected_point1 = None

        if self.selected_point2 is not None:
            self.selected_point2.setColor(WHITE)
            self.selected_point2 = None

    def drawEdges(self):
        # Does double the computation since this is undirected graph but idc
        for p1 in self.adjacency_list:
            for p2 in self.adjacency_list[p1]:
                drawThickLine(BLUE, p1.getCoords(), p2.getCoords())
