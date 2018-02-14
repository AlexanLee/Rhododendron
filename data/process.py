import sys

sys.path.append("..")

from data import utils

if __name__ == '__main__':
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
            print>> log_f, isbn + '\t' + unionId + '\t' + title + '\t' + classify + '\t' + location\
                           + '\t' + gender + '\t' + action
        except:
            print("error:" + str(line))
