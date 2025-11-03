'''
Publish a feature table to an online store

See link for further details
https://docs.databricks.com/aws/en/machine-learning/feature-store/online-feature-store#publish-a-feature-table-to-an-online-store

After your online store is in the AVAILABLE state, you can publish feature tables to make them available for low-latency access. 

Prerequisites for publishing to online stores
All feature tables (with or without time series) must meet these requirements before publishing:

- Primary key constraint: Required for online store publishing
- Non-nullable primary keys: Primary key columns cannot contain NULL values
- Change Data Feed enabled: Required for online store sync. See Enable change data feed
https://docs.databricks.com/aws/en/delta/delta-change-data-feed#enable
'''

from databricks.ml_features.entities.online_store import DatabricksOnlineStore
from databricks.feature_engineering import FeatureEngineeringClient

# Initialize the client
fe = FeatureEngineeringClient()

# Get the online store instance
online_store = fe.get_online_store(name="my-online-store")

# Publish the feature table to the online store
fe.publish_table(
    online_store=online_store,
    source_table_name="catalog_name.schema_name.feature_table_name",
    online_table_name="catalog_name.schema_name.online_feature_table_name"
)

