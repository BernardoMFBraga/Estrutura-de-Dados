import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from bs4 import BeautifulSoup
import requests
import re
import spacy
from spacy.matcher import Matcher

# Verificar se o modelo está instalado, caso contrário, instalar
try:
    nlp = spacy.load('pt_core_news_sm')
except OSError:
    from spacy.cli import download
    download('pt_core_news_sm')
    nlp = spacy.load('pt_core_news_sm')

# URL da Wikipedia
url = "https://pt.wikipedia.org/wiki/Lista_de_medalhas_brasileiras_nos_Jogos_Ol%C3%ADmpicos#Medalhistas"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Encontrar as tabelas com medalhas
tables = soup.find_all('table', {'class': 'wikitable'})

# Função para limpar e normalizar textos
def clean_text(text):
    text = text.strip()
    text = re.sub(r'\[.*?\]', '', text)  # Remove referências entre colchetes
    text = text.replace('\xa0', ' ')  # Remove caracteres não quebra de linha
    return text

# Função para extrair dados das tabelas com limpeza e validação
def extract_medals_data(tables):
    data = []
    for table in tables:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skip header row
            cells = row.find_all('td')
            if len(cells) >= 4:  # Verificar se há células suficientes
                year = clean_text(cells[0].get_text())
                athlete = clean_text(cells[1].get_text())
                sport = clean_text(cells[2].get_text())
                medal = clean_text(cells[3].get_text())
                # Verificar se as células não estão vazias
                if year and athlete and sport and medal:
                    data.append([year, athlete, sport, medal])
    return pd.DataFrame(data, columns=['Year', 'Athlete', 'Sport', 'Medal'])

# Extração de dados com tratamento de erro
try:
    df = extract_medals_data(tables)
except Exception as e:
    print(f"Erro ao extrair dados das tabelas: {e}")
    df = pd.DataFrame(columns=['Year', 'Athlete', 'Sport', 'Medal'])

# Função para identificar entidades com PLN
def extract_entities(text):
    doc = nlp(text)
    entities = {ent.text: ent.label_ for ent in doc.ents}
    return entities

# Função para criar o grafo geral
def create_graph(df):
    G = nx.DiGraph()
    for index, row in df.iterrows():
        try:
            athlete = row['Athlete']
            sport = row['Sport']
            medal = row['Medal']
            year = row['Year']
            
            # Adicionar nós com propriedades
            G.add_node(athlete, type='athlete')
            G.add_node(sport, type='sport')
            G.add_node(medal, type='medal')
            G.add_node(year, type='year')

            # Adicionar arestas com propriedades
            G.add_edge(athlete, medal, relation='ganhou')
            G.add_edge(athlete, sport, relation='competiu em')
            G.add_edge(athlete, year, relation='participou em')
        except Exception as e:
            print(f"Erro ao processar a linha {index}: {e}")
    return G

# Funções para manipulação do grafo

def add_node(G, node, node_type, color='skyblue'):
    if not G.has_node(node):
        G.add_node(node, type=node_type, color=color)
    else:
        print(f"Nó {node} já existe.")

def add_edge(G, source, target, relation):
    if G.has_node(source) and G.has_node(target):
        G.add_edge(source, target, relation=relation)
    else:
        print(f"Nós {source} e/ou {target} não existem.")

def get_node_attributes(G, node):
    return G.nodes[node] if G.has_node(node) else None

def get_edge_attributes(G, source, target):
    return G.get_edge_data(source, target) if G.has_edge(source, target) else None

def visualize_graph(G, title='Grafo'):
    try:
        plt.figure(figsize=(20, 15))
        
        # Definir o layout do grafo
        pos = nx.spring_layout(G, k=0.4, iterations=200, seed=42)
        
        # Obter a cor dos nós com base no tipo
        node_colors = [nx.get_node_attributes(G, 'color').get(node, 'skyblue') for node in G.nodes]
        edge_color = "black"
        node_size = 3000
        font_size = 12

        # Desenhar o grafo
        nx.draw(
            G, pos,
            with_labels=True,
            node_color=node_colors,
            edge_color=edge_color,
            node_size=node_size,
            font_size=font_size,
            font_color='black',
            connectionstyle='arc3,rad=0.1'
        )
        
        # Adicionar rótulos das arestas
        edge_labels = nx.get_edge_attributes(G, 'relation')
        nx.draw_networkx_edge_labels(
            G, pos,
            edge_labels=edge_labels,
            font_size=font_size,
            font_color='black'
        )
        
        # Adicionar uma legenda para os tipos de nós
        node_types = set(nx.get_node_attributes(G, 'type').values())
        colors = {'athlete': 'lightgreen', 'sport': 'lightblue', 'medal': 'lightcoral', 'year': 'lightyellow'}
        
        legend_elements = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors[node_type], markersize=10, label=node_type.capitalize()) for node_type in node_types]
        plt.legend(handles=legend_elements, loc='best')

        plt.title(title, fontsize=16)
        plt.show()
        
    except Exception as e:
        print(f"Erro ao visualizar o grafo: {e}")


# Análise de texto extra
def analyze_text(text):
    entities = extract_entities(text)
    for entity, label in entities.items():
        print(f"Entidade: {entity}, Tipo: {label}")
        # Adiciona as novas entidades ao grafo
        add_node(G, entity, label.lower())

        # Definindo as relações com base no tipo de entidade
        if label == 'MISC':
            add_edge(G, 'Jogos Olímpicos', entity, 'relacionado com')
        elif label == 'ORG':
            add_edge(G, 'Comitê Olímpico Brasileiro', entity, 'relacionado com')
        elif label == 'LOC':
            add_edge(G, 'Brasil', entity, 'localizado em')
        elif label == 'PER':
            add_edge(G, 'Atletas', entity, 'é um')
        elif label == 'EVENT':
            add_edge(G, 'Eventos Olímpicos', entity, 'ocorre em')

# Criar o grafo geral
if not df.empty:
    G = create_graph(df)
    # Adicionar um novo nó e aresta para exemplo
    add_node(G, 'Bernardo Braga', 'athlete', color='lightgreen')
    # Adicionar um nó de medalha exemplo, se necessário
    add_node(G, 'Medalha Exemplo', 'medal')
    # Adicionar a aresta após adicionar ambos os nós
    add_edge(G, 'Bernardo Braga', 'Medalha Exemplo', 'ganhou')
    visualize_graph(G)
else:
    print("Nenhum dado disponível para criar o grafo.")

# Exemplos de uso das novas funções
add_node(G, 'Outro Atleta', 'athlete', color='lightcoral')
# Adicionar um nó de medalha exemplo, se necessário
add_node(G, 'Medalha Exemplo 2', 'medal')
# Adicionar a aresta após adicionar ambos os nós
add_edge(G, 'Outro Atleta', 'Medalha Exemplo 2', 'ganhou')
print(get_node_attributes(G, 'Outro Atleta'))
print(get_edge_attributes(G, 'Outro Atleta', 'Medalha Exemplo 2'))

# Analisar o texto adicional
text = """
A lista abaixo é uma lista de medalhas brasileiras nos Jogos Olímpicos, contando com várias modalidades e eventos.
O Comitê Olímpico Brasileiro tem se esforçado para melhorar o desempenho dos atletas. 
O Brasil tem se destacado em diversos esportes e conquistado medalhas em várias edições dos Jogos Olímpicos.
"""
analyze_text(text)

# Visualizar o grafo atualizado
visualize_graph(G, title='Grafo Atualizado com Texto Adicional')
