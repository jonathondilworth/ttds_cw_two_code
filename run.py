from code.mods import Evaluator
from code.mods import System
from code.evallib import precision_at_k
from code.evallib import recall_at_k
from code.evallib import r_precision
from code.evallib import average_precision

# loading evaluator

evalu = Evaluator("./systems/qrels.txt", quick=True)

def generate_row_heading():
    headers = ["", "P@10", "R@50", "r-Precision", "AP", "nDCG@10", "nDCG@20"]
    return (("\t").join(headers) + "\n")

def generate_results_for(system_number=1, query_number=1):
    s = System("./systems/S" + str(system_number) + ".results", lazy=True)
    res_set = s.result_set()
    rel_docs = evalu.get_rel_docs_for_query(query_number).all_doc_nums()
    ret_docs = res_set.ordered_doc_attrs_for_query_by_rank(query_number, attr='doc_num')
    prec_at_10 = ('{0:.2f}'.format(precision_at_k(rel_docs, ret_docs, 10)))
    rec_at_50 = ('{0:.2f}'.format(recall_at_k(rel_docs, ret_docs, 50)))
    r_prec = ('{0:.2f}'.format(r_precision(rel_docs, ret_docs)))
    ap = ('{0:.2f}'.format(average_precision(rel_docs, ret_docs)))
    # TODO: implement ndcg
    ndcg_10 = ('{0:.2f}'.format(float(0)))
    ndcg_20 = ('{0:.2f}'.format(float(0)))
    row = [query_number, prec_at_10, rec_at_50, r_prec, ap, ndcg_10, ndcg_20]
    return row

# I know it's messy, but I'm running out of time and I've got a headache
def generate_average_results_for(result_list, system_number=None):
    '''a result_list contains 10 lists of the following format:'''
    '''[q_num, prec_at_10, rec_at_50, r_prec, ap, ndcg_10, ndcg_20]'''
    prec_at_10_vals = []
    rec_at_50_vals = []
    r_prec_vals = []
    ap_vals = []
    ndcg_10_vals = []
    ndcg_20_vals = []
    for query_result_set in result_list:
        prec_at_10_vals.append(float(query_result_set[1]))
        rec_at_50_vals.append(float(query_result_set[2]))
        r_prec_vals.append(float(query_result_set[3]))
        ap_vals.append(float(query_result_set[4]))
        ndcg_10_vals.append(float(query_result_set[5]))
        ndcg_20_vals.append(float(query_result_set[6]))
    prec_avg = sum(prec_at_10_vals) / len(prec_at_10_vals)
    rec_avg = sum(rec_at_50_vals) / len(rec_at_50_vals)
    r_prec_avg = sum(r_prec_vals) / len(r_prec_vals)
    ap_avg = sum(ap_vals) / len(ap_vals)
    ndcg_10_avg = sum(ndcg_10_vals) / len(ndcg_10_vals)
    ndcg_20_avg = sum(ndcg_20_vals) / len(ndcg_20_vals)
    return_set = []
    if system_number is not None:
        return_set.append('S' + str(system_number))
    return_set.append('{0:.2f}'.format(prec_avg))
    return_set.append('{0:.2f}'.format(rec_avg))
    return_set.append('{0:.2f}'.format(r_prec_avg))
    return_set.append('{0:.2f}'.format(ap_avg))
    return_set.append('{0:.2f}'.format(ndcg_10_avg))
    return_set.append('{0:.2f}'.format(ndcg_20_avg))
    return return_set

def write_system_results_to_file(system_number, filepath, query_start=1, query_end=11):
    writable_result = ""
    writable_result += generate_row_heading()
    for query in range(query_start, query_end):
        writable_result += ("\t").join([str(x) for x in generate_results_for(system_number=system_number, query_number=query)])
        writable_result += ("\n")
    with open (filepath, "w") as eval_file:
        eval_file.write(writable_result)

def write_mean_results_to_file(filepath, system_start=1, system_end=7, query_start=1, query_end=11):
    system_avg_results = []
    for system in range(system_start, system_end):
        current_sys_results = []
        for query in range(query_start, query_end):
            current_sys_results.append(generate_results_for(system_number=system, query_number=query))
        system_avg_results.append(generate_average_results_for(current_sys_results, system_number=system))
    writable_result = ""
    writable_result += generate_row_heading()
    for avg_results in system_avg_results:
        writable_result += ("\t").join([str(x) for x in avg_results])
        writable_result += "\n"
    with open (filepath, "w") as all_file:
        all_file.write(writable_result)

write_system_results_to_file(system_number=1, filepath="./syseval/S1.eval")
write_system_results_to_file(system_number=2, filepath="./syseval/S2.eval")
write_system_results_to_file(system_number=3, filepath="./syseval/S3.eval")
write_system_results_to_file(system_number=4, filepath="./syseval/S4.eval")
write_system_results_to_file(system_number=5, filepath="./syseval/S5.eval")
write_system_results_to_file(system_number=6, filepath="./syseval/S6.eval")

write_mean_results_to_file("./syseval/ALL.eval")