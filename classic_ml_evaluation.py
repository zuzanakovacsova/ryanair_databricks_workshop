# For the evaluation of classical ML, one can use the mlflow evaluate framework. 

# For example, for a regression model, mlflow will calculate MSE, MAE and R2. 
import mlflow

data = <sample data with features and answer column> #fill in
target = "<target colum name>" #fill in
model_uri = "models:/" + "<model_name>" + "/" + "<model_version>"  #fill in

with mlflow.start_run(run_name = "evaluation"):
    # Log and evaluate regression model
    model_uri = mlflow.get_artifact_uri("model")

    result = mlflow.models.evaluate(
        model_uri,
        data = data,
        targets=target,
        model_type="regressor"
    )

# These metrics will be shown in the mlflow UI 

# You can also define custom metrics and use them in mlflow.models.evaluate(), for more details see
#  https://mlflow.org/docs/3.1.3/ml/evaluation/metrics-visualizations/#quick-start-creating-custom-metrics