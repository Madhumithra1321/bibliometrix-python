from www.services.etl.pipeline import openalex_pipeline
from www.services.biblionetwork import biblionetwork

df = openalex_pipeline(
    query="machine learning",
    max_results=50
)

net = biblionetwork(
    df,
    analysis="collaboration",
    network="authors"
)

print(type(net))
print(net.shape)
print(net.head())