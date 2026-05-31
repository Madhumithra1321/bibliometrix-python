from www.services.etl.pipeline import openalex_pipeline

df = openalex_pipeline(
    query="machine learning",
    max_results=5
)

print(df.columns.tolist())

print("\nID column:")
print(df["ID"].head())

print("\nDE column:")
print(df["DE"].head())