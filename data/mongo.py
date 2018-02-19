import sys

from tool.config import Config

sys.path.append("..")

import utils
import logging


class mongo(object):
    def __init__(self, config):
        self.config = config

    def pull(self):
        logging.getLogger().info('pull mongo data')
        stock_f = file(self.config['stock.file'], 'w')
        collection = utils.mongo(self.config['mongo.host'], self.config['mongo.db'])
        print(collection.find().count())
        for x in collection.find():
            try:
                print >> stock_f, str(x['_id']) + "\t" + str(x['isbn13']) + "\t" + str(
                        x['location'].encode('utf-8')) + "\t" + str(
                        x['title'].encode('utf-8')) + "\t" + str(
                        (x['classify'])['title'].encode('utf-8')) + "\t" + str(x['price'])
            except:
                print("error :" + str(x))


if __name__ == '__main__':
    config = Config('../config/UserKNN.conf')
    m=mongo(config)
    m.pull()
