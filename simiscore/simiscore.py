import sqlite3
import os

from data_processing.database import read_tracescore
import datetime
from sklearn.metrics.pairwise import cosine_similarity

from simiscore.buglocator import BF


def calculate(issues):
    bugReport = [x for x in issues if x.issue_type == "Bug"]
    print(len(bugReport), end=";")
    train_size = int(len(bugReport) * 0.8)
    test_bugs = bugReport[train_size:]

    # 计算相似性
    for i in range(len(test_bugs)):
        issue = test_bugs[i]  # 当前的issue
        index = bugReport.index(issue)
        within365 = bugReport[:index]
        within365 = [x for x in within365 if (issue.created_date>x.fixed_date)]
        # within365 = test_bugs[:i]
        issue.artifacts = [x for x in within365] #不把修改文件过多的requirement和bug report过滤掉，会有些许的提升，因此此处不过滤
        issue.artif_sim = [cosine_similarity(issue.tfidf, x.tfidf) for x in issue.artifacts]
        issue.artif_sim = [float(x[0][0]) for x in issue.artif_sim]

    BF(test_bugs)

#
# path = "C:/Users/Feifei/dataset/tracescore"
# files = os.listdir(path)
# # files = ["derby", "drools", "izpack", "log4j2", "railo", "seam2"]
# files = ["derby", "drools", "hornetq", "izpack", "keycloak", "log4j2", "railo", "seam2", "teiid", "weld", "wildfly"]
# print(";MAP;MRR;Top 1;Top 5;Top 10")
#
# for file in files[:]:
#     print(file, end=" ")
#     filePath = path+"\\"+file + ".sqlite3"
#     issues = read_tracescore(filePath)
#     calculate(issues)
