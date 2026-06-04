# test_histnetwork.py

from www.services.etl.pipeline import openalex_pipeline
from www.services.histnetwork import histNetwork
df = openalex_pipeline(
    query="machine learning",
    max_results=50
)

result = histNetwork(df)

print(type(result))
print(result.keys())