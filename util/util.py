import re


def slice_filename(target_filename):
    pos_list = [pos.start() for pos in re.finditer('_', target_filename)]
    target_prefix = target_filename[:pos_list[0]+1]
    target_title = target_filename[pos_list[0]+1:pos_list[1]]
    target_suffix = target_filename[pos_list[1]:]

    return [target_prefix, target_title, target_suffix]

