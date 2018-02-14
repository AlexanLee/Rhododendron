import sys

sys.path.append("..")

import utils
import logging

if __name__ == '__main__':
    logging.getLogger().info('pull mongo data')
    stock_f = file('../dataset/stock.txt', 'w')
    collection = utils.mongo("localhost", "yuelin-used-book")
    print(collection.find().count())
    # print(collection.find_one())
    # print(collection.find_one()['_id'])
    # print(collection.find_one()['isbn13'])
    for x in collection.find():
        # print(str(x['_id']) + "\t" + str(x['isbn13']) + "\t" + str(
        #         x['location'].encode('utf-8')) + "\t" + str(x['title'].encode('utf-8')) + "\t" +
        #       str((x['classify'])['title'].encode('utf-8')) +
        #       "\t" + str(x['price']))
        try:
            print >> stock_f, str(x['_id']) + "\t" + str(x['isbn13']) + "\t" + str(
                    x['location'].encode('utf-8')) + "\t" + str(
                    x['title'].encode('utf-8')) + "\t" + str(
                    (x['classify'])['title'].encode('utf-8')) + "\t" + str(x['price'])
        except:
            print("error :" + str(x))
