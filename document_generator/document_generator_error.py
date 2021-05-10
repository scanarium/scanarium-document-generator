class DocumentGeneratorError(Exception):
    def parse(self, code, msg):
        super().__init_()
        self.code = code
        self.msg = msg
