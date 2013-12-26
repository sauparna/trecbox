
class SysTerrier():

    def __init__(self, env):

        self.query_map = {"t": "TITLE", "d": "DESC", "n": "NARR"}
        self.model_map = {"bm25": "BM25", "dfr": "DFI0", "tfidf": "TF_IDF"}

    def index(self, doc, itag):

        # doc is the collection.spec file
        # TODO: create collection.spec
        # do something about this step, very irritating indeed

        o_dir = os.path.join(self.env["index"], itag)
        
        if os.path.exists(o_dir):
            os.removedirs(o_dir)

        # TODO: check if needed
        os.mkdir(o_dir)

        subprocess.check_output([
                "/home/rup/terrier-3.5/bin/trec_terrier.sh",
                "-i",
                "-Dcollection.spec=" + doc,
                "-DTrecDocTags.doctag=DOC",
                "-DTrecDocTags.idtag=DOCNO",
                "-DTrecDocTags.process=TEXT,H3,DOCTITLE,HEADLINE,TTL",
                "-DTrecDocTags.skip=DOCHDR",
                "-DTrecDocTags.casesensitive=true",
                "-Dterrier.index.path=" + o_dir])

    def retrieve(self, itag, rtag, m, q, q_mode):

        # q is the topic file
        # q_mode is a string like "tdn"

        l = list(q_mode)

        process = []
        skip = []
        for s in ["t", "d", "n"]:
            if s in l:
                process.append(self.query_map[s])
            else:
                skip.append(self.query_map[s])
        process = ",".join(process)
        skip = ",".join(skip)

        i_dir = os.path.join(self.env["index"], itag)
        
        subprocess.check_output([
            "/home/rup/terrier-3.5/bin/trec_terrier.sh",
            "-r",
            "-Dterrier.index.path=" + i_dir,
            "query": "-Dtrec.topics=" + q,
            "query1": "-DTrecQueryTags.doctag=TOP",
            "query2": "-DTrecQueryTags.idtag=NUM",
            "query3": "-DTrecQueryTags.process=TOP,NUM," + process,
            "query4": "-DTrecQueryTags.skip=" + skip,
            "query5": "-DTrecQueryTags.casesensitive=false",
            "model": "-Dtrec.model=" + self.model_map[m],
            "rundir": "-Dtrec.results=" + self.env["runs"],
            "runfile": "-Dtrec.results.file=" + rtag])

    def evaluate(self, rtag, qrels):

        # overwrites files in eval dir

        # trec_eval -q QREL_file Retrieval_Results > eval_output

        i_file = os.path.join(self.env["runs"], rtag)
        o_file = os.path.join(self.env["evals"], rtag)

        with open(o_file, "w") as f:
            f.write(subprocess.check_output([self.env["treceval"],
                                             "-q",
                                             qrels,
                                             i_file]))
