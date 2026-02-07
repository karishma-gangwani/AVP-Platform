import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

# Define hierarchical data
data = [
    # Level 1 - Main categories
    {"id": "BCP-ALL", "parent": "", "value": 3854, "label": "BCP-ALL (n=3854)"},
    {"id": "T-ALL", "parent": "", "value": 1666, "label": "T-ALL (n=1666)"},
    {"id": "AML", "parent": "", "value": 150, "label": "AML (n=150)"},

    # Level 2 - assay availability
    # {"id": "Paired WGS", "parent": "BCP-ALL", "value": 2094, "label": "Yes Paired WGS (n=2094)"},
    # {"id": "Paired WGS", "parent": "BCP-ALL", "value": 1760, "label": "No Paired WGS (n=1760)"},
    # {"id": "Paired WGS", "parent": "T-ALL", "value": 1366, "label": "Yes Paired WGS (n=1366)"},
    # {"id": "Paired WGS", "parent": "T-ALL", "value": 300, "label": "No Paired WGS (n=300)"},
    
    # Level 3 - BCP-ALL subtypes
    {"id": "Hyperdiploid", "parent": "BCP-ALL", "value": 1023, "label": "Hyperdiploid (n=1023)"},
    {"id": "ETV6::RUNX1", "parent": "BCP-ALL", "value": 936, "label": "ETV6::RUNX1 (n=936)"},
    {"id": "B-other", "parent": "BCP-ALL", "value": 279, "label": "B-other (n=279)"},
    {"id": "PAX5alt", "parent": "BCP-ALL", "value": 265, "label": "PAX5alt (n=265)"},
    {"id": "TCF3::PBX1", "parent": "BCP-ALL", "value": 160, "label": "TCF3::PBX1 (n=160)"},
    {"id": "BCR::ABL1-like_NonCRLF2", "parent": "BCP-ALL", "value": 155, "label": "BCR::ABL1-like_NonCRLF2 (n=155)"},
    {"id": "DUX4", "parent": "BCP-ALL", "value": 148, "label": "DUX4 (n=148)"},
    {"id": "iAMP21", "parent": "BCP-ALL", "value": 147, "label": "iAMP21 (n=147)"},
    {"id": "BCR::ABL1", "parent": "BCP-ALL", "value": 130, "label": "BCR::ABL1 (n=130)"},
    {"id": "KMT2A_BCP_ALL", "parent": "BCP-ALL", "value": 118, "label": "KMT2A (n=118)"},
    {"id": "BCR::ABL1-like_CRLF2", "parent": "BCP-ALL", "value": 103, "label": "BCR::ABL1-like_CRLF2 (n=103)"},
    {"id": "ETV6::RUNX1-like", "parent": "BCP-ALL", "value": 74, "label": "ETV6::RUNX1-like (n=74)"},
    {"id": "ZNF384", "parent": "BCP-ALL", "value": 63, "label": "ZNF384 (n=63)"},
    {"id": "Low hypodiploid", "parent": "BCP-ALL", "value": 46, "label": "Low hypodiploid (n=46)"},
    {"id": "Near haploid", "parent": "BCP-ALL", "value": 44, "label": "Near haploid (n=44)"},
    {"id": "MEF2D", "parent": "BCP-ALL", "value": 42, "label": "MEF2D (n=42)"},
    {"id": "PAX5 P80R", "parent": "BCP-ALL", "value": 32, "label": "PAX5 P80R (n=32)"},
    {"id": "Other subtypes_BCP_ALL", "parent": "BCP-ALL", "value": 89, "label": "Other subtypes (n=89)"},
    
    # Level 3 - T-ALL subtypes
    {"id": "TAL1 DP-like", "parent": "T-ALL", "value": 300, "label": "TAL1 DP-like (n=300)"},
    {"id": "TLX3", "parent": "T-ALL", "value": 244, "label": "TLX3 (n=244)"},
    {"id": "ETP-like", "parent": "T-ALL", "value": 240, "label": "ETP-like (n=240)"},
    {"id": "TAL1 αβ-like", "parent": "T-ALL", "value": 223, "label": "TAL1 αβ-like (n=223)"},
    {"id": "NKX2-1", "parent": "T-ALL", "value": 84, "label": "NKX2-1 (n=84)"},
    {"id": "TLX1", "parent": "T-ALL", "value": 79, "label": "TLX1 (n=79)"},
    {"id": "T-other_T_ALL", "parent": "T-ALL", "value": 55, "label": "T-other (n=55)"},
    {"id": "TAL1_T_ALL", "parent": "T-ALL", "value": 51, "label": "TAL1 (n=51)"},
    {"id": "HOXA", "parent": "T-ALL", "value": 45, "label": "HOXA (n=45)"},
    {"id": "TME-enriched", "parent": "T-ALL", "value": 42, "label": "TME-enriched (n=42)"},
    {"id": "KMT2A_T_ALL", "parent": "T-ALL", "value": 39, "label": "KMT2A (n=39)"},
    {"id": "MLLT10", "parent": "T-ALL", "value": 32, "label": "MLLT10 (n=32)"},
    {"id": "Other subtypes_T_ALL", "parent": "T-ALL", "value": 100, "label": "Other subtypes (n=100)"},
    
    # AML subtypes (Level 3)
    {"id": "MECOM", "parent": "AML", "value": 43, "label": "MECOM (n=43)"},
    {"id": "CEBPA", "parent": "AML", "value": 33, "label": "CEBPA (n=33)"},
    {"id": "AML-MR", "parent": "AML", "value": 29, "label": "AML-MR (n=29)"},
    {"id": "KMT2A_AML", "parent": "AML", "value": 23, "label": "KMT2A (n=23)"},
    {"id": "DEK::NUP214", "parent": "AML", "value": 10, "label": "DEK::NUP214 (n=10)"},
    {"id": "NPM1", "parent": "AML", "value": 6, "label": "NPM1 (n=6)"},
    {"id": "Other subtypes_AML", "parent": "AML", "value": 6, "label": "Other subtypes (n=6)"}
]

# Convert to DataFrame for easier manipulation
df = pd.DataFrame(data)

# Extract the IDs, labels, parents, and values
ids = df['id'].tolist()
labels = df['label'].tolist()
parents = df['parent'].tolist()
values = df['value'].tolist()

# Create a color mapping based on the top-level categories
color_map = {
    "BCP-ALL": "#e7298b",  # Pink
    "T-ALL": "#7470b3",    # Lavender
    "AML": "#1b9e77",      # Green
    "MDS": "#d95f02"       # Orange
}

# Generate colors for all nodes
colors = []
for i, parent in enumerate(parents):
    if parent == "":  # Top-level category
        colors.append(color_map.get(ids[i], "#CCCCCC"))
    else:  # Inherit color from parent
        parent_color = color_map.get(parent, "#CCCCCC")
        colors.append(parent_color)

# Create weighted version for better visibility
display_values = values.copy()
weight_factor = 3  # Weight factor to enhance AML segments

for i, (id_, parent) in enumerate(zip(ids, parents)):
    if parent == "AML":
        display_values[i] = values[i] * weight_factor
    elif id_ == "AML":
        display_values[i] = values[i] * weight_factor

# Create the main visualization
fig = go.Figure()

# Add sunburst trace with labels including numbers in parentheses
fig.add_trace(go.Sunburst(
    ids=ids,
    labels=labels,  # Keep original labels with numbers
    parents=parents,
    # values=display_values,
    # branchvalues="remainder",
    marker=dict(
        colors=colors,
        line=dict(width=1.5, color='white')  # White borders for better separation
    ),
    insidetextorientation='radial',
    rotation=90,
    domain=dict(column=0),
    hoverinfo=None,
    textfont=dict(size=20, color='black', family='Arial, sans-serif')
))

# Update layout for publication quality
fig.update_layout(
    # title={
    #     'text': "Leukemia Classification Hierarchy",
    #     'font': dict(size=24, family='Arial, sans-serif'),
    #     'y': 0.95,
    #     'x': 0.5,
    #     'xanchor': 'center',
    #     'yanchor': 'top'
    # },
    width=1200,
    height=1200,
    # margin=dict(t=80, l=0, r=0, b=0),
    font=dict(family='Arial, sans-serif'),
    paper_bgcolor='white',
    plot_bgcolor='white',
    grid= dict(columns=1, rows=1),
    margin=dict(t=10, l=10, r=10, b=10)
)

# Save as high-resolution JPEG
fig.write_image("leukemia_classification_sunburst.jpeg", scale=4, width=1200, height=1200)