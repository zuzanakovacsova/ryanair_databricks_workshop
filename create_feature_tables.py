'''Feature tables in Unity Catalog are Delta tables. Feature tables must have a primary key. 
Feature tables, like other data assets in Unity Catalog, are accessed using a three-level namespace: <catalog-name>.<schema-name>.<table-name>.

Feature Engineering in Unity Catalog has a Python client FeatureEngineeringClient. 
The class is available on PyPI with the databricks-feature-engineering package and is pre-installed in Databricks Runtime 13.3 LTS ML and above. 
If you use a non-ML Databricks Runtime, you must install the client manually. 

'''

# %pip install databricks-feature-engineering
# dbutils.library.restartPython()


from databricks.feature_engineering import FeatureEngineeringClient

fe = FeatureEngineeringClient()

# Prepare feature DataFrame
def compute_customer_features(data):
  ''' Feature computation code returns a DataFrame with 'customer_id' as primary key'''
  pass

customer_features_df = compute_customer_features(df)

# Create feature table with `customer_id` as the primary key.
# Take schema from DataFrame output by compute_customer_features
customer_feature_table = fe.create_table(
  name='ml.recommender_system.customer_features',
  primary_keys='customer_id',
  schema=customer_features_df.schema,
  description='Customer features'
)


# Read from a feature table in Unity Catalog
# Use read_table to read feature values.
customer_features_df = fe.read_table(
  name='ml.recommender_system.customer_features',
)