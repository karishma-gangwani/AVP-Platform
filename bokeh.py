from bokeh.plotting import figure, show, output_file
from bokeh.transform import cumsum
from bokeh.palettes import Category10, Category20c
from bokeh.models import ColumnDataSource, HoverTool
from math import pi
import pandas as pd
import numpy as np

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

# Extract data for multiple rings
def extract_ring_data(data):
    rings = []
    
    # Top level
    top_level = []
    for label, value, _ in data:
        top_level.append({"category": label, "value": value, "level": "Level 1"})
    rings.append(pd.DataFrame(top_level))
    
    # Second level (all WES)
    second_level = []
    for category, _, children in data:
        for label, value, _ in children:
            second_level.append({
                "category": category,
                "subcategory": label,
                "value": value, 
                "level": "Level 2"
            })
    rings.append(pd.DataFrame(second_level))
    
    # Third level (subtypes)
    third_level = []
    for category, _, l1_children in data:
        for l1_label, _, l2_children in l1_children:
            for label, value, _ in l2_children:
                third_level.append({
                    "category": category,
                    "subcategory": f"{l1_label}-{label}",
                    "value": value,
                    "level": "Level 3"
                })
    rings.append(pd.DataFrame(third_level))
    
    return rings

# Create multiple rings
rings = extract_ring_data(data)

# Create chart with nested rings
output_file("leukemia_distribution_bokeh.html")

# Set up colors
colors = {
    "BCP-ALL": Category10[3][0],
    "T-ALL": Category10[3][1],
    "AML": Category10[3][2]
}

# Create the plots - one for each ring
# We'll use a plotting technique with multiple annular wedges

# Set up figure
p = figure(
    width=700, height=700, 
    title="Leukemia Subtypes Distribution",
    toolbar_location=None, 
    tools="hover",
    tooltips=[("Category", "@category"), ("Value", "@value")]
)

# Create the Level 1 ring (outer)
ring1_df = rings[0].copy()
ring1_df['angle'] = ring1_df['value'] / ring1_df['value'].sum() * 2*pi
ring1_df['start_angle'] = ring1_df['angle'].cumsum().shift(fill_value=0)
ring1_df['end_angle'] = ring1_df['start_angle'] + ring1_df['angle']
ring1_df['color'] = [colors[cat] for cat in ring1_df['category']]

# Source for Level 1
source1 = ColumnDataSource(ring1_df)

# Draw Level 1 ring
p.annular_wedge(
    x=0, y=0,
    inner_radius=0.7, outer_radius=1,
    start_angle='start_angle', end_angle='end_angle',
    fill_color='color', line_color="white", line_width=2,
    source=source1
)

# Add Level 1 labels
text_angles = [(start + end)/2 for start, end in zip(ring1_df['start_angle'], ring1_df['end_angle'])]
text_x = [0.85 * np.cos(ang) for ang in text_angles]
text_y = [0.85 * np.sin(ang) for ang in text_angles]
for i, cat in enumerate(ring1_df['category']):
    angle = text_angles[i]
    text_angle = 0
    if pi/2 < angle < 3*pi/2:
        text_angle = angle + pi
    else:
        text_angle = angle
    p.text(
        text_x[i], text_y[i], 
        text=[cat], 
        text_align="center", text_baseline="middle",
        text_font_size="10pt", text_font_style="bold",
        angle=text_angle
    )

# Create Level 2 ring (middle)
# For demonstration, we'll use a simplified approach just showing the WES segments
level2_data = []
for cat_idx, (category, total, _) in enumerate(data):
    start = ring1_df.iloc[cat_idx]['start_angle']
    end = ring1_df.iloc[cat_idx]['end_angle']
    level2_data.append({
        'category': category, 
        'subcategory': 'WES',
        'value': total,
        'start_angle': start,
        'end_angle': end,
        'color': colors[category]
    })
    
source2 = ColumnDataSource(pd.DataFrame(level2_data))

# Draw Level 2 ring
p.annular_wedge(
    x=0, y=0,
    inner_radius=0.4, outer_radius=0.65,
    start_angle='start_angle', end_angle='end_angle',
    fill_color='color', alpha=0.7, line_color="white", line_width=2,
    source=source2
)

# Add 'WES' label in the middle of Level 2
for row in level2_data:
    angle = (row['start_angle'] + row['end_angle'])/2
    radius = 0.525
    x = radius * np.cos(angle)
    y = radius * np.sin(angle)
    text_angle = 0
    if pi/2 < angle < 3*pi/2:
        text_angle = angle + pi
    else:
        text_angle = angle
    p.text(
        x, y, 
        text=['WES'], 
        text_align="center", text_baseline="middle",
        text_font_size="8pt",
        angle=text_angle
    )

# Create a center circle for the center label
p.circle(0, 0, radius=0.15, fill_color='white', line_color='black')
p.text(0, 0, ['Leukemia\nSubtypes'], text_align="center", text_baseline="middle", text_font_size="10pt")

# Customize the plot
p.axis.visible = False
p.grid.grid_line_color = None
p.x_range.range_padding = 0
p.y_range.range_padding = 0
p.outline_line_color = None

# Show the plot
show(p)