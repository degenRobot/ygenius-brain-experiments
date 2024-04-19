# yGenius Brain Experiment

Some custom scripts combining OS LLM's + RAG mechanics with docs from yGenius repo to answer q&a 

(questions can be asked direclty from terminal)

## Configuration

- copy `.env.sample` to `.env` and set environment variables 
- copy `index.json` model file to the current dir or generate a new one

- Note custom docs can be added in training-data directory if want to have custom context & adapt 
- config.py contains configuration option such as using external api (together.ai) or running LLM locally 
- prompt can be customised in chatMechanics/promptBuilder.py

## Run

setup.py will setup chromadb & create embeddings based on documents in training-data
chat.py will open up chat (either calling together api or running model locally using ollama)

## Development

Whenever making changes to the code base, you need to rebuild a new docker image:
`docker-compose build`

## Usage

`curl "http://localhost:5001/ask?history=&query=what%20is%20yearn%20%3F"`

Output:

```
  Yearn is a decentralized finance (DeFi) platform that provides users with access
  to a range of financial services, including yield farming, liquidity pools, and
  automated portfolio management. Yearn is built on the Ethereum blockchain and is
  designed to make it easier for users to maximize their returns on their investments.
```
