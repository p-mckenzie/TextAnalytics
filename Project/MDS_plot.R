library(ggrepel)
library(tidyverse)
library(ggalt)
MDS_df <- read.csv("MDS_cluster.csv")
MDS_df$X <- NULL

wine_type <- c("White","Red","Red","Red","Red",
               "White","Red","White","Red","Red",
               "Red","Red","White","Special","Red",
               "Red","Red","White","Red","Red",
               "Red","Red","White","Red","Red")

MDS_df$type_wine <- wine_type
reds <- MDS_df %>% filter(type_wine == "Red")
whites <- MDS_df %>% filter(type_wine == "White")


ggplot(MDS_df) +
  geom_point(aes(x=x_vals,y=y_vales),size = 5, color = 'grey') +
  geom_text_repel(
    aes(x_vals, y_vales, label = names),
    fontface = 'bold', color = 'green',
    box.padding = 0.35, point.padding = 0.5,
    segment.color = 'grey50') + 
  geom_encircle(aes(x=x_vals, y=y_vales),
                data=reds,
                color="red",
                size=2,
                expand=0.08) + 
  geom_encircle(aes(x=x_vals, y=y_vales),
                data=whites,
                color="white",
                size=2,
                expand=0.08) + 
  labs(x="",y="",titles="MDS Map of Wine Types") + 
  #theme_dark(base_size = 11, base_family = "") + 
  theme_solarized_2(light = FALSE) + 
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())

### Attempt a polar plot to see if there are differences.    
ggplot(MDS_df,aes(x=x_vals,y=y_vales)) +
  geom_point(size = 5, color = 'grey') +
  geom_text_repel(
    aes(x_vals, y_vales, label = names),
    fontface = 'bold', color = 'green',
    box.padding = 0.35, point.padding = 0.5,
    segment.color = 'grey50') + 
  coord_polar() 
  
 


