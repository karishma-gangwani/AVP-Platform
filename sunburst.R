# Load necessary libraries
library(ggplot2)
library(dplyr)
library(readr)
library(sunburstR) # Try this approach again

# Parse the CSV data
csv_text <- "ids,labels,parents,sizes,colors
BCP-ALL (n=3854),BCP-ALL (n=3854),,3854,#FF9EB1
Paired WGS,Paired WGS (n=2094),BCP-ALL (n=3854),2094,#FF9EB1
Hyperdiploid,Hyperdiploid (n=1023),BCP-ALL (n=3854),1023,#FF9EB1
ETV6::RUNX1,ETV6::RUNX1 (n=936),BCP-ALL (n=3854),936,#FF9EB1
B-other,B-other (n=279),BCP-ALL (n=3854),279,#FF9EB1
PAX5alt,PAX5alt (n=265),BCP-ALL (n=3854),265,#FF9EB1
TCF3::PBX1,TCF3::PBX1 (n=160),BCP-ALL (n=3854),160,#FF9EB1
BCR::ABL1-like_NonCRLF2,BCR::ABL1-like_NonCRLF2 (n=155),BCP-ALL (n=3854),155,#FF9EB1
DUX4,DUX4 (n=148),BCP-ALL (n=3854),148,#FF9EB1
iAMP21,iAMP21 (n=147),BCP-ALL (n=3854),147,#FF9EB1
BCR::ABL1,BCR::ABL1 (n=130),BCP-ALL (n=3854),130,#FF9EB1
KMT2A_BCP_ALL,KMT2A (n=118),BCP-ALL (n=3854),118,#FF9EB1
BCR::ABL1-like_CRLF2,BCR::ABL1-like_CRLF2 (n=103),BCP-ALL (n=3854),103,#FF9EB1
ETV6::RUNX1-like,ETV6::RUNX1-like (n=74),BCP-ALL (n=3854),74,#FF9EB1
ZNF384,ZNF384 (n=63),BCP-ALL (n=3854),63,#FF9EB1
Low hypodiploid,Low hypodiploid (n=46),BCP-ALL (n=3854),46,#FF9EB1
Near haploid,Near haploid (n=44),BCP-ALL (n=3854),44,#FF9EB1
MEF2D,MEF2D (n=42),BCP-ALL (n=3854),42,#FF9EB1
PAX5 P80R,PAX5 P80R (n=32),BCP-ALL (n=3854),32,#FF9EB1
Other subtypes_BCP_ALL,Other subtypes (n=89),BCP-ALL (n=3854),89,#FF9EB1
T-ALL (n=1666),T-ALL (n=1666),,1666,#D8BFD8
Paired WGS,Paired WGS (n=1366),T-ALL (n=1666),1366,#D8BFD8
TAL1 DP-like,TAL1 DP-like (n=300),T-ALL (n=1666),300,#D8BFD8
TLX3,TLX3 (n=244),T-ALL (n=1666),244,#D8BFD8
ETP-like,ETP-like (n=240),T-ALL (n=1666),240,#D8BFD8
TAL1 αβ-like,TAL1 αβ-like (n=223),T-ALL (n=1666),223,#D8BFD8
NKX2-1,NKX2-1 (n=84),T-ALL (n=1666),84,#D8BFD8
TLX1,TLX1 (n=79),T-ALL (n=1666),79,#D8BFD8
T-other_T_ALL,T-other (n=55),T-ALL (n=1666),55,#D8BFD8
TAL1_T_ALL,TAL1 (n=51),T-ALL (n=1666),51,#D8BFD8
HOXA,HOXA (n=45),T-ALL (n=1666),45,#D8BFD8
TME-enriched,TME-enriched (n=42),T-ALL (n=1666),42,#D8BFD8
KMT2A_T_ALL,KMT2A (n=39),T-ALL (n=1666),39,#D8BFD8
MLLT10,MLLT10 (n=32),T-ALL (n=1666),32,#D8BFD8
Other subtypes_T_ALL,Other subtypes (n=100),T-ALL (n=1666),100,#D8BFD8
AML (n=150),AML (n=150),,150,#90EE90
MECOM,MECOM (n=43),AML (n=150),43,#90EE90
CEBPA,CEBPA (n=33),AML (n=150),33,#90EE90
AML-MR,AML-MR (n=29),AML (n=150),29,#90EE90
KMT2A_AML,KMT2A (n=23),AML (n=150),23,#90EE90
DEK::NUP214,DEK::NUP214 (n=10),AML (n=150),10,#90EE90
NPM1,NPM1 (n=6),AML (n=150),6,#90EE90
Other subtypes_AML,Other subtypes (n=6),AML (n=150),6,#90EE90"

# Read the CSV data
df <- read.csv(text = csv_text, stringsAsFactors = FALSE)

# Prepare data for sunburst - resolve duplicate IDs issue
# Create unique paths for each node by combining parent and label
sunburst_data <- data.frame(
  path = character(),
  value = numeric(),
  color = character(),
  stringsAsFactors = FALSE
)

# Process each row to create hierarchical path format
for (i in 1:nrow(df)) {
  row <- df[i, ]
  
  # Create path
  if (is.na(row$parents) || row$parents == "") {
    # Root level node
    path <- row$labels
  } else {
    # Child node - use explicit parent-child path
    path <- paste(row$parents, row$labels, sep = "-")
  }
  
  # Add to data frame
  sunburst_data <- rbind(
    sunburst_data,
    data.frame(
      path = path,
      value = as.numeric(row$sizes),
      color = row$colors,
      stringsAsFactors = FALSE
    )
  )
}

# Create the sunburst chart
sunburst_chart <- sunburst(
  sunburst_data,
  valueField = "value",
  count = FALSE,
  legend = FALSE,
  colors = htmlwidgets::JS(
    sprintf(
      "function(d) { return d.data && d.data.color ? d.data.color : '#ccc'; }"
    )
  ),
  withD3 = TRUE
)

# Create a JPEG file
# First, save as HTML
htmlwidgets::saveWidget(sunburst_chart, "leukemia_subtypes_sunburst.html", selfcontained = TRUE)

# Then, convert to JPEG using webshot
webshot::webshot(
  "leukemia_subtypes_sunburst.html", 
  "leukemia_subtypes_sunburst.jpg", 
  delay = 2,
  zoom = 2,
  vwidth = 800,
  vheight = 800
)

# Return the chart
sunburst_chart