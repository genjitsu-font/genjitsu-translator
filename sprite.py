import os
import json
import unicodedata
from PIL import Image

# Get current directory path
current_dir = os.path.dirname(os.path.abspath(__file__))

# 全画像が格納されているディレクトリ
img_dir = os.path.join(current_dir, 'glyph')

# スプライト画像と座標情報の出力先
output_img_path = os.path.join(current_dir, 'public', 'characters.png')
output_json_path = os.path.join(current_dir, 'public', 'coords.json')

# 全画像のリストを作成
img_files = sorted([f for f in os.listdir(img_dir) if f.endswith('.png')])

# 各画像のオブジェクトと座標情報を格納する辞書
images = {}
coords = {}

x_offset = 0
y_offset = 0
img_height = 0

for img_file in img_files:
    # 画像を開き、images 辞書に格納
    img_path = os.path.join(img_dir, img_file)
    img = Image.open(img_path)
    normalized_key = unicodedata.normalize('NFKC', img_file[:-4])  # ファイル名をNFKC方式で正規化
    images[normalized_key] = img
    img_height = img.height  # 画像の高さ（全画像が同じ高さを持つと仮定）

    # 座標情報を記録
    coords[normalized_key] = { "x": x_offset, "y": y_offset, "w": img.width, "h": img.height }

    # 次の画像のためのオフセットを更新
    x_offset += img.width
    if x_offset >= 500:  # 500pxを超える場合は次の行に移る
        x_offset = 0
        y_offset += img_height

# 行数を計算
num_rows = len(img_files) // 10  # 1行に10枚の画像を配置
if len(img_files) % 10 > 0:  # 余りがある場合は行数を1増やす
    num_rows += 1

# 新しい画像を作成
sprite_img = Image.new('RGBA', (500, num_rows * img_height))

# 各画像を新しい画像にペースト
x_offset = 0
y_offset = 0
for char, img in images.items():
    sprite_img.paste(img, (x_offset, y_offset))
    x_offset += img.width
    if x_offset >= 500:  # 500pxを超える場合は次の行に移る
        x_offset = 0
        y_offset += img_height
    img.close()

# スプライト画像を保存
sprite_img.save(output_img_path)

# 座標情報を JSON として保存
with open(output_json_path, 'w') as f:
    json.dump(coords, f)
