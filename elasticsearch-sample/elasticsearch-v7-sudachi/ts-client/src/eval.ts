import fs from "fs";

import { Client } from "@elastic/elasticsearch";

const index = "sample-like-vacchine-sudachi-tokenizer-20220315";

const client = new Client({
  node: "http://192.168.64.2:9200",
  auth: {
    username: "elastic",
    password: "elastic",
  },
});

interface FIJ {
  post_id: string
  post_discourse: string
}

interface Result {
  details: Object,
  post_id: string,
  post_discourse: string,
}

// TODO

// async function precisionK() {
// }

const fijRatings = () => {
  const dataStr: string = fs.readFileSync("data/fij-post_id-post_discourse/fij-post_id-post_discourse.jsonl", "utf-8");
  const lines: string[] = dataStr.split("\n");
  const ratings = lines.map((x, idx) => {
    return { "_index": index, "_id": "fij_" + String(idx), "rating": idx }
  });

  return ratings;
}

async function generateRequestPrecisionK() {
  const dataStr: string = fs.readFileSync("data/fij-post_id-post_discourse/fij-post_id-post_discourse.jsonl", "utf-8");
  const lines: string[] = dataStr.split("\n");
  const _ratings = await fijRatings();
  const results = [];
  for (let i = 0; i < lines.length; i++) {
    console.log(i);
    console.log(lines[i]);
    if (lines[i] === "") {
      break
    }
    const doc: FIJ = JSON.parse(lines[i]);
    console.log(doc);
    
    // const _itself = fijRatings()[i];
    // const _ratingsOtherItself = _ratings.splice(i);
    // _ratings.splice(i);
    // console.log(_ratingsOtherItself);
    // console.log("otherthan itself ", _ratingsOtherItself.length);
    // _ratings.splice(i, 0, _itself);
    // console.log(_ratings);
    // console.log("_rating.length", _ratings.length);

    // precision@k
    const rank = await client.rankEval({
      index: index,
      requests: [
	{
	  id: doc.post_id,
	  request: {
	    query: {
	      match: {
		raw_body: doc.post_discourse
	      }
	    }
	  },
	  ratings: _ratings
	}
      ],
      metric: {
	precision: {
	  k: 50,
	  relevant_rating_threshold: 1,
	  ignore_unlabeled: false,
	  // normalize: false,
	}
      }
    });

    // // dcg
    // const rank = await client.rankEval({
    //   index: index,
    //   requests: [
    // 	{
    // 	  id: doc.post_id,
    // 	  request: {
    // 	    query: {
    // 	      match: {
    // 		raw_body: doc.post_discourse
    // 	      }
    // 	    }
    // 	  },
    // 	  ratings: _ratings
    // 	}
    //   ],
    //   metric: {
    // 	dcg: {
    // 	  k: 20,
    // 	  // relevant_rating_threshold: 1,
    // 	  // ignore_unlabeled: false,
    // 	  normalize: false,
    // 	}
    //   }
    // });
    const result: Result = {
      details: {},
      post_id: "",
      post_discourse: ""
    };
    result.details = rank.details;
    result.post_id = doc.post_id;
    result.post_discourse = doc.post_discourse;
    console.log(result);
    // console.log(result.details[idx].hits);
    results.push(result);
  }

  // fs.writeFileSync("output_all_eval_query.json", JSON.stringify(results, null, 4), "utf8");
  // fs.writeFileSync("output_all_eval_query_ngram.json", JSON.stringify(results, null, 4), "utf8");
  fs.writeFileSync("output_all_eval_query_sudachi.json", JSON.stringify(results, null, 4), "utf8");
}

generateRequestPrecisionK();
