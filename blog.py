#!/usr/bin/env python
import getopt
import http.server
import json
import os
import shutil
import sys
from functools import partial

import pypandoc
from tqdm import tqdm


class blog(object):

    file_list = {}

    def __init__(self):
        if os.path.exists('./data.json'):
            with open('./data.json') as data:
                self.file_list = json.load(data)
            pass
        else:
            self.get_file_list()
            with open('./data.json', 'w+') as data:
                data.write(json.dumps(self.file_list))
            pass
        return

    def get_file_list(self):
        source = os.listdir('source')
        for i in source:
            self.file_list[i] = []
            if os.path.isdir(os.path.join('source', i)):
                files = os.listdir(os.path.join('source', i))
                for j in files:
                    if os.path.splitext(j)[1] == '.md':
                        self.file_list[i].append(os.path.splitext(j)[0])
        return self.file_list

    def out(self):
        totle_markdown_file_number = 0
        for i in self.file_list:
            totle_markdown_file_number += len(self.file_list[i])
        process_bar = tqdm(total=totle_markdown_file_number)
        for path in self.file_list:
            if os.path.exists(os.path.join('out', path)):
                if os.path.exists(os.path.join('out', path, 'picture')):
                    pass
                else:
                    os.mkdir(os.path.join('out', path, 'picture'))
                    pass
                pass
            else:
                os.mkdir(os.path.join('out', path))
                os.mkdir(os.path.join('out', path, 'picture'))
                pass
            for i in os.listdir(os.path.join('source', path, 'picture')):
                shutil.copyfile(os.path.join('source', path, 'picture', i),
                                os.path.join('out', path, 'picture', i))
            for files in self.file_list[path]:
                input_file = os.path.join('source', path, files) + '.md'
                out_file = os.path.join('out', path, files) + '.html'
                self.markdown_convert_html(input_file, out_file, files)
                process_bar.set_description(f'Converting file:{files}.md')
                process_bar.update(1)
                pass
        pass

    def markdown_convert_html(self, input_file, out_file, title):
        include_after = \
            '''
            <script src='https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js'></script>
            <script>mermaid.initialize({startOnLoad:true});</script>
            <script src='https://cdn.jsdelivr.net/npm/chart.js@2.8.0'></script>
            <script src='/script/mk.js'></script>
            '''
        pdoc_args = [
            '-c',
            '../css/markdown.css',
            '--mathjax=https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js',
            '-s',
            '--highlight-style=breezedark',
            '--variable',
            f'include-after={include_after}',
            '--metadata',
            f'title={title}']
        pypandoc.convert_file(input_file,
                              to='html',
                              outputfile=out_file,
                              format='gfm+tex_math_dollars',
                              extra_args=pdoc_args
                              )
        return

    def start_preview(self):
        PORT = 8000
        handler = partial(
            http.server.SimpleHTTPRequestHandler, directory='./out')
        httpd = http.server.HTTPServer(('', PORT), handler)
        print(f'server has start at 0.0.0.0:{PORT}')
        httpd.serve_forever()


if __name__ == "__main__":
    # file_convert('source/first/test.md', 'out/first/test_py.html', 'test_py')
    myblog = blog()
    opts, args = getopt.getopt(sys.argv[1:], 'oph', ['out', 'preview', 'help'])
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(
                '''-h --help print this page
-o --out convert markdown to html
-p --preview start a http server to preview html
                '''
            )
            sys.exit()
            pass
        elif opt in ('-o', '--out'):
            myblog.out()
            pass
        elif opt in ('-p', '--preview'):
            myblog.start_preview()
            pass
        else:
            print('''
                  -h --help print this page
                  -o --out convert markdown to html
                  -p --preview start a http server to preview html
                  ''')
            pass
        pass
