from evaluation.evaluation import evaluation


def BM_W(test_bugs): #todo
    #     bug report -> methods + refactoring + weight
    for issue in test_bugs:
        methods = {}
        for i in range(len(issue.artifacts)-1, -1, -1):
            method_set = set(m.name for m in issue.artifacts[i].methods if("nonMethodPart" not in m.name))
            method_weight = {}
            for m in issue.artifacts[i].methods:
                method_weight[m.name] = (m.addedLine+m.removedLine)/(m.endLine-m.startLine+1)
            source_len = len(method_set)
            for m in method_set:
                if(m in methods.keys()):
                    methods[m] = methods[m] + method_weight[m] * issue.artif_sim[i] * issue.artif_sim[i] / source_len
                else:
                    methods[m] = method_weight[m] * issue.artif_sim[i] * issue.artif_sim[i] / source_len

        sorted_methods = sorted(methods.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        issue.predict_bm_w = [x[0] for x in sorted_methods]
# evaluation
    ground_truth = [set(m.name for m in issue.methods if("nonMethodPart" not in m.name)) for issue in test_bugs]
    predict_result = [issue.predict_bm_w for issue in test_bugs]
    evaluation(ground_truth, predict_result)