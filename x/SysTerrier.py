
class SysTerrier():

    def __init__(self, env):

        self.query_map = {"t": "TITLE", "d": "DESC", "n": "NARR"}
        self.model_map = {"bm25": "BM25", "dfr": "DFI0", "tfidf": "TF_IDF"}

    def index(self, doc, itag):

        o_file = os.path.join(self.env["index"], ".".join([itag, "doclist"]))
        o_dir = os.path.join(self.env["index"], itag)

        with open(o_file, "w") as f:
            f.write(subprocess.check_output(["find", doc, "-type", "f"]))

        if os.path.exists(o_dir):
            os.removedirs(o_dir)

        # TODO: check if needed
        os.mkdir(o_dir)

        subprocess.check_output([
                "/home/rup/terrier-3.5/bin/trec_terrier.sh",
                "-i",
                "-Dcollection.spec=" + o_file,
                "-DTrecDocTags.doctag=DOC",
                "-DTrecDocTags.idtag=DOCNO",
                "-DTrecDocTags.process=TEXT,H3,DOCTITLE,HEADLINE,TTL",
                "-DTrecDocTags.skip=DOCHDR",
                "-DTrecDocTags.casesensitive=true",
                "-Dterrier.index.path=" + o_dir])

    def retrieve(self, itag, rtag, m, q, q_mode="t"):

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
            "-Dtrec.topics=" + q,
            "-DTrecQueryTags.doctag=TOP",
            "-DTrecQueryTags.idtag=NUM",
            "-DTrecQueryTags.process=TOP,NUM," + process,
            "-DTrecQueryTags.skip=" + skip,
            "-DTrecQueryTags.casesensitive=false",
            "-Dtrec.model=" + self.model_map[m],
            "-Dtrec.results=" + self.env["runs"],
            "-Dtrec.results.file=" + rtag])

    def evaluate(self, rtag, qrels):

        # overwrites files in eval dir

        # trec_eval -q QREL_file Retrieval_Results > eval_output

        i_file = os.path.join(self.env["runs"], rtag)
        o_file = os.path.join(self.env["evals"], rtag)

        with open(o_file, "w") as f:
            f.write(subprocess.check_output(
                    [os.path.join(self.env["treceval"], "trec_eval"),
                     "-q",
                     qrels,
                     i_file]))
