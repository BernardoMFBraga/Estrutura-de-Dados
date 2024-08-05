import networkx as nx
import wikipediaapi
import matplotlib.pyplot as plt

# Configuração do cliente Wikipedia-API com User-Agent personalizado
user_agent = "projetoED (bernardo.braga@upe.br)"
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

def add_genre_hierarchy(graph, genres):
    for genre, subgenres in genres.items():
        graph.add_node(genre, type='genre')
        for subgenre in subgenres:
            graph.add_node(subgenre, type='subgenre')
            graph.add_edge(subgenre, genre, relation='é um subgênero de')

def add_cast_relationships(graph, film, cast):
    for person, role in cast.items():
        graph.add_node(person, type='person')
        graph.add_edge(person, film, relation=role)

def add_character_relationships(graph, film, characters):
    for character in characters:
        graph.add_node(character, type='character')
        graph.add_edge(character, film, relation='aparece em')

def add_temporal_relationships(graph, film, release_date):
    graph.add_node(release_date, type='date')
    graph.add_edge(film, release_date, relation='foi lançado em')

def add_location_relationships(graph, film, locations):
    for location in locations:
        graph.add_node(location, type='location')
        graph.add_edge(film, location, relation='foi filmado em')

def add_awards_relationships(graph, film, awards):
    for award, status in awards.items():
        graph.add_node(award, type='award')
        relation = 'ganhou o prêmio' if status == 'won' else 'foi indicado ao prêmio'
        graph.add_edge(film, award, relation=relation)

def fetch_film_data(film_title):
    film_page = get_wikipedia_page(film_title)
    if not film_page:
        return None
    
    # Para este exemplo, usaremos dados fictícios.
    return {
        "cast": {"Ator X": "atuou em", "Diretor Y": "dirigiu"},
        "characters": ["Personagem A", "Personagem B"],
        "release_date": "2024-07-31",
        "locations": ["Cidade Z", "País Q"],
        "awards": {"Oscar": "won", "Globo de Ouro": "nominated"}
    }

# Adicionando os filmes do artigo
film_title = "Os 100 melhores filmes do século XXI segundo a BBC"
film_page = get_wikipedia_page(film_title)

if film_page:
    G = nx.DiGraph()

    # Adicionando um nó para a página principal
    G.add_node(film_title, type='article')

    # Extraindo links para os filmes mencionados no artigo
    for link in film_page.links:
        G.add_node(link, type='film')
        G.add_edge(link, film_title, relation='mencionado em')

    # Ajustar o layout
    pos = nx.circular_layout(G)  # Layout circular
    pos[film_title] = [0, 0]  # Centralizar o título

    # Ajustar tamanhos
    node_size = 3000
    font_size = 8

    # Desenhar o grafo
    plt.figure(figsize=(14, 10))  # Aumentar o tamanho da figura
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=node_size, font_size=font_size, font_weight='bold', edge_color='gray', width=2)
    edge_labels = nx.get_edge_attributes(G, 'relation')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=font_size)

    plt.show()
else:
    print(f"A página {film_title} não existe na Wikipedia.")
