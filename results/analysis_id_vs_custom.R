library(rjson)
library(data.table)
library(pipeline)
library(ggplot2)
library(lme4)

data = unlist(fromJSON(file='results_10match_agressiveness.json')$results)

data_list = list()
currentIndex = 1
variables = c('win', 'player', 'opponent', 'agressiveness', 'search_depth', 'iterative_depth')
for(element in data) {
  data_list[[variables[((currentIndex-1)%%length(variables))+1]]] = c(data_list[[variables[((currentIndex-1)%%length(variables))+1]]], element)
  currentIndex = currentIndex + 1
}

tournamentDt = data.table(win = data_list$win, player = data_list$player, oponent = data_list$opponent, agressiveness = data_list$agressiveness, search_depth = data_list$search_depth, iterative_depth = data_list$iterative_depth)
tournamentDt[player== "ID_Improved", agressiveness := "1"]
fit = glm(data = tournamentDt, formula = as.numeric(win) ~ as.numeric(agressiveness), family = binomial(link = 'logit'))

summary(fit)

