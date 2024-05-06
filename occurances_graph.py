import nltk
import networkx as nx
import matplotlib.pyplot as plt
# Open the file with character names
with open('characters.txt', 'r', encoding='utf-8') as f:
    characters = [line.lower().strip().split(',') for line in f]

# Initialize a graph
G = nx.Graph()

# Add nodes to the graph
for character_list in characters:
    G.add_node(character_list[0])

# Open the second file
with open('count_of_monte_cristo.txt', 'r', encoding='utf-8') as f:
    # Read the entire file content
    text = f.read().lower()

# Tokenize the text into sentences
sentences = nltk.sent_tokenize(text)


# For each sentence, check if any of the aliases are in the sentence
for sentence in sentences:
    # Find all characters present in the sentence
    characters_in_sentence = [character_list[0] for character_list in characters if any(alias in sentence for alias in character_list)]
    # Add edges between all pairs of characters in the sentence
    for i in range(len(characters_in_sentence)):
        for j in range(i+1, len(characters_in_sentence)):
            if characters_in_sentence[i] != characters_in_sentence[j]:  # Check if the characters are different
                if G.has_edge(characters_in_sentence[i], characters_in_sentence[j]):
                    # if the edge already exists, increment the weight
                    G[characters_in_sentence[i]][characters_in_sentence[j]]['weight'] += 1
                else:
                    # else, create the edge with weight 1
                    G.add_edge(characters_in_sentence[i], characters_in_sentence[j], weight=1)




# Calculate the maximum weight
max_weight = max(G[u][v]['weight'] for u, v in G.edges())

# Normalize the weights to the range [0.1, 1] for visualization
edge_widths = [0.1 + 0.9 * (G[u][v]['weight'] / max_weight) for u, v in G.edges()]

# Generate the layout and draw the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, width=edge_widths, font_weight='bold')

# Draw edge labels
edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.show()

# Calculate the diameter of the graph
if nx.is_connected(G):
    diameter = nx.diameter(G)
    print(f'Diameter: {diameter}')
else:
    print('The graph is not connected. Cannot calculate diameter.')

# Calculate the global clustering coefficient of the graph
global_clustering_coefficient = nx.average_clustering(G)
print(f'Global Clustering Coefficient: {global_clustering_coefficient}')

# Calculate the average shortest path length (average distance) in the graph
if nx.is_connected(G):
    average_distance = nx.average_shortest_path_length(G)
    print(f'Average Distance: {average_distance}')
else:
    print('The graph is not connected. Cannot calculate average distance.')

# Find the smallest and largest components
components = nx.connected_components(G)
components = list(components)  # Convert to list for indexing
smallest_component = min(components, key=len)
largest_component = max(components, key=len)
print(f'Smallest Component: {smallest_component}')
print(f'Largest Component: {largest_component}')

degree_centrality = nx.degree_centrality(G)
top_3_degree_centrality = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:3]
print(f'Top 3 nodes by Degree Centrality: {top_3_degree_centrality}')

# Calculate closeness centrality for all nodes and find the top 3
closeness_centrality = nx.closeness_centrality(G)
top_3_closeness_centrality = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:3]
print(f'Top 3 nodes by Closeness Centrality: {top_3_closeness_centrality}')

# Calculate betweenness centrality for all nodes and find the top 3
betweenness_centrality = nx.betweenness_centrality(G)
top_3_betweenness_centrality = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:3]
print(f'Top 3 nodes by Betweenness Centrality: {top_3_betweenness_centrality}')

# Plot degree centrality distribution
plt.figure(figsize=(10, 6))
plt.hist(list(degree_centrality.values()), bins=20)
plt.title('Degree Centrality Distribution')
plt.xlabel('Degree Centrality')
plt.ylabel('Frequency')
plt.show()

# Plot closeness centrality distribution
plt.figure(figsize=(10, 6))
plt.hist(list(closeness_centrality.values()), bins=20)
plt.title('Closeness Centrality Distribution')
plt.xlabel('Closeness Centrality')
plt.ylabel('Frequency')
plt.show()

# Plot betweenness centrality distribution
plt.figure(figsize=(10, 6))
plt.hist(list(betweenness_centrality.values()), bins=20)
plt.title('Betweenness Centrality Distribution')
plt.xlabel('Betweenness Centrality')
plt.ylabel('Frequency')
plt.show()