"""Python implementation of the TextRank algoritm.
From this paper:
    https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf
Based on:
    https://gist.github.com/voidfiles/1646117
    https://github.com/davidadamojr/TextRank
"""
import editdistance
import io
import itertools
import networkx as nx
import nltk
import os


def setup_environment():
    """Download required resources."""
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    print('Completed resource downloads.')


def _filter_for_tags(tagged, tags=['NN', 'NNP']):
    """Apply syntactic filters based on POS tags."""
    return [item for item in tagged if item[1] in tags]


def _normalize(tagged):
    """Return a list of tuples with the first item's periods removed."""
    return [(item[0].replace('.', ''), item[1]) for item in tagged]


def _unique_everseen(iterable, key=None):
    """List unique elements in order of appearance.
    Examples:
        _unique_everseen('AAAABBBCCDAABBB') --> A B C D
        _unique_everseen('ABBCcAD', str.lower) --> A B C D
    """
    seen = set()
    seen_add = seen.add
    if key is None:
        def key(x): return x
    for element in iterable:
        k = key(element)
        if k not in seen:
            seen_add(k)
            yield element


def _build_graph(nodes):
    """Return a networkx graph instance.
    :param nodes: List of hashables that represent the nodes of a graph.
    """
    gr = nx.Graph()  # initialize an undirected graph
    gr.add_nodes_from(nodes)
    nodePairs = list(itertools.combinations(nodes, 2))

    # add edges to the graph (weighted by Levenshtein distance)
    for pair in nodePairs:
        firstString = pair[0]
        secondString = pair[1]
        levDistance = editdistance.eval(firstString, secondString)
        gr.add_edge(firstString, secondString, weight=levDistance)

    return gr


def extract_key_phrases(text, top_n=0, tags=['NN', 'JJ', 'NNP']):
    """Return a set of key phrases.
    :param text: A string.
    """
    # tokenize the text using nltk
    word_tokens = nltk.word_tokenize(text)

    # assign POS tags to the words in the text
    if os.getcwd() not in nltk.data.path:
        nltk.data.path.append(os.getcwd())
    tagged = nltk.pos_tag(word_tokens)
    textlist = [x[0] for x in tagged]

    tagged = _filter_for_tags(tagged, tags)
    tagged = _normalize(tagged)

    unique_word_set = _unique_everseen(tagged, key=lambda x: x[0])
    word_set_list = list(unique_word_set)

    tag_lookup_table = {}
    for word, tag in word_set_list:
        tag_lookup_table[word] = tag

    # this will be used to determine adjacent words in order to construct
    # keyphrases with two words

    graph = _build_graph([x[0] for x in word_set_list])

    # pageRank - initial value of 1.0, error tolerance of 0,0001,
    calculated_page_rank = nx.pagerank(graph, weight='weight')

    # most important words in ascending order of importance
    keyphrases = sorted(calculated_page_rank, key=calculated_page_rank.get,
                        reverse=True)

    # the number of keyphrases returned will be relative to the size of the
    # text (a third of the number of vertices)
    one_third = len(word_set_list) // 3
    keyphrases = keyphrases[0:one_third + 1]

    # take keyphrases with multiple words into consideration as done in the
    # paper - if two words are adjacent in the text and are selected as
    # keywords, join them together
    modified_key_phrases = set([])

    i = 0
    while i < len(textlist):
        w = textlist[i]
        if w in keyphrases:
            phrase_ws = [w]
            i += 1
            while i < len(textlist) and textlist[i] in keyphrases:
                phrase_ws.append(textlist[i])
                i += 1

            phrase = ' '.join(phrase_ws)
            if phrase not in modified_key_phrases:
                modified_key_phrases.add(phrase)
        else:
            i += 1
    top_n = len(modified_key_phrases) if top_n == 0 else top_n
    modified_key_phrases = list(modified_key_phrases)[0: top_n]
    tagged_keyphrases = []
    for kw in modified_key_phrases:
        try:
            tagged_keyphrases.append((kw, tag_lookup_table[kw]))
        except Exception:
            tagged_keyphrases.append((kw, 'NNP'))
    return tagged_keyphrases

def extract_sentences(text, summary_length=100, clean_sentences=True, language='english'):
    """Return a paragraph formatted summary of the source text.
    :param text: A string.
    """
    if os.getcwd() not in nltk.data.path:
        nltk.data.path.append(os.getcwd())
    sent_detector = nltk.data.load('tokenizers/punkt/'+language+'.pickle')
    sentence_tokens = sent_detector.tokenize(text.strip())
    graph = _build_graph(sentence_tokens)

    calculated_page_rank = nx.pagerank(graph, weight='weight')

    # most important sentences in ascending order of importance
    sentences = sorted(calculated_page_rank, key=calculated_page_rank.get,
                       reverse=True)

    # return a 100 word summary
    summary = ' '.join(sentences)
    summary_words = summary.split()
    summary_words = summary_words[0:summary_length]
    dot_indices = [idx for idx, word in enumerate(summary_words) if word.find('.') != -1]
    if clean_sentences and dot_indices:
        last_dot = max(dot_indices) + 1
        summary = ' '.join(summary_words[0:last_dot])
    else:
        summary = ' '.join(summary_words)

    return summary


def _write_files(summary, key_phrases, filename):
    """Write key phrases and summaries to a file."""
    print("Generating output to " + 'keywords/' + filename)
    key_phrase_file = io.open('keywords/' + filename, 'w')
    for key_phrase in key_phrases:
        key_phrase_file.write(key_phrase + '\n')
    key_phrase_file.close()

    print("Generating output to " + 'summaries/' + filename)
    summary_file = io.open('summaries/' + filename, 'w')
    summary_file.write(summary)
    summary_file.close()

    print("-")


def summarize_all():
    # retrieve each of the articles
    articles = os.listdir("articles")
    for article in articles:
        print('Reading articles/' + article)
        article_file = io.open('articles/' + article, 'r')
        text = article_file.read()
        keyphrases = extract_key_phrases(text)
        summary = extract_sentences(text)
        _write_files(summary, keyphrases, article)