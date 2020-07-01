import os
import re


def safe_open(filename, mode='r'):
    
    if 'w' in mode:
        dirname = os.path.dirname(filename)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)

    if filename.endswith('.gz'):
        import gzip
        return gzip.open(filename, mode=mode)

    return open(filename, mode=mode)


def parse_genelist(genelist):
    genedict = {}

    with safe_open(genelist) as f:
        for line in f:
            linelist = line.strip().split()
            gene = linelist[0]
            color = 'red'
            if len(linelist) == 2:
                color = linelist[1]
            genedict[gene] = color

    return genedict


def parse_conf(conf):
    with safe_open(conf) as f:
        for line in f:
            linelist = line.strip().split('\t')
            res = [each for each in re.split(r'[\s,\(\)]', linelist[0]) if each]
            shape = res[0]
            position = map(int, res[1:])

            url = linelist[1]
            title = linelist[2]
            yield shape, position, url, title


def get_gene_color(title, genedict, conflict_color='green'):
    color = None
    result = re.findall(r'([^\s]+) \((.+?)\)', title)
    if result:
        gene_in_title = [each for part in result for each in part]
        for gene in gene_in_title:
            if genedict.get(gene):
                if color and color != genedict[gene]:  # conflict color in a gene family
                    color = conflict_color
                else:
                    color = genedict[gene]
    return color