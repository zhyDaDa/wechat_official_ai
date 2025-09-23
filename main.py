import web
import os
from handle import Handle

class Index:
    def GET(self):
        html_path = os.path.join(os.path.dirname(__file__), 'html', 'index.html')
        with open(html_path, 'r', encoding='utf-8') as f:
            return f.read()

class Admin:
    def GET(self):
        html_path = os.path.join(os.path.dirname(__file__), 'html', 'admin.html')
        with open(html_path, 'r', encoding='utf-8') as f:
            return f.read()

urls = (
    '/', 'Index',
    '/admin', 'Admin',
    '/wx', 'Handle',
)

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()