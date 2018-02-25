# _*_ coding:utf-8 _*_
import sys

reload(sys)
sys.setdefaultencoding("latin-1")
sys.path.append("..")
from RecQ import RecQ
from tool.config import Config

import pyrestful.rest
import tornado.ioloop

import random
from pyrestful import mediatypes
from pyrestful.rest import get, post
import urllib


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

    @get(_path="/recommend/{is}/{id}/{location}/{num}", _produces=mediatypes.APPLICATION_JSON)
    def recommend(self, i, id, location, num):
        print(id + "\t" + num + "\t" + i + '\t' + urllib.unquote(location).decode('utf-8'))
        location = urllib.unquote(location).decode('utf-8')
        conf = Config('../config/UserKNN.conf')
        if num is None or num < 3:
            num = 3
        if int(i) == 1:
            sysRec = RecQ(conf)
            sysRec.execute()

        model_f = open(conf['model.file'])
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
        lt = []
        with open(conf['stock.file']) as f:
            for ind, line in enumerate(f):
                if line.strip() <> '':
                    li = line.split("\t")
                    x = li[0]
                    e = li[1]
                    loc = li[2]
                    if len(l) == 0:
                        s.append(str(x))
                    else:
                        b_append = False
                        for k in l:
                            if e == k:
                                lt.append(str(x))
                            elif location == loc.decode('utf-8'):
                                b_append = True
                        if b_append:
                            s.append(str(x))
        le = len(s)
        print(le)
        if le > (int(num) - len(l)):
            ret = random.sample(s, int(num) - len(l))
            for r in ret:
                lt.append(r)
        else:
            for r in s:
                lt.append(r)
        return {"list": [lt], "code": 200}


if __name__ == '__main__':
    try:
        print("Start the echo service")
        app = pyrestful.rest.RestService([EchoService])
        app.listen(8888)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\nStop the echo service")
