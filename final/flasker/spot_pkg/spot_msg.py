from flasker.database.database_link import *
from flasker.spot_pkg.SpotClass import *

# 创建景点对象
def spot(spot_id,POOL):
    msg = get_spot_msg(spot_id,POOL)
    spot_name = Spot(*msg)
    return spot_name