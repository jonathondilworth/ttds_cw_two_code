import re

def flatten_white_space(input_string, expression=" +", replacement=" "):
    return re.sub(expression, replacement, input_string)

def parse_rel_result_str(string, delimiter=' ', empty_start=True):
    ''' string : input string'''
    ''' delimiter : seperates results'''
    '''empty_start : is first result empty?'''
    '''return : list of tuples STRINGS'''
    results = string.split(delimiter)
    return results[1:] if empty_start else results

def parse_tuple(string):
    doc_num, score = string.strip('()').split(',')
    return (int(doc_num), int(score))