import pandas as pd
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


import mlflow
import mlflow.sklearn
from mlflow.entities import Dataset


# Fill in this space with your own model or provide some trianing data.
# This example uses a training (train_df) and testing (test_df) dataset

my_df = "<replace with your your actual data set"

# Split into training and testing datasets
train_df, test_df = train_test_split(my_df, test_size=0.2, random_state=42)


# Helper function to compute metrics
def compute_metrics(actual, predicted):
    rmse = mean_squared_error(actual, predicted)
    mae = mean_absolute_error(actual, predicted)
    r2 = r2_score(actual, predicted)
    return rmse, mae, r2

# Start a run to represent the training job
with mlflow.start_run() as training_run:
    # Load the training dataset with MLflow. We will link training metrics to this dataset.
    train_dataset: Dataset = mlflow.data.from_pandas(train_df, name="train")
    train_x = train_dataset.df.drop(["target"], axis=1)
    train_y = train_dataset.df[["target"]]

    # Fit a model to the training dataset
    lr = ElasticNet(alpha=0.5, l1_ratio=0.5, random_state=42)
    lr.fit(train_x, train_y)

    # Log the model, specifying its ElasticNet parameters (alpha, l1_ratio)
    # As a new feature, the LoggedModel entity is linked to its name and params
    model_info = mlflow.sklearn.log_model(
        sk_model=lr,
        name="elasticnet",
        params={
            "alpha": 0.5,
            "l1_ratio": 0.5,
        },
        input_example = train_x
    )

    # Inspect the LoggedModel and its properties
    logged_model = mlflow.get_logged_model(model_info.model_id)
    print(logged_model.model_id, logged_model.params)


    # Inspect the LoggedModel and its properties
    logged_model = mlflow.get_logged_model(model_info.model_id)
    print(logged_model.model_id, logged_model.params)

    # Evaluate the model on the training dataset and log metrics
    # These metrics are now linked to the LoggedModel entity
    predictions = lr.predict(train_x)
    (rmse, mae, r2) = compute_metrics(train_y, predictions)
    mlflow.log_metrics(
        metrics={
            "rmse": rmse,
            "r2": r2,
            "mae": mae,
        },
        model_id=logged_model.model_id,
        dataset=train_dataset
    )

    # Inspect the LoggedModel, now with metrics
    logged_model = mlflow.get_logged_model(model_info.model_id)
    print(logged_model.model_id, logged_model.metrics)


# Start a run to represent the test dataset evaluation job
with mlflow.start_run() as evaluation_run:
  # Load the test dataset with MLflow. We will link test metrics to this dataset.
  test_dataset: mlflow.entities.Dataset = mlflow.data.from_pandas(test_df, name="test")
  test_x = test_dataset.df.drop(["quality"], axis=1)
  test_y = test_dataset.df[["quality"]]

  # Load the model
  model = mlflow.sklearn.load_model(f"models:/{logged_model.model_id}")

  # Evaluate the model on the training dataset and log metrics, linking to model
  predictions = model.predict(test_x)
  (rmse, mae, r2) = compute_metrics(test_y, predictions)
  mlflow.log_metrics(
    metrics={
      "rmse": rmse,
      "r2": r2,
      "mae": mae,
    },
    dataset=test_dataset,
    model_id=logged_model.model_id
  )


# Now register the model to UC. You can also see the model ID, parameters, and metrics in the UC Model Version page
CATALOG = "my_catalog"
SCHEMA = "my_schema"
MODEL = "my_model"
MODEL_NAME = f"{CATALOG}.{SCHEMA}.{MODEL}"

uc_model_version = mlflow.register_model(model_info.model_uri, name=MODEL_NAME)


# Now you can view the model version and all centralized performance data on the model version page in Unity Catalog. You can also get the same information using the API as shown in the following cell.
# Get the model version
from mlflow import MlflowClient
client = MlflowClient()
model_version = client.get_model_version(name=MODEL_NAME, version=uc_model_version.version)
print(model_version)