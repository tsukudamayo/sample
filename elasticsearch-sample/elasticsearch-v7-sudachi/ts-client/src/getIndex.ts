import fs from "fs";

import { Client } from "@elastic/elasticsearch";

const index = "sample-like-vaccine_20220315_3";

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

interface Data {
  id: string
  doc: Document
}

async function run() {
  const jsonData: string = fs.readFileSync(
    "data/fij-post_id-post_discourse/urls_id_list.json",
    "utf-8",
  );
  const urlList: string[] = JSON.parse(jsonData);
  console.log(urlList);

  const results =[];
  for (let i = 0; i < urlList.length; i++) {
    const target = await client.get({
      index: index,
      id: urlList[i],
    });

    const result = {
      "id": target._id,
      "doc": target._source,
    }

    results.push(result);
  }

  console.log(results);
  fs.writeFileSync("id_url_raw_body.json", JSON.stringify(results, null, 4), "utf8");
}

run();
