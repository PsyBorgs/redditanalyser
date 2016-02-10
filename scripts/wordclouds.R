#!/usr/bin/env Rscript
library(wordcloud)
library(RColorBrewer)


DATA_DIR <- file.path("data")
WORD_CLOUD_DIR <- file.path("build", "wordclouds")
FREQ_TABLES_DIR <- file.path(DATA_DIR, "freq_tables")
DESC_STATS_PATH <- file.path(DATA_DIR, "desc_stats.csv")


# get descriptive stats (with subreddit names and IDs)
desc_stats <- read.csv(DESC_STATS_PATH, row.names = 1)

# subreddit info
subreddits <- desc_stats[, c("subreddit_name", "subreddit_id")]
names(subreddits) <- c("name", "id")

for(i in 1:nrow(subreddits)) {
  # import subreddit frequency tables
  .path <- file.path(FREQ_TABLES_DIR, paste0(subreddits$id[i], ".csv"))
  .subreddit.ft <- read.csv(.path)
  names(.subreddit.ft) <- c("word", "count")

  # generate word clouds for each subreddit
  .word_cloud_filename <- paste0(subreddits$name[i], ".png")
  .word_cloud_path <- file.path(WORD_CLOUD_DIR, .word_cloud_filename)

  png(.word_cloud_path, width = 1200, height = 1200)
  wordcloud(
    .subreddit.ft$word, .subreddit.ft$count,
    scale = c(14, 1), colors = brewer.pal(8, "Dark2"),
    min.freq = 20, max.words = 150, random.order = FALSE
  )
  dev.off()
}



