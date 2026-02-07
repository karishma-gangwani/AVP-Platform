import pandas as pd
import plotly.express as px

# Create hierarchical data for visualization
data = [
    # Level 1 - Main categories
    {"id": "BCP-ALL", "parent": "", "value": 3854, "label": "BCP-ALL (n=3854)"},
    {"id": "T-ALL", "parent": "", "value": 1666, "label": "T-ALL (n=1666)"},
    {"id": "AML", "parent": "", "value": 150, "label": "AML (n=150)"},
    {"id": "MDS", "parent": "", "value": 150, "label": "MDS (n=150)"},

    # Level 2 - B-ALL subtypes
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

    # Level 2 - T-ALL subtypes
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

    # AML subtypes (Level 2)
    {"id": "MECOM", "parent": "AML", "value": 43, "label": "MECOM (n=43)"},
    {"id": "CEBPA", "parent": "AML", "value": 33, "label": "CEBPA (n=33)"},
    {"id": "AML-MR", "parent": "AML", "value": 29, "label": "AML-MR (n=29)"},
    {"id": "KMT2A_AML", "parent": "AML", "value": 23, "label": "KMT2A (n=23)"},
    {"id": "DEK::NUP214", "parent": "AML", "value": 10, "label": "DEK::NUP214 (n=10)"},
    {"id": "NPM1", "parent": "AML", "value": 6, "label": "NPM1 (n=6)"},
    {"id": "Other subtypes_AML", "parent": "AML", "value": 6, "label": "Other subtypes (n=6)"}
]

# Convert to DataFrame
df = pd.DataFrame(data)

# Create color mapping for the three main categories
colors = {
    "BCP-ALL": "#6BAED6",  # Blue shades
    "T-ALL": "#74C476",  # Green shades
    "AML": "#FD8D3C",      # Orange shades
    "MDS": "#A9A9A9"       # Grey for MDS
}

# Create a dictionary to map each ID to its top-level color
color_map = {}
for row in data:
    id_val = row['id']
    if id_val == "BCP-ALL":
        color_map[id_val] = colors["BCP-ALL"]
    elif id_val == "T-ALL":
        color_map[id_val] = colors["T-ALL"]
    elif id_val == "AML":
        color_map[id_val] = colors["AML"]
    elif id_val == "MDS":
        color_map[id_val] = colors["MDS"]
    elif row['parent'] == "BCP-ALL":
        color_map[id_val] = colors["BCP-ALL"]
    elif row['parent'] == "T-ALL":
        color_map[id_val] = colors["T-ALL"]
    elif row['parent'] == "AML":
        color_map[id_val] = colors["AML"]
    elif row['parent'] == "MDS":
        color_map[id_val] = colors["MDS"]

# 2. Icicle Plot with Fixed Parent Areas
fig_icicle_fixed = px.icicle(
    df,
    ids='id',
    parents='parent',
    values='value',
    names='label',
    title="Leukemia Classification Systems (Icicle Plot with Fixed Parent Areas)",
    color='id',
    color_discrete_map=color_map,
    branchvalues="remainder"  # Use remainder for sizing children independently
)

# Update layout and traces for readability
fig_icicle_fixed.update_traces(
    textinfo="label+value",  # Show both label and value
    textfont_size=10         # Set smaller font size for better readability
)

fig_icicle_fixed.update_layout(
    width=900,  # Keep the original width
    height=900,  # Keep the original height
    font=dict(size=12),
    title_font=dict(size=18)
)

fig_icicle_fixed.write_html("leukemia_icicle_fixed_chart_colored.html")
fig_icicle_fixed.write_image("leukemia_icicle_fixed_chart_colored.png", width=900, height=900, scale=2)
fig_icicle_fixed.show()

# 3. Sunburst Chart with Fixed Parent Areas
fig_sunburst_fixed = px.sunburst(
    df,
    ids='id',
    parents='parent',
    values='value',
    names='label',
    title="Leukemia Classification Systems: Sunburst with Fixed Parent Areas",
    color='id',
    color_discrete_map=color_map,
    branchvalues="remainder",  # Use remainder for sizing children independently
    maxdepth=2  # Limit depth to 2 levels
)

# Adjust font size and text wrapping
df['label'] = df['label'].str.replace(" ", "<br>")

# Increase the relative size of level 2 nodes
df.loc[df['parent'] != "", 'value'] *= 2  # Double the size of level 2 nodes

# Update layout and traces for readability
fig_sunburst_fixed.update_traces(
    textinfo="label+value",  # Show both label and value
    textfont_size=10         # Set smaller font size for better readability
)

fig_sunburst_fixed.update_layout(
    width=900,  # Keep the original width
    height=900,  # Keep the original height
    font=dict(size=12),
    title_font=dict(size=18)
)

fig_sunburst_fixed.write_html("leukemia_sunburst_fixed_chart_colored.html")
fig_sunburst_fixed.write_image("leukemia_sunburst_fixed_chart_colored.png", width=900, height=900, scale=2)
fig_sunburst_fixed.show()

# Create treemap with fixed parent areas
fig_treemap_fixed = px.treemap(
    df,
    ids='id',
    parents='parent',
    values='value',
    names='label',
    title="Leukemia Classification Systems (Treemap with Adjusted Node Sizes)",
    color='id',
    color_discrete_map=color_map,
    branchvalues="remainder"  # Use remainder for independent child sizing
)

# 1. Treemap with Fixed Parent Areas
fig_treemap_fixed = px.treemap(
    df,
    ids='id',
    parents='parent',
    values='value',
    names='label',
    title="Leukemia Classification Systems (Treemap with Fixed Parent Areas)",
    color='id',
    color_discrete_map=color_map,
    branchvalues="remainder"  # Use remainder for sizing children independently
)

fig_treemap_fixed.update_layout(
    width=900,
    height=900,
    font=dict(size=12),
    title_font=dict(size=18)
)

# Update layout and traces for readability
fig_treemap_fixed.update_traces(
    textinfo="label+value",  # Show both label and value
    textfont_size=10         # Set smaller font size for better readability
)

fig_treemap_fixed.write_html("leukemia_treemap_fixed_chart.html")
fig_treemap_fixed.write_image("leukemia_treemap_fixed_chart.png", width=900, height=900, scale=2)
fig_treemap_fixed.show()
