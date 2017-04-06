library(rjson)
library(data.table)
library(pipeline)
library(ggplot2)
library(lme4)

data = unlist(fromJSON(file='results.json')$results)

data_list = list()
currentIndex = 1
variables = c('win', 'player', 'opponent', 'agressiveness', 'search_depth', 'iterative_depth')
for(element in data) {
  data_list[[variables[((currentIndex-1)%%length(variables))+1]]] = c(data_list[[variables[((currentIndex-1)%%length(variables))+1]]], element)
  currentIndex = currentIndex + 1
}

tournamentDt = data.table(win = data_list$win, player = data_list$player, oponent = data_list$opponent, agresiveness = data_list$agressiveness, search_depth = data_list$search_depth, iterative_depth = data_list$iterative_depth)
tournamentDt[player== "ID_Improved", agresiveness := "1"]
fit = glm(data = tournamentDt[iterative_depth == 0,], formula = as.numeric(win) ~ search_depth * oponent, family = binomial(link = 'logit'))

fitlm = lm(data = tournamentDt[iterative_depth == 0,], formula = win ~ search_depth)

averaged_data = tournamentDt[, list(win_avg = mean(as.numeric(win))), by=c("player", "oponent", "iterative_depth", "search_depth", "agresiveness")]
averaged_data[, player_depth_agressiveness := paste0(player, search_depth, agresiveness)]

PlotXAgainstY(data = averaged_data[player == "ID_Improved" || iterative_depth == 0,], dependantVar = "win_avg", groupingVars = c("player_depth_agressiveness"))

tournamentDt[,win := as.numeric(win)]
tournamentDt[,agresiveness := as.numeric(agresiveness)]
PlotXAgainstY(data = tournamentDt[iterative_depth == 1,], dependantVar = "win", groupingVars = c("agresiveness", "oponent"))

results_er = glmer(formula = win ~  agresiveness + 1|oponent , data = tournamentDt[iterative_depth == 1,], family = binomial)
results_glm = glm(formula = win ~  agresiveness + oponent , data = tournamentDt[iterative_depth == 1,], family = binomial)
results_glm = glm(formula = win ~  agresiveness , data = tournamentDt[iterative_depth == 1 & oponent == "AB_Open",], family = binomial(link = "logit"))
results_glm = glm(formula = win ~  agresiveness , data = tournamentDt[iterative_depth == 1 & agresiveness <= 2,], family = binomial(link = "logit"))

PlotXAgainstY(data = tournamentDt[iterative_depth == 1 & agresiveness <= 5,], dependantVar = "win", groupingVars = c("agresiveness"))

