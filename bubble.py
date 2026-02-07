import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# Define node data as a list of dictionaries
nodes = [
    # Level 1 - Main categories
    {"id": 1, "name": "B-ALL", "size": 1200, "level": 1, "category": "B-ALL", "parent": None},
    {"id": 2, "name": "T-ALL", "size": 450, "level": 1, "category": "T-ALL", "parent": None},
    {"id": 3, "name": "AML", "size": 950, "level": 1, "category": "AML", "parent": None},
    
    # Level 2 - B-ALL subcategories
    {"id": 4, "name": "B-ALL with Recurrent\nGenetic Abnormalities", "size": 600, "level": 2, "category": "B-ALL", "parent": 1},
    {"id": 5, "name": "B-ALL with\nHyperdiploidy", "size": 400, "level": 2, "category": "B-ALL", "parent": 1},
    {"id": 6, "name": "Other B-ALL", "size": 200, "level": 2, "category": "B-ALL", "parent": 1},
    
    # Level 2 - T-ALL subcategories
    {"id": 7, "name": "Early T-cell Precursor\nALL (ETP-ALL)", "size": 185, "level": 2, "category": "T-ALL", "parent": 2},
    {"id": 8, "name": "Other T-ALL", "size": 265, "level": 2, "category": "T-ALL", "parent": 2},
    
    # Level 2 - AML subcategories
    {"id": 9, "name": "AML with Recurrent\nGenetic Abnormalities", "size": 350, "level": 2, "category": "AML", "parent": 3},
    {"id": 10, "name": "AML with\nMyelodysplasia", "size": 200, "level": 2, "category": "AML", "parent": 3},
    {"id": 11, "name": "AML, Not Otherwise\nSpecified", "size": 400, "level": 2, "category": "AML", "parent": 3},
    
    # Level 3 - B-ALL molecular subtypes
    {"id": 12, "name": "ETV6-RUNX1", "size": 180, "level": 3, "category": "B-ALL", "parent": 4},
    {"id": 13, "name": "BCR-ABL1", "size": 170, "level": 3, "category": "B-ALL", "parent": 4},
    {"id": 14, "name": "TCF3-PBX1", "size": 120, "level": 3, "category": "B-ALL", "parent": 4},
    {"id": 15, "name": "KMT2A-rearranged", "size": 130, "level": 3, "category": "B-ALL", "parent": 4},
    {"id": 16, "name": "High Hyperdiploid", "size": 280, "level": 3, "category": "B-ALL", "parent": 5},
    {"id": 17, "name": "Hypodiploid", "size": 120, "level": 3, "category": "B-ALL", "parent": 5},
    
    # Level 4 - BCR-ABL1 variants
    {"id": 18, "name": "p190 BCR-ABL1", "size": 110, "level": 4, "category": "B-ALL", "parent": 13},
    {"id": 19, "name": "p210 BCR-ABL1", "size": 60, "level": 4, "category": "B-ALL", "parent": 13},
    
    # Level 3 - T-ALL molecular subtypes
    {"id": 20, "name": "NOTCH1-mutated", "size": 185, "level": 3, "category": "T-ALL", "parent": 7},
    {"id": 21, "name": "TAL1-positive", "size": 135, "level": 3, "category": "T-ALL", "parent": 8},
    {"id": 22, "name": "TLX3-positive", "size": 130, "level": 3, "category": "T-ALL", "parent": 8},
    
    # Level 3 - AML molecular subtypes
    {"id": 23, "name": "AML with t(8;21)", "size": 145, "level": 3, "category": "AML", "parent": 9},
    {"id": 24, "name": "APL with PML-RARA", "size": 205, "level": 3, "category": "AML", "parent": 9},
    {"id": 25, "name": "AML with NPM1 mut", "size": 200, "level": 3, "category": "AML", "parent": 10},
    {"id": 26, "name": "AML with biallelic CEBPA", "size": 170, "level": 3, "category": "AML", "parent": 11},
    {"id": 27, "name": "AML with FLT3-ITD", "size": 230, "level": 3, "category": "AML", "parent": 11},
    
    # Level 4 - AML with t(8;21) variants
    {"id": 28, "name": "RUNX1-RUNX1T1", "size": 100, "level": 4, "category": "AML", "parent": 23},
    {"id": 29, "name": "variant t(8;21)", "size": 45, "level": 4, "category": "AML", "parent": 23}
]

# Create a directed graph
G = nx.DiGraph()

# Add nodes to the graph with attributes
for node in nodes:
    G.add_node(node['id'], **node)

# Add edges based on parent-child relationships
for node in nodes:
    if node['parent'] is not None:
        G.add_edge(node['parent'], node['id'])

# Define colors for each category
color_map = {'B-ALL': '#6BAED6', 'T-ALL': '#74C476', 'AML': '#FD8D3C'}

# Calculate positions for nodes
pos = {}
np.random.seed(42)  # For reproducibility

# Position nodes by level (x-axis) and category (y-axis)
level_spacing = 2.0
category_positions = {'B-ALL': 2, 'T-ALL': 1, 'AML': 0}

# Group nodes by level and category
nodes_by_level_category = {}
for node_id in G.nodes():
    level = G.nodes[node_id]['level']
    category = G.nodes[node_id]['category']
    key = (level, category)
    if key not in nodes_by_level_category:
        nodes_by_level_category[key] = []
    nodes_by_level_category[key].append(node_id)

# Assign positions
for key, node_ids in nodes_by_level_category.items():
    level, category = key
    base_x = level * level_spacing
    base_y = category_positions[category]
    
    # If more than one node in this group, spread them out
    if len(node_ids) > 1:
        for i, node_id in enumerate(node_ids):
            # Calculate vertical spread
            spread = 0.6
            offset = spread * (i / (len(node_ids) - 1) - 0.5)
            pos[node_id] = (base_x, base_y + offset)
    else:
        pos[node_ids[0]] = (base_x, base_y)

# Prepare the plot
plt.figure(figsize=(15, 10))

# Draw the edges
nx.draw_networkx_edges(G, pos, alpha=0.3, arrows=False)

# Draw the nodes with size based on patient numbers
node_sizes = [np.sqrt(G.nodes[n]['size']) * 50 for n in G.nodes()]
node_colors = [color_map[G.nodes[n]['category']] for n in G.nodes()]

nx.draw_networkx_nodes(G, pos, 
                      node_size=node_sizes,
                      node_color=node_colors,
                      alpha=0.7,
                      linewidths=1,
                      edgecolors='black')

# Draw node labels
labels = {n: f"{G.nodes[n]['name']}\n(n={G.nodes[n]['size']})" for n in G.nodes()}
nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_family='sans-serif', 
                        font_weight='bold', verticalalignment='center')

# Add a legend
handles = []
for cat, color in color_map.items():
    handles.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, 
                             markersize=15, label=cat))
plt.legend(handles=handles, loc='upper left', fontsize=12)

# Set title and remove axes
plt.title("Leukemia Classification Systems: Bubble Chart\nWHO to Molecular Subtypes", fontsize=16)
plt.axis('off')
plt.tight_layout()

# Save the figure
plt.savefig("leukemia_bubble_chart_python.png", dpi=300, bbox_inches='tight')

# Show the plot
plt.show()