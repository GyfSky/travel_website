from flasker.database.database_link import *


interest_spots = set(i for i in range(10))
print(interest_spots)

print(get_spot_score(133))