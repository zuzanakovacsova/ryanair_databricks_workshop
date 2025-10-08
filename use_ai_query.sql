-- The ai_query() function allows you to apply any AI model to data for both generative AI and classical ML tasks,
-- including extracting information, summarizing content, identifying fraud, and forecasting revenue. 

-- Traditional models

-- For specific request (example can be found in the UI when you go to your serving endpoint and select USE->QUERY)
ai_query(
    endpoint => "your_endpoint",
    request => "your_request_body"
    ) AS response

-- For batch inference on tables, columns are input fields for your model and are selected from your table
ai_query(
  endpoint => "<model_endpoint>",
  request => named_struct(
    "<field 1>", <column 1>,
    "<field 2>", <column 2>,
    "<field 3>", <column 3>),
  returnType => "<return type>") AS model_prediction 
FROM <catalog.schema.table>
LIMIT 10

-- LLMs

-- Foundational models, or your own LLM: replace Claude with your model of choice
SELECT <input_column>, ai_query(
    "databricks-claude-sonnet-4",
    CONCAT(<prompt_placeholder>, <input_column>) 
) AS output_column
FROM <catalog.schema.table>;