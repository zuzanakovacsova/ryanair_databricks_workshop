'''
Production monitoring for GenAI on Databricks lets you automatically run MLflow 3 scorers
on traces from your production GenAI apps to continuously monitor quality.
'''

# Create scorers for your ML experiment and GenAI App.


# MLflow provides several predefined scorers that you can use out-of-the-box for monitoring.
from mlflow.genai.scorers import Safety, ScorerSamplingConfig

# Register the scorer with a name and start monitoring
safety_scorer = Safety().register(name="my_safety_scorer")  # name must be unique to experiment
safety_scorer = safety_scorer.start(sampling_config=ScorerSamplingConfig(sample_rate=0.7))


# Guidelines-based LLM scorers can evaluate inputs and outputs using pass/fail natural language criteria.

from mlflow.genai.scorers import Guidelines

# Create and register the guidelines scorer
english_scorer = Guidelines(
  name="english",
  guidelines=["The response must be in English"]
).register(name="is_english")  # name must be unique to experiment

# Start monitoring with the specified sample rate
english_scorer = english_scorer.start(sampling_config=ScorerSamplingConfig(sample_rate=0.7))


'''or maximum flexibility, including the option to forego LLM-based scoring, you can define and use a custom scorer function for monitoring.

When defining custom scorers, do not use type hints that need to be imported in the function signature. If the scorer function body uses packages that need to be imported, import these packages inline within the function for proper serialization.

Some packages are available by default without the need for an inline import. These include databricks-agents, mlflow-skinny, openai, and all packages included in Serverless environment version 2.
'''

from mlflow.genai.scorers import scorer, ScorerSamplingConfig


@scorer
def formality(inputs, outputs, trace):
    # Must be imported inline within the scorer function body
    from mlflow.genai.judges.databricks import custom_prompt_judge
    from mlflow.entities.assessment import DEFAULT_FEEDBACK_NAME

    formality_prompt = """
    You will look at the response and determine the formality of the response.

    <request>{{request}}</request>
    <response>{{response}}</response>

    You must choose one of the following categories.

    [[formal]]: The response is very formal.
    [[semi_formal]]: The response is somewhat formal. The response is somewhat formal if the response mentions friendship, etc.
    [[not_formal]]: The response is not formal.
    """

    my_prompt_judge = custom_prompt_judge(
        name="formality",
        prompt_template=formality_prompt,
        numeric_values={
            "formal": 1,
            "semi_formal": 0.5,
            "not_formal": 0,
        },
        model="databricks:/databricks-gpt-oss-20b",  # optional
    )

    result = my_prompt_judge(request=inputs, response=inputs)
    if hasattr(result, "name"):
        result.name = DEFAULT_FEEDBACK_NAME
    return result

# Register the custom scorer and start monitoring
formality_scorer = formality.register(name="my_formality_scorer")  # name must be unique to experiment
formality_scorer = formality_scorer.start(sampling_config=ScorerSamplingConfig(sample_rate=0.1))