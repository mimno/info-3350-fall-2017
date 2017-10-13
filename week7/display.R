library(tidyverse)

file_vectors <- read_tsv("file_vectors.tsv")

# geom_* specifies shapes
# aes(...) defines visual properties of those shapes
ggplot(file_vectors, aes(x=V0, y=V1, label=Title)) + geom_point() + geom_text(alpha=0.8)
