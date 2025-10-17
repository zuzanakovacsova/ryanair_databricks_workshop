from mlflow.deployments import get_deploy_client

# Deploy a seving endpoint. Suitable for creating generic Model Serving endpoints (custom models,
# foundation models with provisioned throughput, and external models like OpenAI/Anthropic)
# with explicit configuration of served entities, routing, compute, and governance features.
# Use client.create_endpoint() when you need full control or non-agent workloads.

# For deploying agent andpoints, try agents.deploy() instead.

client = get_deploy_client("databricks")

# Choose an endpoint name
endpoint_name = "<your_endpoint_name>"
try: 
    endpoint = client.create_endpoint(
        name=endpoint_name,
        config = {
            "served_entities": [
                {
                    "name": "<your_served_entity_name>", #fill in
                    "entity_name": "<catalog>,<schema>.<your_served_entity_name>", #fill in
                    "model_version": "<version, e.g. 1>", #fill in
                    "scale_to_zero_enabled": True,
                    "workload_size": "Small",
                },
            ],
            "traffic_config": {
                "routes": [
                    {"served_model_name": "<your_served_entity_name>-<version, e.g. 1>", "traffic_percentage": 100}, #fill in
                ]
            },
            "auto_capture_config":{
                "catalog_name": "<catalog>", #fill in
                "schema_name": "<schema>", #fill in
                "table_name_prefix": "<inference_table_prefix>" #fill in
            }
        }
    )

except Exception as e:
  if f"Endpoint with name '{endpoint_name}' already exists" in e.args[0]:
    print(f"Endpoint with name {endpoint_name} already exists")
  else:
    raise(e)
  
  # Endpoints can take a while to spin up, you can monitor the progress in the UI.