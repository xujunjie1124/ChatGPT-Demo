import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "text-davinci-003"

prompt = """产品描述: 蔬菜精灵菜狗娃娃抱枕睡觉抱玩偶女生生日礼物白菜狗公仔毛绒玩具    

1. 为这个商品写一个适合在amazon上使用的英文标题.
2. 用中文给这个商品写5个卖点
3. 卖多少钱比较合适

用json格式输出，包含title, selling_points, price_range三个属性"""


def get_response(prompt):
    completions = openai.Completion.create(
        engine=MODEL,
        prompt=prompt,
        max_tokens=512,
        n=1,
        stop=None,
        temperature=0.0
    )
    message = completions.choices[0].text
    return message

print(get_response(prompt))