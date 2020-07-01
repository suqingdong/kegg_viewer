"""
    KEGG API
"""
import os

from .webrequest import WebRequest
from .logger import MyLogger


class KEGGRest(object):
    KEGG_BASE_URL = 'https://www.kegg.jp'
    KEGG_API_URL = 'http://rest.kegg.jp'
    logger = MyLogger('KEGGRest')

    @classmethod
    def get(cls, entry, option='image'):
        url = '{api}/get/{entry}/{option}'.format(api=cls.KEGG_API_URL, **locals())
        return url
        
    @classmethod
    def list(cls):
        pass

    @classmethod
    def link(cls):
        pass
        
    @classmethod
    def show_pathway(cls, mapid, dataset=None, default=None):
        """
            special character replace
            <TAB>  =>  %09
            =      =>  %3d
            #      =>  %23
        """
        url = '{}/pathway/{}'.format(cls.KEGG_BASE_URL, mapid)

        if dataset:
            additions = []
            for item in dataset:
                if isinstance(item, str):
                    additions.append(item)
                elif len(item) == 2:
                    additions.append('{}%09{}'.format(*item))
                elif len(item) == 3:
                    additions.append('{}%09{},{}'.format(*item))
            url += '/' + '/'.join(additions)


        if default:
            url += '/default%3d' + default

        url = url.replace('#', '%23')

        return url

    @classmethod
    def check_path(cls, path, cache_dir):
        png = '{cache_dir}/{path}.png'.format(**locals())
        conf = '{cache_dir}/{path}.conf'.format(**locals())
        for filename, option in zip([png, conf], ['image', 'conf']):
            if not os.path.isfile(filename):
                cls.logger.debug('downloading file: {} ...'.format(filename))
                url = cls.get(path, option=option)
                resp = WebRequest.get_response(url, stream=True)

                if resp.status_code != 200:
                    return None, None

                WebRequest.save_file(resp, filename)

        return png, conf


if __name__ == '__main__':

    print KEGGRest.get('ko00500')
    print KEGGRest.get('ko00500', option='conf')

    dataset = [
        'E2.4.1.13',
        'K00696',
        ('K02810', 'blue'),
        ('K01193', '', '#FFEECC'),
        ('K02810', 'yellow', 'pink'),
    ]

    print KEGGRest.show_pathway('ko00500')
    print KEGGRest.show_pathway('ko00500', dataset)
    print KEGGRest.show_pathway('ko00500', dataset, default='pink')
