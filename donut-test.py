import numpy as np
import matplotlib.pyplot as plt

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

# Sunburst function
def sunburst(nodes, total=np.pi * 2, offset=0, level=0, ax=None):
    ax = ax or plt.subplot(111, projection='polar')

    if level == 0 and len(nodes) == 1:
        label, value, subnodes = nodes[0]
        ax.bar([0], [0.5], [np.pi * 2])
        ax.text(0, 0, label, ha='center', va='center')
        sunburst(subnodes, total=value, level=level + 1, ax=ax)
    elif nodes:
        d = np.pi * 2 / total
        labels = []
        widths = []
        local_offset = offset
        for label, value, subnodes in nodes:
            labels.append(label)
            widths.append(value * d)
            sunburst(subnodes, total=total, offset=local_offset,
                     level=level + 1, ax=ax)
            local_offset += value
        values = np.cumsum([offset * d] + widths[:-1])
        heights = [1] * len(nodes)
        bottoms = np.zeros(len(nodes)) + level - 0.5
        
        # Add white boundaries between segments
        rects = ax.bar(
            values, heights, widths, bottoms, linewidth=2,  # Increased linewidth
            edgecolor='white', align='edge'
        )
        
        for rect, label in zip(rects, labels):
            x = rect.get_x() + rect.get_width() / 2
            y = rect.get_y() + rect.get_height() / 2
            rotation = (90 + (360 - np.degrees(x) % 180)) % 360
            ax.text(x, y, label, rotation=rotation, ha='center', va='center') 

    if level == 0:
        ax.set_theta_direction(-1)
        ax.set_theta_zero_location('N')
        ax.set_axis_off()

# Create the sunburst chart
fig = plt.figure(figsize=(10, 10))
sunburst(data)
plt.show()

