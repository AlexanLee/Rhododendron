import sys
from itertools import groupby
from operator import itemgetter

sys.path.append("..")

from data import utils


def clean():
    source_log = file("/data/yuelin/xx.log")
    log_f = file('../dataset/log.txt', 'w')
    for line in source_log:
        try:
            fields = utils.get_line_fields(line)
            action = fields.get("action", 0)
            # if 1 == int(fields.get("action", 1)):
            #     print("weight:1")
            isbn = fields.get("isbn", None)
            title = fields.get("title", None)
            # print(fields.get("tags", None))
            classify = fields.get("classify", None)
            unionId = fields.get("unionId", None)
            # print(fields.get("openId", None))
            gender = fields.get("gender", None)
            location = fields.get("location", None)
            # print(fields.get("createdAt", None))
            # print("====" * 10)
            print>> log_f, isbn + '\t' + unionId + '\t' + title + '\t' + classify + '\t' + location \
                           + '\t' + gender + '\t' + action
        except:
            print("error:" + str(line))


def calc():
    stock_f = open("../dataset/stock.txt")
    with open("../dataset/log.txt") as f:
        for ind, line in enumerate(f):
            if line.strip() <> '':
                li = line.split("\t")
                x = li[0]
                print("log line:" + x)
                for sline in stock_f:
                    if sline <> '':
                        sli = sline.split("\t")
                        print("stock line:" + sli[1])
                        if x == sli[1]:
                            print("===========" + x)
    return


def read_mapper_output(file, separator='\t'):
    for line in file:
        l = line.rstrip().split(separator)
        if len(l) > 5:
            user = l[0]
            item = l[1]
            weight = l[6]
            yield (user + "|" + item, weight)


def reduce():
    rate_f = file('../dataset/ratings.txt', 'w')
    data = read_mapper_output(open('../dataset/log.txt'))
    for user, group in groupby(data, itemgetter(0)):
        total_count = sum(int(count) for item, count in group)
        print("%s%s%d" % (user, '\t', total_count))
        u = user.split('|')
        print >> rate_f, u[1], u[0], total_count


if __name__ == '__main__':
    # clean()
    reduce()
