from evaluation.evaluation import evaluation


def isExist(method_name, source_files, method_file):
    for file in method_file[method_name]:
        if file in source_files:
            return True
    return False


def BM(test_bugs):
    # bug report -> method BM
    for issue in test_bugs:
        methods = {}
        method_file = {} # method:set(files) store files
        for i in range(len(issue.artifacts)-1, -1, -1):
            method_set = set(m.name for m in issue.artifacts[i].methods if("nonMethodPart" not in m.name))
            # 存储方法所在的文件的信息
            for m in issue.artifacts[i].methods:
                if m.name in method_file:
                    method_file[m.name].add(m.filePath)
                else:
                    method_file[m.name] = set()
                    method_file[m.name].add(m.filePath)
            source_len = len(method_set)
            for m in method_set:
                if(m in methods.keys()):
                    methods[m] = methods[m] + issue.artif_sim[i] * issue.artif_sim[i] / source_len
                else:
                    methods[m] = issue.artif_sim[i] * issue.artif_sim[i] / source_len
        sorted_methods = sorted(methods.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        issue.predict_bm = [x[0] for x in sorted_methods]
#         if isExist(x[0], issue.source_files, method_file)


#     evaluation
    ground_truth = [set(m.name for m in issue.methods if("nonMethodPart" not in m.name)) for issue in test_bugs]
    predict_result = [issue.predict_bm for issue in test_bugs]
    print("BM", end=";")
    evaluation(ground_truth, predict_result)