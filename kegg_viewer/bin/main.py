#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
import sys
import time
import json
import argparse


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, ROOT_DIR)

from kegg_viewer.util.keggrest import KEGGRest
from kegg_viewer.util.webrequest import WebRequest
from kegg_viewer.util.svg import SVG
from kegg_viewer.util.png import PNG
from kegg_viewer.util.logger import MyLogger
from kegg_viewer.util import parse_genelist, parse_conf


__author__ = 'suqingdong'
__author_email__ = 'suqingdong@novogene.com'


__doc__ = '\033[1;36m{}\033[0m'.format(open(os.path.join(ROOT_DIR, 'banner.txt')).read())


__epilog__ = '''
\033[32mexamples:
    %(prog)s -h
    %(prog)s -p ko00196
    %(prog)s -p ko00196,ko00197
    %(prog)s -p path.list
    %(prog)s -p path.list -g gene.list -c ./cache -O output
    %(prog)s -p path.list -g gene.list -m online
    %(prog)s -p path.list -g gene.list -t png
    %(prog)s -p path.list -g gene.list -t both
\033[0m\033[33m
contact: {__author__} <{__author_email__}>\033[0m
'''.format(**locals())


def get_args():

    parser = argparse.ArgumentParser(prog='kegg_viewer',
                                     description= __doc__,
                                     epilog= __epilog__,
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-p', '--path', help='the input pathway(s)')
    parser.add_argument('-g', '--genelist',
                        help='the genelist to highlight, format like: gene[<tab>bgcolor[<tab>fgcolor]]')

    parser.add_argument('-O', '--outdir', help='the output directory [%(default)s]', default='.')

    parser.add_argument('-c', '--cache',
                        help='the cache directory to store png/conf files [%(default)s]',
                        default=os.path.join(ROOT_DIR, 'cache'))

    parser.add_argument('-t', '--type',
                        help='the type of output file [%(default)s]',
                        choices=['svg', 'png', 'both'],
                        default='svg')

    svg_parser = parser.add_argument_group(title='svg relative args', description=None)
    svg_parser.add_argument('-m', '--mode',
                            help='the mode of output svg [%(default)s]',
                            choices=['local', 'online', 'base64'],
                            default='base64')

    args = vars(parser.parse_args())

    if not args['path']:
        parser.print_help()
        exit()

    return args


def main():

    args = get_args()

    start_time = time.time()

    outdir = args['outdir']
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    logger = MyLogger(name='MAIN', verbose=True)
    logger.info('input arguments:\n\033[32m{}\033[0m'.format(json.dumps(args, indent=2)))
    KEGGRest.logger = logger

    if os.path.isfile(args['path']):
        path_list = open(args['path']).read().split()
    else:
        path_list = args['path'].split(',')

    genedict = {}
    if args['genelist'] and os.path.isfile(args['genelist']):
        logger.debug('parsing genelist file: {genelist}'.format(**args))
        genedict = parse_genelist(args['genelist'])

    for path in path_list:
        png_filename, conf_filename = KEGGRest.check_path(path, args['cache'])
        if not png_filename:
            logger.warn('this pathway is not exists, please check: {}'.format(path))
            continue

        conf_data = list(parse_conf(conf_filename))

        if args['type'] in ('svg', 'both'):
            logger.info('generating svg file for: {} ...'.format(path))
            outfile = '{}/{}.svg'.format(args['outdir'], path)
            svg = SVG(png_filename, conf_data, genedict=genedict, mode=args['mode'], logger=logger)
            svg.build_svg(outfile)
            logger.info('>>> save svg file: {}'.format(outfile))

        if args['type'] in ('png', 'both'):
            if not genedict:
                logger.warn('png mode needs a genelist to highlight!')
                continue
            logger.info('generating png file for: {} ...'.format(path))
            outfile = '{}/{}.png'.format(args['outdir'], path)
            png = PNG(png_filename, conf_data, genedict)
            png.build_png(outfile)
            logger.info('>>> save png file: {}'.format(outfile))

    logger.info('time used: {:.1f}s'.format(time.time() - start_time))


if __name__ == '__main__':
    main()

