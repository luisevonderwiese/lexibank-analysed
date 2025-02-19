import os
import pandas as pd
from pyglottolog import Glottolog

def get_all_families():
    glot = Glottolog("glottolog", cache = True)
    families = {}
    for languoid in glot.languoids(exclude_pseudo_families=True):
        if languoid.category == "Family" or languoid.family is None:
            continue
        family = languoid.family.glottocode
        if not family in families:
            families[family] = []
        families[family].append(languoid.glottocode)
    return families


def filter(concepts, glottocodes, wordlist_path):
    if os.path.isfile(wordlist_path):
        return
    df = pd.read_csv(os.path.join("wordlists", "lexibank-anaylzed_wordlist.tsv"), sep = "\t", dtype = "str")
    if len(concepts) > 0:
        df = df[df["CONCEPTICON_ID"].isin(concepts)]
    if len(glottocodes) > 0:
        df = df[df["GLOTTOCODE"].isin(glottocodes)]
    if len(df) > 0:
        df.to_csv(wordlist_path, sep = "\t")

def filter_family(name, members):
    wordlist_path = os.path.join("wordlists", "families", name + "_wordlist.tsv")
    filter([], members, wordlist_path)

def filter_swadesh(languagelist):
    with open(os.path.join("languagelists", languagelist + "_languages.txt"), "r") as languages_file:
        glottocodes = languages_file.read().split("\n")
    concept_df = pd.read_csv("conceptlists/swadesh100.tsv", sep = "\t", dtype = "str")
    concepts = list(concept_df["CONCEPTICON_ID"])
    wordlist_path = os.path.join("wordlists", "swadesh100", languagelist + "_swadesh100_wordlist.tsv")
    filter(concepts, glottocodes, wordlist_path)



def create_full_wordlist():
    wordlist_path = os.path.join("wordlists", "lexibank-anaylzed_wordlist.tsv")
    if os.path.isfile(wordlist_path):
        return
    df = pd.read_csv("cldf/forms.csv", dtype = "str")
    languages_df = pd.read_csv("cldf/languages.csv", dtype = "str")
    df = pd.merge(df, languages_df, how="outer", left_on=['Language_ID'], right_on=['ID'])
    concepts_df = pd.read_csv("cldf/concepts.csv", dtype = "str")
    df = pd.merge(df, concepts_df, how="outer", left_on=['Parameter_ID'], right_on=['ID'])
    df = df.astype("str")
    df = df[df['Parameter_ID'] != "nan"]
    df = df[df['Language_ID'] != "nan"]
    df = df[df['Form'] != "nan"]
    #df = df[df['Segments'].notna()]
    df = df[df['Segments'] != "nan"]

    with open(wordlist_path, "w+") as wordlist_file:
        wordlist_file.write("\t".join(["ID", "DOCULECT", "GLOTTOCODE", "ISO_CODE", "CONCEPT", "CONCEPTICON_ID", "CONCEPTICON_GLOSS", "FORM", "IPA", "TOKENS"]) + "\n")

    for i, row in df.iterrows():
        with open(wordlist_path, "a") as wordlist_file:
            wordlist_file.write("\t".join([
            str(i+1), row["Language_ID"], row["Glottocode"], row["ISO639P3code"], row["Parameter_ID"], row["Concepticon_ID"], row["Concepticon_Gloss"], "", row["Form"], row["Segments"]]) + "\n")
            print(row["Language_ID"], row["Parameter_ID"], row["Segments"])




if not os.path.isdir(os.path.join("wordlists", "swadesh100")):
    os.makedirs(os.path.join("wordlists", "swadesh100"))
if not os.path.isdir(os.path.join("wordlists", "families")):
    os.makedirs(os.path.join("wordlists", "families"))

#create_full_wordlist()

#filter_swadesh("dense")
#filter_swadesh("iecor")
families = get_all_families()
for name, members in families.items():
    print(name)
    filter_family(name, members)
