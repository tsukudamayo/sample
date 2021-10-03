import csv
import fileinput
import functools
import gc
import os
import time

import numpy as np
import pandas as pd

import spacy
from ja_sentence_segmenter.common.pipeline import make_pipeline
from ja_sentence_segmenter.concatenate.simple_concatenator import concatenate_matching
from ja_sentence_segmenter.normalize.neologd_normalizer import normalize
from ja_sentence_segmenter.split.simple_splitter import split_newline, split_punctuation


DATA_DIR = "../../../../data"
TEST_FILENAME = "sbd_dataset_20211001"
TEST_FILEEXT = ".tsv"

MIN_SENTENCE_LEN = 5
MAX_SENTENCE_LEN = 1000
DEFAULT_COL_DELIMITER = '\t'


def load_dataset(data_filepath: str, documents_filepath: str) -> pd.DataFrame:
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
    gc.collect()
    
    return


def fetch_url_index(documents_filepath: pd.DataFrame) -> np.ndarray:
    df = pd.read_csv(
        documents_filepath,
        delimiter="\t",
        names=["label", "url", "status", "doc", "title", "meta:keyword", "meta:description"],
        header=0,
    )
    print(df.head())
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
        start = time.time()
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
            end = time.time()
            print("finish : ", end - start)


def extract_sentences(nlp, text: str):
    try:
        if type(nlp) == spacy.lang.ja.Japanese:
            doc = nlp(text)
            return doc.sents
        else:
            return nlp(text)
    except MemoryError:
        print("MemoryError")
        print(text)
        return []
    except ValueError as e:
        print("ValueError")
        print(text)
        return []    


def compare_spacy_jaseg(
    sentences_filepath_spacy: str,
    sentences_filepath_jaseg: str,
):

    df_spacy = pd.read_csv(
        os.path.join(DATA_DIR, "sentences_docs_all_valuecommerce_20210901_200_spacy.tsv"),
        delimiter="\t",
        header=0,
    )

    df_jaseg = pd.read_csv(
        senteces_filepath_jaseg,
        delimiter="\t",
        header=0,
    )

    print(df_spacy)
    print(df_jaseg)


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

    # spacy 
    nlp = spacy.load("ja_ginza", exclude=["ner"])

    # # ja_segmenter
    # split_punc2 = functools.partial(split_punctuation, punctuations=r"。!?")
    # concat_tail_no = functools.partial(concatenate_matching, former_matching_rule=r"^(?P<result>.+)(の)$", remove_former_matched=False)
    # nlp = make_pipeline(normalize, split_newline, concat_tail_no, split_punc2)

    print(type(nlp))

    # extract_all(
    #     documents_filepath,
    #     nlp,
    #     sentences_filepath_jaseg,
    #     text_id,
    # )

    compare_spacy_jaseg(
        sentences_filepath_spacy,
        sentences_filepath_jaseg,
    )


if __name__ == "__main__":
    main()
