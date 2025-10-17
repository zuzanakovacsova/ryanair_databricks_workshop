# Databricks workshop Wrocław October 2025

Welcome to our Databricks hands-on session! These materials have all the tools and documentation you need to build and productionise classical ML models and GenAI agents. 

## End-to-end model deployment pipeline
### Hyperparameter tuning (optional)
### Register and retrieve model 
### Set up an online feature store
### Build a multi-agent system
One can orchestrate a multiagent system, with an agent calling tools, and a supervisor LLM deciding what the appropriate tools are. In this example, an agent has access to a genie space to get data points. However, one can also give it access to a knowledge store, MCP server, and any other tool.
#### Multi-agent system with a Genie space
If you are interested in your agent being able to call a Genie space as a tool, you can import the following notebook for example code: https://docs.databricks.com/aws/en/notebooks/source/generative-ai/langgraph-multiagent-genie.html \
Make sure to fill all the `TODO` sections.
##### Genie
Genie is Databricks AI/BI’s conversational analytics tool. Business users ask natural-language questions, Genie generates SQL over governed Unity Catalog data and returns tables or visualizations.\
Create a space: click Genie in the sidebar → New; choose Unity Catalog tables/views, set a default warehouse, add a clear title/description and optional sample questions.\
Teach Genie for accuracy: add verified example SQL queries, relevant UC functions, and concise instructions; start small (focused, well-annotated tables) and use data sampling to improve column/value matching. 
### Serve model
Once 
#### Real-time querying
#### Batch inference
### Model evaluation 
### Monitoring
### Deploy model in an app
Once your model is served, once can query it from an app in Databricks Apps. To deploy lakehouse apps, you only need the source code (many frameworks are supported, eg. Dash, Streamlit, Node.js...) and when creating the compute,  give your app access to the Databricks resources it might have to query. For example, if you want to deploy the agent that is calling a Genie space in your app, you need to add the endpoint, the Genie space and the corresponding warehouse as an [app resource](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/resources). 
#### Chatbot app
This repo has source code for a basic streamlit app that will connect to your endpoint. While the `app.yaml` file does reference the `SERVING_ENDPOINT` environmental variable, you do not have to set this as it will be assigned from the resource.\
However, if you are going to test your app locally, you will have to set this variable, either as an environmental variable, or you can use [Databricks secrets](https://docs.databricks.com/aws/en/security/secrets/) to fetch it.
#### Connect your app to a Lakebase instance
### Deploy your model with MLOps stacks
[MLOps stacks](https://github.com/databricks/mlops-stacks) has a template for deploying ML models in Databricks that follow production best practices, including asset bundles, testing and deploying via GitHub actions or Azure DevOps. 
Initial setup is not trivial (setting up of workspaces, repos, credentials...) so we recommend to deprioritise spending time on this during the workshop.


