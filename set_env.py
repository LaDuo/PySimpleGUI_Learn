import os
from defi import Av2_Output
from defi import Av2_Input
from defi import Analyze
from defi import ALL


# 检测本地环境，查看是否存在指定目录<Analyze>,<Av2_Output>, <Av2_Input>
def detect_env():
    counts = 0
    if not os.path.exists(Av2_Input):
        counts += 1
    elif not os.path.exists(Av2_Output):
        counts += 1
    elif not os.path.exists(Analyze):
        counts += 1
    if counts != 0:
        return True
    else:
        return False


def env_set():
    count = 0
    if not os.path.exists(Av2_Input):
        os.mkdir(Av2_Input)
        count += 1
    elif not os.path.exists(Av2_Output):
        os.mkdir(Av2_Output)
        count += 1
    elif not os.path.exists(Analyze):
        os.mkdir(Analyze)
        os.mkdir(ALL)
        count += 1
    if count != 0:
        return True
    else:
        return False
