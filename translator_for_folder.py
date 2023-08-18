import ana2
import webtooncom_scrapper
import os

# Call webtooncom_scrapper.py to download the images for the given chapter
webtooncom_scrapper.main("https://www.webtoons.com/en/heartwarming/tata-the-cat/episode-1/viewer?title_no=5547&episode_no=1", "webtoon_images")

# Call ana2.py for each image in the folder
for filename in os.listdir("webtoon_images"):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        ana2.main("webtoon_images/" + filename, "webtoon_images_translated/" + filename, False)
        continue
    else:
        continue
