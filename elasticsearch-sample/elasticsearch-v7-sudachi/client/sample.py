from elasticsearch import Elasticsearch


def main():
    index = "index"
    index_file = "./index.json"

    es = Elasticsearch("http://192.168.64.2:9200")

    with open(index_file) as f:
        source = f.read().strip()
        print(es.indices.create(index, source))

    pharse = "今日は晴れです"
    body = {
        "analyzer": "sudachi_analyzer",
        "text": pharse
    }
    es.indices.analyze(index=index, body=body)["tokens"]
    


if __name__ == "__main__":
    main()
