class Transcript:
    def __init__(self):
        self.text = ""
        self.items = []
        self.sentences = []

    def __repr__(self):
        return "Transcript %d items, %d sentences: %s" % (len(self.items), len(self.sentences), self.text)

    def __str__(self):
        return self.text