import json

import matplotlib
matplotlib.use('Agg')

import cStringIO, base64
import matplotlib, datetime
import matplotlib.pyplot as plt

from django.shortcuts import render
from django.template import Context, loader
from django.http import HttpResponse

from plotting import plot_sample_path, plot_average, plot_errors


def _get_params(request):
    params = dict()
    for param in ['r', 'K', 'beta', 'X0', 'T', 'h', 'M']:
        value = request.GET.get(param, 1)
        params[param] = float(value)
    return params

def index(request):
    template = loader.get_template("index.html")
    c = Context({})
    return HttpResponse(template.render(c))

def sample_path(request):
    params = _get_params(request)
    
    ax = plot_sample_path(params)

    output = cStringIO.StringIO()
    plt.savefig(output, bbox_inches='tight')
    img_txt = base64.b64encode(output.getvalue())

    response = { 'image': img_txt }
    
    return HttpResponse(json.dumps(response), content_type='application/json')

def average(request):
    params = _get_params(request)
    
    try:
        ax, errs = plot_average(params)
    except Exception, e:
        print str(e)

    output = cStringIO.StringIO()
    plt.savefig(output, bbox_inches='tight')
    img_txt = base64.b64encode(output.getvalue())

    response = { 'image': img_txt }
    response.update(errs)
    
    return HttpResponse(json.dumps(response), content_type='application/json')

def error(request):
    params = _get_params(request)
    
    try:
        ax = plot_errors(params)
    except Exception, e:
        print str(e)

    output = cStringIO.StringIO()
    plt.savefig(output, bbox_inches='tight')
    img_txt = base64.b64encode(output.getvalue())

    response = { 'image': img_txt }
    
    return HttpResponse(json.dumps(response), content_type='application/json')
