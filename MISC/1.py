def to_base(num, base):
    """将十进制数转换为指定进制"""
    if num == 0:
        return "0"
    
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    if base > 36:
        # 扩展到包含大写字母
        digits = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    result = ""
    while num > 0:
        result = digits[num % base] + result
        num //= base
    return result

# feed 的十六进制值
feed_hex = 0xfeed
beef_hex = 0xbeef

print(f"feed (16进制) = {feed_hex} (10进制)")
print(f"beef (16进制) = {beef_hex} (10进制)")
print()

# 尝试所有可能的进制
for base in range(2, 100):
    result_feed = to_base(feed_hex, base)
    result_beef = to_base(beef_hex, base)
    
    if result_feed == "2cfb":
        print(f"找到了！进制 = {base}")
        print(f"feed (16进制) = {feed_hex} (10进制) = 2cfb ({base}进制)")
        print(f"beef (16进制) = {beef_hex} (10进制) = {result_beef} ({base}进制)")
        print()
        
        # 现在计算 6422
        result_6422 = to_base(0x6422, base)
        print(f"6422 (10进制) = {result_6422} ({base}进制)")
        print(f"\n答案: 6422 = {result_6422}")
        break
    
    if result_beef == "1o99":
        print(f"beef 匹配！进制 = {base}")
        print(f"但 feed = {result_feed} (不是 2cfb)")
