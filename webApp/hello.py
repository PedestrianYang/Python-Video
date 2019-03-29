#coding:utf-8

def application(environ, start_response):
    start_response("200 OK", [("Content-Type", 'text/html')])
    body = '<h1>Hello,Python web! %s</h1>' % (environ['PATH_INFO'][1:] or 'web')
    print(environ)
    return [body.encode('utf-8')]
    # return [b'<h1>Hello,Python web!</h1>']