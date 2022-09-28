from evaluation.evaluation import evaluation


def BF_RW(test_bugs):

    # bug report - file + refactoring BF_R
    for issue in test_bugs:
        classBlocks = {}
        for i in range(len(issue.artifacts)-1, -1, -1):
            files_set = {f.classBlockID:f.removedLine for f in issue.artifacts[i].files}
            lines = sum([files_set[f] for f in files_set.keys()]) #统计一共修改了多少行代码
            # source_len = len(files_set)
            for f in files_set.keys():
                if files_set[f]>0:
                    if(f in classBlocks.keys()):
                        classBlocks[f] = classBlocks[f] + issue.artif_sim[i] * issue.artif_sim[i] / lines * files_set[f] # 增加的代码行数 除以本bug report总共增加的代码行数
                    else:
                        classBlocks[f] = issue.artif_sim[i] * issue.artif_sim[i] / lines * files_set[f]

        sorted_classBlocks = sorted(classBlocks.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        issue.predict_bf_r = [x[0] for x in sorted_classBlocks if x[0] in issue.source_files_ID]
    ground_truth = [set(f.classBlockID for f in issue.files) for issue in test_bugs]
    predict_result = [issue.predict_bf_r for issue in test_bugs]
    print("bf_r", end=";")
    evaluation(ground_truth, predict_result)

    # include delete files into ground truth
    # print("bf_r", end=";")
    # ground_truth_m = [set(m.filePath for m in issue.methods) for issue in test_bugs]
    # ground_truth = [ground_truth[i].union(ground_truth_m[i]) for i in range(len(ground_truth))]
    # evaluation(ground_truth, predict_result)