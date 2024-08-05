import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import wikipediaapi
import spacy
import textacy
import networkx as nx
import dateparser

topic = "Russo-Ukrainian War"
wiki = wikipediaapi.Wikipedia('en')
page = wiki.page(topic)
txt = page.text[:page.text.find("See also")]

nlp = spacy.load("en_core_web_sm")
doc = nlp(txt)

def extract_entities(doc):
    a, b, prev_dep, prev_txt, prefix, modifier = "", "", "", "", "", ""
    for token in doc:
        if token.dep_ != "punct":
            if token.dep_ == "compound":
                prefix = prev_txt + " " + token.text if prev_dep == "compound" else token.text
            if token.dep_.endswith("mod"):
                modifier = prev_txt + " " + token.text if prev_dep == "compound" else token.text
            if token.dep_.find("subj") != -1:
                a = modifier + " " + prefix + " " + token.text
                prefix, modifier, prev_dep, prev_txt = "", "", "", ""
            if token.dep_.find("obj") != -1:
                b = modifier + " " + prefix + " " + token.text
            prev_dep, prev_txt = token.dep_, token.text
    a = " ".join([i for i in a.split()])
    b = " ".join([i for i in b.split()])
    return (a.strip(), b.strip())

def extract_relation(doc, nlp):
    matcher = spacy.matcher.Matcher(nlp.vocab)
    p1 = [{'DEP':'ROOT'}, {'DEP':'prep', 'OP':"?"}, {'DEP':'agent', 'OP':"?"}, {'POS':'ADJ', 'OP':"?"}]
    matcher.add(key="matching_1", patterns=[p1])
    matches = matcher(doc)
    k = len(matches) - 1
    span = doc[matches[k][1]:matches[k][2]]
    return span.text

dic = {"id":[], "text":[], "entity":[], "relation":[], "object":[]}
for n, sentence in enumerate(doc.sents):
    lst_generators = list(textacy.extract.subject_verb_object_triples(sentence))
    for sent in lst_generators:
        subj = "_".join(map(str, sent.subject))
        obj = "_".join(map(str, sent.object))
        relation = "_".join(map(str, sent.verb))
        dic["id"].append(n)
        dic["text"].append(sentence.text)
        dic["entity"].append(subj)
        dic["object"].append(obj)
        dic["relation"].append(relation)

df = pd.DataFrame(dic)

G = nx.from_pandas_edgelist(df, source="entity", target="object", edge_attr="relation", create_using=nx.DiGraph())

# Desenho do Grafo
plt.figure(figsize=(15,10))
pos = nx.spring_layout(G, k=1)
node_color = "skyblue"
edge_color = "black"
nx.draw(G, pos=pos, with_labels=True, node_color=node_color, edge_color=edge_color, cmap=plt.cm.Dark2, node_size=2000, connectionstyle='arc3,rad=0.1')
nx.draw_networkx_edge_labels(G, pos=pos, label_pos=0.5, edge_labels=nx.get_edge_attributes(G, 'relation'), font_size=12, font_color='black', alpha=0.6)
plt.show()
