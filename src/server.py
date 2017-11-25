from http.server import BaseHTTPRequestHandler, HTTPServer
#import SocketServer
import simplejson
import requests
from image_emotion_gender_demo import make_label

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>hi!</h1></body></html>")

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        self._set_headers()
        print ("in post method")
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

        self.send_response(200)
        self.end_headers()

        data_get = simplejson.loads(self.data_string)

        path = data_get['image_path']
        id_ = data_get['request_id']

        label = make_label(path)
        json_dict = dict()
        json_dict.update({'self_confidence': label, 'request_id': id_})
        
        # requests.post('35.196.246.109:5000/confresult', json=json_dict)
        requests.post('http://localhost:8000', json=bytes(json_dict))
        #self.wfile.write(bytes("<html><body><h1>{}</h1></body></html>".format(json_dict['self_confidence'])))

        # with open("test123456.json", "w") as outfile:
        #     simplejson.dump(data, outfile)
        # print "{}".format(data)
        # f = open("for_presen.py")
        # self.wfile.write(f.read())
        # return
        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()