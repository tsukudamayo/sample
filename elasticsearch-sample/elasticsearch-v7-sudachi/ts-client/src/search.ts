import fs from "fs";

import { Client } from "@elastic/elasticsearch";

const index = "sample-like-vaccine_20220315";

const client = new Client({
  node: "http://192.168.64.6:9200",
  auth: {
    username: "elastic",
    password: "elastic",
  },
});

interface Document {
  post_id: string
  post_discourse: string
}

async function run() {

  // call evaluation function
  const result = await client.search<Document>({
    index: index,
    size: 100,
    query: {
      // id 23901
      match: { raw_body: "未接種でコロナに感染し回復した人が、他人に感染させた例はないとCDCが認めた。これまで、CDCは、感染経験のある人にも接種を推奨していたが、その根拠がなくなった。感染により免疫を獲得した以上、ワクチン接種は必要ない。" }
      // match: {
      // 	raw_body: "コロナ感染予防のためマスクをすることで妊婦さんの酸素飽和度が低くなり赤ちゃんのへその緒が短くなっているらしい大切なことなのでシェアしたいです"
      // }
    }
  });

  fs.writeFileSync("output.json", JSON.stringify(result.hits.hits, null, 4), "utf8");
};

run();

async function runAllQuery() {
  let results = [];
  const dataStr: string = fs.readFileSync("data/fij-post_id-post_discourse/fij-post_id-post_discourse.jsonl", "utf-8");
  const lines: string[] = dataStr.split("\n");
  for (let i = 0; i < lines.length; i++) {
    try {
      // parse JSON data
      console.log(i);
      const doc: Document = JSON.parse(lines[i]);
      const result = await client.search<Document>({
	index: index,
	size: 100,
	query: {
	  match: { raw_body: doc.post_discourse }
	}
      });
      results.push(result.hits.hits);
    } catch(e) {
      console.log(e);
    }
  }
  fs.writeFileSync("output_all_query.json", JSON.stringify(results, null, 4), "utf8");
}

runAllQuery();
