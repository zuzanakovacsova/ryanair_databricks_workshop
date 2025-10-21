# Databricks workshop Wrocław October 2025

Welcome to our Databricks hands-on session! These materials have all the tools and documentation you need to build and productionise classical ML models and GenAI agents. 

## End-to-end model deployment pipeline
### Hyperparameter tuning (optional)
### Register and retrieve model 

### Feature stores
The Databricks Feature Store provides a central registry for features used in your AI and ML models.  When you use features from the feature store to train models, the model automatically tracks lineage to the features that were used in training. At inference time, the model automatically looks up the latest feature values. The feature store also provides on-demand computation of features for real-time applications. 

- [See Feature Store concepts here](https://docs.databricks.com/aws/en/machine-learning/feature-store/concepts)
- [See an example tutorial notebook](https://docs.databricks.com/aws/en/notebooks/source/machine-learning/feature-store-with-uc-taxi-example.html)

### Set up an online feature store
Databricks Online Feature Stores are a high-performance, scalable solution for serving feature data to online applications and real-time machine learning models. 
Powered by Databricks Lakebase, it provides low-latency access to feature data at a high scale while maintaining consistency with your offline feature tables.

The primary use cases for Online Feature Stores include:

- Serving features to real-time applications like recommendation systems, fraud detection, and personalization engines using Feature Serving Endpoints.
- Automatic feature lookup for real-time inference in model serving endpoints.

### Build a multi-agent system
One can orchestrate a multiagent system, with an agent calling tools, and a supervisor LLM deciding what the appropriate tools are. In this example, an agent has access to a genie space to get data points. However, one can also give it access to a knowledge store, MCP server, call an ML model or use any other tool. \
An example of how to crate custom tools can be found [here](https://github.com/zuzanakovacsova/ryanair_databricks_workshop/blob/main/create_tools.py). After you have created the tools, you can use Playground to provide an agent access to those tools. Note that not all LLMs available in the Playground will be able to use tools, you have to pick one with the "Tools enabled" tag, for example GPT OSS 20B. You can then add your UC registered tools, customise the prompt and toggle judges. When ready, you can export the code to deploy your new agent.
#### Multi-agent system with a Genie space
If you are interested in your agent being able to call a Genie space as a tool, you can import [this notebook](https://docs.databricks.com/aws/en/notebooks/source/generative-ai/langgraph-multiagent-genie.html) for example code. \
Make sure to fill all the `TODO` sections.
##### Genie
Genie is Databricks AI/BI’s conversational analytics tool. Business users ask natural-language questions, Genie generates SQL over governed Unity Catalog data and returns tables or visualizations.\
Create a space: click Genie in the sidebar → New; choose Unity Catalog tables/views, set a default warehouse, add a clear title/description and optional sample questions.\
Teach Genie for accuracy: add verified example SQL queries, relevant UC functions, and concise instructions; start small (focused, well-annotated tables) and use data sampling to improve column/value matching. 
### Serve model/agent
Once your classical ML model or agent is ready for deployment, use Model Serving to deploy it. Model serving is the process of deploying a trained model behind a scalable, governed endpoint (typically a REST API) so applications can send requests and receive predictions in real time. \
You can serve a model from the the model UI in Unity Catalog, or use APIs. There are two code samples, either [`client.create_endpoint()`](https://github.com/zuzanakovacsova/ryanair_databricks_workshop/blob/main/set_up_endpoint.py) more suitable for classical ML models (more customisation needed) or [`agents.deploy()`](https://github.com/zuzanakovacsova/ryanair_databricks_workshop/blob/main/set_up_agent_endpoint.py) which is focused on MLflow ResponsesAgents / ChatAgents.
#### Real-time querying & batch inference
Once you have a serving endpoint, the model is available for real-time or batch inference. You can try it out in the Playground, using the REST API or using `ai_query`. The UI has a **Use** button to take you to Playground or show curl examples. `ai_query` code examples can be seen in [`use_ai_query.sql`](https://github.com/zuzanakovacsova/ryanair_databricks_workshop/blob/main/use_ai_query.sql) \
\
`ai_query` gives you SQL-native, serverless, auto-scaling batch inference, with structured outputs and built-in monitoring. You can however also do batch inference locally on the cluster with Spark UDFs or with pandas UDF, retrieving the model from UC or mlflow registry.
### Model evaluation 
mlflow 3 on Databricks provides solutions for GenAI evaluation and classical ML evaluation. An example of evaluating an LLM model can be found [here](https://github.com/zuzanakovacsova/ryanair_databricks_workshop/blob/main/agent_evaluation.py). Evaluation can be run against sample answers, with custom metrics, and one can also use the Databricks review app to engage SMEs and collect their feedback. \
For classical ML, `mlflow.evaluate()` provides common metrics out of the box or one can use custom metrics. Example code can be found [here](https://github.com/zuzanakovacsova/ryanair_databricks_workshop/blob/main/classic_ml_evaluation.py). \
\
The promotion/comparison of new model versions can be automated with Deployment jobs. Deployment jobs automate evaluation, gated approval, and deployment for each new Unity Catalog model version by linking the model to a Lakeflow Job, with status and history tracked on the model/version pages. Approval can either be based on the passing of metrics, or a person can validate them and approve the deployment of the model. Find out more about Deployment jobs, and example notebooks, in the [docs](https://docs.databricks.com/aws/en/mlflow/deployment-job).
### Monitoring
### Deploy model in an app
Once your model is served, once can query it from an app in Databricks Apps. To deploy lakehouse apps, you only need the source code (many frameworks are supported, eg. Dash, Streamlit, Node.js...) and when creating the compute,  give your app access to the Databricks resources it might have to query. For example, if you want to deploy the agent that is calling a Genie space in your app, you need to add the endpoint, the Genie space and the corresponding warehouse as an [app resource](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/resources). 
#### Chatbot app
This repo has an [example](https://github.com/zuzanakovacsova/ryanair_databricks_workshop/tree/main/streamlit-chatbot-app) of a simple streamlit app that will connect to your endpoint. While [`app.yaml`](https://github.com/zuzanakovacsova/ryanair_databricks_workshop/blob/main/streamlit-chatbot-app/app.yaml) does reference the `SERVING_ENDPOINT` environmental variable, you do not have to set this as it will be assigned from the resource.\
However, if you are going to test your app locally, you will have to set this variable, either as an environmental variable, or you can use [Databricks secrets](https://docs.databricks.com/aws/en/security/secrets/) to fetch it.
#### Connect your app to a Lakebase instance
If you want your app to keep state or save any of the user inputs, you can add a lakebase instance as a resource. [This example](https://github.com/zuzanakovacsova/ryanair_databricks_workshop/tree/main/streamlit-chatbot-app-with-postgres) uses the above chat app and stores the prompts and responses in a table in lakebase, also showing a history of most recent conversations.
#### Other app tasks
You can have your Databricks app do many different tasks, from triggering classical ML models and uploading data to triggering workflows or visualising dashboards. The [Apps Cookbook](https://github.com/databricks-solutions/databricks-apps-cookbook) has plenty of examples. You can deploy it in your own workspace by selecting a framework folder (FastAPI, Dash, Streamlit) as source code for your deployment, or use the example code in the repo itself for inspiration.
### Deploy your model with MLOps stacks
[MLOps stacks](https://github.com/databricks/mlops-stacks) has a template for deploying ML models in Databricks that follow production best practices, including asset bundles, testing and deploying via GitHub actions or Azure DevOps. 
Initial setup is not trivial (setting up of workspaces, repos, credentials...) so we recommend to deprioritise spending time on this during the workshop.


