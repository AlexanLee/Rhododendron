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

    @get(_path="/hello/{is}/{id}/{num}", _produces=mediatypes.APPLICATION_JSON)
    def recommend(self, i, id, num):
        print(id + "\t" + num + "\t" + i)
        if num is None or num < 3:
            num = 3
        if int(i) == 1:
            conf = Config('../config/UserKNN.conf')
            sysRec = RecQ(conf)
            sysRec.execute()

        model_f = open('../results/UserKNN.txt')
        lr = []
        for line in model_f:
            l = line.split(' ')
            if str(l[0]) == str(id):
                lr.append(line)
                print("l:{}".format(l))
        l = []
        for r in lr:
            rs = str(r).split(' ')
            if len(l) < int(num):
                l.append(rs[1])
                print("r :{}".format(rs[1]))

        s = []
        with open("../dataset/stock.txt") as f:
            for ind, line in enumerate(f):
                if line.strip() <> '':
                    li = line.split("\t")
                    x = li[0]
                    if len(l) == 0:
                        s.append(str(x))
                    else:
                        for k in l:
                            if x <> k:
                                s.append(str(x))
        print(len(s))
        ret = random.sample(s, int(num) - len(l))
        for r in ret:
            l.append(r)
        return {"list": [l], "code": 200}


if __name__ == '__main__':
    try:
        print("Start the echo service")
        app = pyrestful.rest.RestService([EchoService])
        app.listen(8080)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\nStop the echo service")
