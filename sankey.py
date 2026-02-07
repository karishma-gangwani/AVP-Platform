import plotly.graph_objects as go

# Define nodes (boxes in the diagram)
nodes = {
    # Main categories
    "B-ALL": 0,
    "T-ALL": 1,
    "AML": 2,
    
    # B-ALL subcategories
    "B-ALL with Recurrent Genetic Abnormalities": 3,
    "B-ALL with Hyperdiploidy": 4,
    "Other B-ALL": 5,
    
    # T-ALL subcategories
    "Early T-cell Precursor ALL (ETP-ALL)": 6,
    "Other T-ALL": 7,
    
    # AML subcategories
    "AML with Recurrent Genetic Abnormalities": 8,
    "AML with Myelodysplasia": 9,
    "AML, Not Otherwise Specified": 10,
    
    # B-ALL molecular subtypes
    "ETV6-RUNX1": 11,
    "BCR-ABL1": 12,
    "TCF3-PBX1": 13,
    "KMT2A-rearranged": 14,
    "High Hyperdiploid": 15,
    "Hypodiploid": 16,
    "p190 BCR-ABL1": 17,
    "p210 BCR-ABL1": 18,
    
    # T-ALL molecular subtypes
    "NOTCH1-mutated": 19,
    "TAL1-positive": 20,
    "TLX3-positive": 21,
    
    # AML molecular subtypes
    "AML with t(8;21)": 22,
    "APL with PML-RARA": 23,
    "AML with NPM1 mut": 24,
    "AML with biallelic CEBPA": 25,
    "AML with FLT3-ITD": 26,
    "RUNX1-RUNX1T1": 27,
    "variant t(8;21)": 28
}

# Define links (connections between nodes)
links_source = []
links_target = []
links_value = []
links_color = []

# Helper function to add a link
def add_link(source, target, value, color):
    links_source.append(nodes[source])
    links_target.append(nodes[target])
    links_value.append(value)
    links_color.append(color)

# Define consistent values for links at each level
main_to_sub_value = 1      # Main category to subcategory
sub_to_molecular_value = 1 # Subcategory to molecular subtype
molecular_to_variant_value = 1  # Molecular subtype to variant

# B-ALL links
b_all_color = "rgba(100, 170, 225, 0.8)"
add_link("B-ALL", "B-ALL with Recurrent Genetic Abnormalities", main_to_sub_value, b_all_color)
add_link("B-ALL", "B-ALL with Hyperdiploidy", main_to_sub_value, b_all_color)
add_link("B-ALL", "Other B-ALL", main_to_sub_value, b_all_color)

add_link("B-ALL with Recurrent Genetic Abnormalities", "ETV6-RUNX1", sub_to_molecular_value, b_all_color)
add_link("B-ALL with Recurrent Genetic Abnormalities", "BCR-ABL1", sub_to_molecular_value, b_all_color)
add_link("B-ALL with Recurrent Genetic Abnormalities", "TCF3-PBX1", sub_to_molecular_value, b_all_color)
add_link("B-ALL with Recurrent Genetic Abnormalities", "KMT2A-rearranged", sub_to_molecular_value, b_all_color)

add_link("B-ALL with Hyperdiploidy", "High Hyperdiploid", sub_to_molecular_value, b_all_color)
add_link("B-ALL with Hyperdiploidy", "Hypodiploid", sub_to_molecular_value, b_all_color)

add_link("BCR-ABL1", "p190 BCR-ABL1", molecular_to_variant_value, b_all_color)
add_link("BCR-ABL1", "p210 BCR-ABL1", molecular_to_variant_value, b_all_color)

# T-ALL links
t_all_color = "rgba(100, 200, 120, 0.8)"
add_link("T-ALL", "Early T-cell Precursor ALL (ETP-ALL)", main_to_sub_value, t_all_color)
add_link("T-ALL", "Other T-ALL", main_to_sub_value, t_all_color)

add_link("Early T-cell Precursor ALL (ETP-ALL)", "NOTCH1-mutated", sub_to_molecular_value, t_all_color)
add_link("Other T-ALL", "TAL1-positive", sub_to_molecular_value, t_all_color)
add_link("Other T-ALL", "TLX3-positive", sub_to_molecular_value, t_all_color)

# AML links
aml_color = "rgba(240, 180, 100, 0.8)"
add_link("AML", "AML with Recurrent Genetic Abnormalities", main_to_sub_value, aml_color)
add_link("AML", "AML with Myelodysplasia", main_to_sub_value, aml_color)
add_link("AML", "AML, Not Otherwise Specified", main_to_sub_value, aml_color)

add_link("AML with Recurrent Genetic Abnormalities", "AML with t(8;21)", sub_to_molecular_value, aml_color)
add_link("AML with Recurrent Genetic Abnormalities", "APL with PML-RARA", sub_to_molecular_value, aml_color)

add_link("AML with Myelodysplasia", "AML with NPM1 mut", sub_to_molecular_value, aml_color)

add_link("AML, Not Otherwise Specified", "AML with biallelic CEBPA", sub_to_molecular_value, aml_color)
add_link("AML, Not Otherwise Specified", "AML with FLT3-ITD", sub_to_molecular_value, aml_color)

add_link("AML with t(8;21)", "RUNX1-RUNX1T1", molecular_to_variant_value, aml_color)
add_link("AML with t(8;21)", "variant t(8;21)", molecular_to_variant_value, aml_color)

# Define node colors based on category
node_colors = []
for node_name in nodes:
    if "B-ALL" in node_name or node_name in ["ETV6-RUNX1", "BCR-ABL1", "TCF3-PBX1", "KMT2A-rearranged", 
                                          "High Hyperdiploid", "Hypodiploid", "p190 BCR-ABL1", "p210 BCR-ABL1"]:
        node_colors.append(b_all_color)
    elif "T-ALL" in node_name or node_name in ["NOTCH1-mutated", "TAL1-positive", "TLX3-positive"]:
        node_colors.append(t_all_color)
    else:  # AML and subtypes
        node_colors.append(aml_color)

# Create the Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=list(nodes.keys()),
        color=node_colors
    ),
    link=dict(
        source=links_source,
        target=links_target,
        value=links_value,
        color=links_color
    )
)])

# Update layout
fig.update_layout(
    title_text="Leukemia Classification Systems: WHO to Molecular Subtypes",
    font=dict(size=12),
    autosize=True,
    margin=dict(l=25, r=25, b=25, t=75),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Show the plot
fig.show()

# If you want to save the figure
# fig.write_html("leukemia_classification.html")
# fig.write_image("leukemia_classification.png", width=1200, height=800)