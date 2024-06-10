# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 19:46:16 2024

@author: IvanL
"""
import heapq
import matplotlib.pyplot as plt
import networkx as nx

class Grafo:
    def __init__(self):
        self.grafo = {}

    def agregar_vertice(self, vertice):
        if vertice not in self.grafo:
            self.grafo[vertice] = {}

    def agregar_arista(self, desde, hacia, peso):
        self.grafo[desde][hacia] = peso
        self.grafo[hacia][desde] = peso  # Para grafos no dirigidos

    def prim(self, inicio):
        mst = []
        visitados = set([inicio])
        aristas = [(peso, inicio, hacia) for hacia, peso in self.grafo[inicio].items()]
        heapq.heapify(aristas)
        paso_a_paso = []

        while aristas:
            peso, desde, hacia = heapq.heappop(aristas)
            if hacia not in visitados:
                visitados.add(hacia)
                mst.append((desde, hacia, peso))

                for siguiente, p in self.grafo[hacia].items():
                    if siguiente not in visitados:
                        heapq.heappush(aristas, (p, hacia, siguiente))
            
            # Guardar el estado actual del MST para graficar después
            paso_a_paso.append((list(visitados), list(mst)))

        return mst, paso_a_paso

    def graficar_resultado(self, mst):
        G = nx.Graph()
        for vertice in self.grafo:
            G.add_node(vertice)
        for vertice in self.grafo:
            for vecino, peso in self.grafo[vertice].items():
                G.add_edge(vertice, vecino, weight=peso)

        pos = nx.spring_layout(G)

        # Dibujar el grafo original
        plt.figure(figsize=(10, 7))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=700)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.title('Grafo Original')
        plt.show()

        # Dibujar el MST final
        mst_G = nx.Graph()
        mst_G.add_edges_from([(u, v) for u, v, w in mst])
        plt.figure(figsize=(10, 7))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=700, alpha=0.3)
        nx.draw(mst_G, pos, with_labels=True, node_color='lightgreen', node_size=700, edge_color='red')
        edge_labels = {(u, v): f'{w}' for u, v, w in mst}
        nx.draw_networkx_edge_labels(mst_G, pos, edge_labels=edge_labels, font_color='red')
        plt.title('Árbol de Expansión Mínima')
        plt.show()

# Ejemplo de uso
grafo = Grafo()
grafo.agregar_vertice('A')
grafo.agregar_vertice('B')
grafo.agregar_vertice('C')
grafo.agregar_vertice('D')
grafo.agregar_vertice('E')

grafo.agregar_arista('A', 'B', 1)
grafo.agregar_arista('A', 'C', 3)
grafo.agregar_arista('B', 'C', 1)
grafo.agregar_arista('B', 'D', 6)
grafo.agregar_arista('C', 'D', 4)
grafo.agregar_arista('C', 'E', 2)
grafo.agregar_arista('D', 'E', 5)

mst, pasos = grafo.prim('A')
print("Árbol de Expansión Mínima:", mst)

grafo.graficar_resultado(mst)


