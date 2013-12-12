class Topics():
    def __init__(self, f):
        self.file = f
        self.query = "t"

    def build_query(self, opt):
        # opt is a string
        self.query = opt.lower()
