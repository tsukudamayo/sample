from typing import List
import json

import matplotlib.pyplot as plt
import seaborn as sns


RANK_EVAL_SCORE_FILE = "data/output/output_all_eval_query_ngram.json"


def select_some_fij_dataset() -> None:
    fij_data_file: str = "data/fij-post_id-post_discourse/fij-post_id-post_discourse.jsonl"
    with open(fij_data_file, "r", encoding="utf-8") as r:
        lines: List[str] = r.readlines()
        for line in lines:
            print(json.loads(line))
            print(type(json.loads(line)))

    return None


class EvaluationByES:    
    def __init__(self) -> None:
        result_data_file = RANK_EVAL_SCORE_FILE
        with open(result_data_file, "r", encoding="utf-8") as r:
            self.result_data = json.load(r)


def _mean(scores: List[float]) -> float:
    return sum(scores) / len(scores)


def _aggregate_score(result: EvaluationByES) -> List[float]:
    scores = []
    for data in result.result_data:
        tmp_scores = []
        for d in data:
            tmp_scores.append(d["_score"])
        scores.append(tmp_scores)
    
    return scores



def main():
    result = EvaluationByES()
    scores = _aggregate_score(result)
    mean_scores = [_mean(s) for s in scores]
    print(mean_scores)

    plt.hist(mean_scores)
    plt.savefig("sample.png")


if __name__ == "__main__":
    main()
