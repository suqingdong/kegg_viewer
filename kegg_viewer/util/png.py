from PIL import Image, ImageColor, ImageDraw

from . import get_gene_color
from .logger import MyLogger


class PNG(object):
    
    def __init__(self, image_filename, conf_data, genedict, logger=None):
        self.image_filename = image_filename
        self.conf_data = conf_data
        self.genedict = genedict
        self.logger = logger or MyLogger(name='PNG')

    def build_png(self, outfile):

        im = Image.open(self.image_filename)

        for shape, position, _, title in self.conf_data:
            color = get_gene_color(title, self.genedict)
            if not color or shape != 'rect':
                continue
            X, Y, RX, RY = position

            try:
                color_rgba = ImageColor.getcolor(color, 'RGBA')
                for x in range(X, RX):
                    for y in range(Y, RY):
                        if im.getpixel((x, y))[0] > 0:  # pixel > 0 means this point is not black
                            ImageDraw.floodfill(im, xy=(x, y), value=color_rgba)
            except:
                self.logger.warn('this color is invalid: {}'.format(color))

        im.save(outfile)
