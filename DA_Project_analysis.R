
#naming the file
library(ggplot2)
movies_everything1  <-  movies_everything[,1  :  4]   

names(movies_everything1)  <-  c("Movies",  "US_Revenue"
                ,  "Foreign_Revenue",  "International_Revenue")
revenue_relation  <-  lm(Foreign_Revenue  ~  US_Revenue
                         ,  data  =  movies_everything1)

p1  <-  ggplot(movies_everything1,  aes(x  =  US_Revenue,  y  =  Foreign_Revenue))
p1  <-  p1  +  geom_point()
p1  <-  p1  +  labs(title  =  "Rich here then Rich outside too")  
p1  <-  p1  +  theme(plot.title  =  element_text(lineheight  =  1.8,  face  =  "bold"))
p1  <-  p1  +  stat_smooth(method  =  "glm",   fill  =  "blue", 
                           colour  =  "darkblue",  size  =  2,  alpha  =  0.25)
p1  <-  p1  +  theme(aspect.ratio  =  1) 
p1  <-  p1  +  theme(panel.background  =  element_rect(fill  =  "lightblue"))
ggsave("Foreign_US.png",  p1)
