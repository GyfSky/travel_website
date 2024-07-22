import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
 
# 假设我们有以下数据：用户对电影的评分
data = {
    'User': ['Alice', 'Bob', 'Cindy', 'Dan', 'Eva'],
    'Matrix': [5, 3, None, 1, None],
    'Titanic': [1, 2, 5, 2, 5],
    'Die Hard': [None, 5, 1, 5, None],
    'Forrest Gump': [2, 4, 2, None, 3],
    'Wall-E': [None, None, None, 5, 4]
}
 
df = pd.DataFrame(data).set_index('User')
df.fillna(0, inplace=True) 

# 计算物品之间的余弦相似度
item_similarity = cosine_similarity(df.T)
similarity_df = pd.DataFrame(item_similarity, index=df.columns, columns=df.columns)

print("Item Similarity Matrix:")
print(similarity_df)

def recommend_movies(similarity, movie_name, user_rating):
    scores = similarity[movie_name] * (user_rating - 2.5)  # 将评分调整，考虑用户评分
    scores = scores.sort_values(ascending=False)
    return scores
 
print("Recommendations for Alice if she rated 'Titanic' 5 stars:")
print(recommend_movies(similarity_df, 'Wall-E', 3))