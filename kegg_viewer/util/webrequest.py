import requests
from kegg_viewer.util import safe_open


class WebRequest(object):
    @classmethod
    def get_response(cls, url, method='GET', **kwargs):
        response = requests.request(method, url, **kwargs)
        return response

    @classmethod
    def save_file(cls, response, outfile, mode='wb', trunk_size=1024):
        with safe_open(outfile, mode) as out:
            for trunk in response.iter_content(trunk_size):
                out.write(trunk)


if __name__ == '__main__':
    
    url = 'http://rest.kegg.jp/get/ko00500/image'
    response = WebRequest.get_response(url, stream=True)
    WebRequest.save_file(response, 'ko00500.png')
    
    url = 'http://rest.kegg.jp/get/ko00500/conf'
    response = WebRequest.get_response(url, stream=True)
    WebRequest.save_file(response, 'ko00500.conf')
