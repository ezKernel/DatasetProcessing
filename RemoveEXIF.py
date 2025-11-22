
from PIL import Image, ExifTags
import os

def fix_orientation(image_path, output_path=None):
    """修正单张图片的方向，使像素矩阵物理上为正方向"""
    try:
        img = Image.open(image_path)

        # 获取 EXIF 信息
        exif = img._getexif()
        if exif is not None:
            # 找到 Orientation 字段的键
            for key, val in ExifTags.TAGS.items():
                if val == 'Orientation':
                    orientation_key = key
                    break

            orientation = exif.get(orientation_key, 1)

            # 根据 orientation 旋转或翻转图像
            if orientation == 2:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                img = img.rotate(180, expand=True)
            elif orientation == 4:
                img = img.transpose(Image.FLIP_TOP_BOTTOM)
            elif orientation == 5:
                img = img.transpose(Image.FLIP_LEFT_RIGHT).rotate(90, expand=True)
            elif orientation == 6:
                img = img.rotate(270, expand=True)
            elif orientation == 7:
                img = img.transpose(Image.FLIP_LEFT_RIGHT).rotate(270, expand=True)
            elif orientation == 8:
                img = img.rotate(90, expand=True)

        # 默认保存到原路径
        if output_path is None:
            output_path = image_path

        # 保存时丢弃 EXIF（避免再次旋转）
        root, _ = os.path.splitext(image_path)
        output_path = root + ".jpg"
        img.save(output_path, "JPEG", quality=100)

        print(f"已修正: {image_path}")

    except Exception as e:
        print(f"处理 {image_path} 出错: {e}")


def batch_fix(folder):
    """批量修正文件夹下所有 JPG 图片"""
    for filename in os.listdir(folder):
        if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
            path = os.path.join(folder, filename)
            fix_orientation(path)


if __name__ == "__main__":
    folder = "./Electroscope"  # 修改为你的文件夹路径
    batch_fix(folder)
