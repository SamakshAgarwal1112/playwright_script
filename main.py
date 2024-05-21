from playwright.sync_api import sync_playwright
from ad_skipper import ad_skipper
from screenshot import screenshot

def main(query):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('https://www.youtube.com/')
        
        input_field = page.locator('input#search').first
        input_field.type(query)
        page.wait_for_timeout(1000)
        input_field.press('Enter')
        page.wait_for_selector('ytd-video-renderer a#thumbnail', timeout=10000)
        print("Video Found Successfully!")
        
        page.locator('ytd-video-renderer a#thumbnail').first.click()
        page.wait_for_selector('video', timeout=10000)
        page.wait_for_timeout(2000)
        video = page.locator('video').first
        page.wait_for_timeout(2000)
        print("First Video Selected!")
        
        print("Checking for Ads...")
        ad_skipper(page)

        result_path = screenshot(page,video)
        browser.close()
        if result_path:
            print("Path were the screenshots are saved:", result_path)
        else:
            print("Resultant path for screenshots not fetched due to random error!")
       
def run():
    query = input('Enter a string: ')
    main(query)
    
if __name__ == "__main__":
    run()