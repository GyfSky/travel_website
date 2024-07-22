import numpy as np
import random
from flasker.database.database_link import *
from recommendation import *

import numpy as np
import random
import numpy as np
import random


def allspots_ACO(distmat, start_id, end_id, interest_weights):
    numcity = distmat.shape[0]
    numant = 10
    alpha = 1
    beta = 5
    rho = 0.05
    Q = 20
    itermax = 100

    etatable = 1.0 / (distmat + np.diag([1e10] * numcity))
    pheromonetable = np.ones((numcity, numcity))
    pathtable = np.zeros((numant, numcity), dtype=int)
    lengthaver = np.zeros(itermax)
    lengthbest = np.zeros(itermax)
    pathbest = np.zeros((itermax, numcity))

    start_city = get_index_by_id(start_id)
    end_city = get_index_by_id(end_id)
    pathtable[:, 0] = start_city

    best_path = None
    best_length = np.inf

    for iter in range(itermax):
        lengths = np.zeros(numant)
        paths = np.zeros((numant, numcity), dtype=int)

        for i in range(numant):
            visiting = start_city
            unvisited = set(range(numcity)) - {start_city, end_city}
            path = [start_city]

            while unvisited:
                list_unvisited = list(unvisited)
                probtrans = np.zeros(len(list_unvisited))

                for k in range(len(list_unvisited)):
                    next_city = list_unvisited[k]
                    interest_factor = interest_weights[next_city] if interest_weights[next_city] > 0 else 1e-10
                    probtrans[k] = (np.power(pheromonetable[visiting][next_city], alpha) *
                                    np.power(etatable[visiting][next_city], beta) *
                                    interest_factor)

                if probtrans.sum() == 0:
                    next_city = random.choice(list_unvisited)
                else:
                    probtrans /= probtrans.sum()
                    next_city = np.random.choice(list_unvisited, p=probtrans)

                path.append(next_city)
                unvisited.remove(next_city)
                lengths[i] += distmat[visiting][next_city]
                visiting = next_city

            path.append(end_city)
            lengths[i] += distmat[visiting][end_city]
            paths[i] = path

        if lengths.min() < best_length:
            best_length = lengths.min()
            best_path = paths[lengths.argmin()]

        delta_pheromone = np.zeros_like(pheromonetable)
        for i in range(numant):
            for j in range(numcity - 1):
                delta_pheromone[paths[i, j]][paths[i, j + 1]] += Q / distmat[paths[i, j]][paths[i, j + 1]]
            delta_pheromone[paths[i, -2]][paths[i, -1]] += Q / distmat[paths[i, -2]][paths[i, -1]]

        pheromonetable = (1 - rho) * pheromonetable + delta_pheromone

        if iter % 5 == 0:
            print("Iteration:", iter, "Best Path Length:", best_length)

    print("Best Path:", best_path, "Length:", best_length)



# Example distance matrix and interest weights


distmat = get_adjacent_matrix()
interests = get_recommendation('users_1')

new_dict = {int(key.split('_')[-1]): value for key, value in interests.items()}

interests = [0] * len(interests)
for key, value in new_dict.items():
    spot_index = get_index_by_id(key)
    interests[spot_index] = value
print(interests)
allspots_ACO(distmat, 133, 218, interests)
