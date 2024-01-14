class Sentence:

    def __init__(self, docid, num, wdcount, text):
        self.docId = docid
        self.num = num
        self.wdcount = wdcount
        self.text = text

    def __str__(self):
        return f"docId = {self.docid}, num = {self.num}, wdcount = {self.wdcount}, text = {self.text}"
