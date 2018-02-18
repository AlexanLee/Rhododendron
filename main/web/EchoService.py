import pyrestful.rest
import tornado.ioloop

import random
# import m4_predict
from pyrestful import mediatypes
from pyrestful.rest import get, post


# p = m4_predict.OnlinePredictor()

class EchoService(pyrestful.rest.RestHandler):
    def data_received(self, chunk):
        pass

    # predictor()
    #    def __init__(self):
    #       self.p = OnlinePredictor()

    @post(_path="/hack", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def hack(self, num):
        print str(self) + "\t" + str(num)
        try:
            print 'start.'
            # global p
            # res = p.predict_one_sample(text.encode('utf-8'))
            # print res
            # print 'predict after'
            # if len(res) < 3:
            #     return {"list": [], "code": 1}
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
            # index=random.randint(0, 19)
            # index_1=random.randint(0,19)
            # index_2=random.randint(0,19)
            # index = res[0]
            # index_1 = res[1]
            # index_2 = res[2]
            # print 'in_0:' + str(index) + '  in_1:' + str(index_1) + "  in_2:" + str(index_2)
            # emoji_0 = emoji.emojize(emoji_list[index])
            # emoji=unicode(unquote(em), 'utf-8')
            # emoji_1=unicode(unquote(emoji_list[index_1]),'utf-8')
            # emoji_2=unicode(unquote(emoji_list[index_2]),'utf-8')

            # emoji_1 = emoji.emojize(emoji_list[index_1])
            # emoji_2 = emoji.emojize(emoji_list[index_2])
            # print emoji_0.encode('utf-8') + '\t' + emoji_1.encode('utf-8') + '\t' + emoji_2.encode(
            #     'utf-8')
            # return {"list": [1, 2, 3], "code": 200}

    @get(_path="/hello/{id}/{num}", _produces=mediatypes.APPLICATION_JSON)
    def sayHello(self, id, num):
        print(id + "\t" + num)
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
