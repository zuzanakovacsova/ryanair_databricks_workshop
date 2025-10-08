from mlflow.deployments import get_deploy_client

client = get_deploy_client("databricks")
endpoint_name = "<your_endpoint_name>"
try: 
    endpoint = client.create_endpoint(
        name=endpoint_name,
        config = {
            "served_entities": [
                {
                    "name": "<your_served_entity_name>",
                    "entity_name": "<catalog>,<schema>.<your_served_entity_name>",
                    "model_version": "<version, e.g. 1>",
                    "scale_to_zero_enabled": True,
                    "workload_size": "Small",
                },
            ],
            "traffic_config": {
                "routes": [
                    {"served_model_name": "<your_served_entity_name>-<version, e.g. 1>", "traffic_percentage": 100},
                ]
            },
            "auto_capture_config":{
                "catalog_name": "<catalog>",
                "schema_name": "<schema>",
                "table_name_prefix": "<inference_table_prefix"
            }
        }
    )

except Exception as e:
  if f"Endpoint with name '{endpoint_name}' already exists" in e.args[0]:
    print(f"Endpoint with name {endpoint_name} already exists")
  else:
    raise(e)