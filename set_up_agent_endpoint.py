# Compared to client.create_endpoint, agent.deploy() is a higher-level Databricks Agents SDK API that takes 
# a Unity Catalog–registered AI agent (MLflow ResponsesAgent/ChatAgent) and deploys it to Mosaic AI Model
# Serving, wiring up review apps, inference tables, and tracing/monitoring out of the box. 

# Use agents.deploy() when you’re deploying a Databricks-authored agent and want 
# integrated deployment + review UI + AI Gateway-enabled inference tables + MLflow tracing/monitoring with minimal config.

# agents.deploy() requires the databricks-agents SDK and an agent logged/registered to Unity Catalog.

from databricks import agents

# Deploy a UC-registered agent (model name + version)
deployment = agents.deploy("<your model, e.g. catalog.schema.agent_model>", <model version integer>) #fill in

print("Query URL:", deployment.query_endpoint) #your endpoint
