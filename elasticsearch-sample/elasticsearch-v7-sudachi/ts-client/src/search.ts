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
  url: string
  raw_body: string
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

  // console.log(result.hits.hits);
  console.log(result.hits.hits);
  console.log(result.hits.hits.length);
  fs.writeFileSync("output.json", JSON.stringify(result.hits.hits, null, 4), "utf8");
};

run();
