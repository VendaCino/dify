# Llm Backend

## Overview
启动 rerank 和 embedding server，基于llama cpp
download release in https://github.com/ggerganov/llama.cpp/releases

## prepare llama cpp
```sh
cd llm
mkdir llama_cpp
cd llama_cpp
curl -L -o llama_cpp.zip https://github.com/ggerganov/llama.cpp/releases/download/b4568/llama-b4568-bin-ubuntu-x64.zip
unzip llama_cpp.zip
```

## prepare model
```sh
cd llm
mkdir model
cd model
# reranker model
curl -L -o bge-reranker-v2-m3-Q5_K_M.gguf https://huggingface.co/gpustack/bge-reranker-v2-m3-GGUF/resolve/main/bge-reranker-v2-m3-Q5_K_M.gguf?download=true
# embedding model
curl -L -o bge-large-zh-v1.5-q4_k_m.gguf https://huggingface.co/CompendiumLabs/bge-large-zh-v1.5-gguf/resolve/main/bge-large-zh-v1.5-q4_k_m.gguf?download=true
```

test llama cpp
```sh
cd llm
./llama_cpp/build/bin/llama-embedding -c 4096 -b 4096 -m ./model/bge-large-zh-v1.5-q4_k_m.gguf -ngl 99 -p "Hi"
```

run server
```sh
./llama_cpp/build/bin/llama-server \
    -m ./model/bge-reranker-v2-m3-Q5_K_M.gguf \
    --host 127.0.0.1 --port 8012 -lv 1 \
    --rerank 

./llama_cpp/build/bin/llama-server \
    -m ./model/bge-large-zh-v1.5-q4_k_m.gguf \
    -c 4096 -b 4096 \
    --host 127.0.0.1 --port 8013 -lv 1 \
    --embeddings
```

```sh
curl -X POST "http://localhost:8013/v1/embeddings" --data '{"content":"some text to embed"}'

curl -X POST http://localhost:8012/v1/rerank \
     -H "Content-Type: application/json" \
     -d '{
       "query": "如何学习机器学习",
       "documents": [
         "提供 Python 编程课程",
         "解释什么是神经网络",
         "提供一本机器学习书籍推荐"
       ]
     }'
```