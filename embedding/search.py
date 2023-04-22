import openai, os, backoff
import pandas as pd
from openai.embeddings_utils import get_embeddings, get_embedding, cosine_similarity


openai.api_key = os.getenv("OPENAI_API_KEY")
COMPLETION_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"

'''
def generate_data_by_prompt(prompt):
    response = openai.Completion.create(
        engine=COMPLETION_MODEL,
        prompt=prompt,
        temperature=0.5,
        max_tokens=2048,
        top_p=1,
    )
    return response.choices[0].text

# 生成3C数码类测试数据
prompt = """请你生成50条京东里的商品标题，每条在30个字左右，品类是3C数码产品，标题里往往也会有一些促销类的信息，每行一条。"""
data = generate_data_by_prompt(prompt)
product_names = data.strip().split('\n')
df = pd.DataFrame({'product_name': product_names})

# 去掉前面的序号
df.product_name = df.product_name.apply(lambda x: x.split('.')[1].strip())
df.head()

# 生成服饰类测试数据
clothes_prompt = """请你生成50条京东里的商品的标题，每条在30个字左右，品类是儿童的服饰等等，标题里往往也会有一些促销类的信息，每行一条。"""
clothes_data = generate_data_by_prompt(clothes_prompt)
clothes_product_names = clothes_data.strip().split('\n')
clothes_df = pd.DataFrame({'product_name': clothes_product_names})
clothes_df.product_name = clothes_df.product_name.apply(lambda x: x.split('.')[1].strip())
clothes_df.head()

df = pd.concat([df, clothes_df], axis=0)
df = df.reset_index(drop=True)

batch_size = 100

@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def get_embeddings_with_backoff(prompts, engine):
    embeddings = []
    for i in range(0, len(prompts), batch_size):
        batch = prompts[i:i+batch_size]
        embeddings += get_embeddings(list_of_text=batch, engine=engine)
    return embeddings

prompts = df.product_name.tolist()
prompt_batches = [prompts[i:i+batch_size] for i in range(0, len(prompts), batch_size)]

embeddings = []
for batch in prompt_batches:
    batch_embeddings = get_embeddings_with_backoff(prompts=batch, engine=EMBEDDING_MODEL)
    embeddings += batch_embeddings

df["embedding"] = embeddings
df.to_parquet("data/jd_product_title.parquet", index=False)
'''

# search through the reviews for a specific product
def search_product(df, query, n=3, pprint=True):
    product_embedding = get_embedding(
        query,
        engine=EMBEDDING_MODEL
    )
    df["similarity"] = df.embedding.apply(lambda x: cosine_similarity(x, product_embedding))

    results = (
        df.sort_values("similarity", ascending=False)
        .head(n)
        .product_name
    )
    if pprint:
        for r in results:
            print(r)
    return results

df = pd.read_parquet("data/jd_product_title.parquet")
results = search_product(df, "天冷穿销量好的衣服", n=3)