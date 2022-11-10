import fs from 'fs';

import { Client } from '@elastic/elasticsearch';

const index = "sample-like-vacchine-bigram-tokenizer-20220315";

const client = new Client({
  node: "http://192.168.64.2:9200",
  auth: {
    username: "elastic",
    password: "elastic",
  },
});

interface Document {
  url: string
  raw_body: string
}

interface FIJ {
  post_id: number
  post_discourse: string
}

async function crawlDocsToIndex() {
  const dataDir: string[] = fs.readdirSync("./data/crawl-docs-url-raw_body-like-vaccine_20220315/")

  for (let i = 0; i < dataDir.length; i++) {
    console.log(i);
    const start = new Date().getTime();
    const dataStr: string = fs.readFileSync("./data/crawl-docs-url-raw_body-like-vaccine_20220315/crawl-docs-url-raw_body-like-vaccine_20220315_00000000000" + String(i), "utf-8");
    const lines: string[] = dataStr.split("\n");
    
    for (let j = 0; j < lines.length; j++) {
      try {
	// parse JSON data
	const doc: Document = JSON.parse(lines[j]);
	// create client.index
	await client.index({
	  index: index,
	  document: {
	    url: doc.url,
	    raw_body: doc.raw_body,
	  },
	  id: "crawl_docs_" + String(j)
	});
      } catch (e) {
	console.log(e);
      }
    }
    const elapsed = new Date().getTime() - start;
    console.log("time")
    console.log(elapsed);
  }

  await client.indices.refresh({ index: index });
}

async function fijToIndex() {
  const dataStr: string = fs.readFileSync("data/fij-post_id-post_discourse/fij-post_id-post_discourse.jsonl", "utf-8");
  const lines: string[] = dataStr.split("\n");
  for (let j = 0; j < lines.length; j++) {
    try {
      // parse JSON data
      console.log(j);
      const doc: FIJ = JSON.parse(lines[j]);
      // create client.index
      await client.index({
	index: index,
	document: {
	  url: doc.post_id,
	  raw_body: doc.post_discourse,
	},
	id: "fij_" + String(j)
      });
    } catch (e) {
      console.log(e);
    }
  }
}

crawlDocsToIndex().catch(console.log);
fijToIndex().catch(console.log);
