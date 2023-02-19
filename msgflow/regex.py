import regex_spm


def match(*args, **argv):
    return regex_spm.match_in(*args, **argv)


def search(*args, **argv):
    return regex_spm.search_in(*args, **argv)
