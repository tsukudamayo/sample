from api.pipeline import (
    aggregate_score_by_post_id,
    fetch_hit_crawl_docs_data,
    fetch_hit_data_by_post_id,
    parse_annotation_relevant_vacchine_or_not,
    split_query_evaluation_data_relevant_vacchine_or_not,
)
from api.model import tokenize, extract_key_phrase


def run():
    # eval_es = EvaluationByES()
    # metric_scores_by_post_id = eval_es.generate_metric_score_post_id_more_than_threshold(threshold=0.03)

    # TARGET = "23718"
    # id_score_map = fetch_hit_data_by_post_id(TARGET)
    # all_hit_data_by_query = fetch_hit_crawl_docs_data(id_score_map)
    # scores = aggregate_score_by_post_id(TARGET)
    # # print(scores[1:])
    # annotations = parse_annotation_relevant_vacchine_or_not()
    # # print(annotations)
    # distribution = split_query_evaluation_data_relevant_vacchine_or_not(annotations)
    # print(distribution)

    # tokens = [tokenize(hit_data["doc"]["hit_data"]) for hit_data in all_hit_data_by_query]
    # print(tokens)

    keywords = extract_key_phrase("遂に … テドロスが コロナワクチン接種を推奨しない… 公言した。 WHOのテドロスが遂にギブアップ")
    print(keywords)


def main():
    run()


if __name__ == "__main__":
    main()
