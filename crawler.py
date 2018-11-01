#!/usr/local/bin/python3

import sys
import csv
import urllib.request
import os
import ssl
from termcolor import colored
from argparse import ArgumentParser

class Crawler:
    _args = None

    def _parse_args(self):
        parser = ArgumentParser(
            description='Image Crawler - utilitário da FBITS para baixar arquivos em massa')

        parser.add_argument('-a', '--arquivo', dest='arquivo', action='store',
                            help='Informe o nome do arquivo CVS com separador ";" para o processamento do download das imagens.')

        parser.add_argument('-i', '--info', dest='info', action='store_true', default=True,
                            help='Imprime todas as informações de download no Console.')

        parser.add_argument('-d', '--diretorio', dest='diretorio', default='output', action='store',
                            help='Diretório para salvar as fotos que será feitas download.')

        parser.add_argument('-t', '--tamanho', dest='tamanho', default=-1, type=int, action='store',
                            help='Tamanho da lista. -1 (todo arquivo. nuúmero inteiro o tamanho de linhas a serem consumidas).')

        parser.add_argument('-f', '--apartir_de', dest='apartir_de', default=0, type=int, action='store',
                            help='A partir de determinada linha. Número diferente de zero.')

        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)

        self._args = parser.parse_args()

    def _print(self, str, error=False, ok=False, end='\n'):
        if not self._args.info:
            return

        color = None
        if error:
            color = 'red'
        if ok:
            color = 'blue'
        print(colored(str, color=color), end=end)

    def _get_file_extension(self, content_type):
        exts = {
            'image/jpeg': 'jpg',
            'image/gif': 'gif',
            'image/png': 'png',
            'image/jpg': 'jpg',
        }
        return exts[content_type]

    def _read_file(self):
        with open(self._args.arquivo) as arq:
            lines = list(csv.DictReader(arq))

            # Corta a lista a partir de um range
            if self._args.apartir_de > 0:
               lines = lines[self._args.apartir_de:] 

            # Corta a lista de acordo com um tamanho
            if self._args.tamanho > 0:
               lines = lines[:self._args.tamanho] 
 
            # Loop para processar os arquivos
            for line in lines:
                self._print('Download: {} > {}'.format(
                    line['url'], line['nome']), end='')
                if not self._download_img(line['url'], line['nome']):
                    self._print(
                        ' > Erro ao fazer download e salvar a imagem.', error=True)
                else:
                    self._print(' > ok', ok=True)

    def _check_or_create_output_dir(self):
        if not os.path.exists(self._args.diretorio):
            os.makedirs(self._args.diretorio)

    def _file_name_to_save(self, img_url, filename, extension):
        if filename == None:
            filename = img_url.split('/')[-1]

        return os.path.join(self._args.diretorio, '{}.{}'.format(filename, extension))

    def _download_img(self, img_url, filename):
        try:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            image_on_web = urllib.request.urlopen(img_url, context=ssl_context)
            ext = self._get_file_extension(
                image_on_web.headers.get('Content-Type'))
            if ext:
                buf = image_on_web.read()
                downloaded_image = open(
                    self._file_name_to_save(img_url, filename, ext), "wb")
                downloaded_image.write(buf)
                downloaded_image.close()
                image_on_web.close()
            else:
                return False
        except Exception as e:
            self._print(e, error=True)
            return False
        return True

    def main(self):
        self._parse_args()
        self._check_or_create_output_dir()
        self._read_file()

'''
    Main of Script
'''
if __name__ == '__main__':
    app = Crawler()
    app.main()
