import plotly.express as px
import pandas as pd

# Define hierarchical data in the format expected by the sunburst function
data = [
    (
        "BCP-ALL", 3854, [
            (
                "WES", 3854, [
                    ("Hyperdiploid", 1023, []),
                    ("ETV6::RUNX1", 936, []),
                    ("B-other", 279, []),
                    ("PAX5alt", 265, []),
                    ("TCF3::PBX1", 160, []),
                    ("BCR::ABL1-like_NonCRLF2", 155, []),
                    ("DUX4", 148, []),
                    ("iAMP21", 147, []),
                    ("BCR::ABL1", 130, []),
                    ("KMT2A", 118, []),
                    ("BCR::ABL1-like_CRLF2", 103, []),
                    ("ETV6::RUNX1-like", 74, []),
                    ("ZNF384", 63, []),
                    ("Low hypodiploid", 46, []),
                    ("Near haploid", 44, []),
                    ("MEF2D", 42, []),
                    ("PAX5 P80R", 32, []),
                    ("Other subtypes", 89, [])
                ]
            )
        ]
    ),
    (
        "T-ALL", 1666, [
            (
                "WES", 1666, [
                    ("TAL1 DP-like", 300, []),
                    ("TLX3", 244, []),
                    ("ETP-like", 240, []),
                    ("TAL1 αβ-like", 223, []),
                    ("NKX2-1", 84, []),
                    ("TLX1", 79, []),
                    ("T-other", 55, []),
                    ("TAL1", 51, []),
                    ("HOXA", 45, []),
                    ("TME-enriched", 42, []),
                    ("KMT2A", 39, []),
                    ("MLLT10", 32, []),
                    ("Other subtypes", 100, [])
                ]
            )
        ]
    ),
    (
        "AML", 150, [
            (
                "WES", 150, [
                    ("MECOM", 43, []),
                    ("CEBPA", 33, []),
                    ("AML-MR", 29, []),
                    ("KMT2A", 23, []),
                    ("DEK::NUP214", 10, []),
                    ("NPM1", 6, []),
                    ("Other subtypes", 6, [])
                ]
            )
        ]
    )
]

# Flatten the hierarchical data
flat_data = []

def flatten_data(nodes, path=None):
    if path is None:
        path = []
    
    for label, value, children in nodes:
        current_path = path + [label]
        flat_data.append({
            "Count": value,
            "path": current_path.copy()
        })
        if children:
            flatten_data(children, current_path)

flatten_data(data)

# Create a DataFrame with path columns
df = pd.DataFrame(flat_data)
df["Category"] = df["path"].apply(lambda x: x[0] if len(x) > 0 else "")
df["Sequencing"] = df["path"].apply(lambda x: x[1] if len(x) > 1 else "")
df["Subtype"] = df["path"].apply(lambda x: x[2] if len(x) > 2 else "")

# Create sunburst with plotly express
fig = px.sunburst(
    df,
    path=["Category", "Sequencing", "Subtype"],
    values="Count",
    color="Category",
    color_discrete_map={"BCP-ALL": "#8dd3c7", "T-ALL": "#bebada", "AML": "#fb8072"},
    title="Leukemia Subtypes Distribution",
    branchvalues="total"
)

fig.update_layout(
    width=800, 
    height=800,
    margin=dict(t=30, l=0, r=0, b=0)
)

# Customize appearance
fig.update_traces(
    textinfo="label+percent parent",
    insidetextorientation="radial"
)

fig.show()