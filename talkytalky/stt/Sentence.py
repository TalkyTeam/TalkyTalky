
class Sentence:
    """Aggregates items into suspected sentences."""
    def __init__(self):
        self.text = ""
        self.start_time = 0.0
        self.end_time = 0.0
        self.word_count = 0
        self.character_count = 0
        self.items = []

    def __repr__(self):
        return "Sentence (%.2f - %.2f): %s" % (self.start_time, self.end_time, self.text)

    def __str__(self):
        return self.text


