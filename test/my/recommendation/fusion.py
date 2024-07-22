import numpy as np

# 假设有5个用户和10部电影的评分矩阵（简化示例）
ratings = np.array([
    [5, 4, 0, 0, 3, 0, 0, 0, 0, 2],  # 用户1的评分
    [0, 0, 0, 0, 4, 0, 0, 5, 0, 1],  # 用户2的评分
    [3, 2, 0, 0, 0, 0, 0, 0, 0, 4],  # 用户3的评分
    [0, 0, 0, 0, 4, 5, 0, 4, 0, 0],  # 用户4的评分
    [0, 0, 5, 4, 0, 0, 0, 0, 0, 3],  # 用户5的评分
])

# 假设有10部电影，每部电影有几个简单的特征（类型，演员等）
# 这里简化为电影类型
movie_genres = {
    0: ["Action"],
    1: ["Drama"],
    2: ["Comedy"],
    3: ["Action", "Drama"],
    4: ["Comedy", "Romance"],
    5: ["Horror"],
    6: ["Action", "Comedy"],
    7: ["Drama", "Romance"],
    8: ["Sci-Fi"],
    9: ["Thriller"]
}

# 电影标题
movie_titles = {
    0: "Movie1",
    1: "Movie2",
    2: "Movie3",
    3: "Movie4",
    4: "Movie5",
    5: "Movie6",
    6: "Movie7",
    7: "Movie8",
    8: "Movie9",
    9: "Movie10"
}

# 用户喜欢的电影
user_likes = {
    0: [0, 3, 5],   # 用户1喜欢的电影
    1: [1, 4, 7],   # 用户2喜欢的电影
    2: [0, 3, 9],   # 用户3喜欢的电影
    3: [4, 5, 7],   # 用户4喜欢的电影
    4: [2, 3, 9]    # 用户5喜欢的电影
}

# 计算基于内容的推荐
def content_based_recommendation(user_id):
    liked_movies = user_likes[user_id]
    recommended_movies = set()

    for movie_id in liked_movies:
        movie_genre = movie_genres[movie_id]
        for key, genres in movie_genres.items():
            if key not in liked_movies and any(genre in genres for genre in movie_genre):
                recommended_movies.add(key)

    return recommended_movies

# 计算基于用户的协同过滤推荐
def collaborative_filtering_recommendation(user_id):
    similar_users = []
    for other_user_id, ratings_vector in enumerate(ratings):
        if other_user_id != user_id:
            similarity = np.dot(ratings[user_id], ratings[other_user_id]) / (np.linalg.norm(ratings[user_id]) * np.linalg.norm(ratings[other_user_id]))
            similar_users.append((other_user_id, similarity))

    similar_users.sort(key=lambda x: x[1], reverse=True)

    recommended_movies = set()
    for other_user_id, similarity in similar_users[:2]:
        for movie_id, rating in enumerate(ratings[other_user_id]):
            if rating > 3 and ratings[user_id][movie_id] == 0:
                recommended_movies.add(movie_id)

    return recommended_movies

# 融合推荐结果
def hybrid_recommendation(user_id):
    content_based = content_based_recommendation(user_id)
    collaborative_filtering = collaborative_filtering_recommendation(user_id)
    recommended_movies = list(content_based.union(collaborative_filtering))
    return recommended_movies

# 测试
user_id = 0
print(f"用户{user_id+1}的推荐结果：")
print("基于内容的推荐：", [movie_titles[movie_id] for movie_id in content_based_recommendation(user_id)])
print("协同过滤的推荐：", [movie_titles[movie_id] for movie_id in collaborative_filtering_recommendation(user_id)])
print("融合推荐：", [movie_titles[movie_id] for movie_id in hybrid_recommendation(user_id)])