from collections import defaultdict
from .utillib import flatten_white_space
from .utillib import parse_rel_result_str

def parse_document(string):
    doc_num, score = string.strip('()').split(',')
    return Document(int(doc_num), int(score))

class Query():
    
    def __init__(self, rel_docs, ret_docs, total_rel_docs=None, score=None):
        self.rel_docs = rel_docs
        self.ret_docs = ret_docs
        if total_rel_docs is None:
            self.total_rel_docs = len(self.rel_docs)
        else:
            self.total_rel_docs = total_rel_docs
        self.score = score


class QuerySet():

    def __init__(self, queries):
        self.queries = queries


class Document():

    def __init__(self, doc_num, score):
        self.doc_num = doc_num
        self.score = score
        
    def __repr__(self):
        return "(" + str(self.doc_num) + "," + str(self.score) + ")"


class DocumentSet():

    def __init__(self, list_or_set_of_documents):
        self.docs = list_or_set_of_documents

    def all_doc_nums(self):
        doc_nums = []
        for document in self.docs:
            doc_nums.append(document.doc_num)
        return set(doc_nums)
    
    def all_docs(self):
        return self.docs
    
    def all_docs_ordered_by_score(self, rev=True):
        return sorted(self.docs, key=lambda document: document.score, reverse=rev)

    def all_docs_ordered_by_doc_num(self, rev=True):
        return sorted(self.docs, key=lambda document: document.doc_num, reverse=rev)

    def doc_score(self, doc_num):
        for document in self.docs:
            if int(document.doc_num) == int(doc_num):
                return int(document.score)
        return 0


class Result():

    def __init__(self, query_num, doc_num, rank, score):
        self.query_num = int(query_num)
        self.doc_num = int(doc_num)
        self.rank = int(rank)
        self.score = float(score)


class ResultSet():

    def __init__(self, results):
        self.results = results
        
    def results_for_query(self, query_num):
        result_set = []
        for current_result in self.results:
            if current_result.query_num == int(query_num):
                result_set.append(current_result)
        return result_set
    
    def get_doc_attributes_for_query(self, query_num, attribute='doc_num'):
        results = self.results_for_query(query_num)
        return_set = []
        for current_result in results:
            return_set.append(getattr(current_result, attribute))
        return return_set
    
    def ordered_doc_attrs_for_query_by_rank(self, query_num, attr='doc_num', rev=False):
        results = sorted(self.results_for_query(query_num), key=lambda result: result.rank, reverse=rev)
        return_set = []
        for current_result in results:
            return_set.append(getattr(current_result, attr))
        return return_set
    
    # note: sorted has some weird behaviour as lots of scores are the same.. watch out for this..
    def ordered_doc_attrs_for_query_by_score(self, query_num, attr='doc_num', rev=True):
        results = sorted(self.results_for_query(query_num), key=lambda result: result.score, reverse=rev)
        return_set = []
        for current_result in results:
            return_set.append(getattr(current_result, attr))
        return return_set


class System():
    
    def __init__(self, filepath, lazy=False):
        self.filepath = filepath
        self.raw_results = None
        self.results = None
        if lazy:
            self.loader()

    def read_raw_result_set(self):
        with open(self.filepath, "r") as results_file:
            data = results_file.readlines()
        self.raw_results = [x.strip('\n') for x in data]
    
    def raw_result_set(self):
        if self.raw_results is None:
            self.read_raw_result_set()    
        return self.raw_results
         
    def result_set(self):
        if self.results is not None:
            return self.results
        if self.raw_results is None:
            self.read_raw_result_set()
        new_result_set = []
        for current_result in self.raw_results:
            # current result attributes
            attrs = current_result.split(' ')
            # TODO: replace 0, 2, 3 and 4 with CONSTS
            new_result_set.append(Result(attrs[0], attrs[2], attrs[3], attrs[4]))
        self.results = ResultSet(new_result_set)
        return self.results

    def loader(self):
        self.result_set

    
class Evaluator():
    
    def __init__(self, filepath, quick=False):
        self.filepath = filepath
        self.raw_eval_file = None
        self.relevent_documents_for_q = None
        if quick:
            self.quick_parse()
        
    def read_eval_file(self):
        with open(self.filepath, "r") as evaluation_file:
            data = evaluation_file.readlines()
        self.raw_eval_file = [x.strip('\n') for x in data]
    
    def eval_file(self):
        if self.raw_eval_file is None:
            self.read_eval_file()
        return self.raw_eval_file
    
    def parse_queries_for_rel_docs(self):
        if self.raw_eval_file is None:
            self.read_eval_file()
        query_rel_docs = defaultdict(int)
        # TODO: replace ':' literal with CONST
        # we're breaking the evaluation file in a query # and their relevent results
        for query, results in [qrel.split(':') for qrel in self.raw_eval_file]:
            q_idx = int(query)
            q_rel = flatten_white_space(results)
            rel_docs = [parse_document(doc_tup) for doc_tup in parse_rel_result_str(q_rel)]
            query_rel_docs[q_idx] = DocumentSet(rel_docs)
        self.relevent_documents_for_q = query_rel_docs
    
    def quick_parse(self):
        self.parse_queries_for_rel_docs()

    def get_rel_docs_for_query(self, query_number):
        if self.relevent_documents_for_q is None:
            self.parse_queries_for_rel_docs()
        return self.relevent_documents_for_q[query_number]