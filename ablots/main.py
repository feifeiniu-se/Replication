import os

from ablots.classifier import MLP
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

def evaluate3(issues):
    bugReport = [x for x in issues if x.issue_type == "Bug"]
    print(len(bugReport), end=";")
    train_size = int(len(bugReport) * 0.8)

    bugReport.sort(key=lambda x: x.fixed_date)
    test = bugReport[train_size:]

    ground_truth = [set(f.new_filePath for f in issue.files if f.new_filePath != "/dev/null" and f.new_filePath is not None) for issue in test]
    for issue in test:
        predict = issue.cache_score
        sorted_files = sorted(predict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        issue.bluir = [x[0] for x in sorted_files]
    predict_result = [issue.bluir for issue in test]
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
        issue.ablots = [x[0] for x in sorted_files]


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
                value.append("bug")
            else:
                value.append("no_bug")
            pairs.append(value)
    return pairs



def calculate(issues):
    bugReport = [x for x in issues if x.issue_type == "Bug"]
    print(len(bugReport), end=";")
    train_size = int(len(bugReport) * 0.8)

    bugReport.sort(key=lambda x: x.fixed_date)
    test = bugReport[train_size:]
    train = bugReport[:train_size]

    # j48 model train
    pairs_train = make_pairs(train)
    pairs_test = make_pairs(test)

    # # J48
    # result = J48(pairs_train, pairs_test)

    # DT
    # result = DT(pairs_train, pairs_test)

    # MLP
    result = MLP(pairs_train, pairs_test)
    reRank(test, pairs_test, result)
    evaluate(test)

    #RF
    # result = RF(pairs_train, pairs_test)
    # reRank(test, pairs_test, result)
    # evaluate(test, "ablots")


# # tracescore dataset
# path = "C:/Users/Feifei/dataset/tracescore"
# files = os.listdir(path)
# # files = ["derby", "drools", "izpack", "log4j2", "railo", "seam2"]
# files = ["derby", "drools", "hornetq", "izpack", "keycloak", "log4j2", "railo", "seam2", "teiid", "weld", "wildfly"]
# print(";MAP;MRR;Top 1;Top 5;Top 10")
# for file in files[:]:
#     print(file, end=" ")
#     filePath = path+"\\"+file + ".sqlite3"
#     issues = read_sqlite(filePath)
#     read_scores(filePath, issues)
#     # evaluate3(issues)
#     calculate(issues)

#issues dataset
path = "C:/Users/Feifei/dataset/issues"
files = os.listdir(path)
# files = ["derby", "drools", "izpack", "log4j2", "railo", "seam2"]
files = ["archiva", "axis2", "cassandra", "derby", "drools", "errai", "flink", "groovy", "hadoop", "hbase", "hibernate", "hive", "hornetq", "infinispan", "izpack", "jbehave", "jboss-transaction-manager", "jbpm", "kafka", "keycloak", "log4j2", "lucene", "maven", "pig", "railo", "resteasy", "seam2", "spark", "switchyard", "teiid", "weld", "wildfly", "zookeeper"]
print(";MAP;MRR;Top 1;Top 5;Top 10")
for file in files[0:1]:
    print(file, end=" ")
    filePath = path+"\\"+file + ".sqlite3"
    issues = read_issues(filePath)
    read_scores(filePath, issues)
    # evaluate3(issues)
    calculate(issues)