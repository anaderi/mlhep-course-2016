import numpy
from sklearn.linear_model import LinearRegression

__author__ = 'mikhail91'


class SimpleTemplateMatching(object):
    def __init__(self, n_hits, window_width):
        """
        This class is a simple realization of a Template Matching paradigm for the straight tracks in 2D.

        :param n_hits: int, min number of hits to consider the track recognized.
        :param window_width: float, width of a searching window to consider the hists in the window to be belonged to the track.
        """

        self.window_width = window_width
        self.n_hits = n_hits
        self.labels_ = None
        self.tracks_params_ = None

    def fit(self, x, y):
        """
        Fit the method.

        :param x: numpy.ndarray shape=[n_hits, n_features], X of hits.
        :param y: numpy.array shape=[n_hits], y of hits.
        :return:
        """

        used = numpy.zeros(len(x))
        labels = -1. * numpy.ones(len(x))
        track_id = 0
        tracks_params = []

        for first_ind in range(len(x)):

            for second_ind in range(len(x)):

                x1 = x[first_ind]
                y1 = y[first_ind]

                x2 = x[second_ind]
                y2 = y[second_ind]

                if (x1 >= x2) or (used[first_ind] == 1) or (used[second_ind] == 1):
                    continue

                k = 1. * (y2 - y1) / (x2 - x1)
                b = y1 - k * x1

                y_upper = b + k * x.reshape(-1) + self.window_width
                y_lower = b + k * x.reshape(-1) - self.window_width

                track_mask = (y <= y_upper) & (y >= y_lower) & (used == 0)

                if track_mask.sum() >= self.n_hits:
                    used[track_mask] = 1
                    labels[track_mask] = track_id
                    track_id += 1

                    X_track = x[track_mask]
                    y_track = y[track_mask]

                    lr = LinearRegression()
                    lr.fit(X_track.reshape(-1, 1), y_track)

                    params = list(lr.coef_) + [lr.intercept_]
                    tracks_params.append(params)

        self.labels_ = labels
        self.tracks_params_ = numpy.array(tracks_params)