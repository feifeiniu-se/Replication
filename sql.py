import os
import sqlite3

path = "C:/Users/Feifei/dataset/issues"
files = os.listdir(path)
files = ["archiva", "cassandra",  "errai", "flink", "groovy","hbase", "hibernate", "hive", "jboss-transaction-manager", "kafka", "lucene", "maven", "resteasy", "spark", "switchyard", "zookeeper"]
# "axis2","derby", "drools","hadoop", "izpack", "hbase",
# jbehave jbpm

for file in files[:]:
    print(file, end=" ")
    filePath = path+"\\"+file + ".sqlite3"
    connection = sqlite3.connect(filePath)
    cursor = connection.cursor()
    # cursor.execute("CREATE VIEW v_code_change AS SELECT change_set_link.issue_id, change_set.*, code_change.* FROM code_change INNER JOIN change_set ON change_set.commit_hash = code_change.commit_hash inner join change_set_link on change_set_link.commit_hash=change_set.commit_hash")
    # cursor.execute("CREATE VIEW v_commit_change_file AS SELECT change_set.*, code_change.* FROM code_change INNER JOIN change_set ON change_set.commit_hash = code_change.commit_hash")
    cursor.execute("select count(*) from Bluir")
    result = cursor.fetchall()
    print(result[0][0])
    cursor.close()
    connection.close()
