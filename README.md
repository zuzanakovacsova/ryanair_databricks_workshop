# Databricks workshop Wrocław October 2025

Welcome to our Databricks hands-on session! These materials have all the tools and documentation you need to build and productionise classical ML models and GenAI agents. 

## End-to-end model deployment pipeline
### Hyperparameter tuning (optional)
### Register and retrieve model 
### Set up an online feature store
### Build a multi-agent system
Using Langchain, one can orchestrate 
#### Example notebook
#### Set up a Genie space 
If you are interested in your agent being able to call a Genie space as a tool, you can import the following notebook for example code: https://docs.databricks.com/aws/en/notebooks/source/generative-ai/langgraph-multiagent-genie.html
##### Genie
Genie is Databricks AI/BI’s conversational analytics tool. Business users ask natural-language questions, Genie generates SQL over governed Unity Catalog data and returns tables or visualizations.\
Create a space: click Genie in the sidebar → New; choose Unity Catalog tables/views, set a default warehouse, add a clear title/description and optional sample questions.\
Teach Genie for accuracy: add verified example SQL queries, relevant UC functions, and concise instructions; start small (focused, well-annotated tables) and use data sampling to improve column/value matching. 
### Set up custom judges
### Serve model
#### Real-time querying
#### Batch inference
### Deploy model in an app
#### Connect your app to a Lakebase instance
### Set up monitoring
### Deploy your model with MLOps stacks
[MLOps stacks](https://github.com/databricks/mlops-stacks) has a template for deploying ML models in Databricks that follow production best practices, including asset bundles, testing and deploying via GitHub actions or Azure DevOps. 
Initial setup is not trivial (setting up of workspaces, repos, credentials...) so we recommend to deprioritise spending time on this during the workshop.


