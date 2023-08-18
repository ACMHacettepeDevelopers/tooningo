import os
import requests
from bs4 import BeautifulSoup

def get_chapter_images(chapter_url, output_folder):
    headers = {
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/92.0.4515.107 Safari/537.36"
        ),
        "referer": "https://www.webtoons.com/"
    }

    response = requests.get(chapter_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    image_urls = [img["data-url"] for img in soup.select(".viewer_img img")]

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for idx, image_url in enumerate(image_urls, start=1):
        image_response = requests.get(image_url, headers=headers, stream=True)
        image_extension = image_url.split(".")[-1]
        image_filename = f"{idx:03d}.{image_extension}"
        image_path = os.path.join(output_folder, image_filename)

        with open(image_path, "wb") as image_file:
            for chunk in image_response.iter_content(chunk_size=8192):
                image_file.write(chunk)

        image_path_without_query = image_path.split("?")[0]
        os.rename(image_path, image_path_without_query)

def main():
    chapter_url = "https://www.webtoons.com/en/heartwarming/tata-the-cat/episode-1/viewer?title_no=5547&episode_no=1"
    output_folder = "images/"

    get_chapter_images(chapter_url, output_folder)

if __name__ == "__main__":
    main()
