# Unity Catalog functions are used to create AI agent tools that execute custom logic and perform specific tasks. 
# You can define them in python or in SQL. You always have to provide descriptions so that the LLM knows which tool to use when.
 # Install Unity Catalog AI integration packages with the Databricks extra


#%pip install unitycatalog-ai[databricks]
#%pip install unitycatalog-langchain[databricks]
#%pip install databricks-langchain

#dbutils.library.restartPython()

from unitycatalog.ai.core.databricks import DatabricksFunctionClient

client = DatabricksFunctionClient()

# Python definition of a sample function

CATALOG = "<your catalog>"  #fill in
SCHEMA = "<your schema>"    #fill in

def convert_to_markdown(text: str, formatting: str) -> str:
    """
    A function that accepts a string and a formatting directive, and returns
    the string wrapped in the corresponding Markdown syntax.

    Args:
        text (str): The input string to format.
        formatting (str): The Markdown formatting to apply (e.g., "header", "bold").

    Returns:
        str: The Markdown-formatted string. 

    Raises:
        ValueError: If an unsupported formatting option is provided.
    """
    fmt = formatting.strip().lower()

    format_map = {
        "header": lambda s: f"# {s}",
        "h1": lambda s: f"# {s}",
        "h2": lambda s: f"## {s}",
        "h3": lambda s: f"### {s}",
        "bold": lambda s: f"**{s}**",
        "italic": lambda s: f"*{s}*",
        "strikethrough": lambda s: f"~~{s}~~",
        "quote": lambda s: f"> {s}",
        "inline_code": lambda s: f"`{s}`",
        "code": lambda s: f"\n{s}\n",
        "bullet": lambda s: f"- {s}",
        "numbered": lambda s: f"1. {s}",
    }

    try:
        return format_map[fmt](text)
    except KeyError:
        supported = ", ".join(sorted(format_map.keys()))
        raise ValueError(f"Unsupported formatting '{formatting}'. Supported formats: {supported}")


# Registration of the function to UC
client.create_python_function(        #note it's using create_python_function here
    func=convert_to_markdown,
    catalog=CATALOG,
    schema=SCHEMA,
    replace=True
)

# SQL definition of a sample function
sql_body = """
CREATE FUNCTION <your catalog>.<your schema>.<sample_function>(param STRING COMMENT 'A string to convert to uppercase.')
RETURNS STRING
LANGUAGE PYTHON
COMMENT 'Converts an input string to uppercase.'
AS $$
    return param.upper()
$$
"""

# Registration of the function to UC 
client.create_function(sql_function_body=sql_body) #note it's using create_function here