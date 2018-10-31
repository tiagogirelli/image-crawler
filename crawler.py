#!/usr/local/bin/python3

import sys
import csv
import urllib.request
import os
import ssl
from termcolor import colored

def _print(str, error=False, ok=False, end='\n'):
    color = None
    if error:
        color = 'red'
    if ok:
        color = 'blue'
    print(colored(str, color=color), end=end)

def _read_file(filename):
    with open(os.path.join(os.getcwd(), filename)) as arq:
        lines = csv.DictReader(arq)
        for line in lines:
            _print('Download: {} > {}'.format(line['url'], line['nome']), end='')
            if not _download_img(line['url'], line['nome']):
                _print(' > Erro ao fazer download e salvar a imagem.', error=True)
            else:
                _print(' > ok', ok=True)

def _download_img(img_url, filename):
    try:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        image_on_web = urllib.request.urlopen(img_url, context=ssl_context)
        if image_on_web.headers.get('Content-Type') == 'image/jpeg':
            buf = image_on_web.read()
            downloaded_image = open(os.path.join(os.getcwd(), 'output', filename), "wb")
            downloaded_image.write(buf)
            downloaded_image.close()
            image_on_web.close()
        else:
            return False    
    except:
        return False
        #raise
    return True

def main():
    #print(sys.argv)
    _read_file(sys.argv[1])

if __name__=='__main__':
    main()
