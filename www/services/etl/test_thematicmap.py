from www.services.etl.pipeline import openalex_pipeline
from www.services.thematicmap import thematic_map

df = openalex_pipeline(
    query="machine learning",
    max_results=50
)

result = thematic_map(
    df,
    field="ID"
)

print(type(result))
print(len(result))

for i, item in enumerate(result):
    print(f"\n===== RESULT[{i}] =====")
    print(type(item))

    try:
        print(item.head())
    except:
        print(item)