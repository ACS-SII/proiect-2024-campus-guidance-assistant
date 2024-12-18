# from llama_index.llms.ollama import Ollama
# from llama_index.experimental import PandasQueryEngine
# from prompts import new_prompt, template_instructions
# import pandas as pd
# import os

# llm = Ollama(model="Llama3.2:1B", request_timeout=60.0)

# stations_path = os.path.join("data", "stations.csv")
# stations_df = pd.read_csv(stations_path)

# # Initialize the Pandas Query Engine
# stations_query_engine = PandasQueryEngine(
#     stations_df,
#     instruction_str=template_instructions,
#     verbose=True,
#     llm=llm
# )

# stations_query_engine.update_prompts({"pandas_prompt": new_prompt})

# # Run a query
# try:
#     response = stations_query_engine.query("Give me details about the first row.")
#     print("AI Response:", response)
# except Exception as e:
#     print("Error during query execution:", e)

from llama_index.llms.ollama import Ollama
from llama_index.experimental import PandasQueryEngine
from prompts import new_prompt, template_instructions
import pandas as pd
import os

# Initialize the LLM with a longer timeout
llm = Ollama(model="Llama3.2:1B", request_timeout=60.0)

# Path to the JSON file
stations_path = os.path.join("data", "stations.json")

# Load the dataset from the JSON file
stations_df = pd.read_json(stations_path)

# Initialize the Pandas Query Engine
stations_query_engine = PandasQueryEngine(
    stations_df,
    instruction_str=template_instructions,
    verbose=True,
    llm=llm
)

# Update the prompt to use conversational style
stations_query_engine.update_prompts({"pandas_prompt": new_prompt})

# Run a query
try:
    response = stations_query_engine.query("Give me details about the first row.")
    print("AI Response:", response)
except Exception as e:
    print("Error during query execution:", e)
