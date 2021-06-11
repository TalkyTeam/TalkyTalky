class Item:
    """Encapsulates ASR Item data. Does not support multiple alternatives."""
    def __init__(self):
        self.content = ""
        self.confidence = 0.0
        self.punctuation = False
        self.pronunciation = False
        self.start_time = 0.0
        self.end_time = 0.0

    def __repr__(self):
        if self.pronunciation:
            return "Pronunciation (%.2f - %.2f): %s" % (self.start_time, self.end_time, self.content)
        else:
            return "Punctuation: %s" % self.content

    def __str__(self):
        return self.content
