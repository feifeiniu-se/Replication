import sqlite3
import os

from data_processing.database import read_sqlite, insert_database_tracescore
from sklearn.metrics.pairwise import cosine_similarity

from BF import BF

PM = True
# todo
if PM == True:
    big_bug_req_filter = True
    whole_history = False
else:
    big_bug_req_filter = False
    whole_history = True

def calculate(issues, filePath):
    bugReport = [x for x in issues if x.issue_type == "Bug"]
    print(len(bugReport), end=";")
    train_size = int(len(bugReport) * 0.8)
    test_bugs = bugReport[:]

    for i in range(len(test_bugs)):
        issue = test_bugs[i]  # current issue
        index = issues.index(issue) #index of current issue
        # # 找到list中符合条件的第一个 然后截取第一个到当前issue的前一个，都是within365的 并且根据sourceFile的数量过滤
        if whole_history==True:
            within365 = issues[:index]
            within365 = [x for x in within365 if (issue.first_commit_date>x.fixed_date)]
        else:
            within365 = [x for x in issues[:index] if (issue.first_commit_date - x.fixed_date).days <= 365 and issue.first_commit_date>x.fixed_date]
            # within365 = [x for x in issues[:index] if (issue.created_date - x.fixed_date).days <= 365 and issue.created_date>x.fixed_date]
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

    issue_mapping = {issue.issue_id:issue for issue in test_bugs}
    link_mapping = {} # issue_id, set()
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

    # insert_database_tracescore(filePath, test_bugs)


path = "C:/Users/Feifei/dataset/tracescore"
files = os.listdir(path)
files = ["derby", "drools", "hornetq", "izpack", "keycloak", "log4j2", "railo", "seam2", "teiid", "weld", "wildfly"]
print(";MAP;MRR;Top 1;Top 5;Top 10")
for file in files[:]:
    print(file, end=" ")
    filePath = path+"\\"+file + ".sqlite3"
    issues = read_sqlite(filePath)
    calculate(issues, filePath)
