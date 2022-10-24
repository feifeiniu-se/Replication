import os
import sqlite3

path = "C:/Users/Feifei/dataset/issues"
files = os.listdir(path)
files = ["archiva", "cassandra",  "errai", "flink", "groovy","hbase", "hibernate", "hive", "jboss-transaction-manager", "kafka", "lucene", "maven", "resteasy", "spark", "switchyard", "zookeeper"]
# "axis2","derby", "drools","hadoop", "izpack", "hbase",
# jbehave jbpm
def include_id(message, ids):
    for id in ids:
        if id in message:
            return True
    return False

for file in files[:]:
    print(file, end=";")
    filePath = path+"\\"+file + ".sqlite3"
    connection = sqlite3.connect(filePath)
    cursor = connection.cursor()
    # cursor.execute("CREATE VIEW v_code_change AS SELECT change_set_link.issue_id, change_set.*, code_change.* FROM code_change INNER JOIN change_set ON change_set.commit_hash = code_change.commit_hash inner join change_set_link on change_set_link.commit_hash=change_set.commit_hash")
    # cursor.execute("CREATE VIEW v_commit_change_file AS SELECT change_set.*, code_change.* FROM code_change INNER JOIN change_set ON change_set.commit_hash = code_change.commit_hash")
    # cursor.execute("select count(*) from Bluir")
    cursor.execute("select count(*) from issue where type='Bug' and issue_id in (select issue_id from v_code_change)")
    result = cursor.fetchall()
    print(result[0][0])
    # cursor.execute("select distinct issue_id from v_code_change")
    # result = cursor.fetchall()
    # ids = set([tmp[0].lower() for tmp in result])
    # cursor.execute("select message from change_set")
    # result = cursor.fetchall()
    # a = len(result)
    # print(len(result), end=";")
    # count_a = 0
    # count_b = 0
    # count_c = 0
    # for tmp in result:
    #     message = tmp[0].lower()
    #     if "fix" in message or "bug" in message:
    #         count_a = count_a + 1
    #     if include_id(message, ids):
    #         count_b = count_b + 1
    #         if "fix" in message or "bug" in message:
    #             count_c = count_c + 1
    # print(count_a, end=";")
    # print(count_b, end=";")
    # print(count_c, end=";")
    # print(count_b-count_c, end=";")
    # print((count_b-count_c)/a)
    cursor.close()
    connection.close()
