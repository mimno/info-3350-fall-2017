library(tidyverse)

file_vectors <- read_tsv("file_vectors.tsv")
word_vectors <- read_tsv("word_vectors.tsv")

# geom_* specifies shapes
# aes(...) defines visual properties of those shapes
for (i in 1:4) {
  x_var = as.name(paste("V", i, sep=""))
  for (j in (i+1):5) {
    y_var = as.name(paste("V", j, sep=""))
    p <- ggplot(file_vectors, aes_(x=x_var, y=y_var, label=as.name("Title")))
    p + geom_point() + geom_text(alpha=0.8, hjust="inward", vjust="inward", size=2) + ggtitle(paste("Factors", i, "and", j)) + theme_minimal()
    ggsave(paste("figures/files_", i, "_", j, ".pdf", sep=""), height=8, width=8)
  }
}

