import random
from model import User

# 昵称词库，咖啡主题
prefix_list = ["咖啡", "拿铁", "美式", "摩卡", "瑞幸", "冰吸", "椰云", "生椰", "陨石", "厚乳"]
suffix_list = ["爱好者", "达人", "星友", "玩家", "小主", "食客", "追光者", "少年", "晚风", "橘子"]


def get_random_nickname():
    while True:
        pre = random.choice(prefix_list)
        suf = random.choice(suffix_list)
        num = random.randint(100, 999)
        nick = f"{pre}{suf}{num}"
        if not User.query.filter_by(nickname=nick).first():
            return nick
