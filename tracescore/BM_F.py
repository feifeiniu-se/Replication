from evaluation.evaluation import evaluation


def BM_F(test_bugs):
    for issue in test_bugs:
        files = {}#用来存储每个文件的权重
        methods = {}# 用来存储每个方法的权重
        mapping = {}# 用来存储<method.name, method.filePath> 对
        for i in range(len(issue.artifacts)):
            file_path = set(f.filePath for f in issue.artifacts[i].files)
            method_set = set(m.name for m in issue.artifacts[i].methods if m.filePath in file_path)
            tmp = [m for m in issue.artifacts[i].methods if m.filePath in file_path]
            for m in tmp:
                mapping[m.name] = m.filePath
            source_len = len(method_set)
            for m in method_set:
                if(m in methods.keys()):
                    methods[m] = methods[m] + issue.artif_sim[i] * issue.artif_sim[i] / source_len
                else:
                    methods[m] = issue.artif_sim[i] * issue.artif_sim[i] / source_len

        for m in methods.keys():
            if(mapping[m] in files):
                files[mapping[m]] = files[mapping[m]] + methods[m]
            else:
                files[mapping[m]] = methods[m]
        sorted_files = sorted(files.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        issue.predict_bm_f = [x[0] for x in sorted_files]

    ground_truth = [set(f.filePath for f in issue.files) for issue in test_bugs]
    predict_result = [issue.predict_bm_f for issue in test_bugs]
    evaluation(ground_truth, predict_result)