import sqlite3
import os

from ablots.classifier import J48, DT, MLP, RF
from data_processing.database import read_sqlite, read_cha
import datetime
from sklearn.metrics.pairwise import cosine_similarity

from evaluation.evaluation import evaluation
from tracescore.BF import BF
# from BF_RW import BF_RW
# from BM import BM
# from BM_R import BM_R

PM = True
# todo
if PM == True:
    big_bug_req_filter = True
    whole_history = False
else:
    big_bug_req_filter = False
    whole_history = True


def evaluate(test, type):
    ground_truth = [set(f.new_filePath for f in issue.files if f.new_filePath != "/dev/null") for issue in test]
    # print("amalgam", end=";")
    # predict_result = [issue.amalgam for issue in test]
    # evaluation(ground_truth, predict_result)

    predict_result = [issue.ablots for issue in test]
    print("ablots", end=";")
    evaluation(ground_truth, predict_result)

def reRank(test, pairs_test, result):
    test_mapping = {issue.issue_id: issue for issue in test}
    for i in range(len(pairs_test)):
        tmp = pairs_test[i]
        issue = test_mapping.get(tmp[0])
        issue.ablots_score[tmp[1]] = result[i][0]
    for issue in test:
        predict = issue.ablots_score
        sorted_files = sorted(predict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        issue.ablots = [x[0] for x in sorted_files]


def make_pairs(issues, flag):
    pairs = []
    if flag=='file':
        for issue in issues:
            ground_truth = set(f.new_filePath for f in issue.files if f.new_filePath != "/dev/null")
            for f in issue.amalgam_score:
                value = []
                value.append(issue.issue_id)
                value.append(f)
                value.append(issue.cache_score[f])
                value.append(issue.bluir_score[f])
                value.append(issue.simi_score[f])
                if f in ground_truth:
                    value.append("bug")
                else:
                    value.append("no_bug")
                pairs.append(value)
    return pairs



def calculate(issues, filePath, history):
# def calculate(issues, filePath, train_size):
    bugReport = [x for x in issues if x.issue_type == "Bug"]
    # print(len(bugReport), end=";")
    print(len(bugReport), end=";")
    train_size = int(len(bugReport) * 0.8)
    test_bugs = bugReport[:]


    # 计算相似性
    for i in range(len(test_bugs)):
        issue = test_bugs[i]  # 当前的issue
        index = issues.index(issue)
        # # 找到list中符合条件的第一个 然后截取第一个到当前issue的前一个，都是within365的 并且根据sourceFile的数量过滤
        if whole_history==True:
            within365 = issues[:index]
        else:
            within365 = [x for x in issues[:index] if (datetime.datetime.strptime(issue.created_date.replace("T", " ").replace("Z", ""), "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(x.fixed_date.replace("T", " ").replace("Z", ""), "%Y-%m-%d %H:%M:%S")).days <= 365]
        if big_bug_req_filter==True:
            issue.artifacts = [x for x in within365 if (x.issue_type == "Bug" and len(set(f.filePath for f in x.files)) <= 10) or (x.issue_type != "Bug" and len(set(f.filePath for f in x.files)) <= 20)]
        else:
            issue.artifacts = [x for x in within365] #不把修改文件过多的requirement和bug report过滤掉，会有些许的提升，因此此处不过滤
        issue.artif_sim = [cosine_similarity(issue.tfidf, x.tfidf) for x in issue.artifacts]
        issue.artif_sim = [float(x[0][0]) for x in issue.artif_sim]

    # 数据库读取issue_link 如果两个issue之间存在连接 将权重设为1
    connection = sqlite3.connect(filePath)
    connection.text_factory = str
    cursor = connection.cursor()

    issue_mapping = {issue.issue_id: issue for issue in test_bugs}
    link_mapping = {}  # issue_id, set()
    cursor.execute("select * from issue_link")
    result = cursor.fetchall()
    for tmp in result:
        if tmp[0] in link_mapping:
            link_mapping[tmp[0]].add(tmp[1])
        else:
            link_mapping[tmp[0]] = set()
            link_mapping[tmp[0]].add(tmp[1])
        if tmp[1] in link_mapping:
            link_mapping[tmp[1]].add(tmp[0])
        else:
            link_mapping[tmp[1]] = set()
            link_mapping[tmp[1]].add(tmp[0])
    for id, links in link_mapping.items():
        issue = issue_mapping.get(id)
        if issue is not None:
            # 遍历所有的issue.artifacts，如果二者之间存在关系 就更新权重为1
            for i in range(0, len(issue.artifacts)):
                if issue.artifacts[i].issue_id in links:
                    issue.artif_sim[i] = 1.0


    BF(test_bugs)#todo
    # BF_R(test_bugs, history)
    # BM_R(test_bugs, history)
    train_size = int(len(test_bugs) * 0.8)
    test = test_bugs[train_size:]
    train = test_bugs[:train_size]

    # j48 model train
    pairs_train = make_pairs(train, "file")
    pairs_test = make_pairs(test, "file")

    # # J48
    # result = J48(pairs_train, pairs_test)

    # DT
    # result = DT(pairs_train, pairs_test)

    # MLP
    result = MLP(pairs_train, pairs_test, [])
    reRank(test, pairs_test, result)
    evaluate(test, "ablots")

    #RF
    # result = RF(pairs_train, pairs_test)
    # reRank(test, pairs_test, result)
    # evaluate(test, "ablots")




path = "C:/Users/Feifei/dataset/tracescore"
files = os.listdir(path)
# files = ["derby", "drools", "izpack", "log4j2", "railo", "seam2"]
files = ["derby", "drools", "hornetq", "izpack", "keycloak", "log4j2", "railo", "seam2", "teiid", "weld", "wildfly"]
print(";MAP;MRR;Top 1;Top 5;Top 10;P@1;P@5;P@10;R@1;R@5;R@10;Top 1%; Top 2%;Top 5%;Top 10%;Top 20%;Top 50%;R@1%;R@2%;R@5%;R@10%;R@20%;R@50%")
# print('issue_id;GT;Prediction;TP;TP/GT;TP/Prediction;Position;Days')
# for file in files:
for file in files[:]:
    # file = "wildfly.sqlite3"
    print(file, end=" ")
    filePath = path+"\\"+file + ".sqlite3"
    issues = read_sqlite(filePath)
    # history = read_cha(filePath)
    # train_sizes = [50, 100, 150, 200, 250, 300]
    # for train_size in train_sizes:
    #     calculate(issues, filePath, train_size) #for different part of test set
    calculate(issues, filePath, "")
