import mlflow
from databricks.sdk import WorkspaceClient

# Import mlflow scorers
from mlflow.genai.scorers import (
    Guidelines,
    RelevanceToQuery,
    RetrievalGroundedness,
    RetrievalRelevance,
    Safety,
)

# Enable MLflow's autologging to instrument your application with Tracing
mlflow.openai.autolog()

# Set up MLflow tracking to Databricks, create a new experiment
mlflow.set_tracking_uri("databricks")
mlflow.create_experiment("/Users/<your user email>/ml_code_samples/<experiment name>")
mlflow.set_experiment("/Users/<your user email>m/ml_code_samples/<experiment name>")

# Create an OpenAI client that is connected to Databricks-hosted LLMs
w = WorkspaceClient()
client = w.serving_endpoints.get_open_ai_client()

# Select an LLM
model_name = "databricks-claude-sonnet-4"

# Use the trace decorator to capture the application's entry point
@mlflow.trace
def my_app(input: str):
    # This call is automatically instrumented by `mlflow.openai.autolog()`
    response = client.chat.completions.create(
        model=model_name,  # This example uses a Databricks hosted LLM - you can replace this with any AI Gateway or Model Serving endpoint. If you provide your own OpenAI credentials, replace with a valid OpenAI model e.g., gpt-4o, etc.
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": input,
            },
        ],
    )
    return response.choices[0].message.content

# Create evaluation datasets 
eval_dataset = [
    {
        "inputs": {
            "input": "What is the most common aggregate function in SQL?"
        }
    },
    {
        "inputs": {
            "input": "How do I use MLflow?"
        }
    },
]

eval_dataset_2 = [
    {
        "inputs": {
            "input": "How much does a microwave cost?",
        }
    },
    {
        "inputs": {
            "input": "I'm having trouble with my account.  I can't log in. I'm using the website.",
        }
    },
    {
        "inputs": {
            "input": "I'm having trouble with my account.  I can't log in. JUST FIX IT FOR ME",
        }
    },
]

# Run predefined scorers 

# These scorers don't need an aswer key to my inputs. You can choose to add scorers which will compare the output to your desired
# aswer, see Databricks documentation for more details.


# I need an evalaution dataset: example input requests, and predict_fn, which is the app to call the llm
mlflow.genai.evaluate(
    data=eval_dataset,
    predict_fn=my_app,
    scorers=[
        RelevanceToQuery(),
        RetrievalGroundedness(),
        RetrievalRelevance(),
        Safety()
    ],
)
 # Run custom scorers
tone = "The response must maintain a courteous, respectful tone throughout.  It must show empathy for customer concerns."
structure = "The response must use clear, concise language and structures responses logically.  It must avoids jargon or explains technical terms when used."
banned_topics = "If the request is a question about product pricing, the response must politely decline to answer and refer the user to the pricing page."


mlflow.genai.evaluate(
    data=eval_dataset_2,
    predict_fn=my_app,
    scorers=[
        Guidelines(name="tone", guidelines=tone),
        Guidelines(name="structure", guidelines=structure),
        Guidelines(name="banned_topics", guidelines=banned_topics),
    ],
)

# Results will be tracked in the Experiment UI