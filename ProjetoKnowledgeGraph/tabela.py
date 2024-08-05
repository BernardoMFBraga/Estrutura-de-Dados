import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import wikipediaapi
from bs4 import BeautifulSoup
import re

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

# Função para limpar e transformar texto
def clean_text(text):
    # Remover hiperlinks e números
    text = BeautifulSoup(text, "html.parser").text
    text = ''.join([i for i in text if not i.isdigit()]).strip()
    return text

# Obter a página da Wikipedia
tópico = "Lista de medalhas brasileiras nos Jogos Olímpicos"
página = get_wikipedia_page(tópico)

if página:
    # Obter o HTML da página
    html = página.text
    soup = BeautifulSoup(html, 'html.parser')  # Use 'html.parser' para análise mais robusta

    # Definir os intervalos das tabelas
    intervalos = [
        ("Medalhistas", "Medalhistas em esportes de demonstração")
    ]

    # Encontrar todas as seções
    sections = soup.find_all('span', {'class': 'mw-headline'})
    section_titles = [section.get_text() for section in sections]
    print("Títulos das Seções Encontradas:", section_titles)

    # Criar um DataFrame para armazenar as relações extraídas
    dic = {"entidade": [], "objeto": [], "relação": []}

    # Função para encontrar o índice de uma seção
    def find_section_index(title):
        for idx, section in enumerate(section_titles):
            if section == title:
                return idx
        return None

    # Extração de tabelas entre intervalos
    def extract_tables(start_marker, end_marker):
        start_idx = find_section_index(start_marker)
        end_idx = find_section_index(end_marker)
        
        if start_idx is not None and end_idx is not None:
            print(f"Extraindo tabelas entre '{start_marker}' e '{end_marker}'")
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    cols = [clean_text(ele.text.strip()) for ele in cols]
                    if len(cols) >= 3:  # Verificar se há pelo menos 3 colunas
                        atleta = cols[0]
                        medalha = cols[1]
                        esporte = cols[2]
                        
                        # Adicionar relações ao DataFrame
                        dic["entidade"].append(atleta)
                        dic["objeto"].append(medalha)
                        dic["relação"].append("ganhou")
                        
                        dic["entidade"].append(atleta)
                        dic["objeto"].append(esporte)
                        dic["relação"].append("foi campeão de")

    # Extrair dados para cada intervalo
    for start_marker, end_marker in intervalos:
        extract_tables(start_marker, end_marker)

    # Criar um DataFrame com as relações extraídas
    dtf = pd.DataFrame(dic)

    # Garantir que todas as colunas relevantes sejam strings
    dtf['entidade'] = dtf['entidade'].astype(str)
    dtf['objeto'] = dtf['objeto'].astype(str)

    # Verificar se o DataFrame contém dados
    print("Total de relações extraídas:", len(dtf))
    print(dtf.head())

    # Função para criar e desenhar o grafo
    def criar_e_desenhar_grafo(dtf):
        G = nx.DiGraph()

        # Adicionar nós e arestas ao grafo
        for idx, row in dtf.iterrows():
            entidade = row['entidade']
            objeto = row['objeto']
            G.add_node(entidade)
            G.add_node(objeto)
            G.add_edge(entidade, objeto, label=row['relação'])

        # Desenhar o grafo
        plt.figure(figsize=(15, 10))
        pos = nx.spring_layout(G, seed=42)  # Define um seed para a disposição dos nós
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_weight="bold", edge_color="gray")
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

        plt.title("Grafo de Relações Olímpicas")
        plt.show()

    # Chamar a função para criar e desenhar o grafo
    criar_e_desenhar_grafo(dtf)
else:
    print("Não foi possível obter a página da Wikipedia.")
