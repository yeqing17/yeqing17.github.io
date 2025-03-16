from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
import os
from datetime import datetime

client = genai.Client(api_key="Your API Key")
contents = ('Hi, can you create a 3d rendered image of a pig '
            'with wings and a top hat flying over a happy ' 
            'futuristic scifi city with lots of greenery?')

response = client.models.generate_content(
    model="models/gemini-2.0-flash-exp",
    contents=contents,
    config=types.GenerateContentConfig(response_modalities=['Text', 'Image'])
)

# 在 response 之后添加以下代码
save_dir = os.path.join(os.path.dirname(__file__), 'GeminiFlash2.0Exp')
os.makedirs(save_dir, exist_ok=True)

for part in response.candidates[0].content.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        try:
            image_data = base64.b64decode(part.inline_data.data)
            image = Image.open(BytesIO(image_data))
            
            # 生成带时间戳的文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            image_path = os.path.join(save_dir, f'gemini_image_{timestamp}.png')
            
            # 保存图片
            image.save(image_path)
            print(f'图片已保存至: {image_path}')
            
            # 显示图片
            image.show()
        except Exception as e:
            print(f"无法处理图像数据: {e}")
            print(f"数据类型: {type(part.inline_data.data)}")