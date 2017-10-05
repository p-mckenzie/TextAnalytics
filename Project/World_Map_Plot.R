library(tidyverse)
library(ggmap)
options(stringsAsFactors = FALSE)
wine_df <- read.csv("winemag-data_first150k.csv",na.strings=c(""," ","NA"))
## Drop Variable
wine_df$X <- NULL

usa_df_loc <- wine_df %>% filter(country == "US")
not_usa_df_loc <- wine_df %>% filter(!(country == "US"))

usa_df_loc$location <- apply(usa_df_loc[,c('region_1','province','country')], 1, function(x) toString(na.omit(x)))
not_usa_df_loc$location <- apply(not_usa_df_loc[,c('region_1','country')], 1, function(x) toString(na.omit(x)))

wine_df <- rbind(usa_df_loc,not_usa_df_loc)

### Aggregate Location

## When not US, use country
## When NA in region_1 just use country
loc_subset <- wine_df %>% select(location) %>% distinct()

geo_pause <- function(locat){
  print(locat)
  deg <- geocode(locat,override_limit=TRUE)
  return(deg)
}

loc_subset$loc_det <- apply(loc_subset,1,geo_pause)
saveRDS(loc_subset,"location.RDS",compress = FALSE)

loc_subset <- loc_subset %>% unnest()

### Merge Locations back
map_wine_loc <- wine_df %>% group_by(location) %>% summarize(count=n())

map_wine_loc <- inner_join(map_wine_loc,loc_subset,by="location")
wine_selc <- wine_df %>% select(location,country) %>% distinct()
map_wine_loc <- inner_join(map_wine_loc,wine_selc,by="location")
map_wine_loc$country <- as.factor(map_wine_loc$country)


map_wine_finish <- map_wine_loc %>% mutate(perc = count/sum(count)) %>% filter(count>300)


#### Plot on map
library(maptools)
library(maps)
library(ggthemes)
mp <- NULL
mapWorld <- borders("world", colour="gray50", fill="gray50") # create a layer of borders
mp <- ggplot() +   mapWorld

#Now Layer the cities on top
mp <- mp+ geom_point(data=map_wine_finish,aes(x=lon, y=lat,size=count,color=country))
mp + theme_map() + theme(strip.background=element_blank()) + theme(legend.position="none")
