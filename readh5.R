library(rhdf5)

get_read_counts <- function(file_path, target_gene_symbol) {
  # Open the h5 file
  h5file <- H5Fopen(file_path)
  
  # Try reading gene symbols
  if ("gene_symbols" %in% h5ls(h5file)$name) {
    gene_symbols <- h5read(h5file, "gene_symbols")
  } else if ("gene_names" %in% h5ls(h5file)$name) {
    gene_symbols <- h5read(h5file, "gene_names")
  } else {
    H5Fclose(h5file)
    stop("Neither 'gene_symbols' nor 'gene_names' found in the file.")
  }

  # Find the index of the target gene symbol
  gene_index <- which(gene_symbols == target_gene_symbol)

  if (length(gene_index) > 0) {
    # Read the counts data
    all_counts <- h5read(h5file, "counts")

    # Extract the read counts for the target gene (all rows, the identified column)
    read_counts <- all_counts[, gene_index]

    H5Fclose(h5file)
    return(read_counts)
  } else {
    H5Fclose(h5file)
    return(NULL)
  }
}

# Function to calculate descriptive statistics
calculate_statistics <- function(read_counts) {
  stats <- list(
    mean = mean(read_counts),
    median = median(read_counts),
    std_dev = sd(read_counts),
    min = min(read_counts),
    max = max(read_counts)
  )
  return(stats)
}

# Example usage
file_path <- '~/data/tp/files/hg38/ash/transcriptomics/ash.hg38.fpkm.matrix2.h5'
gene_name <- 'DUX4'
read_counts <- get_read_counts(file_path, gene_name)

if (!is.null(read_counts)) {
  stats <- calculate_statistics(read_counts)
  print(paste("Descriptive statistics for gene", gene_name, ":"))
  print(paste("Mean:", stats$mean))
  print(paste("Median:", stats$median))
  print(paste("Standard Deviation:", stats$std_dev))
  print(paste("Minimum:", stats$min))
  print(paste("Maximum:", stats$max))
} else {
  print(paste("Gene", gene_name, "not found in the file."))
}
