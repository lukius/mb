import math
import numpy as np

from bm import LinearBrownianMotion


class SDESolver(object):
    
    DEFAULT_H = 0.1 
    
    @classmethod
    def from_values(cls, solver_name, r, K, beta, X0):
        return EMSolver(r, K, beta, X0)
    
    @classmethod
    def solve_all(cls, r, K, beta, X0, T, h=None):
        h = h or cls.DEFAULT_H
        N = math.ceil(T/h)
        times = np.linspace(0, T, N)
        B = LinearBrownianMotion.from_times(times)
        
        sol = SDEAnalyticSolution(r, K, beta, X0)
        em = EMSolver(r, K, beta, X0)
        milstein = MilsteinSolver(r, K, beta, X0)
        
        sol_X = sol._solve(times, B)
        em_X = em._solve(times, B)
        milstein_X = milstein._solve(times, B)
        
        X = {sol.name() : sol_X,
             em.name() : em_X,
             milstein.name() : milstein_X}
        
        return times, X
    
    def __init__(self, r, K, beta, X0):
        self.r = r
        self.K = K
        self.beta = beta
        self.X0 = X0
        
    def _drift(self, x):
        return self.r * x * (self.K - x)
    
    def _diffusion(self, x):
        return self.beta * x
    
    def _Xn(self, Xn1, tn1, tn, B):
        raise NotImplementedError
    
    def solve(self, T, h=None):
        h = h or cls.DEFAULT_H
        N = math.ceil(T/h)
        times = np.linspace(0, T, N)
        B = LinearBrownianMotion.from_times(times)
        return times, self._solve(times, B)
        
    def _solve(self, times, B):
        X = [self.X0]
        for n in xrange(1, len(times)):
            Xn1 = X[n-1]
            tn1, tn = times[n-1], times[n]
            Xn = self._Xn(Xn1, tn1, tn, B)
            X.append(Xn)
        return np.array(X)

        
class EMSolver(SDESolver):
    
    @classmethod
    def name(cls):
        return 'Euler-Maruyama'
    
    def _Xn(self, Xn1, tn1, tn, B):
        return  Xn1 +\
                self._drift(Xn1) * (tn - tn1) +\
                self._diffusion(Xn1) * (B(tn) - B(tn1))


class MilsteinSolver(SDESolver):
    
    @classmethod
    def name(cls):
        return 'Milstein'
    
    def _Xn(self, Xn1, tn1, tn, B):
        bXn1 = self._diffusion(Xn1)
        delta_B = B(tn) - B(tn1)
        delta_t = tn - tn1
        
        return  Xn1 +\
                self._drift(Xn1) * delta_t +\
                bXn1 * delta_B +\
                self.beta * 0.5 * bXn1 * (delta_B**2 - delta_t)
                
                
class SDEAnalyticSolution(SDESolver):
    
    DEFAULT_DT = 1e-3
    
    @classmethod
    def name(cls):
        return 'Solucion'
    
    def _integrate(self, t, B):
        dt = np.linspace(0, t, t/self.DEFAULT_DT)
        value = 0
        
        for i in xrange(1, len(dt)):
            s = dt[i]
            x = np.exp((self.r*self.K - 0.5*self.beta**2)*s + self.beta*B(s))
            value += x * (dt[i] - dt[i-1])
            
        return value
    
    def _solve(self, times, B):
        X = [self.X0]
        for t in times[1:]:
            integral = self._integrate(t, B)
            num = np.exp((self.r*self.K - 0.5*self.beta**2)*t + self.beta*B(t))
            den = (1/self.X0) + self.r*integral
            X.append(num/den)
        return np.array(X)
