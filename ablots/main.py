import os

from ablots.classifier import  DT
from data_processing.database import read_tracescore, read_scores
from evaluation.evaluation import evaluation
from replication.read import read_issues

PM = True
# todo
if PM == True:
    big_bug_req_filter = True
    whole_history = False
else:
    big_bug_req_filter = False
    whole_history = True


def evaluate(test):
    ground_truth = [set(f.new_filePath for f in issue.files if f.new_filePath != "/dev/null" and f.new_filePath is not None) for issue in test]

    predict_result = [issue.ablots for issue in test]
    evaluation(ground_truth, predict_result)

def evaluate3(issues, flag):
    bugReport = [x for x in issues if x.issue_type == "Bug"]
    print(len(bugReport), end=";")
    train_size = int(len(bugReport) * 0.8)

    bugReport.sort(key=lambda x: x.fixed_date)
    test = bugReport[train_size:]

    ground_truth = [set(f.new_filePath for f in issue.files if f.new_filePath != "/dev/null" and f.new_filePath is not None) for issue in test]
    for issue in test:
        if flag=="cache":
            predict = issue.cache_score
        elif flag=="bluir":
            predict = issue.bluir_score
        elif flag=="tracescore":
            predict = issue.simi_score
        sorted_files = sorted(predict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        issue.predict_bf = [x[0] for x in sorted_files if x[0] in issue.source_files]
    predict_result = [issue.predict_bf for issue in test]
    evaluation(ground_truth, predict_result)


def reRank(test, pairs_test, result):
    test_mapping = {issue.issue_id: issue for issue in test}
    for i in range(len(pairs_test)):
        tmp = pairs_test[i]
        issue = test_mapping.get(tmp[0])
        issue.ablots_score[tmp[1]] = result[i]
    for issue in test:
        predict = issue.ablots_score
        sorted_files = sorted(predict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        issue.ablots = [x[0] for x in sorted_files if x[0] in issue.source_files]


def make_pairs(issues):
    pairs = []
    for issue in issues:
        ground_truth = set(f.new_filePath for f in issue.files if f.new_filePath != "/dev/null" and f.new_filePath is not None)
        file_candidate = []
        file_candidate.extend([f for f in issue.bluir_score])
        file_candidate.extend([f for f in issue.simi_score])
        file_candidate = set(file_candidate)
        for f in file_candidate:
            value = []
            value.append(issue.issue_id)
            value.append(f)
            value.append(issue.cache_score[f] if f in issue.cache_score else 0)
            value.append(issue.bluir_score[f] if f in issue.bluir_score else 0)
            value.append(issue.simi_score[f] if f in issue.simi_score else 0)
            if f in ground_truth:
                value.append(1)
            else:
                value.append(-1)
            # if (value[2]+value[3]+value[4])>0.5:
            pairs.append(value)

    # map_count = {}
    # for i in pairs:
    #     k = i[0]
    #     if k in map_count:
    #         map_count[k] = map_count[k] + 1
    #     else:
    #         map_count[k] = 1
    # total = 0
    # for k, v in map_count.items():
    #     total = total + v
    # average = total/len(map_count)
    # print(total/len(map_count))


    return pairs



def calculate(issues):
    bugReport = [x for x in issues if x.issue_type == "Bug"]
    print(len(bugReport), end=";")
    train_size = int(len(bugReport) * 0.8)

    bugReport.sort(key=lambda x: x.fixed_date)
    test = bugReport[train_size:]
    train = bugReport[:train_size]

    pairs_train = make_pairs(train)
    pairs_test = make_pairs(test)

    # # J48
    # result = J48(pairs_train, pairs_test)

    # DT
    result = DT(pairs_train, pairs_test)
    reRank(test, pairs_test, result)
    evaluate(test)

def calculate_fixed(issues):
    bugReport = [x for x in issues if x.issue_type=="Bug"]
    train_size = int(len(bugReport) * 0.8)

    bugReport.sort(key=lambda x: x.fixed_date)
    test = bugReport[train_size:]

    for issue in test:
        amalgam_score = {}
        file_candidate = []
        file_candidate.extend([f for f in issue.bluir_score])
        file_candidate.extend([f for f in issue.simi_score])
        file_candidate = set(file_candidate)
        for f in file_candidate:
            cache_score = issue.cache_score[f] if f in issue.cache_score else 0
            bluir_score = issue.bluir_score[f] if f in issue.bluir_score else 0
            simi_score = issue.simi_score[f] if f in issue.simi_score else 0
            score = (0.2 * simi_score + 0.8 * bluir_score) * 0.7 + cache_score * 0.3
            amalgam_score[f] = score
        sorted_files = sorted(amalgam_score.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        issue.ablots = [x[0] for x in sorted_files if x[0] in issue.source_files]


    evaluate(test)



# # old dataset
path = "C:/Users/Feifei/dataset/tracescore"
files = os.listdir(path)
# files = ["derby", "drools", "izpack", "log4j2", "railo", "seam2"]
files = ["derby", "drools", "hornetq", "izpack", "keycloak", "log4j2", "railo", "seam2", "teiid", "weld", "wildfly"]
print(";MAP;MRR;Top 1;Top 5;Top 10")
for file in files[:]:
    print(file, end=" ")
    filePath = path+"\\"+file + ".sqlite3"
    issues = read_tracescore(filePath)
    read_scores(filePath, issues)
    # evaluate3(issues, "tracescore")
    calculate(issues)
    # calculate_fixed(issues)

# #new dataset
# path = "C:/Users/Feifei/dataset/issues"
# files = os.listdir(path)
# # files = ["derby", "drools", "izpack", "log4j2", "railo", "seam2"]
# files = ["archiva", "cassandra", "errai", "flink", "groovy", "hbase", "hibernate", "hive", "jboss-transaction-manager", "kafka", "lucene", "maven", "resteasy", "spark", "switchyard", "zookeeper"]
# # "jbehave", "jbpm"
# print(";MAP;MRR;Top 1;Top 5;Top 10")
# for file in files[:]:
#     print(file, end=" ")
#     filePath = path+"\\"+file + ".sqlite3"
#     issues = read_issues(filePath)
#     read_scores(filePath, issues)
#     issues = [issue for issue in issues if len(issue.files) > 0]
#     # evaluate3(issues,"cache")
#     # calculate(issues)
#     calculate_fixed(issues)
