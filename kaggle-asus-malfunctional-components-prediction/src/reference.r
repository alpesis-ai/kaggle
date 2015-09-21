require(plyr)
options(stringsAsFactors = FALSE)
setwd("~/asus")
 
DEFAULT_DECAY <- -.05
 
SaleTrain <- read.csv("SaleTrain.csv")
RepairTrain <- read.csv("RepairTrain.csv")
mapping <- read.csv("Output_TargetID_Mapping.csv")
 
mapping$id <- 1:nrow(mapping)
 
# Fix goofy names in the source data
names(SaleTrain)[3] <- "year_month_sale"
names(RepairTrain)[3] <- "year_month_sale"
names(RepairTrain)[4] <- "year_month_repair"
 
# Create derived variables
repair_train <- transform(RepairTrain, 
                          year_repair  = as.integer(substr(year_month_repair, 1, 4)), 
                          month_repair = as.integer(substr(year_month_repair, 6, 7)),
                          year_sale    = as.integer(substr(year_month_sale, 1, 4)), 
                          month_sale   = as.integer(substr(year_month_sale, 6, 7)))
 
repair_train <- transform(repair_train, 
                          year_month_repair = year_repair * 100 + month_repair,
                          year_month_sale = year_sale * 100 + month_sale,
                          number_repair = pmax(number_repair, 0))
 
# Right now just projecting off the last six months in the experience period
repair_train <- subset(repair_train, year_month_repair >= 200907)
 
# repair_train is at the individual repair level, roll it up to make predictions
repair_agg <- aggregate(number_repair ~ module_category + component_category +
                                    year_month_repair, repair_train, sum)
repair_agg$t <- repair_agg$year_month_repair - 200907
 
# Create a block_id for each module/component combination
df_id <- unique(mapping[ , c("module_category", "component_category")])
df_id$block_id <- 1:nrow(df_id)
repair_agg <- merge(repair_agg, df_id)
 
# Function for fitting exponential decay models to repair counts
linmod <- function(df) {
  lm(log(number_repair) ~ t, data = df)$coef
}
 
# Compute a model for each module/component combination
models <- ddply(repair_agg, .(block_id), linmod)
avg <- with(repair_agg, tapply(number_repair, block_id, mean))
ind <- models$t > -.001
ind[is.na(ind)] <- FALSE
models$t[ind] <- DEFAULT_DECAY
models$"(Intercept)"[ind] <- log(avg[ind]) - 5*DEFAULT_DECAY
 
# Join model coefficients to test data and make predictions
mapping <- merge(mapping, df_id, all.x = TRUE)
mapping <- merge(mapping, models, all.x = TRUE )
mapping <- rename(mapping, c("(Intercept)"="beta0", "t" = "beta1"))
mapping$t <- with(mapping, (year - 2009) * 12 +(month - 7))
mapping$pred <- round(with(mapping, round(exp(beta1*t + beta0), 1)), 0)
 
# NAs for model coefficients means we did not have enough non-zero
# data for a fit, so 0 is the appropriate prediction
mapping$pred[is.na(mapping$pred)] <- 0
 
# Two out of three zeros filter
zero_check <- ddply(repair_agg, .(block_id), summarize, 
                    nonzero = sum(number_repair > 0 & year_month_repair >= 200910))
mapping <- merge(mapping, zero_check, all.x = T)
mapping$pred <- with(mapping, ifelse(!is.na(nonzero) & nonzero <= 1, 0, pred))
 
sub <- mapping[, c("id", "pred")]
colnames(sub) <- c("id", "target")
sub <- arrange(sub, id)
write.csv(sub, "submission.csv", row.names=F)
