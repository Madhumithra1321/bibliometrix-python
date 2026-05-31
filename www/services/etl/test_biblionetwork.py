from www.services.etl.pipeline import openalex_pipeline
from www.services.biblionetwork import biblionetwork

df = openalex_pipeline(
    query="machine learning",
    max_results=50
)

print("Records:", len(df))

print(df["ID"].head())

net = biblionetwork(
    df,
    analysis="co-occurrences",
    network="keywords"
)

print(type(net))
print(net)