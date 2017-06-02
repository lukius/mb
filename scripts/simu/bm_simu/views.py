import json

import matplotlib
matplotlib.use('Agg')

import cStringIO, base64
import matplotlib, datetime
import matplotlib.pyplot as plt

from scipy.stats import arcsine

from django.shortcuts import render
from django.template import Context, loader
from django.http import HttpResponse

from plotting import plot_bm_with_last_zero_lt


def index(request):
    template = loader.get_template("index.html")
    c = Context({})
    return HttpResponse(template.render(c))

def plot(request):
    x = float(request.POST['x'])
    
    if  ('clear' in request.POST) or\
        ('x' not in request.session) or\
        x != request.session['x']:
        request.session['x'] = x
        request.session['n_x'] = 0
        request.session['d_x'] = 1
        
    ax, n = plot_bm_with_last_zero_lt(x)
    
    request.session['n_x'] += 1 
    request.session['d_x'] += n 

    output = cStringIO.StringIO()
    plt.savefig(output, bbox_inches='tight')
    img_txt = base64.b64encode(output.getvalue())

    prob_x = arcsine.cdf(x)
    n_x = request.session['n_x']
    d_x = request.session['d_x']

    response = {'image': img_txt, 
                'prob': '%.4f' % prob_x,
                'frq': '%.4f' % (float(n_x)/d_x),
                'n_x': n_x,
                'd_x': d_x}
    
    return HttpResponse(json.dumps(response), content_type='application/json')
