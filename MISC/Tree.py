import math
import time
import os

def draw_tree():
    width = 80
    height = 40
    
    # 动画无限循环
    t = 0
    while True:
        # 类似显存的缓存区 (Z-buffer 和 字符 buffer)
        z_buffer = [0] * (width * height)
        screen = [' '] * (width * height)
        
        # 每一帧增加时间 t，让树旋转
        t += 0.1
        
        # 树的主体 (螺旋线条)
        for i in range(2000):
            # 随机或有序生成点，这里用简单的数学构造螺旋圆锥
            y_norm = (i / 2000) # 0 到 1，从树顶到树底
            radius = y_norm * 2  # 半径随高度变大
            angle = i * 0.1 + t  # 旋转角度
            
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            y = y_norm * 3 - 1.5 # 调整高度位置
            
            # 简单的 3D 投影公式
            # 绕 X 轴微倾斜让视角更好看
            rx = x
            ry = y * math.cos(0.5) - z * math.sin(0.5)
            rz = y * math.sin(0.5) + z * math.cos(0.5)
            
            # 透视投影
            perspective = 1 / (2.5 - rz)
            px = int(width / 2 + rx * perspective * 20)
            py = int(height / 2 - ry * perspective * 10)
            
            # 绘制点
            if 0 <= px < width and 0 <= py < height:
                idx = px + py * width
                if perspective > z_buffer[idx]:
                    z_buffer[idx] = perspective
                    # 根据深度显示不同字符，模拟光影
                    if y_norm < 0.1: # 星星
                        screen[idx] = '*' 
                    else:
                        screen[idx] = '.' if rz < 0 else 'o' # 树身
        
        # 清屏并打印
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # 加上 Merry Christmas
        msg = "Merry Christmas"
        start_pos = (height - 2) * width + (width - len(msg)) // 2
        for i, char in enumerate(msg):
            if 0 <= start_pos + i < len(screen):
                screen[start_pos + i] = char

        print(''.join(screen))
        time.sleep(0.05)

if __name__ == "__main__":
    try:
        draw_tree()
    except KeyboardInterrupt:
        print("\nBye!")