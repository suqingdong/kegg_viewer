import re
import os
import base64
from collections import defaultdict

import PIL.Image

from pysvg.structure import Svg, Image
from pysvg.shape import Rect, Circle
from pysvg.style import Style
from pysvg.linking import A
from pysvg.text import Text

from .keggrest import KEGGRest
from logger import MyLogger
from . import safe_open, get_gene_color


class SVG(object):
    
    def __init__(self, image_filename, conf_data, genedict=None, conflict_color='green', mode='base64', logger=None):
        self.image_filename = image_filename
        self.conf_data = conf_data
        self.conflict_color = conflict_color
        self.mode = mode
        self.genedict = genedict or {}
        self.logger = logger or MyLogger(name='SVG')

    def build_svg(self, outfile):

        # background image
        bg_image = PIL.Image.open(self.image_filename)
        width, height = bg_image.size

        # build a svg object, which size is the same as background
        svg = Svg(width=width, height=height)

        # add background image
        png_link = bg_image.filename
        if self.mode == 'online':
            path = os.path.basename(self.image_filename).split('.')[0]
            png_link = '{}/get/{}/image'.format(KEGGRest.KEGG_API_URL, path)
        elif self.mode == 'base64':
            with safe_open(self.image_filename, 'rb') as f:
                png_link = 'data:image/png;base64,' + base64.b64encode(f.read())

        im = Image(x=0, y=0, width=width, height=height)
        im.set_xlink_href(png_link)
        svg.addElement(im)

        for shape, position, url, title in self.conf_data:
            a = A(target='new_window')
            a.set_xlink_title(title)
            a.set_xlink_href(KEGGRest.KEGG_BASE_URL +url)

            # check gene, and add a highlighted rect or circle
            color = get_gene_color(title, self.genedict)
            child = self.add_child(shape, position, color)
            if child:
                a.addElement(child)
            
            svg.addElement(a)

        svg.save(outfile, encoding='UTF-8', standalone='no')

    def add_child(self, shape, position, color):

        if color:
            style = 'stroke: {0}; stroke-width: 1; fill:{0}; fill-opacity: 0.5'.format(color)
        else:
            style = 'fill-opacity: 0'

        if shape == 'rect':
            x, y, rx, ry = position
            w, h = rx - x, ry - y
            child = Rect(x=x, y=y, width=w, height=h)
        elif shape == 'circ':
            cx, cy, r = position
            child = Circle(cx=cx, cy=cy, r=r)
        else:
            self.logger.warn('unexpected shape: {}'.format(shape))
            return

        child.set_style(style)
        return child
