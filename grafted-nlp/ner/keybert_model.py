from keybert import KeyBERT
import time
from keyphrase_vectorizers import KeyphraseCountVectorizer
from transformers import AutoTokenizer

model_names = ['all-MiniLM-L6-v2', 'allenai/scibert_scivocab_uncased', 'sentence-transformers/all-roberta-large-v1',
               'bert-base-uncased', 'microsoft/codebert-base', 'google/electra-small-discriminator', 'microsoft/codebert-base-mlm']

vectorizer = KeyphraseCountVectorizer()

doc = ''
with open('data/processed/ner/test.txt', 'r') as file:
    doc = file.read()
lists = []

for bert in model_names:
    try:
        kw_model = KeyBERT(model=bert)
        bts = time.time()
        keywords = kw_model.extract_keywords(
            doc, keyphrase_ngram_range=(1, 2), use_maxsum=True, diversity=0.7, vectorizer=vectorizer, top_n=10)
        cts = time.time()
        print(keywords)
        ts = round(cts-bts, 2)
        print(ts)
        lists.append([keywords, ts, bert])
    except Exception as e:
        print("error at %s" % bert)
        print(e)

with open('results.txt', 'w') as f:
    for item in lists:
        f.write("bert:%s,  time:%s\n" % (item[2], item[1]))
        f.write((', ').join([x[0] if len(x) > 1 else x for x in item[0]]))
        f.write('\n\n')
