import datetime


class Issue:
    def __init__(self, info):
        self.issue_id = info[0]
        self.issue_type = info[1]
        self.fixed_date = datetime.datetime.strptime(info[2].replace("T", " ").replace("Z", ""), "%Y-%m-%d %H:%M:%S")
        self.created_date = datetime.datetime.strptime(info[5].replace("T", " ").replace("Z", ""), "%Y-%m-%d %H:%M:%S")
        self.first_commit_date = '2022-12-31 11:59:59'
        self.first_commit_hash = set()
        self.summary_stem = info[3]
        self.description_stem = info[4]
        self.tfidf = []
        self.files = [] # ground truth of file level
        self.artifacts = []
        self.artif_sim = []
        self.source_files = set() # file path of all source code at current version

        self.summary = ""
        self.description = ""

        self.cache_score = {}
        self.bluir_score = {}
        self.simi_score = {}
        self.amalgam = []
        self.amalgam_score = {}
        self.ablots = []
        self.ablots_score = {}

        self.predict_bf = []


