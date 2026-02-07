# Load required libraries
library(ggplot2)
library(dplyr)

# Sample data for a Sankey diagram
data <- data.frame(
  Level1 = c("B-ALL", "B-ALL", "T-ALL", "T-ALL", "AML", "AML"),
  Level2 = c("B-ALL with Recurrent Genetic Abnormalities", 
             "B-ALL with Hyperdiploidy", 
             "Early T-cell Precursor ALL", 
             "Other T-ALL", 
             "AML with Recurrent Genetic Abnormalities", 
             "AML with Myelodysplasia"),
  Level3 = c("ETV6-RUNX1", "High Hyperdiploid", "NOTCH1-mutated", 
             "TAL1-positive", "AML with t(8;21)", "AML with NPM1"),
  Value = c(25, 15, 12, 8, 22, 10)
)

# Prepare data for nodes
nodes <- data.frame(
  Node = c(unique(data$Level1), unique(data$Level2), unique(data$Level3)),
  Level = c(rep(1, length(unique(data$Level1))),
            rep(2, length(unique(data$Level2))),
            rep(3, length(unique(data$Level3))))
)

# Add positions for nodes
nodes <- nodes %>%
  group_by(Level) %>%
  mutate(Position = row_number())

# Prepare data for links
links <- data %>%
  mutate(Source = match(Level1, nodes$Node),
         Target1 = match(Level2, nodes$Node),
         Target2 = match(Level3, nodes$Node),
         SourcePosition = nodes$Position[match(Level1, nodes$Node)],
         Target1Position = nodes$Position[match(Level2, nodes$Node)],
         Target2Position = nodes$Position[match(Level3, nodes$Node)])

# Plot the Sankey diagram
ggplot() +
  # Draw nodes
  geom_rect(data = nodes, aes(xmin = Level - 0.1, xmax = Level + 0.1, 
                              ymin = Position - 0.5, ymax = Position + 0.5, 
                              fill = Node)) +
  # Draw links between Level1 and Level2
  geom_curve(data = links, aes(x = 1, xend = 2, y = SourcePosition, 
                               yend = Target1Position, size = Value), 
             curvature = 0.5, alpha = 0.5) +
  # Draw links between Level2 and Level3
  geom_curve(data = links, aes(x = 2, xend = 3, y = Target1Position, 
                               yend = Target2Position, size = Value), 
             curvature = 0.5, alpha = 0.5) +
  scale_fill_brewer(palette = "Set3") +
  labs(title = "Leukemia Classification Systems", x = "Levels", y = "Nodes") +
  theme_minimal()

# Save the plot as a .jpg file
ggsave("leukemia_classification_sankey.jpg", width = 10, height = 6, dpi = 300)