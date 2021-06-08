from talkytalky import asr_json
from talkytalky.util import html
from typing import List


class AlignedItem:
    html_item: List[html.HtmlItem]
    trans_item: List[asr_json.Item]

    def __init__(self):
        self.trans_item = []
        self.html_item = []

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content
