from typing import List

from sudachipy import MorphemeList, dictionary
from pke.unsupervised import TopicRank
from pke.base import stopwords


# -------- #
# tokenize #
# -------- #
def tokenize(text: str) -> List[str]:
    tokenizer_obj = dictionary.Dictionary().create()
    tokens = _delete_stop_words(tokenizer_obj.tokenize(text))

    return [token.surface() for token in tokens]


def _delete_stop_words(morpheme_list: MorphemeList) -> List:
    return _select_noun_verb_adjective(morpheme_list)


def _select_noun_verb_adjective(morpheme_list: MorphemeList) -> List:
    target = []
    condition = set(["名詞", "動詞", "形容詞",])
    for morpheme in morpheme_list:
        if morpheme.part_of_speech()[0] in condition:
            target.append(morpheme)

    return target


# ----- #
# model #
# ----- #
def extract_key_phrase(text: str):
    stopwords['ja_ginza'] = 'japanese'
    extractor = TopicRank()
    extractor.load_document(input=text, language="ja", normalization=None)
    extractor.candidate_selection()
    extractor.candidate_weighting()
    keypharases = extractor.get_n_best(n=10)

    return keypharases
