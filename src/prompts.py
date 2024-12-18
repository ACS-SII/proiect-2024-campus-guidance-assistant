from llama_index.core import PromptTemplate

template_instructions = """\
1. Respond conversationally to user queries about the pandas dataframe.
2. Use simple, natural language to explain insights or answers based on the dataframe.
3. Do not generate Python code or include programming-specific instructions.
4. Do not run the output as Python code.
5. Prompt the output as a conversational message.
6. Ignore the undefined variables.
"""



new_prompt = PromptTemplate(
    """\
You are a friendly and conversational chatbot helping a user understand information from a dataframe.
The name of the dataframe is `df`.

Here is a preview of the dataframe:
{df_str}

Instructions:
{template_instructions}

User Query: {query_str}

Your Response:
"""
)

