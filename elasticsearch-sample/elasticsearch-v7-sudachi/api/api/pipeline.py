from typing import List, Dict, Tuple
import json


RANK_EVAL_SCORE_FILE = "data/output/output_all_eval_query_ngram.json"
TARGET_QUERY_SCORE_OUTPUT = "target_query_and_score.json"


class EvaluationByES:    
    def __init__(
        self,
        rank_eval_score_file,
        target_query_score_output_file,
    ) -> None:
        self.target_query_score_output_file = target_query_score_output_file
        with open(rank_eval_score_file, "r", encoding="utf-8") as r:
            self.result_data = json.load(r)

    def fetch_all_details(self) -> List[Dict]:
        return [d["details"] for d in self.result_data]

    def fetch_all_post_id_of_query(self) -> List[str]:
        return [list(d.keys())[0] for d in self.fetch_all_details()]

    def fetch_all_metric_scores(self) -> List[float]:
        return [d[k]["metric_score"] for (k, d)
                in zip(self.fetch_all_post_id_of_query(), self.fetch_all_details())]

    def generate_metric_score_post_id_more_than_threshold(self, threshold: float) -> List[Tuple]:
        score_and_post_id_more_than_threshold = []
        for (k, d) in zip(self.fetch_all_post_id_of_query(), self.fetch_all_details()):
            if d[k]["metric_score"] > threshold:
                score_and_post_id_more_than_threshold.append(
                    {"post_id": k, "score": d[k]["metric_score"]}
                )

        sorted_key_by_score = sorted(
            score_and_post_id_more_than_threshold,
            key=lambda x: x["score"], reverse=True,
        )

        return [(s["post_id"], s["score"]) for s in sorted_key_by_score]

    def output_json_score_of_target_query(
        self,
        targets: List[Tuple],
        fij_json_data: List[Dict],
    ) -> List:
        # TODO
        # This function needs to do refactoring
        output = []
        count = 0
        for target in targets:
            idx = target[0]
            for f in fij_json_data:
                if f["post_id"] == idx:
                    post_discourse = f["post_discourse"]
                    print(idx, target[1], post_discourse)
                    output.append(
                        {
                         "post_id": idx,
                         "metric_score": target[1],
                         "post_discorse": post_discourse,
                        }
                    )
            count += 1
        print("count: ", count)
        print(count/651.0)
        with open(self.target_query_score_output_file, "w", encoding="utf-8") as w:
            json.dump(output, w, ensure_ascii=False, indent=4)

        return output


class FIJ:
    def __init__(self) -> None:
        fij_data_file = "data/fij-post_id-post_discourse/fij-post_id-post_discourse.jsonl"
        with open(fij_data_file, "r", encoding="utf-8") as r:
            lines: List[str] = r.readlines()
            self.json_data = []
            for line in lines:
                self.json_data.append(json.loads(line))

                
class DataLoader:
    def __init__(self, target_query_score_output_file) -> None:
        with open(target_query_score_output_file, encoding="utf-8") as r:
            self.query_and_score = json.load(r)

    def aggregate_score_url_by_post_id(self, eval_es: EvaluationByES) -> List:
        score_url_by_post_id = []
        for data in self.query_and_score:
            post_id = data["post_id"]
            print("post_id")
            print(post_id)
    
            for r in eval_es.result_data:
                target_id = list(r["details"].keys())[0]
                urls_and_scores = []
                if target_id == post_id:
                    print(r["details"][target_id]["hits"])
                    for hit in r["details"][target_id]["hits"]:
                        # print('"'+ hit["hit"]["_id"] + '",', end="")
                        print(hit)
                        urls_and_scores.append(
                            {
                             "_id": hit["hit"]["_id"],
                             "_score": hit["hit"]["_score"],
                            }
                        )
                    print(urls_and_scores)
                    score_url_by_post_id.append(
                        {
                         "post_id": post_id,
                         "hit" : urls_and_scores,
                        }
                    )
        self.score_url_by_post_id = score_url_by_post_id
        return self.score_url_by_post_id

    def generate_url_id_list(self):
        urls = []
        for d in self.score_url_by_post_id:
            for hit in d["hit"]:
                url = hit["_id"]
                urls.append(url)
            
        unique_urls = set(urls)
        print(unique_urls)
        url_id_list = list(unique_urls)

        self.url_id_list = url_id_list
        with open("urls_id_list.json", "w", encoding="utf-8") as w:
            json.dump(url_id_list, w, ensure_ascii=False, indent=4)


# TODO integretion ESEvaluate Class
def fetch_hit_data_by_post_id(target: str) -> Dict:
    with open(rank_eval_score_file, "r", encoding="utf-8") as r:
        output = json.load(r)
    id_score_map = {}
    for o in output:
        details = o["details"]
        post_id = list(details.keys())[0]
        if post_id == target:
            for hit in details[post_id]["hits"]:
                element = hit["hit"]
                id_score_map[element["_id"]] = element["_score"]
            break

    return id_score_map


def fetch_hit_crawl_docs_data(id_score_map: Dict) -> List:
    crawl_docs = []
    with open("data/fij-post_id-post_discourse/id_url_raw_body.json", "r", encoding="utf-8") as r:
        id_url_raw_bodys = json.load(r)

    ids_set = set(id_score_map.keys())
    for id_url_raw_body in id_url_raw_bodys:
        if id_url_raw_body["id"] in ids_set:
            id_url_raw_body["score"] = id_score_map[id_url_raw_body["id"]]
            crawl_docs.append(id_url_raw_body)

    return crawl_docs


def aggregate_score_by_post_id(target: str, rank_eval_score_file: str) -> List[float]:
    with open(rank_eval_score_file, "r", encoding="utf-8") as r:
        output = json.load(r)
    scores = []
    for o in output:
        details = o["details"]
        post_id = list(details.keys())[0]
        if post_id == target:
            for idx, hit in enumerate(details[post_id]["hits"]):
                if idx == 0:
                    continue
                element = hit["hit"]
                score = element["_score"]
                scores.append(score)
            break

    return scores


def parse_annotation_relevant_vacchine_or_not() -> List[List[str]]:
    annotations = []
    with open(
        "data/annotation/annotation_query_relevant_covid19_or_not.csv",
        "r",
        encoding="utf-8",
    ) as r:
        lines = r.readlines()
        for line in lines:
            line = line.strip()
            annotation = line.split(",")
            annotations.append(annotation)

    return annotations


def split_query_evaluation_data_relevant_vacchine_or_not(annotations: List) -> Dict:
    vacchine_query, not_vacchine_query = [], []
    vacchine_query_scores, not_vacchine_query_scores = [], []
    for annotation in annotations:
        if annotation[1] == "1":
            vacchine_query.append(annotation[0])
            vacchine_query_scores.append(aggregate_score_by_post_id(annotation[0]))
        elif annotation[1] == "0":
            not_vacchine_query.append(annotation[0])
            not_vacchine_query_scores.append(aggregate_score_by_post_id(annotation[0]))
        else:
            raise ValueError("something wrong")

    return {
        "vacchine_query": vacchine_query,
        "vacchine_query_scores": vacchine_query_scores,
        "not_vacchine_query": not_vacchine_query,
        "not_vacchine_query_scores": not_vacchine_query_scores,
    }


def main():
    # eval_es = EvaluationByES()
    # fij = FIJ()
    # for f in fij.json_data:
    #     if f["post_id"] == "19953":
    #         print(f["post_discourse"])

    # # aggregate scores and post_ids
    # metric_scores = eval_es.fetch_all_metric_scores()
    # plt.hist(metric_scores)
    # plt.savefig("precision_metric_scores.png")

    # targets = eval_es.generate_metric_score_post_id_more_than_threshold(threshold=0.03)
    # _ = eval_es.output_json_score_of_target_query(targets, fij.json_data)

    # # analyze
    # data = DataLoader()
    # score_url_by_post_id = data.aggregate_score_url_by_post_id(eval_es=eval_es)
    # data.generate_url_id_list()

    ids = fetch_hit_data_by_post_id("19953")
    crawl_docs = fetch_hit_crawl_docs_data(ids)
    print(crawl_docs)


if __name__ == "__main__":
    main()
