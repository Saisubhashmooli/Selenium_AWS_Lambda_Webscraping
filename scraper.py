# import required libraries
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# url for scrape the data
YOUTUBE_TRENDING_URL = "https://www.youtube.com/results?search_query=trending+videos"

# Creating the driver
def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  return driver

# get the videos using url
def get_videos(driver):
  VIDEO_DIV_TAG = 'ytd-video-renderer'
  driver.get(YOUTUBE_TRENDING_URL)
  videos = driver.find_elements(By.TAG_NAME, VIDEO_DIV_TAG)
  return videos

# Parsing the videos
def parse_video(video):
  title_tag = video.find_element(By.ID, 'video-title')
  title = title_tag.text
  url = title_tag.get_attribute('href')

  thumbnail_tag = video.find_element(By.TAG_NAME, 'img')
  thumbnail_url = thumbnail_tag.get_attribute('src')

  channel_div = video.find_element(By.CLASS_NAME, 'ytd-channel-name')
  channel_name = channel_div.text

  views_div = videos.find_element(By.CLASS, 'ytd-video-meta-block')
  views = views_div.text

  uploaded_div = videos.find_element(By.CLASS, 'ytd-video-meta-block')
  uploaded = uploaded_div.text

  description = video.find_element(By.ID, 'description-text').text
    
  return {
  'title': title,
  'url': url,
  'thumbnail_url': thumbnail_url,
  'channel' : channel_name,
  'views': views,
  'uploaded': uploaded,
  'description': description
}

def send_email():
  pass


if __name__ == "__main__":
  print('Creating driver')
  driver = get_driver()

  print('Fetching trending vidoes')
  videos = get_videos(driver)
  
 #print(f'Found {len(video_divs)} videos')

print('Parsing top 10 videos')
videos_data = [parse_video(video) for video in videos[:10]]

#print(videos_data[3])

print('Save the data to a CSV')
videos_df = pd.DataFrame(videos_data)
print(videos_df)
videos_df.to_csv('trending.csv', index=None)

print("Send an email")
send_email()