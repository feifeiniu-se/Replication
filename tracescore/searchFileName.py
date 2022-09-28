# see how many
import os

from data_processing.database import read_sqlite, read_text_sqlite

path = "C:/Users/Feifei/dataset/tracescore"
path2 = "C:/Users/Feifei/dataset/issues"
files = os.listdir(path)
files = ["derby", "drools", "hornetq", "izpack", "keycloak", "log4j2", "railo", "seam2", "teiid", "weld", "wildfly"]
for file in files[:2]:
    # file = "wildfly.sqlite3"
    print(file, end=" ")
    filePath = path+"\\"+file + ".sqlite3"
    issues = read_sqlite(filePath)

    filePath2 = path2+"\\"+file+".sqlite3"
    issues = read_text_sqlite(issues, filePath2)
    count = 0
    for issue in issues:
        for f in issue.files:
            if f.filePath is not None:
                if f.filePath is not None and f.filePath in issue.original_summary:
                    count = count + 1
                    # print(issue.original_summary)
                if f.filePath is not None and str(f.filePath) in str(issue.original_description):
                        count = count + 1
                        # print(issue.original_description)
    print(count)

    count = 0
    for issue in issues:
        if ".java" in str(issue.original_summary) or ".java" in str(issue.original_description):
            count = count + 1
        #     print(issue.original_summary)
        #     for f in issue.files:
        #         print(f.filePath + " ; " + f.new_filePath)
        # if ".java" in str(issue.original_description):
        #     count = count + 1
            # print(issue.original_description)
            # for f in issue.files:
            #     print(f.filePath + " ; " + f.new_filePath)

    print("second: ", end=";")
    print(count)
