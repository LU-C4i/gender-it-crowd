#!/usr/bin/env python2.7
# encoding: utf-8
'''Expose view(template_name) to render Jinja2 templates.

Works just like bottle templates:
    * Templates should be placed in '/views'.
    * dict() => rendered as HTML
    * other  => rendered as str

Usage:
    import template
    @app.route('/')
    @template.view('index.html')
    def index():
        return dict(msg='hello')
'''
import itertools
import functools
import jinja2

EXTENSIONS = ('.html', '.jinja')
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('./view'),
    undefined=jinja2.StrictUndefined,
    autoescape=True,
)
# Add any custom python functions required by templates here
env.globals.update(zip=itertools.izip)

def view(template_name):
    template_name = _default_extension(template_name)

    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(*args, **kwargs):
            response = view_func(*args, **kwargs)

            if isinstance(response, dict):
                template = env.get_template(template_name)
                return template.render(**response)
            else:
                return str(response)

        return wrapper

    return decorator

def _default_extension(fname):
    if any(fname.endswith(ext) for ext in EXTENSIONS):
        return fname
    return fname + '.jinja'
