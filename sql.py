import os
import sqlite3

path = "C:/Users/Feifei/dataset/issues"
files = os.listdir(path)
files = ["archiva", "axis2", "cassandra", "derby", "drools", "errai", "flink", "groovy", "hadoop", "hbase", "hibernate", "hive", "hornetq", "infinispan", "izpack", "jbehave", "jboss-transaction-manager", "jbpm", "kafka", "keycloak", "log4j2", "lucene", "maven", "pig", "railo", "resteasy", "seam2", "spark", "switchyard", "teiid", "weld", "wildfly", "zookeeper"]

for file in files[:]:
    print(file, end=" ")
    filePath = path+"\\"+file + ".sqlite3"
    connection = sqlite3.connect(filePath)
    cursor = connection.cursor()
    # cursor.execute("CREATE VIEW v_code_change AS SELECT change_set_link.issue_id, change_set.*, code_change.* FROM code_change INNER JOIN change_set ON change_set.commit_hash = code_change.commit_hash inner join change_set_link on change_set_link.commit_hash=change_set.commit_hash")
    cursor.execute("CREATE VIEW v_commit_change_file AS SELECT change_set.*, code_change.* FROM code_change INNER JOIN change_set ON change_set.commit_hash = code_change.commit_hash")
    cursor.close()
    connection.close()
