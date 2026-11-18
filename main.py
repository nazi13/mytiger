import os
import json
import requests
import subprocess
import anthropic

# ۱. دریافت ترند روز از ردیت (رایگان و بدون نیاز به احراز هویت پیچیده)
def get_daily_trend():
    headers = {'User-Agent': 'TrendTigerBot/1.0'}
    res = requests.get("https://www.reddit.com/r/popular/top.json?t=day&limit=1", headers=headers)
    post = res.json()['data']['children'][0]['data']
    return post['title']

# ۲. تولید اسکریپت و پرامپت لباسِ متضاد با کلاد
def generate_script_and_prompts(trend_title):
    client = anthropic.Anthropic(api_key=os.environ["CLAUDE_API_KEY"])
    
    # امضای ثابت برای حفظ ظاهر ببر دختر در تمام ویدیوها
    base_character = "Cute 3D Pixar-style female tiger character, big expressive eyes, fluffy cheeks"
    
    prompt = f"""
    موضوع ترند امروز: {trend_title}
    یک ویدیوی شورتس ۲۰ ثانیه‌ای به زبان انگلیسی (یا اسپانیایی) طراحی کن.
    خروجی رو دقیقاً با فرمت JSON زیر بده:
    {{
      "voiceover": "متن جذاب و طنزآمیز با قلاب اولیه قوی",
      "image_prompts": [
        "{base_character}, wearing [لباس متضاد و خنده‌دار متناسب با صحنه ۱], 3D render, 9:16",
        "{base_character}, wearing [لباس متضاد برای صحنه ۲], shocked expression, 3D render, 9:16",
        "{base_character}, wearing [لباس متضاد برای صحنه ۳], laughing, 3D render, 9:16"
      ],
      "title": "عنوان وایرال برای یوتیوب و تیک‌تاک #shorts"
    }}
    """
    
    message = client.messages.create(
        model="claude-3-5-haiku-latest",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(message.content[0].text)

# ۳. ساخت صدا و زیرنویس با edge-tts
def make_audio(text):
    subprocess.run([
        "edge-tts",
        "--voice", "en-US-AnaNeural", # صدای دخترانه و کیوت
        "--text", text,
        "--write-media", "voice.mp3",
        "--write-subtitles", "subs.srt"
    ], check=True)
