from PatternMining import Types
from PatternMining.test import read_commits_all, find_last_modify
from evaluation.evaluation import evaluation
from PatternMining.Types import types
import numpy as np

def isExist(methodBlock, source_files, method_file):
    for file in method_file[methodBlock]:
        if file in source_files:
            return True
    return False

def BM_R(test_bugs, history_):
    # history: codeBlockID: codeBlock
    # bug report -> methods + refactorings
    for issue in test_bugs:
        methodBlocks = {} # <methodBlockID, score>
        method_file = {} # <methodBlockID, new_classBlockID>
        fileBlocks = {}
        # last_modify = {} #fileID, last_modify_hash
        for i in range(len(issue.artifacts)-1, -1, -1):
            methodBlock_set = set(m.methodBlockID for f in issue.artifacts[i].files for m in f.methods if f.new_classBlockID is not None)
            for f in issue.artifacts[i].files:
                if f.new_classBlockID is not None:
                    # last_modify[f.new_classBlockID] = f.last_modify_hash
                    for m in f.methods:
                        if m.methodBlockID not in method_file:
                            method_file[m.methodBlockID] = f.new_classBlockID
                #             用这个字典 保存最新的method file关系，这样用于最后的筛选
            source_len = len(methodBlock_set)
            for m in methodBlock_set:
                if (m in methodBlocks.keys()):
                    methodBlocks[m] = methodBlocks[m] + issue.artif_sim[i] * issue.artif_sim[i] / source_len
                else:
                    methodBlocks[m] = issue.artif_sim[i] * issue.artif_sim[i] / source_len

        sorted_methods = sorted(methodBlocks.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        issue.predict_bm_r = [x[0] for x in sorted_methods if method_file[x[0]] in issue.source_files_ID]

        # convert from method level to file level
        for m in methodBlocks:
            if method_file[m] in fileBlocks.keys():
                fileBlocks[method_file[m]] = fileBlocks[method_file[m]] + methodBlocks[m]
            else:
                fileBlocks[method_file[m]] = methodBlocks[m]

        sorted_files = sorted(fileBlocks.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        issue.predict_bm_r_f = [x[0] for x in sorted_files if x[0] in issue.source_files_ID]

###amaglam
        mapping_result = {}
        bluir_id_score = issue.bluir_id_score
        cache_id_score = issue.cache_id_score
        cache_id_score_new = issue.cache_id_score_new
        mapping_result.update({k: 0 for k in fileBlocks})
        mapping_result.update({k: 0 for k in bluir_id_score})
        fileBlocks = {k: fileBlocks[k] if k in fileBlocks else 0 for k in mapping_result}
        bluir_id_score = {k: bluir_id_score[k] if k in bluir_id_score else 0 for k in mapping_result}
        cache_id_score = {k: cache_id_score[k] if k in cache_id_score else 0 for k in mapping_result}
        cache_id_score_new = {k: cache_id_score_new[k] if k in cache_id_score_new else [0,0,0,0,0,0,0] for k in mapping_result}
        for f in mapping_result:
            score = (0.2 * fileBlocks.get(f) + 0.8 * bluir_id_score.get(f)) * 0.7 + cache_id_score.get(f) * 0.3
            mapping_result[f] = score
        sorted_files = sorted(mapping_result.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        issue.amalgam = [x[0] for x in sorted_files if x[0] in issue.source_files_ID]
        issue.simi_id_score = fileBlocks
        issue.cache_id_score = cache_id_score
        issue.cache_id_score_new = cache_id_score_new
        issue.bluir_id_score = bluir_id_score
        issue.amalgam_score = mapping_result
###amaglam

    # return test_bugs
        #
        # previous_commit = [commit for commit in commits_all if commit.committed_date < str(issue.first_commit_date)]
        # refactoring = {}
        # for f in mapping_result:
        #     type_count = [0 for t in Types.types]
        #     last_modify_hash = find_last_modify(previous_commit, f)
        #     classBlock = history_.get(f)
        #     if classBlock is not None:
        #         classBlockTimes = classBlock.History
        #         for blockTime in classBlockTimes:
        #             if blockTime.commitID==last_modify_hash:
        #                 refact_type = blockTime.refactorType.replace("_", " ")
        #                 if refact_type in types:
        #                     index = types.index(refact_type)
        #                     type_count[index] = type_count[index] + 1
        #     refactoring[f] = type_count
        #
        # refactoring_method = {}
        # for m in mapping_result:
        #     type_count = [0 for t in Types.types]
        #     filename = method_file[m]
        #     last_modify_hash = find_last_modify(previous_commit, filename)
        #     methodBlock = history_.get(m)
        #     if methodBlock is not None:
        #         methodBlockTimes = methodBlock.History
        #         for blockTime in methodBlockTimes:
        #             if blockTime.commitID == last_modify_hash:
        #                 refact_type = blockTime.refactorType.replace("_", " ")
        #                 if refact_type in types:
        #                     index = types.index(refact_type)
        #                     type_count[index] = type_count[index] + 1
        #     if refactoring_method.get(filename) is not None:
        #         refactoring_method[filename] = np.array(refactoring_method[filename]) + np.array(type_count)
        #     else:
        #         refactoring_method[method_file[m]] = type_count
        #
        #
        # issue.refactoring = refactoring
        # issue.refactoring_method = refactoring_method


        #         if len(h.deriver) > 0:
        #             for d in h.deriver:
        #                 if d.CodeBlockID in history:
        #                     derive.add(d.CodeBlockID)
        #                     derive.add(k)
        #
        #         if len(h.derivee) > 0:
        #             for d in h.derivee:
        #                 if d.CodeBlockID in history:
        #                     derive.add(k)
        #                     derive.add(d.CodeBlockID)

        # for m in methodBlocks:
        #     if m in derive:
        #         methodBlocks[m] = methodBlocks[m] * 1.2
        #     # if m in history:
        #     #     methodBlocks[m] = methodBlocks[m] * 1.5
        # sorted_methods = sorted(methodBlocks.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        # issue.predict_bm = [x[0] for x in sorted_methods if method_file[x[0]] in issue.source_files_ID]

        # # convert from method level to file level
        # for m in methodBlocks:
        #     if method_file[m] in fileBlocks.keys():
        #         fileBlocks[method_file[m]] = fileBlocks[method_file[m]] + methodBlocks[m]
        #     else:
        #         fileBlocks[method_file[m]] = methodBlocks[m]
        # sorted_files = sorted(fileBlocks.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        # issue.predict_bf = [x[0] for x in sorted_files if x[0] in issue.source_files_ID]



# # evaluation
# #      method level evaluation
#     ground_truth = [set(m.methodBlockID for f in issue.files for m in f.methods if f.classBlockID is not None) for issue in test_bugs]
#     predict_result = [issue.predict_bm_r for issue in test_bugs]
#     print("BM_R", end=";")
#     evaluation(ground_truth, predict_result)
#
#     ground_truth = [set(m.methodBlockID for f in issue.files for m in f.methods if f.classBlockID is not None) for issue
#                     in test_bugs]
#     predict_result = [issue.predict_bm for issue in test_bugs]
#     print("BM_R", end=";")
#     evaluation(ground_truth, predict_result)
#
#     # file level evaluation
#     ground_truth = [set(f.classBlockID for f in issue.files if f.classBlockID is not None) for issue in test_bugs]
#     predict_result = [issue.predict_bm_r_f for issue in test_bugs]
#     print("BM_R_F", end=";")
#     evaluation(ground_truth, predict_result)
#
#     predict_result = [issue.predict_bf for issue in test_bugs]
#     print("BM_R_F", end=";")
#     evaluation(ground_truth, predict_result)
#
#     print("amaglam", end=";")
#     predict_result = [issue.amalgam for issue in test_bugs]
#     evaluation(ground_truth, predict_result)