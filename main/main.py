import sys

sys.path.append("..")
from RecQ import RecQ
from tool.config import Config

import pyrestful.rest
import tornado.ioloop

import random
from pyrestful import mediatypes
from pyrestful.rest import get, post


class EchoService(pyrestful.rest.RestHandler):
    def data_received(self, chunk):
        pass


    @post(_path="/hack", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def hack(self, num):
        print str(self) + "\t" + str(num)
        try:
            print 'start.'
            L = []
            for x in range(1, 10000):
                L.append(x)
            if num is None or num < 3:
                num = 3
            ret = random.sample(L, num)
            return {"list": [ret], "code": 200}
        except Exception, e:
            print 'except.' + str(e)
            ret = [random.randint(1, 10), random.randint(10, 20), random.randint(20, 30)]
            return {"list": [ret], "code": 200}

    @get(_path="/hello/{id}/{num}", _produces=mediatypes.APPLICATION_JSON)
    def sayHello(self, id, num):
        print(id + "\t" + num)
        conf=Config('../config/UserKNN.conf')
        sysRec=RecQ(conf)
        sysRec.execute()

        l = []
        for x in range(1, 1000):
            l.append(x)
        if num is None or num < 3:
            num = 3
        ret = random.sample(l, int(num))
        return {"list": [ret], "code": 200}

if __name__ == '__main__':
    try:
        print("Start the echo service")
        app = pyrestful.rest.RestService([EchoService])
        app.listen(8080)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\nStop the echo service")
