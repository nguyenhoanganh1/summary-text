import re

from myapp.models.sentence import Sentence

WORD_PATTERN = r'<s docid="(.*?)" num="(.*?)" wdcount="(.*?)">(.*?)</s>'


def get_sentence(value):
    documents = []
    pattern = re.compile(WORD_PATTERN)
    matches = re.finditer(pattern, value)
    for match in matches:
        doc_id = match.group(1)
        num = match.group(2)
        wd_count = match.group(3)
        text = match.group(4)
        documents.append(Sentence(doc_id.strip(), int(num), int(wd_count), text.lower().strip()))
    return documents

