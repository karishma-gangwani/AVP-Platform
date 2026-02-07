import plotly.graph_objects as go
import pandas as pd

# Define hierarchical data
data = [
    # Level 1 - Main categories
    {"id": "BCP-ALL", "parent": "", "value": 3854, "label": "BCP-ALL (n=3854)"},
    {"id": "T-ALL", "parent": "", "value": 1666, "label": "T-ALL (n=1666)"},
    {"id": "AML", "parent": "", "value": 150, "label": "AML (n=150)"},

    # Level 2 - assay availability
    {"id": "Paired WGS", "parent": "BCP-ALL", "value": 2094, "label": "Paired WGS (n=2094)"},
    {"id": "Paired WGS", "parent": "T-ALL", "value": 1366, "label": "Paired WGS (n=1366)"},
    
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
    "BCP-ALL": "#FF9EB1",  # Pink
    "T-ALL": "#D8BFD8",    # Lavender
    "AML": "#90EE90",      # Light Green
}

# Generate colors for all nodes
colors = []
for i, parent in enumerate(parents):
    if parent == "":  # Top-level category
        colors.append(color_map.get(ids[i], "#CCCCCC"))
    else:  # Inherit color from parent
        parent_color = color_map.get(parent, "#CCCCCC")
        colors.append(parent_color)

# Create a Figure with custom layout
fig = go.Figure()

# First, create a sunburst chart for the outer rings (excluding the main categories)
outer_ids = [ids[i] for i in range(len(ids)) if parents[i] in ["BCP-ALL", "T-ALL", "AML"]]
outer_labels = [labels[i] for i in range(len(ids)) if parents[i] in ["BCP-ALL", "T-ALL", "AML"]]
outer_parents = [parents[i] for i in range(len(ids)) if parents[i] in ["BCP-ALL", "T-ALL", "AML"]]
outer_values = [values[i] for i in range(len(ids)) if parents[i] in ["BCP-ALL", "T-ALL", "AML"]]
outer_colors = [colors[i] for i in range(len(ids)) if parents[i] in ["BCP-ALL", "T-ALL", "AML"]]

# Add the main categories to make sunburst work
for i in range(len(ids)):
    if parents[i] == "":
        outer_ids.append(ids[i])
        outer_labels.append(labels[i])
        outer_parents.append(parents[i])
        outer_values.append(values[i])
        outer_colors.append(colors[i])

# Combine to create the sunburst chart
fig.add_trace(go.Sunburst(
    ids=outer_ids,
    labels=outer_labels,
    parents=outer_parents,
    # values=outer_values,
    # branchvalues="total",
    marker=dict(
        colors=outer_colors,
        line=dict(width=1.5, color='white')
    ),
    insidetextorientation='radial',
    textfont=dict(size=14, family='Arial, sans-serif')
))

# Then, create a separate pie chart for the center (main categories only)
fig.add_trace(go.Pie(
    labels=["BCP-ALL", "T-ALL", "AML"],
    values=[3854, 1666, 150],
    marker=dict(colors=["#FF9EB1", "#D8BFD8", "#90EE90"]),
    textinfo='label',
    textfont=dict(size=16, family='Arial, sans-serif'),
    hole=0.7,  # Create the donut effect
    domain=dict(x=[0.3, 0.7], y=[0.3, 0.7]),  # Position in the center
    showlegend=False
))

# Add annotations
fig.update_layout(
    width=1200,
    height=1200,
    margin=dict(t=10, l=10, r=10, b=10),
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=False,
    annotations=[
        dict(
            text="BCP-ALL<br>(n=3854)",
            x=0.3,
            y=0.53,
            showarrow=False,
            font=dict(size=18, color='black', family='Arial, sans-serif')
        ),
        dict(
            text="T-ALL<br>(n=1666)",
            x=0.7,
            y=0.53,
            showarrow=False,
            font=dict(size=18, color='black', family='Arial, sans-serif')
        ),
        dict(
            text="AML<br>(n=150)",
            x=0.5,
            y=0.75,
            showarrow=False,
            font=dict(size=18, color='black', family='Arial, sans-serif')
        )
    ]
)

# Save as high-quality JPEG
fig.write_image("leukemia_classification_sunburst_donut.jpeg", scale=4, width=1200, height=1200)