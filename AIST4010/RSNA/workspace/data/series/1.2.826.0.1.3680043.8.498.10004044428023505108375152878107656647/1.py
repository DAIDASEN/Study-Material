import pydicom
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm

def dicom_to_gif(
    dicom_folder='.',
    output_gif='output.gif',
    fps=20
):
    """
    使用 Pillow 保存 GIF，速度控制更准确
    """
    
    duration_ms = int(1000 / fps)  # 转换为毫秒
    
    dcm_files = sorted(Path(dicom_folder).glob('*.dcm'))
    
    if not dcm_files:
        print("❌ 未找到 DICOM 文件")
        return
    
    print(f"📁 找到 {len(dcm_files)} 个 DICOM 文件")
    
    slices = []
    for dcm_file in tqdm(dcm_files, desc="读取"):
        ds = pydicom.dcmread(dcm_file)
        slices.append(ds)
    
    try:
        slices.sort(key=lambda x: int(x.InstanceNumber))
    except:
        pass
    
    pil_frames = []
    total_slices = len(slices)
    
    for i, ds in enumerate(tqdm(slices, desc="处理")):
        img = ds.pixel_array.astype(float)
        img = (img - img.min()) / (img.max() - img.min()) * 255
        img = img.astype(np.uint8)
        
        pil_img = Image.fromarray(img).convert('RGB')
        draw = ImageDraw.Draw(pil_img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        text = f"{i+1}/{total_slices}"
        draw.text((10, 10), text, fill=(255, 255, 0), font=font)
        
        pil_frames.append(pil_img)
    
    # 使用 Pillow 保存，duration 单位是毫秒
    pil_frames[0].save(
        output_gif,
        save_all=True,
        append_images=pil_frames[1:],
        duration=duration_ms,  # 毫秒
        loop=0,
        optimize=False
    )
    
    total_time = len(pil_frames) * duration_ms / 1000
    print(f"✅ 完成: {output_gif}")
    print(f"   帧数: {len(pil_frames)}")
    print(f"   速度: {fps} FPS ({duration_ms}ms/帧)")
    print(f"   总时长: {total_time:.2f}秒")

if __name__ == '__main__':
    dicom_to_gif('.', 'fast.gif', fps=30)   # 快速
