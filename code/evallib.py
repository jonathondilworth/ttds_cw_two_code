# TODO: tidy up comments & add author

from .mods import Document
from .mods import DocumentSet
from .mods import Result
from .mods import ResultSet

def precision(rel_docs, ret_docs):
    '''fraction of relevent documents that have been retrieved | this query'''
    numerator = len(rel_docs.intersection(ret_docs))
    denominator = len(ret_docs)
    return float(numerator) / float(denominator)


def recall(rel_docs, ret_docs):
    '''fraction of relevent documents retrived | set of all relevent documents '''
    numerator = len(rel_docs.intersection(ret_docs))
    denominator = len(rel_docs)
    return float(numerator) / float(denominator)

# TODO: Write Tests
def accuracy(true_positives, true_negatives, total_examples):
    '''not particularly used in IR, -> 99.99% in lots of instances'''
    numerator = true_positives + true_negatives
    return float(numerator) / float(total_examples)


def f1_score(rel_docs, ret_docs):
    '''f1 = (2 * p * r) / (p + r)'''
    numerator = 2 * precision(rel_docs, ret_docs) * recall(rel_docs, ret_docs)
    denominator = precision(rel_docs, ret_docs) + recall(rel_docs, ret_docs)
    return float(numerator) / float(denominator)


def f_measure(rel_docs, ret_docs, hyper_beta=1):
    '''fb = ((b^2 + 1) * p) * r / ((b^2) * p) + r'''
    numerator_scalar = (hyper_beta ** 2) + 1
    denominator_scalar = hyper_beta ** 2
    numerator = numerator_scalar * precision(rel_docs, ret_docs) * recall(rel_docs, ret_docs)
    denominator = (denominator_scalar * precision(rel_docs, ret_docs)) + recall(rel_docs, ret_docs)
    return float(numerator) / float(denominator)


def precision_at_k(rel_docs, ret_docs, k=5):
    '''ret_docs list is assumed to be ordered (ranked, most => least)'''
    '''its possible that k > len(ret_docs) => always divide by k (precision)'''
    # I don't think we should be truncating the relevent documents.. - TODO: check this
    # in this SPECIAL INSTANCE, casting will be included in the function
    rel_docs = set(rel_docs)
    # truncated_rel_docs = set(rel_docs[0:k])
    truncated_rel_docs = rel_docs
    truncated_ret_docs = set(ret_docs[0:k])
    precision_at_k_numerator = len(truncated_rel_docs.intersection(truncated_ret_docs))
    precision_at_k_denominator = k
    return float(precision_at_k_numerator) / float(precision_at_k_denominator)


# TODO: implement a unit test for this
def recall_at_k(rel_docs, ret_docs, k=50):
    '''recall @ some value will simply calculate the recall at some point k in'''
    '''the ranked list of retrieved documents'''
    rel_docs = set(rel_docs)
    truncated_ret_docs = set(ret_docs[0:k])
    return recall(rel_docs, truncated_ret_docs)


def r_precision(rel_docs, ret_docs, r=None):
    '''assumes that the length of the set of relevent documents is known: r'''
    '''taking the precision at this length is an accurate measure of real precision'''
    '''problem: how is the system / annotator suppose to know what r is on every query?'''
    return precision_at_k(rel_docs, ret_docs, len(rel_docs) if r is None else r)


def average_precision(rel_docs, ret_docs, unknown_rel_docs=None):
    total_rel_docs = len(rel_docs)
    if unknown_rel_docs is not None:
        total_rel_docs = unknown_rel_docs
    total_found_rel_docs = 0
    total_precision_scores = []

    for idx, document in enumerate(ret_docs):
        current_document = idx + 1
        if document in rel_docs:
            total_found_rel_docs += 1
            total_precision_scores.append(float(total_found_rel_docs) / float(current_document))

    total_precision = sum(total_precision_scores)
    average_precision = float(total_precision) / float(total_rel_docs)
    return average_precision


def mean_average_precision(queries):
    average_precision_values = []
    for q in queries:
        computed_value = average_precision(q.rel_docs, q.ret_docs, q.total_rel_docs)
        average_precision_values.append(computed_value)
    total_avg_precision = sum(average_precision_values)
    mean_average_precision = float(total_avg_precision) / float(len(average_precision_values))
    return mean_average_precision


# TODO: implement
# Note: due to time constraints, tests could not be implemented for these functions
# Note2: due to time constraints, could not finish implementing dg / ndcg / indcg
def discounted_gain(rel_docs, ret_docs, k=2):
    '''rel_docs '''
    rel_docs_ordered_by_score = rel_docs.all_docs_ordered_by_score()
    rel_1 = rel_docs_ordered_by_score[0].score
    total_score = float(rel_1)
    # ret_docs.ordered_doc_attrs_for_query_by_rank()
    for doc_idx in range(1, (k + 1)):
        total_score += (float((''' DOC SCORE FOR CURRENT DOCUMENT ''')) / float(log(doc_idx, 2)))
    return total_score

# TODO: implement
# Note: due to time constraints, tests could not be implemented for these functions
def norm_discounted_cumulative_gain():
    pass

# Note: due to time constraints, tests could not be implemented for these functions
def ndcg_at_k(rel_docs, ret_docs, k):
    '''rel_docs should be a DocumentSet'''
    '''ret_docs should be a ResultSet'''
    pass