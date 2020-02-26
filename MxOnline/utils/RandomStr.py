import random
import string


def random_str(num):
    # 生成四位随机数
    salt = ''.join(random.sample(string.digits, num))

    return salt
