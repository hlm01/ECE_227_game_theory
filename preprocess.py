import os
import json
import time
import networkx as nx
import pickle

json_root = "reply_networks"
json_files = [os.path.join(json_root, f) for f in os.listdir(json_root)]

FILENAME = "haskell"
combined_edges = []

print("Starting to process dictionaries and gather edges...")
start_time_processing = time.time()


with open(os.path.join(json_root, f"{FILENAME}.json"), "r") as f:
    data_dict = json.load(f)
data_dict = data_dict[0]
for source_node, target_nodes in data_dict.items():
    for target_node in target_nodes:
        combined_edges.append((source_node, target_node))

processing_time = time.time() - start_time_processing
print(
    f"Time taken to process dictionaries and create edge list: {processing_time:.4f} seconds"
)
print(f"Total number of edges collected: {len(combined_edges)}")

print("\nCreating graph from combined edge list using NetworkX...")
start_time_graph_creation = time.time()

graph = nx.DiGraph()
graph.add_edges_from(combined_edges)

graph_creation_time = time.time() - start_time_graph_creation
print(f"Time taken for NetworkX graph creation: {graph_creation_time:.4f} seconds")
print(f"Number of nodes in the graph: {graph.number_of_nodes()}")
print(f"Number of edges in the graph: {graph.number_of_edges()}")
graph = graph.to_undirected()
pos = nx.spring_layout(graph, k=0.7, seed=42)
graph.remove_edges_from(nx.selfloop_edges(graph))
degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)
average_degree = sum(degree_sequence) / len(degree_sequence) if degree_sequence else 0
print(f"Average degree of the graph: {average_degree:.4f}")

print("\nSaving graph to file...")

with open(f"{FILENAME}.pkl", "wb") as f:
    pickle.dump((graph, pos), f)
print(f"Graph saved to {FILENAME}.pkl")
