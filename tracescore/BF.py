from evaluation.evaluation import evaluation

def BF(test_bugs):
    for issue in test_bugs:
        files = {}
        for i in range(len(issue.artifacts)-1, -1, -1):
            files_set = set(f.new_filePath for f in issue.artifacts[i].files if f.new_filePath!="/dev/null")
            source_len = len(files_set)
            for f in files_set:
                if (f in files.keys()):
                    files[f] = files[f] + issue.artif_sim[i] * issue.artif_sim[i] / source_len
                else:
                    files[f] = issue.artif_sim[i] * issue.artif_sim[i] / source_len

        issue.simi_score = files
        sorted_files = sorted(files.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        issue.predict_bf = [x[0] for x in sorted_files if x[0] in issue.source_files]


    # evaluation
    ground_truth = [set(f.filePath for f in issue.files if f.filePath!="/dev/null") for issue in test_bugs]
    predict_result = [issue.predict_bf for issue in test_bugs]

    # index = [i for i in range(len(ground_truth)) if len(ground_truth[i])==0]
    # ground_truth = [ground_truth[i] for i in range(len(ground_truth)) if i not in index]
    # predict_result = [predict_result[i] for i in range(len(predict_result)) if i not in index]

    evaluation(ground_truth, predict_result)

