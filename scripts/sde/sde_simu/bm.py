import numpy as np


class LinearBrownianMotion(object):

    @classmethod
    def random(cls, start, end, at=0, n_points=1000):
        times = np.linspace(start, end, n_points)
        return cls.from_times(times, at)
    
    @classmethod
    def from_times(cls, times, at=0):
        points = [at]
        zeros = list()
        times_to_points = {times[0] : at}
        for i, t in enumerate(times[1:], 1):
            prev_t = times[i-1]
            prev_point = points[i-1]
            step = np.random.normal(at, np.sqrt(t-prev_t), 1)[0]
            point = prev_point + step
            points.append(point)
            if prev_point * point <= 0:
                zeros.append(i)
            times_to_points[t] = point
        return cls(times, points, times_to_points, zeros)
    
    def __init__(self, times, points, times_to_points=None, zeros=None):
        self._times = times
        self.points = points
        self.zeros_indices = zeros
        self.times_to_points = times_to_points
        
    def _interpolate(self, t, i):
        t0 = self._times[i-1]
        t1 = self._times[i]
        x0 = self.points[i-1]
        x1 = self.points[i]     
        return (x0 * (t1-t) + x1 * (t-t0) ) / (t1 - t0)
    
    def times(self):
        return np.array(self._times)
        
    def last_zero(self):
        if self.zeros_indices is None:
            raise Exception('TODO')
        i = self.zeros_indices[-1]
        t0 = self._times[i-1]
        t1 = self._times[i]
        x0 = self.points[i-1]
        x1 = self.points[i]
        return (x1*t0 - x0*t1) / (x1 - x0)
    
    def _eval(self, t):
        if t < self._times[0] or t > self._times[-1]:
            raise Exception('t = %.5f not in domain!' % t)
        value = self.times_to_points.get(t, None)
        if value is None:
            for i, t0 in enumerate(self._times):
                if t0 > t:
                    break
            value = self._interpolate(t, i)
        return value
    
    def __call__(self, t):
        if isinstance(t, (int,float)):
            return self._eval(t)
        if isinstance(t, (list, np.ndarray)):
            return np.array([self._eval(t0) for t0 in t])
        