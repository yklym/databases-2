class Link:

    def __init__(self, url: str, filename: str):
        self.url = url
        self.filename = filename
        self.is_parsed = False

    def set_parsed(self):
        self.is_parsed = True
