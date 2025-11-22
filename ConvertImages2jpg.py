import os
from PIL import Image

def ConvertImages2jpg(folder_path):
    """
    将文件夹中的图片转换为JPG格式
    支持格式：png, tiff, jpeg等 -> jpg
    如果是JPG/JPEG/jpeg，则直接修改后缀名为.jpg
    """
    # 支持的图片格式映射
    supported_formats = {
        '.png': 'PNG',
        '.tiff': 'TIFF', 
        '.tif': 'TIFF',
        '.bmp': 'BMP',
        '.jpeg': 'JPEG',
        '.jpg': 'JPEG'
    }
    
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # 跳过目录
        if os.path.isdir(file_path):
            continue
            
        # 获取文件扩展名（小写）
        file_ext = os.path.splitext(filename)[1].lower()
        
        # 检查是否为支持的图片格式
        if file_ext in supported_formats:
            try:
                # 处理JPG/JPEG文件：直接修改后缀名
                if file_ext in ['.jpg', '.jpeg']:
                    if file_ext != '.jpg':
                        new_filename = os.path.splitext(filename)[0] + '.jpg'
                        new_file_path = os.path.join(folder_path, new_filename)
                        
                        # 避免覆盖已存在的文件
                        if not os.path.exists(new_file_path):
                            os.rename(file_path, new_file_path)
                            print(f"重命名: {filename} -> {new_filename}")
                        else:
                            print(f"跳过 {filename}：目标文件已存在")
                
                # 处理其他格式：转换为JPG
                else:
                    with Image.open(file_path) as img:
                        # 转换为RGB模式（处理RGBA等格式）
                        if img.mode in ('RGBA', 'LA', 'P'):
                            rgb_img = img.convert('RGB')
                        else:
                            rgb_img = img
                        
                        # 生成新文件名
                        new_filename = os.path.splitext(filename)[0] + '.jpg'
                        new_file_path = os.path.join(folder_path, new_filename)
                        
                        # 保存为JPG格式
                        rgb_img.save(new_file_path, 'JPEG', quality=95)
                        
                        # 删除原文件
                        os.remove(file_path)
                        print(f"转换: {filename} -> {new_filename}")
                        
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {str(e)}")

if __name__ == "__main__":
    # 使用示例
    folder_path = input("请输入文件夹路径: ").strip()
    
    if os.path.exists(folder_path):
        convert_images_to_jpg(folder_path)
        print("转换完成！")
    else:
        print("文件夹路径不存在！")
