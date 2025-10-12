import pandas as pd

import mlflow
from mlflow.entities import Dataset

# Start a run to represent the training job
with mlflow.start_run() as training_run:
    # Load the training dataset with MLflow. We will link training metrics to this dataset.
    train_dataset: Dataset = mlflow.data.from_pandas('<your train dataframe>', name="train")
    train_x = train_dataset.df.drop(["target"], axis=1)
    train_y = train_dataset.df[["target"]]

    # Fit a model to the training dataset
    lr = MODEL()
    lr.fit(train_x, train_y)

    # Log the model, specifying its MODEL parameters (param_1, param_2)
    # As a new feature, the LoggedModel entity is linked to its name and params
    model_info = mlflow.sklearn.log_model(
        sk_model=lr,
        name="model_name",
        params={
            "param_1": 0,
            "param_2": 0,
        },
        input_example = train_x
    )

    # Inspect the LoggedModel and its properties
    logged_model = mlflow.get_logged_model(model_info.model_id)
    print(logged_model.model_id, logged_model.params)

    # Evaluate the model on the training dataset and log metrics
    # These metrics are now linked to the LoggedModel entity
    predictions = lr.predict(train_x)
    (m1, m2, m3) = compute_metrics_function(train_y, predictions)
    mlflow.log_metrics(
        metrics={
            "metric_1": m1,
            "metric_2": m2,
            "metric_3": m3,
        },
        model_id=logged_model.model_id,
        dataset=train_dataset
    )

    # Inspect the LoggedModel, now with metrics
    logged_model = mlflow.get_logged_model(model_info.model_id)
    print(logged_model.model_id, logged_model.metrics)


# Now register the model to UC. You can also see the model ID, parameters, and metrics in the UC Model Version page
CATALOG = "my_catalog"
SCHEMA = "my_schema"
MODEL = "my_model"
MODEL_NAME = f"{CATALOG}.{SCHEMA}.{MODEL}"

uc_model_version = mlflow.register_model(model_info.model_uri, name=MODEL_NAME)


# Now you can view the model version and all centralized performance data on the model version page in Unity Catalog. 
# You can also get the same information using the API as shown in the following cell.
# Get the model version
from mlflow import MlflowClient
client = MlflowClient()
model_version = client.get_model_version(name=MODEL_NAME, version=uc_model_version.version)
print(model_version)