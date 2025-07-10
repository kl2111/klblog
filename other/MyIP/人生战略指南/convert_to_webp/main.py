import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from PIL import Image
import io
import os
import time
import imageio

# 打印Python环境信息
print("Python executable:", sys.executable)
print("Python path:", sys.path)

# 设置无头浏览器
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('window-size=960x1280')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 获取上一级目录中的HTML文件
parent_directory = os.path.abspath('..')
html_files = [file for file in os.listdir(parent_directory) if file.endswith('.html')]
print("检查目录:", parent_directory)
print("找到的文件:", os.listdir(parent_directory))

if not html_files:
    print("无合适的html内容")
    driver.quit()
    exit()

# Process each HTML file
for file_path in html_files:
    webp_count = 0
    full_path = f'file:///{os.getcwd()}/{file_path}'
    driver.get(full_path)
    time.sleep(10)  # Increase wait time to ensure all animations have started

    # Remove unnecessary browser elements via JavaScript
    driver.execute_script("document.body.style.overflow = 'hidden';")  # Hide scrollbars

    # Identify dynamic elements like GIFs or SVGs
    dynamic_elements = driver.find_elements(By.CSS_SELECTOR, "img[src*='.gif'], svg")

    if not dynamic_elements:  # Check if there are no dynamic elements
        print(f"No dynamic elements in {file_path}. No WebP file created.")
        continue  # Skip to the next HTML file

    # Capture and process each dynamic element
    for index, element in enumerate(dynamic_elements):
        # Scroll element into view
        driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(3)  # Allow additional time for animations to load fully

        # Capture frames for this dynamic content
        images = []
        viewport_height = driver.execute_script('return window.innerHeight')
        frame_count = 5  # Capture 5 frames to ensure dynamic effect
        for i in range(frame_count):
            driver.execute_script(f"window.scrollBy(0, {viewport_height / 4 * i})")
            time.sleep(0.5)  # Reduce time interval to capture continuous frames
            png = driver.get_screenshot_as_png()
            image = Image.open(io.BytesIO(png))
            images.append(image)

        # Resize images to ensure they are 960x1280 before saving
        resized_images = [img.resize((960, 1280), Image.Resampling.LANCZOS) for img in images]

        # Save as animated WebP for each dynamic element, in the same directory as the HTML
        webp_path = f'./{os.path.splitext(file_path)[0]}_dynamic_content_{index + 1}.webp'
        imageio.mimsave(webp_path, resized_images, format='WEBP', loop=0, fps=5)  # Adjust fps as needed
        webp_count += 1

    print(f"{file_path} - {webp_count}张webp图")

driver.quit()
