# libraries
library(tidyverse)
library(treemap)
library(sunburstR)
library(htmlwidgets)
library(RColorBrewer)
library(viridis)


# Check for conflicts
if ("conflicted" %in% installed.packages()) {
  library(conflicted)
  conflict_prefer("filter", "dplyr")
  conflict_prefer("lag", "dplyr")
  conflict_prefer("select", "dplyr") # Add preference for select
  conflict_prefer("mutate", "dplyr") # Add preference for mutate
}

# Load dataset from github
data <- read.table("ash.rsunburst.csv", header=T, sep=";", stringsAsFactors=F)
data[ which(data$value==-1),"value"] <- 1
colnames(data) <- c("parent", "child", "key", "value")

# Reformat data for the sunburstR package
data <- data %>%
  filter(parent != "") %>%
  mutate(path = paste(parent, child, key, sep="-")) %>%
  dplyr::select(path, value)

# Generate pastel colors using RColorBrewer
num_paths <- length(unique(data$path))  # Count unique paths
palette <- colorRampPalette(brewer.pal(9, "Pastel1"))(num_paths)  # Generate `num_paths` pastel colors
colors <- setNames(palette, unique(data$path))  # Map colors to paths

# Debug: Inspect the generated colors
# print("Generated pastel colors:")
# print(colors)

# Create the sunburst chart using the same colors
p <- sunburst(data, colors = colors, legend = TRUE)

# Create a data frame for the legend
legend_data <- tibble(
  Path = names(colors),  # Path names
  Color = colors         # Corresponding colors
)

# Create a horizontal legend using ggplot2
legend_plot <- ggplot(legend_data, aes(x = Path, y = 1, fill = Path)) +
  geom_tile() +  # Create tiles for each path
  scale_fill_manual(values = colors) +  # Apply the same colors as the chart
  theme_void() +  # Remove default ggplot axes and gridlines
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1, size = 8),  # Rotate text for readability
    legend.position = "none"  # Disable ggplot2's default legend
  ) +
  labs(title = "Legend")  # Add a title to the legend

# Save the legend as an image
ggsave("horizontal_legend.png", legend_plot, width = 12, height = 4)

# Save the sunburst chart
saveWidget(p, "sunburst_chart.html", selfcontained = TRUE)