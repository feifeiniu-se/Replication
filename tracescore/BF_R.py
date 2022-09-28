from evaluation.evaluation import evaluation
# from utils import time_span_analyze


def BF_R(test_bugs, history):

    # bug report - file + refactoring BF_R
    for issue in test_bugs:
        classBlocks = {}
        for i in range(len(issue.artifacts)-1, -1, -1):
            files_set = set(f.new_classBlockID for f in issue.artifacts[i].files if f.new_classBlockID is not None)
            source_len = len(files_set)
            for f in files_set:
                if(f in classBlocks.keys()):
                    classBlocks[f] = classBlocks[f] + issue.artif_sim[i] * issue.artif_sim[i] / source_len
                else:
                    classBlocks[f] = issue.artif_sim[i] * issue.artif_sim[i] / source_len

        sorted_classBlocks = sorted(classBlocks.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        issue.predict_bf_r = [x[0] for x in sorted_classBlocks]
# amaglam score
#         mapping_result = {}
#         bluir_id_score = issue.bluir_id_score
#         cache_id_score = issue.cache_id_score
#         mapping_result.update({k: 0 for k in classBlocks})
#         mapping_result.update({k: 0 for k in bluir_id_score})
#         classBlocks = {k: classBlocks[k] if k in classBlocks else 0 for k in mapping_result}
#         bluir_id_score = {k: bluir_id_score[k] if k in bluir_id_score else 0 for k in mapping_result}
#         cache_id_score = {k: cache_id_score[k] if k in cache_id_score else 0 for k in mapping_result}
#         for f in mapping_result:
#             score = (0.2 * classBlocks.get(f) + 0.8 * bluir_id_score.get(f)) * 0.7 + cache_id_score.get(f) * 0.3
#             mapping_result[f] = score
#         sorted_files = sorted(mapping_result.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
#         issue.amalgam = [x[0] for x in sorted_files if x[0] in issue.source_files_ID]
#         issue.simi_id_score = classBlocks
#         issue.cache_id_score = cache_id_score
#         issue.bluir_id_score = bluir_id_score
#         issue.amalgam_score = mapping_result

        # # refactoring ###
        # history = {k:v for k,v in history.items() if k in classBlocks.keys()}
        # for k, v in history.items():
        #     v.cutHistory(issue.first_commit_hash)
        #     # v.filterHistory()
        # history = {k:v for k, v in history.items() if len(v.History)>0 and v.Type!="Package"}
        # derive = set()
        # # derivee = set()
        # for k, v in history.items():
        #     for h in v.History:
        #         if len(h.deriver)>0:
        #             for d in h.deriver:
        #                 if d.CodeBlockID in history:
        #                     derive.add(d.CodeBlockID)
        #                     derive.add(k)
        #
        #         if len(h.derivee)>0:
        #             for d in h.derivee:
        #                 if d.CodeBlockID in history:
        #                     derive.add(k)
        #                     derive.add(d.CodeBlockID)
        #
        #
        # for f in issue.cache_score:
        #     classBlocks[f] = classBlocks[f] + issue.cache_score[f]*10000
        #     # print(classBlocks[f])
        #
        # # for id in classBlocks:
        # #     if id in derive:
        # #         classBlocks[id] = classBlocks[id] * 1.5
        #     # if id in history:
        #     #     classBlocks[id] = classBlocks[id] * 1.2
        # sorted_classBlocks = sorted(classBlocks.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        # issue.predict_bf = [x[0] for x in sorted_classBlocks if x[0] in issue.source_files_ID]#使用bf来存储加了refactoring 权重的结果
        # x1 = [f for f in issue.predict_bf_r if f in gt and f in history]
        # x3 = [f for f in issue.predict_bf_r if f in gt and f not in history]
        # x2 = [f for f in issue.predict_bf_r if f not in gt and f in history]
        # x4 = [f for f in issue.predict_bf_r if f not in gt and f not in history]
        # print(str(len(x1)) + " " + str(len(x3)) + " " + str(len(x2)) + " " + str(len(x4)))
        # print(set(h.refactorType for f in x1 for h in history[f].History ))
        # # if len(history)>0:
        # #     print("OK")
        ###

    ground_truth = [set(f.classBlockID for f in issue.files if f.classBlockID is not None) for issue in test_bugs]
    predict_result = [issue.predict_bf_r for issue in test_bugs]

    index = [i for i in range(len(ground_truth)) if len(ground_truth[i]) == 0]
    ground_truth = [ground_truth[i] for i in range(len(ground_truth)) if i not in index]
    predict_result = [predict_result[i] for i in range(len(predict_result)) if i not in index]

    evaluation(ground_truth, predict_result)
    #
    # print("amaglam", end=";")
    # predict_result = [issue.amalgam for issue in test_bugs]
    # evaluation(ground_truth, predict_result)



    # output data for hist
    # print("bf_r")
    # time_span_analyze(ground_truth, predict_result, test_bugs)  # 计算每个issue的predict，GT之间的交集