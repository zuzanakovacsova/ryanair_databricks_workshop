'''
Databricks Online Feature Stores are a high-performance, scalable solution for serving feature data to online applications and real-time machine learning models. 
Powered by Databricks Lakebase, it provides low-latency access to feature data at a high scale while maintaining consistency with your offline feature tables.

The primary use cases for Online Feature Stores include:

- Serving features to real-time applications like recommendation systems, fraud detection, and personalization engines using Feature Serving Endpoints.
- Automatic feature lookup for real-time inference in model serving endpoints.
'''


# %pip install databricks-feature-engineering>=0.13.0
# dbutils.library.restartPython()


from databricks.feature_engineering import FeatureEngineeringClient

# Initialize the client
fe = FeatureEngineeringClient()

# Create an online store with specified capacity
fe.create_online_store(
    name="my-online-store",
    capacity="CU_2"  # Valid options: "CU_1", "CU_2", "CU_4", "CU_8"
)

# Get information about an existing online store
store = fe.get_online_store(name="my-online-store")
if store:
    print(f"Store: {store.name}, State: {store.state}, Capacity: {store.capacity}")

# Update the capacity of an online store
updated_store = fe.update_online_store(
    name="my-online-store",
    capacity="CU_4"  # Upgrade to higher capacity
)