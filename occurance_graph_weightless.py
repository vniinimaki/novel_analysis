import nltk
import networkx as nx
import matplotlib.pyplot as plt
import powerlaw
import community as community_louvain
import matplotlib.cm as cm

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
                # Add the edge without weight
                G.add_edge(characters_in_sentence[i], characters_in_sentence[j])

# Generate the layout and draw the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, font_weight='bold')

plt.show()

# Calculate and print the number of nodes
num_nodes = G.number_of_nodes()
print(f'Number of nodes: {num_nodes}')

# Calculate and print the number of edges
num_edges = G.number_of_edges()
print(f'Number of edges: {num_edges}')


if nx.is_connected(G):
    diameter = nx.diameter(G)
    print(f'Diameter: {diameter}')
else:
    print('Graph is not connected, cannot calculate diameter.')

# Calculate the global clustering coefficient of the graph
global_clustering_coefficient = nx.average_clustering(G)
print(f'Global Clustering Coefficient: {global_clustering_coefficient}')

# Calculate the average shortest path length in the graph
# Note: this requires the graph to be connected
if nx.is_connected(G):
    avg_distance = nx.average_shortest_path_length(G)
    print(f'Average Distance: {avg_distance}')
else:
    print('Graph is not connected, cannot calculate average distance.')

# Find the smallest and largest components
components = nx.connected_components(G)
components = list(components)  # Convert to list for indexing
smallest_component = min(components, key=len)
largest_component = max(components, key=len)

print(f'Smallest Component: {smallest_component}')
print(f'Largest Component: {largest_component}')

# Calculate degree centrality for all nodes
degree_centrality = nx.degree_centrality(G)
# Get the nodes with the three highest degree centrality
highest_degree_centrality = sorted(degree_centrality, key=degree_centrality.get, reverse=True)[:3]

# Calculate closeness centrality for all nodes
closeness_centrality = nx.closeness_centrality(G)
# Get the nodes with the three highest closeness centrality
highest_closeness_centrality = sorted(closeness_centrality, key=closeness_centrality.get, reverse=True)[:3]

# Calculate betweenness centrality for all nodes
betweenness_centrality = nx.betweenness_centrality(G)
# Get the nodes with the three highest betweenness centrality
highest_betweenness_centrality = sorted(betweenness_centrality, key=betweenness_centrality.get, reverse=True)[:3]

print(f'Nodes with highest degree centrality: {highest_degree_centrality}')
print(f'Nodes with highest closeness centrality: {highest_closeness_centrality}')
print(f'Nodes with highest betweenness centrality: {highest_betweenness_centrality}')

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

# Fit power law to degree centrality distribution and calculate goodness of fit
fit_degree = powerlaw.Fit(list(degree_centrality.values()), discrete=True)
R_degree, p_degree = fit_degree.distribution_compare('power_law', 'exponential')
print(f'Degree Centrality: R = {R_degree}, p = {p_degree}')

# Fit power law to closeness centrality distribution and calculate goodness of fit
fit_closeness = powerlaw.Fit(list(closeness_centrality.values()), discrete=False)
R_closeness, p_closeness = fit_closeness.distribution_compare('power_law', 'exponential')
print(f'Closeness Centrality: R = {R_closeness}, p = {p_closeness}')

# Fit power law to betweenness centrality distribution and calculate goodness of fit
fit_betweenness = powerlaw.Fit(list(betweenness_centrality.values()), discrete=False)
R_betweenness, p_betweenness = fit_betweenness.distribution_compare('power_law', 'exponential')
print(f'Betweenness Centrality: R = {R_betweenness}, p = {p_betweenness}')

# Fit truncated power law to degree centrality distribution and calculate goodness of fit
R_degree, p_degree = fit_degree.distribution_compare('truncated_power_law', 'exponential', normalized_ratio=True)
print(f'Degree Centrality: R = {R_degree}, p = {p_degree}')

# Fit truncated power law to closeness centrality distribution and calculate goodness of fit
R_closeness, p_closeness = fit_closeness.distribution_compare('truncated_power_law', 'exponential', normalized_ratio=True)
print(f'Closeness Centrality: R = {R_closeness}, p = {p_closeness}')

# Fit truncated power law to betweenness centrality distribution and calculate goodness of fit
R_betweenness, p_betweenness = fit_betweenness.distribution_compare('truncated_power_law', 'exponential', normalized_ratio=True)
print(f'Betweenness Centrality: R = {R_betweenness}, p = {p_betweenness}')

# Compute the best partition using the Louvain method
partition = community_louvain.best_partition(G)

# Compute the modularity of the partition
modularity = community_louvain.modularity(partition, G)
print(f'Modularity: {modularity}')

# Create a color map for the communities
colors = [partition[node] for node in G.nodes()]

# Draw the graph with node color indicating community
nx.draw(G, pos, node_color=colors, with_labels=True, font_weight='bold')

plt.show()