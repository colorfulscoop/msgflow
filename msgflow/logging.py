import json
import datetime


def print_json_log(logger_, level_, message_):
    dict_ = {"level": level_, "message": message_, "time": str(datetime.datetime.now())}
    json_str = json.dumps(dict_)
    getattr(logger_, level_)(json_str)
