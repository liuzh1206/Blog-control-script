#!/usr/bin/env python
import getopt
import http.server
import json
import os
import shutil
import sys
from functools import partial

import pypandoc
import webbrowser


class Process():
    def __init__(self, total=0, start_str='', end_str=''):
        self.total = total
        self.status = 0
        self.start_str = start_str
        self.end_str = end_str

        if self.end_str == '':
            self.end_str = str(self.total)

        self.start_str += ' '
        total_length = os.get_terminal_size().columns
        total_length -= len(self.start_str + self.end_str+'  ' +
                            ' {}|'.format(self.status/self.total*100))
        bar = ''.join(["\033[7m "] * int(self.status /
                                         self.total * total_length))
        bar = '\r' + self.start_str + bar + \
            '\033[0m {}|'.format(self.status) + self.end_str
        print(bar, end='', flush=True)

    def set_start_str(self, start_str):
        self.start_str = start_str + ' '

    def set_end_str(self, end_str):
        self.end_str = end_str

    def update(self, update):

        self.status += update
        total_length = os.get_terminal_size().columns
        total_length -= len(self.start_str + self.end_str+'  ' +
                            ' {}|'.format(self.status/self.total*100))
        bar = ''.join(["\033[7m "] * int(self.status /
                                         self.total * total_length))
        bar = '\r' + self.start_str + bar + \
            '\033[0m {}|'.format(self.status) + self.end_str
        print(bar, end='', flush=True)


class blog(object):

    THEME = 'panda'
    file_list = {}
    n = 0
    process_bar = None

    def __init__(self):
        pass

    def get_files(self, path):
        dirs = {}
        files = []
        for i in os.listdir(path):
            if os.path.isdir(os.path.join(path, i)):
                dirss, filess = self.get_files(os.path.join(path, i))
                if dirss == {}:
                    dirs[i] = [*filess]
                else:
                    dirs[i] = [*filess, dirss]
            else:
                if os.path.splitext(i)[1] == '.md':
                    self.n += 1
                files.append(i)
        return dirs, files

    def write_data(self):
        file_data = self.get_files('source')
        with open('./out/data.json', 'w') as data:
            data.write(json.dumps({'source': [file_data[0], *file_data[1]]}))

    def out(self):
        self.write_data()
        with open('./out/data.json') as datas:
            files = json.load(datas)
        self.process_bar = Process(self.n)
        self.compile_html('source', 'out', files['source'])

    def compile_html(self, mk_path, html_path, paths):
        if isinstance(paths, list):
            for i in paths:
                if isinstance(i, dict):
                    self.compile_html(mk_path, html_path, i)
                else:
                    if os.path.splitext(i)[1] == '.md':
                        self.process_bar.set_start_str(i)
                        if i == 'index.md':
                            self.markdown_convert_html(os.path.join(mk_path, i), os.path.join(
                                html_path, os.path.splitext(i)[0] + '.html'), os.path.splitext(i)[0], 'index')
                            if not os.path.exists(os.path.join(html_path, 'script')):
                                os.mkdir(os.path.join(html_path, 'script'))
                            if not os.path.exists(os.path.join(html_path, 'script', os.path.splitext(i)[0] + '.js')):
                                with open(os.path.join(html_path, 'script', os.path.splitext(i)[0] + '.js'), 'w') as js:
                                    js.write('')
                        else:
                            self.markdown_convert_html(os.path.join(mk_path, i), os.path.join(
                                html_path, os.path.splitext(i)[0] + '.html'), os.path.splitext(i)[0], os.path.splitext(i))
                            if not os.path.exists(os.path.join(html_path, 'script')):
                                os.mkdir(os.path.join(html_path, 'script'))
                            if not os.path.exists(os.path.join(html_path, 'script', os.path.splitext(i)[0] + '.js')):
                                with open(os.path.join(html_path, 'script', os.path.splitext(i)[0] + '.js'), 'w') as js:
                                    js.write('')
                        self.process_bar.update(1)
                    else:
                        shutil.copyfile(os.path.join(
                            'source', i), os.path.join('out', i))
        elif isinstance(paths, dict):
            for i in paths:
                if not os.path.exists(os.path.join(html_path, i)):
                    os.mkdir(os.path.join(html_path, i))
                for j in paths[i]:
                    if isinstance(j, dict):
                        self.compile_html(os.path.join(
                            mk_path, i), os.path.join(html_path, i), j)
                    else:
                        if os.path.splitext(j)[1] == '.md':
                            self.process_bar.set_start_str(j)
                            self.markdown_convert_html(os.path.join(mk_path, i, j), os.path.join(
                                html_path, i, os.path.splitext(j)[0] + '.html'), os.path.splitext(j)[0], os.path.splitext(j)[0])
                            if not os.path.exists(os.path.join(html_path, i, 'script')):
                                os.mkdir(os.path.join(html_path, i, 'script'))
                            if not os.path.exists(os.path.join(html_path, i, 'script', os.path.splitext(j)[0] + '.js')):
                                with open(os.path.join(html_path, i, 'script', os.path.splitext(j)[0] + '.js'), 'w') as js:
                                    js.write('')
                            self.process_bar.update(1)
                        else:
                            shutil.copyfile(os.path.join(
                                mk_path, i, j), os.path.join(html_path, i, j))
            pass

    def markdown_convert_html(self, input_file, out_file, title, *args):
        header_includes = \
            '''
            <script src='/static/lib/mermaid.min.js'></script>
            <script src='/static/lib/chart.js'></script>
            <script src="/static/lib/highlight.min.js"></script>
            <link href="/static/lib/atelier-lakeside-dark.min.css" rel="stylesheet"/>
            <script src="/static/lib/highlightjs-line-numbers.min.js"></script>
            <!--<script src="https://twemoji.maxcdn.com/v/13.0.1/twemoji.min.js" integrity="sha384-5f4X0lBluNY/Ib4VhGx0Pf6iDCF99VGXJIyYy7dDLY5QlEd7Ap0hICSSZA1XYbc4" crossorigin="anonymous"></script>-->
            <script>mermaid.initialize({startOnLoad:true});</script>
            <script>hljs.initHighlightingOnLoad();</script>
            <script>hljs.initLineNumbersOnLoad();</script>
            <script src="//unpkg.com/valine/dist/Valine.min.js"></script>
            '''
        include_after = \
            '''
            <!--<script>twemoji.parse(document.body);</script>-->
            <div id="vcomments"></div>
            <script src='/static/markdown.js'></script>
            '''
        if args:
            include_after += f'''
            <script src='./script/{args[0]}.js'></script>
            '''
        pdoc_args = [
            '-c',
            f'/static/css/{self.THEME}/{self.THEME}.css',
            '--mathjax=https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js',
            '-s',
            '--highlight-style=breezedark',
            '--variable',
            f'header-includes={header_includes}',
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
        webbrowser.open_new_tab(f'0.0.0.0:{PORT}')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\npreview has stoped")


if __name__ == "__main__":
    # file_convert('source/first/test.md', 'out/first/test_py.html', 'test_py')

    myblog = blog()
    opts = []
    args = []
    help_str = '''  -h --help print this page
  -o --out convert markdown to html
  -p --preview start a http server to preview html
            '''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'oph', [
                                   'out', 'preview', 'help'])
    except getopt.GetoptError as err:
        print(help_str+str(err))
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(help_str)
            sys.exit()
            pass
        elif opt in ('-o', '--out'):
            myblog.out()
            pass
        elif opt in ('-p', '--preview'):
            myblog.start_preview()
            pass
        else:
            print(help_str)
            pass
        pass
