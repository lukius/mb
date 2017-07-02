import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

import matplotlib as mpl
mpl.rcParams['text.usetex'] = True

from solver import SDESolver, EMSolver, MilsteinSolver


def plot_sample_path(params):
    fig = plt.figure(figsize=(9,5))
    ax = fig.add_subplot(111)
    
    r = params['r']
    K = params['K']
    beta = params['beta']
    X0 = params['X0']
    T = params['T']
    h = params['h'] 
    
    times, X = SDESolver.solve_all(r, K, beta, X0, T, h)

    for solver, points in X.items():
        ax.plot(times, points, label=solver)
        
    ax.set_xlabel('$t$')
    ax.set_ylabel('$X(t)$')

    configure(ax)
    
    return ax

def plot_average(params):
    fig = plt.figure(figsize=(9,5))
    ax = fig.add_subplot(111)
    
    r = params['r']
    K = params['K']
    beta = params['beta']
    X0 = params['X0']
    T = params['T']
    h = params['h']
    M = params['M']
    
    X_avg = dict()
    colors = ['blue', 'green', 'red']
    solver_colors = dict()
    err_em = err_milstein = 0.

    for i in xrange(int(M)):
        times, X = SDESolver.solve_all(r, K, beta, X0, T, h)
        for solver, points in X.items():
            if i > 0:
                X_avg[solver] += points
            else:
                X_avg[solver] = points
                
        err_milstein += np.abs(X['Milstein'][-1] - X['Solucion'][-1])
        err_em += np.abs(X['Euler-Maruyama'][-1] - X['Solucion'][-1])

    for solver, points in X.items():
        solver_colors[solver] = colors.pop(0)
        ax.plot(times, points, label=solver, color=solver_colors[solver], alpha=0.3)

    avg_label = True
    for solver, points in X_avg.items():
        if avg_label:
            ax.plot(times, points/M, label='Media', linestyle='--', color=solver_colors[solver])
            avg_label = False
        else:
            ax.plot(times, points/M, linestyle='--', color=solver_colors[solver])
        
    ax.set_xlabel('$t$')
    ax.set_ylabel('$X(t)$')

    configure(ax)
    
    return ax, {'err_em' : err_em/M, 'err_milstein' : err_milstein/M }

def plot_errors(params):
    fig = plt.figure(figsize=(9,5))
    ax = fig.add_subplot(111)
    
    r = params['r']
    K = params['K']
    beta = params['beta']
    X0 = params['X0']
    T = params['T']
    M = params['M']
    
    hs = [0.025, 0.05, 0.075, 0.1, 0.15, 0.2]
    errs_em = list()
    errs_milstein = list()

    for h in hs:
        err_em = err_milstein = 0.
        
        for i in xrange(int(M)):
            times, X = SDESolver.solve_all(r, K, beta, X0, T, h)
        
            err_milstein += np.abs(X['Milstein'][-1] - X['Solucion'][-1])
            err_em += np.abs(X['Euler-Maruyama'][-1] - X['Solucion'][-1])
            
        errs_em.append(err_em/M)
        errs_milstein.append(err_milstein/M)

    ax.plot(hs, errs_em, label='Euler-Maruyama', marker='x')
    ax.plot(hs, errs_milstein, label='Milstein', marker='x')
    
    #ax.plot(hs, np.sqrt(hs))

    ax.set_xlabel('$h$')
    ax.set_ylabel('$|X^h(T) -X(T)|$')

    ax.set_xlim([hs[0], hs[-1]])
    
    plt.locator_params(axis='x', nticks=len(hs))

    configure(ax)
    
    return ax

def configure(ax):
    ax.grid(True)
    ax.legend(fontsize='medium')