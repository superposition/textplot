

import math
import matplotlib.pyplot as plt
import textplot.utils as utils
import numpy as np

from collections import OrderedDict


class Circle(object):


    def __init__(self, text, radius=100):

        """
        Store the text, initialize the circle.

        :param text: A text instance.
        """

        self.text = text
        self.radius = radius
        self.build_circle()


    def point_from_angle(self, angle):

        """
        Given an angle, return the X/Y point on the circle.

        :param angle: An angle, in radians.
        """

        x = self.radius * math.cos(angle)
        y = self.radius * math.sin(angle)

        return (x, y)


    def build_circle(self):

        """
        Set the initial term positions.
        """

        self.circle = OrderedDict()

        # Angle between each word.
        interval = float(360) / len(self.text.terms)

        # Iterate over terms in the text.
        for i, term in enumerate(self.text.get_shuffled_terms()):

            # Initialize the point.
            angle = math.radians(interval * i)
            self.circle[term] = self.point_from_angle(angle)


    def get_centroid(self, window):

        """
        Get the centroid of a window of words.

        :param window: The words in the window.
        """

        points = []

        # Get the locations of the words.
        for word in window:
            points.append(self.circle[word])

        return utils.centroid(points)


    def slide_window(self, window_width=100, squeeze_ratio=0.9):

        """
        Slide a rolling window across the text, squeezing the words in the
        window around the point on the circle nearest to the centroid.

        :param window_width: The number of words in the window.
        :param squeeze_ratio: The scaling factor. Eg, 0.6 squeezes 10 -> 6.
        """

        for window in self.text.slide_window(window_width):

            # Geometric centroid.
            centroid = np.array(self.get_centroid(window))

            # Normalize the centroid vector.
            normalized = centroid / np.linalg.norm(centroid)

            # Get the circle intersection.
            center = normalized * self.radius

            # TODO: Squeeze the window around the center
            for word in window: pass


    def plot(self):

        """
        Plot the circle.
        """

        # Zip the X/Y coordinates.
        coords = zip(*self.circle.values())

        # Plot the points.
        plt.scatter(coords[0], coords[1])

        # Label the words.
        for word, point in self.circle.items():
            plt.annotate(word, point)

        plt.show()
