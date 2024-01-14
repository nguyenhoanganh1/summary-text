import os

import numpy as np
from django.shortcuts import render

from myapp.page_rank_hadler.handler import sentence_count, get_score_page_rank
from myapp.helper.replacer import get_sentence

stop_words = ["a", "able", "about", "after", "all", "also", "am",
              "an", "and", "any", "are", "as", "at", "be", "been", "but", "by", "can", "cannot", "could", "did",
              "do", "does", "either", "else", "ever", "every", "for", "from", "get", "got", "had",
              "has", "have", "he", "her", "hers", "him", "his", "how", "I",
              "if", "in", "into", "is", "it", "its", "just", "let", "like", "likely", "may", "me",
              "might", "most", "must", "my", "neither", "no", "not", "of", "off",
              "often", "on", "only", "or", "other", "our", "own", "said", "say", "says", "she",
              "should", "so", "some", "than", "that", "the", "their", "them", "then", "there",
              "these", "they", "this", "they're", "to", "too", "that's", "us", "was", "we", "were",
              "what", "when", "where", "which", "while", "who", "whom", "why", "will", "with",
              "would", "yet", "you", "your", "you're"]


def summary_document(request):
    input_folder = "DUC_TEXT"
    output_folder = "Summaries"
    document_by_doc_id = {}
    stopWord = stop_words

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        output_file_path = f"{output_folder}/{filename}"

        with open(os.path.join(input_folder, filename), 'r', encoding='utf-8') as file:
            file_content = file.read()

            sentence = get_sentence(file_content)
            print(f"sentence: {sentence}")

            for sen in sentence:
                docId = sen.docId
                if docId not in document_by_doc_id:
                    document_by_doc_id[docId] = {"docId": docId, "sens": []}
                document_by_doc_id[docId]["sens"].append(sen)

            content_html = ""

            for docId, sens in document_by_doc_id.items():
                print(f"docId  = {docId}, sens = {sens}")
                # flattened_sens = [item for sublist in sens for item in sublist]

                sen = sens.get('sens')
                matrix_sens = np.zeros([len(sen), len(sen)])

                for i in range(len(sen)):
                    for j in range(len(sen)):
                        if i != j:
                            matrix_sens[i][j] = sentence_count(sen[i], sen[j], stopWords=stopWord, stopNum=1)

                print(f"matrix_se = \n{matrix_sens}")

                page_rank_scores = get_score_page_rank(matrix_sens)

                sentences_with_scores = list(zip(page_rank_scores, sen))

                with open(output_file_path, 'a', encoding='utf-8') as output_file:
                    for score, sen in sentences_with_scores:
                        if score < 0.16:
                            print(f"score = {score}, sentence = {sen.text}")
                            result = f"<s docid='{docId}' num='{sen.num}' wdcount='{sen.wdcount}'> {sen.text}</s> \n"
                            output_file.write(result)

    return render(request, 'summary-text.html')
