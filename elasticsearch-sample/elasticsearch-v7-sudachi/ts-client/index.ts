import { Client } from '@elastic/elasticsearch';


const client = new Client({
  node: "http://192.168.64.4:9200",
  auth: {
    username: "elastic",
    password: "elastic",
  },
});

interface Document {
  character: string
  quote: string
}

async function run() {
  console.log("hello");
  await client.index({
    index: "game-of-thrones",
    document: {
      character: "Ned Stark",
      quote: "Winter is coming.",
    }
  });

  await client.index({
    index: "game-of-thrones",
    document: {
      character: "Daenerys Targaryen",
      quote: "I am the blood of the dragon.",
    }
  });

  await client.index({
    index: "game-of-thrones",
    document: {
      character: "Tyrion Lannister",
      quote: "A mind needs books like a sword needs a whetstone.",
    }
  });

  await client.indices.refresh({ index: "game-of-thrones" });

  const result = await client.search<Document>({
    index: "game-of-thrones",
    query: {
      match: { quote: "Winter" }
    }
  });

  console.log(result.hits.hits);
}

run().catch(console.log);

