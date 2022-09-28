from evaluation.evaluation import evaluation


def BM_R_F(test_bugs):
    for issue in test_bugs:
        files = {}
        methodBlock = {}
        mapping = {}
        # mapping 将methodBlockID转化为所属的file
        for i in range(len(issue.artifacts)):
            file_path = set(f.filePath for f in issue.artifacts[i].files)
            method_set = set(m.methodBlockID for m in issue.artifacts[i].methods if m.filePath in file_path)
            tmp = [m for m in issue.artifacts[i].methods if m.filePath in file_path]
            for m in tmp:
                mapping[m.methodBlockID] = m.filePath
            source_len = len(method_set)
            for m in method_set:
                if(m in methodBlock.keys()):
                    methodBlock[m] = methodBlock[m] + issue.artif_sim[i] * issue.artif_sim[i] / source_len
                else:
                    methodBlock[m] = issue.artif_sim[i] * issue.artif_sim[i] / source_len

        for m in methodBlock.keys():
            if (mapping[m] in files):
                files[mapping[m]] = files[mapping[m]] + methodBlock[m]
            else:
                files[mapping[m]] = methodBlock[m]
        sorted_files = sorted(files.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        issue.predict_bm_r_f = [x[0] for x in sorted_files]

#     evaluation
    ground_truth = [set(f.filePath for f in issue.files) for issue in test_bugs]
    predict_result = [issue.predict_bm_r_f for issue in test_bugs]
    evaluation(ground_truth, predict_result)