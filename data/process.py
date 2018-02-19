import sys
from itertools import groupby
from operator import itemgetter

from tool.config import Config

sys.path.append("..")

from data import utils


class process(object):
    def __init__(self, config):
        self.config = config

    def clean(self):
        source_log = open(self.config['source.log.file'])
        log_f = file(self.config['process.log.file'], 'w')
        for line in source_log:
            try:
                fields = utils.get_line_fields(line)
                action = fields.get("action", 0)
                isbn = fields.get("isbn", None)
                title = fields.get("title", None)
                classify = fields.get("classify", None)
                unionId = fields.get("unionId", None)
                gender = fields.get("gender", None)
                location = fields.get("location", None)
                print>> log_f, isbn + '\t' + unionId + '\t' + title + '\t' + classify + '\t' + location \
                               + '\t' + gender + '\t' + action
            except:
                print("error:" + str(line))

    @staticmethod
    def read_mapper_output(file, separator='\t'):
        for line in file:
            l = line.rstrip().split(separator)
            if len(l) > 5:
                user = l[0]
                item = l[1]
                weight = l[6]
                yield (user + "|" + item, weight)

    def reduce(self):
        rate_f = file(self.config['ratings'], 'w')
        data = self.read_mapper_output(open(self.config['process.log.file']))
        for user, group in groupby(data, itemgetter(0)):
            total_count = sum(int(count) for item, count in group)
            # print("%s%s%d" % (user, '\t', total_count))
            u = user.split('|')
            print >> rate_f, u[1], u[0], total_count


if __name__ == '__main__':
    # clean()
    # reduce()
    config = Config('../config/UserKNN.conf')
    p = process(config)
    p.clean()
