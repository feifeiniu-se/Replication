import os
import sqlite3
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stopwords = stopwords.words('english')
def text_preprocessing(text):
    result = []
    for t in text:
        t_tokens = word_tokenize(t)
        t_tokens_sw = [word for word in t_tokens if not word in stopwords]
        t = [word for word in t ]




path = "C:/Users/Feifei/dataset/issues"
files = os.listdir(path)
files = ["archiva", "axis2", "cassandra", "derby", "drools", "errai", "flink", "groovy", "hadoop", "hbase", "hibernate", "hive", "hornetq", "infinispan", "izpack", "jbehave", "jboss-transaction-manager", "jbpm", "kafka", "keycloak", "log4j2", "lucene", "maven", "pig", "railo", "resteasy", "seam2", "spark", "switchyard", "teiid", "weld", "wildfly", "zookeeper"]
print(";MAP;MRR;Top 1;Top 5;Top 10")
for file in files[:]:
    print(file, end=" ")
    filePath = path+"\\"+file + ".sqlite3"
    connection = sqlite3.connect(filePath)
    connection.text_factory = str
    cursor = connection.cursor()
    cursor.execute(
        "select issue_id, summary, description from issue")
    result = cursor.fetchall()

    summary = [tmp[1] for tmp in result]
    description = [tmp[2] for tmp in result]
    print("OK")