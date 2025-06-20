import random
import string

def random_ascii(length=10):
    """生成随机ASCII字符串（字母+数字+标点）"""
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

# 打印2400个随机ASCII字符串
for _ in range(2400):
    print(random_ascii())