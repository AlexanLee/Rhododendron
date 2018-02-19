import os
from pymongo import MongoClient


def read_conf(config_file):
    if not os.path.isfile(config_file):
        msg = "ERROR: Config file '%s' doesn't exist" % config_file
        print msg
        return
    try:
        config = {}
        for l in file(config_file):
            sl = l.strip()
            if sl and not sl.startswith('#'):
                items = sl.split('=', 1)
                if len(items) >= 2:
                    config[items[0].strip()] = items[1].strip()
        if "rcv_source_num" in config:
            config["rcv_source_num"] = str(config["rcv_source_num"])
            # if 'postback_ip_whitelist' in config:
            # config['postback_ip_whitelist'] = load_whitelist_ip_file(config['postback_ip_whitelist'])
        if 'video_duration_time' not in config:
            config['video_duration_time'] = '300000'
        return config
    except:
        msg = "ERROR: Config file '%s' cann't parse" % config_file
        print msg
        return


def get_line_fields(line):
    return dict([x.split('=', 1) for x in line.split() if x.find('=') > 0])


def mongo(url, db):
    client = MongoClient(url, 27017)
    db = client[db]
    collection = db.postbookmodels
    return collection
