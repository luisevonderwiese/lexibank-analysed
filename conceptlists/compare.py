import os
import pandas as pd

concepticon_df = pd.read_csv("Swadesh-1952-200.tsv", sep = "\t")
concepts = list(concepticon_df["CONCEPTICON_GLOSS"])
concepts = [concept.lower() for concept in concepts]

my_df = pd.read_csv("swadesh207_POS.txt")
my_concepts = list(my_df["Concept"])

for concept in concepts:
    if concept not in my_concepts:
        print(concept)
print("-----------------------")
for concept in my_concepts:
    if concept not in concepts:
        print(concept)
