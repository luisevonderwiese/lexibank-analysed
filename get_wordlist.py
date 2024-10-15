import os
import pandas as pd
import glottolog

def get_all_families():
    glottolog.load_families()
    families = set()
    for glottocode, family in glottolog.family_dict.items():
        families.add(family)
    return list(families)


def get_glottocodes(families):
    if families == ["all"]:
        return []
    glottocodes = []
    for glottocode, family in glottolog.family_dict.items():
        if family in families:
            glottocodes.append(glottocode)
    return glottocodes


def get_concepts(conceptlist):
    if conceptlist == "all":
        return []
    elif conceptlist == "swadesh100":
        concept_df = pd.read_csv("conceptlists/swadesh100.tsv", sep = "\t", dtype = "str")
    elif conceptlist == "swadesh200":
        concept_df = pd.read_csv("conceptlists/swadesh200.tsv", sep = "\t", dtype = "str")
    else:
        print("Illegal concept list")
        return None
    concepticon_ids = list(concept_df["CONCEPTICON_ID"])
    return concepticon_ids




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
    #for glottocode in glottocodes:
    #    if glottocode not in set(df["GLOTTOCODE"]):
    #        print(glottocode)
    #print(len(glottocodes))
    #print(len(set(df["GLOTTOCODE"])))

def filter_for(conceptlist, family):
    concepts = get_concepts(conceptlist)
    glottocodes = get_glottocodes([family])
    wordlist_path = os.path.join("wordlists", "families", family + "_" + conceptlist + "_wordlist.tsv")
    filter(concepts, glottocodes, wordlist_path)

def filter_for_list(conceptlist, languagelist):
    if languagelist == "all":
        glottocodes = []
    else:
        with open(os.path.join("languagelists", languagelist + "_languages.txt"), "r") as languages_file:
            glottocodes = languages_file.read().split("\n")
    concepts = get_concepts(conceptlist)
    wordlist_path = os.path.join("wordlists", "languagelists", languagelist + "_" + conceptlist + "_wordlist.tsv")
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
            str(i), row["Language_ID"], row["Glottocode"], row["ISO639P3code"], row["Parameter_ID"], row["Concepticon_ID"], row["Concepticon_Gloss"], "", row["Form"], row["Segments"]]) + "\n")
            print(row["Language_ID"], row["Parameter_ID"], row["Segments"])



#create_full_wordlist()
if not os.path.isdir(os.path.join("wordlists", "languagelists")):
    os.makedirs(os.path.join("wordlists", "languagelists"))
for languagelist in ["iecor", "main", "all"]:
    for conceptlist in ["all", "swadesh100", "swadesh200"]:
        filter_for_list(conceptlist,languagelist)
if not os.path.isdir(os.path.join("wordlists", "families")):
    os.makedirs(os.path.join("wordlists", "families"))
families = get_all_families()
families.append("all")
for family in families:
    print(family)
    for conceptlist in ["all", "swadesh100", "swadesh200"]:
        filter_for(conceptlist, family)
