# %pip install mlflow --upgrade
# %pip install optuna


'''
Define an objective function to optimize. Within the objective function, define the hyperparameter search space. 
For more details, see Optuna documentation.

Below is an example for model selection and hyperparameter tuning with sckit-learn. 
The example defines the objective function objective, and calls the suggest_float function to define the search space for the parameter x.
'''

import sklearn

def objective(trial):
    # Invoke suggest methods of a Trial object to generate hyperparameters.
    regressor_name = trial.suggest_categorical('classifier', ['SVR', 'RandomForest'])
    if regressor_name == 'SVR':
        svr_c = trial.suggest_float('svr_c', 1e-10, 1e10, log=True)
        regressor_obj = sklearn.svm.SVR(C=svr_c)
    else:
        rf_max_depth = trial.suggest_int('rf_max_depth', 2, 32)
        regressor_obj = sklearn.ensemble.RandomForestRegressor(max_depth=rf_max_depth)

    X, y = sklearn.datasets.fetch_california_housing(return_X_y=True)
    X_train, X_val, y_train, y_val = sklearn.model_selection.train_test_split(X, y, random_state=0)

    regressor_obj.fit(X_train, y_train)
    y_pred = regressor_obj.predict(X_val)

    error = sklearn.metrics.mean_squared_error(y_val, y_pred)

    return error  # An objective value linked with the Trial object



'''
Create a shared storage for distributed optimization. With MlflowStorage, you can use MLflow Tracking Server as the storage backend.
'''

import mlflow
from mlflow.optuna.storage import MlflowStorage

experiment_id = mlflow.get_experiment_by_name(dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()).experiment_id

mlflow_storage = MlflowStorage(experiment_id=experiment_id)


'''
Create an Optuna Study object, and run the tuning algorithm by calling the optimize function of the Study object. MlflowSparkStudy can run launching parallel Optuna studies using PySpark executors.
Below is an example from the Optuna documentation.

Create a Study, and optimize the objective function with 8 trials (8 calls of the objective function with different values of x).
Get the best parameters of the Study
'''


from mlflow.pyspark.optuna.study import MlflowSparkStudy

mlflow_study = MlflowSparkStudy(
    study_name="spark-mlflow-tuning",
    storage=mlflow_storage,
)

mlflow_study.optimize(objective, n_trials=8, n_jobs=4)

best_params = study.best_params