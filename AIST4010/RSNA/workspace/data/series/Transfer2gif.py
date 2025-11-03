import pydicom
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm

def process_single_folder(
    dicom_folder,
    output_folder,
    fps=20
):
    """
    处理单个文件夹的 DICOM 文件
    """
    duration_ms = int(1000 / fps)
    
    dcm_files = sorted(Path(dicom_folder).glob('*.dcm'))
    
    if not dcm_files:
        return None
    
    # 读取切片
    slices = []
    for dcm_file in dcm_files:
        ds = pydicom.dcmread(dcm_file)
        slices.append(ds)
    
    # 排序
    try:
        slices.sort(key=lambda x: int(x.InstanceNumber))
    except:
        pass
    
    # 转换为图像
    pil_frames = []
    total_slices = len(slices)
    
    for i, ds in enumerate(slices):
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
    
    # 保存 GIF
    folder_name = Path(dicom_folder).name
    output_path = Path(output_folder) / f"{folder_name}.gif"
    
    pil_frames[0].save(
        output_path,
        save_all=True,
        append_images=pil_frames[1:],
        duration=duration_ms,
        loop=0,
        optimize=False
    )
    
    return {
        'name': folder_name,
        'frames': len(pil_frames),
        'path': output_path
    }

def batch_dicom_to_gif(
    root_folder='.',
    output_folder='gifs',
    fps=20
):
    """
    批量处理多个子文件夹的 DICOM 文件
    
    参数:
        root_folder: 包含多个子文件夹的根目录
        output_folder: GIF 输出目录
        fps: 帧率
    """
    root_path = Path(root_folder)
    output_path = Path(output_folder)
    
    # 创建输出目录
    output_path.mkdir(exist_ok=True)
    
    # 获取所有子文件夹
    subfolders = [f for f in root_path.iterdir() if f.is_dir()]
    
    if not subfolders:
        print("❌ 未找到子文件夹")
        return
    
    print(f"📁 找到 {len(subfolders)} 个子文件夹")
    print(f"📤 输出目录: {output_path.absolute()}")
    print(f"🎬 帧率: {fps} FPS\n")
    
    results = []
    
    # 处理每个子文件夹
    for folder in tqdm(subfolders, desc="总体进度"):
        folder_name = folder.name
        tqdm.write(f"🔄 处理: {folder_name}")
        
        result = process_single_folder(folder, output_path, fps)
        
        if result:
            results.append(result)
            tqdm.write(f"   ✅ {result['frames']} 帧 → {result['path'].name}")
        else:
            tqdm.write(f"   ⚠️  跳过（无 DICOM 文件）")
    
    # 输出统计
    print(f"\n{'='*50}")
    print(f"✅ 完成！共生成 {len(results)} 个 GIF 文件")
    print(f"{'='*50}")
    
    for r in results:
        total_time = r['frames'] * (1000/fps) / 1000
        print(f"  📄 {r['name']}.gif")
        print(f"     - 帧数: {r['frames']}")
        print(f"     - 时长: {total_time:.2f}秒")

if __name__ == '__main__':
    # 示例 1: 使用默认参数（当前目录的子文件夹 → gifs 文件夹）
    batch_dicom_to_gif('.', 'gifs', fps=30)
    
    # 示例 2: 自定义路径
    # batch_dicom_to_gif(
    #     root_folder='data/patients',
    #     output_folder='output/animations',
    #     fps=25
    # )
