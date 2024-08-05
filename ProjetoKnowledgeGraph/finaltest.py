# Importar bibliotecas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import spacy
from spacy import displacy
import textacy
import networkx as nx
import wikipediaapi

# Definir o tópico e criar uma instância da API
user_agent = "ProjetoED (bernardo.braga@upe.br)"
wiki_wiki = wikipediaapi.Wikipedia(
    language='pt',
    user_agent=user_agent
)

def get_wikipedia_page(title):
    page = wiki_wiki.page(title)
    if page.exists():
        return page
    else:
        print(f"A página {title} não existe na Wikipedia.")
        return None

# Obter a página da Wikipedia
tópico = "Lista de medalhas brasileiras nos Jogos Olímpicos"
página = wiki_wiki.page(tópico)

# Obter o texto da página excluindo a seção de Medalhistas por estado de nascimento e referências
txt = página.text[:página.text.find("Medalhistas por estado de nascimento")]
print(txt[:500])  # Mostrar um trecho do texto para verificação

# Inicializar o modelo SpaCy
nlp = spacy.load("pt_core_news_sm")

# Processar o texto com SpaCy
doc = nlp(txt)

# Segmentação de frases
lst_docs = [sent for sent in doc.sents]
print("Total de frases:", len(lst_docs))

# Análise POS e DEP
for token in lst_docs[0]:
    print(token.text, "-->", "POS:", token.pos_, "|", "DEP:", token.dep_)

# Visualizar análise de dependência
displacy.render(lst_docs[0], style="dep", options={"distance": 100})

# Reconhecimento de Entidades
for ent in lst_docs[0].ents:
    print(ent.text, f"({ent.label_})")
    
# Visualizar entidades
displacy.render(lst_docs[0], style="ent")

# Função para extrair entidades
def extract_entities(doc):
    a, b, prev_dep, prev_txt, prefix, modificador = "", "", "", "", "", ""
    for token in doc:
        if token.dep_ != "punct":
            if token.dep_ == "compound":
                prefix = prev_txt + " " + token.text if prev_dep == "compound" else token.text
            if token.dep_.endswith("mod"):
                modificador = prev_txt + " " + token.text if prev_dep == "compound" else token.text
            if "subj" in token.dep_:
                a = modificador + " " + prefix + " " + token.text
                prefix, modificador, prev_dep, prev_txt = "", "", "", ""
            if "obj" in token.dep_:
                b = modificador + " " + prefix + " " + token.text
            prev_dep, prev_txt = token.dep_, token.text
    a = " ".join([i for i in a.split()])
    b = " ".join([i for i in b.split()])
    return (a.strip(), b.strip())

# Função para extrair relações
def extract_relation(doc, nlp):
    matcher = spacy.matcher.Matcher(nlp.vocab)
    p1 = [{'DEP': 'ROOT'}, {'DEP': 'prep', 'OP': "?"}, {'DEP': 'agent', 'OP': "?"}, {'POS': 'ADJ', 'OP': "?"}]
    matcher.add(key="matching_1", patterns=[p1])
    matches = matcher(doc)
    k = len(matches) - 1
    span = doc[matches[k][1]:matches[k][2]]
    return span.text

# Criar um DataFrame com as entidades e relações extraídas
dic = {"id": [], "texto": [], "entidade": [], "relação": [], "objeto": []}
for n, sent in enumerate(lst_docs):
    lst_generators = list(textacy.extract.subject_verb_object_triples(sent))
    for sent in lst_generators:
        subj = "_".join(map(str, sent.subject))
        obj = "_".join(map(str, sent.object))
        relação = "_".join(map(str, sent.verb))
        dic["id"].append(n)
        dic["texto"].append(sent.text)
        dic["entidade"].append(subj)
        dic["objeto"].append(obj)
        dic["relação"].append(relação)

dtf = pd.DataFrame(dic)

# Criar e plotar o grafo
G = nx.from_pandas_edgelist(dtf, source="entidade", target="objeto", edge_attr="relação", create_using=nx.DiGraph())

plt.figure(figsize=(15, 10))
pos = nx.spring_layout(G, k=1)
nx.draw(G, pos=pos, with_labels=True, node_color="skyblue", edge_color="black", node_size=2000, connectionstyle='arc3,rad=0.1')
nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=nx.get_edge_attributes(G, 'relação'), font_size=12, font_color='black', alpha=0.6)
plt.show()

# Filtrar entidades mais frequentes
f = "Rússia"
tmp = dtf[(dtf["entidade"] == f) | (dtf["objeto"] == f)]

# Criar um gráfico filtrado
G_filtered = nx.from_pandas_edgelist(tmp, source="entidade", target="objeto", edge_attr="relação", create_using=nx.DiGraph())

# Plotar o gráfico filtrado
plt.figure(figsize=(15, 10))
pos = nx.spring_layout(G_filtered, k=1)  # Alterado para spring_layout
node_color = ["red" if node == f else "skyblue" for node in G_filtered.nodes]
edge_color = ["red" if edge[0] == f else "black" for edge in G_filtered.edges]

nx.draw(G_filtered, pos=pos, with_labels=True, node_color=node_color, edge_color=edge_color, node_size=2000, connectionstyle='arc3,rad=0.1')
nx.draw_networkx_edge_labels(G_filtered, pos=pos, edge_labels=nx.get_edge_attributes(G_filtered, 'relação'), font_size=12, font_color='black', alpha=0.6)
plt.show()
