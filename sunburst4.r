# Libraries
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
  conflict_prefer("select", "dplyr")
  conflict_prefer("mutate", "dplyr")
}

# Load dataset
data <- read.table("ash.rsunburst.csv", header=TRUE, sep=";", stringsAsFactors=FALSE)
data[which(data$value == -1), "value"] <- 1
colnames(data) <- c("parent", "child", "key", "value")

# Reformat data for the sunburstR package
data <- data %>%
  filter(parent != "") %>%
  mutate(path = paste(parent, child, key, sep="-")) %>%
  dplyr::select(path, value)

# Generate colors using RColorBrewer
num_paths <- length(unique(data$path))
palette <- colorRampPalette(brewer.pal(9, "Pastel1"))(num_paths)
colors <- setNames(palette, unique(data$path))

# Create the sunburst chart
p <- sunburst(data, colors = colors, legend = FALSE)  # Turn off default legend

# Add custom horizontal legend
p <- p %>%
  htmlwidgets::onRender(
    "function(el, x) {
      // Create main container for the legend
      var legendContainer = d3.select(el).append('div')
        .attr('class', 'horizontal-legend')
        .style('position', 'relative')
        .style('width', '100%')
        .style('margin-top', '20px')
        .style('padding', '10px');
        
      // Add legend title
      legendContainer.append('div')
        .attr('class', 'legend-title')
        .style('text-align', 'center')
        .style('font-weight', 'bold')
        .style('margin-bottom', '10px')
        .text('Legend');
      
      // Create flexbox container for legend items
      var legendItems = legendContainer.append('div')
        .style('display', 'flex')
        .style('flex-wrap', 'wrap')
        .style('justify-content', 'center')
        .style('gap', '10px');
      
      // Get paths and colors
      var paths = Object.keys(x.options.colors);
      var colors = paths.map(function(p) { return x.options.colors[p]; });
      
      // Custom sort function if needed - uncomment and modify as needed
      /*
      paths.sort(function(a, b) {
        // Custom sorting logic
        return a.localeCompare(b);
      });
      */
      
      // Create legend items
      paths.forEach(function(path, i) {
        // Extract just the last part of the path for display
        var pathParts = path.split('-');
        var displayLabel = pathParts[pathParts.length - 1];
        
        var item = legendItems.append('div')
          .style('display', 'flex')
          .style('align-items', 'center')
          .style('padding', '3px 8px')
          .style('border', '1px solid #eaeaea')
          .style('border-radius', '3px')
          .style('background-color', '#ffffff');
        
        // Color box
        item.append('div')
          .style('width', '12px')
          .style('height', '12px')
          .style('background-color', colors[i])
          .style('margin-right', '5px');
        
        // Label
        item.append('span')
          .text(displayLabel)
          .style('font-size', '12px');
          
        // Optional tooltip for full path
        item.attr('title', path)
          .style('cursor', 'pointer');
      });
    }"
  )

# Save the widget
saveWidget(p, "sunburst_chart_horizontal_legend.html", selfcontained = TRUE)
