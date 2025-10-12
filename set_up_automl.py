'''
Set up AutoML experiment with the AutoML API
https://docs.databricks.com/aws/en/machine-learning/automl/regression-train-api#setup-an-experiment-using-the-automl-api
'''

from databricks import automl

# Regression example
summary = automl.regress(dataset=train_pdf, target_col="col_to_predict")

# Classification example
summary = automl.classification(dataset=train_pdf, target_col="col_to_predict")

# Forecasting example
summary = automl.forecast(dataset=train_pdf, target_col="col_to_predic", time_col="date_col", horizon=horizon, frequency="d", output_database="default")



# The following command displays information about the AutoML output.
help(summary)

# You can use the model trained by AutoML to make predictions on new data. 
model_uri = summary.best_trial.model_path