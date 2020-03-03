import random
import string


def random_str(num, types):
    if types == 1:
        # 生成数值随机数
        salt = ''.join(random.sample(string.digits, num))

    elif types == 2:
        # 生成数值加字母随机数
        salt = ''.join(random.sample(string.digits + string.ascii_letters, num))

    return salt
