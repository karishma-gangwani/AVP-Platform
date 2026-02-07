import plotly.express as px

# Sample data
node_info = [
    {"name": "Leukemia", "parent": "", "n": 2600},
    {"name": "B-ALL", "parent": "Leukemia", "n": 1200},
    {"name": "T-ALL", "parent": "Leukemia", "n": 450},
    {"name": "AML", "parent": "Leukemia", "n": 950},
    {"name": "B-ALL with Recurrent\nGenetic Abnormalities", "parent": "B-ALL", "n": 600},
    {"name": "B-ALL with\nHyperdiploidy", "parent": "B-ALL", "n": 400},
    {"name": "Other B-ALL", "parent": "B-ALL", "n": 200},
    {"name": "Early T-cell Precursor\nALL (ETP-ALL)", "parent": "T-ALL", "n": 185},
    {"name": "Other T-ALL", "parent": "T-ALL", "n": 265},
    {"name": "AML with Recurrent\nGenetic Abnormalities", "parent": "AML", "n": 350},
    {"name": "AML with\nMyelodysplasia", "parent": "AML", "n": 200},
    {"name": "AML, Not Otherwise\nSpecified", "parent": "AML", "n": 400},
    {"name": "ETV6-RUNX1", "parent": "B-ALL with Recurrent\nGenetic Abnormalities", "n": 180},
    {"name": "BCR-ABL1", "parent": "B-ALL with Recurrent\nGenetic Abnormalities", "n": 170},
    {"name": "TCF3-PBX1", "parent": "B-ALL with Recurrent\nGenetic Abnormalities", "n": 120},
    {"name": "KMT2A-rearranged", "parent": "B-ALL with Recurrent\nGenetic Abnormalities", "n": 130},
    {"name": "High Hyperdiploid", "parent": "B-ALL with\nHyperdiploidy", "n": 280},
    {"name": "Hypodiploid", "parent": "B-ALL with\nHyperdiploidy", "n": 120},
    {"name": "p190 BCR-ABL1", "parent": "BCR-ABL1", "n": 110},
    {"name": "p210 BCR-ABL1", "parent": "BCR-ABL1", "n": 60},
    {"name": "NOTCH1-mutated", "parent": "Early T-cell Precursor\nALL (ETP-ALL)", "n": 185},
    {"name": "TAL1-positive", "parent": "Other T-ALL", "n": 135},
    {"name": "TLX3-positive", "parent": "Other T-ALL", "n": 130},
    {"name": "AML with t(8;21)", "parent": "AML with Recurrent\nGenetic Abnormalities", "n": 145},
    {"name": "APL with PML-RARA", "parent": "AML with Recurrent\nGenetic Abnormalities", "n": 205},
    {"name": "AML with NPM1 mut", "parent": "AML with Recurrent\nGenetic Abnormalities", "n": 200},
    {"name": "AML with biallelic CEBPA", "parent": "AML with Recurrent\nGenetic Abnormalities", "n": 170},
    {"name": "AML with FLT3-ITD", "parent": "AML with Recurrent\nGenetic Abnormalities", "n": 230},
    {"name": "RUNX1-RUNX1T1", "parent": "AML with t(8;21)", "n": 100},
    {"name": "variant t(8;21)", "parent": "AML with t(8;21)", "n": 45}
]

# Create Treemap
fig = px.treemap(
    names=[node['name'] for node in node_info],
    parents=[node['parent'] for node in node_info],
    values=[node['n'] for node in node_info],
    title='Leukemia Classifications'
)
fig.show()
