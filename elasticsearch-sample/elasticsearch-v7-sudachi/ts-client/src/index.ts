import fs from 'fs';

import { Client } from '@elastic/elasticsearch';

const index = "sample-like-vaccine_20220315_2";

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
  console.log("hello");
  // await client.index({
  //   index: "game-of-thrones",
  //   document: {
  //     character: "Ne Stark",
  //     quote: "Winter is comin.",
  //   }
  // });

  // await client.index({
  //   index: "game-of-thrones",
  //   document: {
  //     character: "Daenery Targaryen",
  //     quote: "I am the bloo of the dragon.",
  //   }
  // });

  // await client.index({
  //   index: "game-of-thrones",
  //   document: {
  //     character: "Tyrio Lannister",
  //     quote: "A mind needs books lik a sword needs a whetstone.",
  //   }
  // });
  
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
	  }
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

run().catch(console.log);
