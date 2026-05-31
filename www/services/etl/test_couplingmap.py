from www.services.etl.pipeline import openalex_pipeline
from www.services.couplingmap import couplingMap

df = openalex_pipeline(
    query="machine learning",
    max_results=50
)

result = couplingMap(
    df,
    analysis="documents",
    field="CR"
)

print(type(result))
print(result.keys())