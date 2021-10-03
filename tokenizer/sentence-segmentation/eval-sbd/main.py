import gc
import os
import time

import numpy as np
import pandas as pd

import spacy


DATA_DIR = "../../../../data"
TEST_FILENAME = "sbd_dataset_20211001"
TEST_FILEEXT = ".tsv"

MIN_SENTENCE_LEN = 5
MAX_SENTENCE_LEN = 1000
DEFAULT_COL_DELIMITER = '\t'


def load_dataset() -> pd.DataFrame:
    start = time.time()
    df_url = pd.read_csv(
        data_filepath,
        delimiter="\t",
        names=["label", "url", "status", "doc", "title", "meta:keyword", "meta:description"]
    )\
    .dropna(subset=["doc"])\
    .reset_index()
    end = time.time()
    time_load_data = end - start
    print("load dataset : ", time_load_data)
    print("length dataframe : ", len(df_url))

    df_url.to_csv(
        documents_filepath,
        sep="\t",
        index=False,
    )

    del df_url
    
    return


def fetch_url_index(documents_filepath: pd.DataFrame) -> np.ndarray:
    df = pd.read_csv(
        documents_filepath,
        delimiter="\t",
        names=["label", "url", "status", "doc", "title", "meta:keyword", "meta:description"],
    )
    return df.index.values


def extract_sentence(nlp, text: str):
    try:
        doc = nlp(text)
        return doc.sents
    except MemoryError:
        print("MemoryError")
        print(text)
        return []
    except ValueError:
        print("ValueError")
        print(text)
        return []


def extract_all(inputpath,
                nlp,
                outputpath,
                text_id, # add tsukuda
                delim=DEFAULT_COL_DELIMITER,
                min_len=MIN_SENTENCE_LEN, max_len=MAX_SENTENCE_LEN):
    with fileinput.input(inputpath) as f:

        # This workaround(csv.field_size_limit(1000000000)) is
        # for "Error: field larger than field limit (131072)"
        csv.field_size_limit(1000000000)
        csv_rows = csv.reader(f, delimiter=delim)
#        print("tracemalloc")
#        snapshot1 = tracemalloc.take_snapshot()
#        start = time.time()
        with open(outputpath, "w", encoding="utf-8") as w:
            w.write("\"text\"\t\"text_id\"\t\"url\"\n")
            next(csv_rows)
            print("next")
            for idx, row in zip(text_id, csv_rows):
                if idx % 10 == 0:
                    print("=============time================")
                    in_progress = time.time()
                    print("idx " + str(idx) + ": " + str(in_progress - start))
                for text in row:                    
                    text = text.strip()
                    if not text:  # ignore blank line or text
                        continue
                    for sentence in extract_sentences(nlp, text):
                        l = len(sentence)
                        if l > 10000:                            
                            print("len(senetence)")
                            print(l)
                        if l < min_len:  # skip too short sentence
                            continue
                        if l > max_len:
                            sentence = sentence[:max_len]
                        if not sentence: # ignore empty line
                            continue                        
                        w.write("\"" + str(sentence) + "\"\t" + "\"" + str(idx) + "\"" + "\n")





def main():
    data_filepath = os.path.join(DATA_DIR, TEST_FILENAME + TEST_FILEEXT)
    documents_filepath = os.path.join(DATA_DIR, TEST_FILENAME + "_200" + TEST_FILEEXT)
    sentences_filepath_spacy = os.path.join(
        DATA_DIR,  "sbd_" + TEST_FILENAME + "_200" + "_spacy" + TEST_FILEEXT
    )
    sentences_filepath_jaseg = os.path.join(
        DATA_DIR,  "sbd_" + TEST_FILENAME + "_200" + "_jaseg" + TEST_FILEEXT
    )
    load_dataset(data_filepath, documents_filepath)
    
    text_id = fetch_url_index(documents_filepath)
    print(text_id)
    nlp = spacy.load("ja_ginza", exclude=["ner"])
    start = time.time()
    extract_all(
        documents_filepath,
        nlp,
        sentences_filepath_spacy,
        text_id,
    )


if __name__ == "__main__":
    main()


