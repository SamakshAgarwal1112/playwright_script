from playwright.sync_api import sync_playwright
import os 

def main(s):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('https://www.youtube.com/')
        input_field = page.locator('input#search').first
        input_field.type(s)
        page.wait_for_timeout(1000)
        input_field.press('Enter')
        page.wait_for_selector('ytd-video-renderer a#thumbnail', timeout=10000)
        page.locator('ytd-video-renderer a#thumbnail').first.click()
        page.wait_for_selector('video', timeout=10000)
        page.wait_for_timeout(2000)
        video = page.locator('video').first
        page.wait_for_timeout(3000)

        def skip_ads(page):
            try:
                ad_preview_button = page.locator('.ytp-preview-ad').first
                if(ad_preview_button.is_visible()):
                    page.wait_for_timeout(5000)
                    video.evaluate('video => video.pause()')
                
                ad_skip_button = page.locator('.ytp-skip-ad-button')
                if ad_skip_button.is_visible():
                    ad_skip_button.click()
                    print("Ad skipped")
                else:
                    print("No ads to skip")
            except Exception as e:
                print(f"No ads to skip: {e}")

        ad_check_duration = 1000
        max_check_time = 60000
        elapsed_time = 0

        while elapsed_time < max_check_time:
            skip_ads(page)
            page.wait_for_timeout(ad_check_duration)
            elapsed_time += ad_check_duration

            if not page.locator('.ytp-ad-player-overlay').is_visible() and not page.locator('.ytp-ad-skip-button').is_visible():
                break

        video.evaluate('video => video.pause()')
        duration = video.evaluate('video => video.duration')
        print(f"Video duration: {duration} seconds")
        
        count = 0
        current_time = 0
        current_dir = os.getcwd()
        result_path = f'{current_dir}\screenshots'
        
        while current_time < duration:
            video.evaluate(f'video => video.currentTime = {current_time}')
            page.wait_for_timeout(1000)
            current_time += 10
            count += 1
            page.screenshot(path=f'{result_path}\screenshot_{count}.png')
            
        video.evaluate(f'video => video.currentTime = {duration}')
        page.wait_for_timeout(1000)
        browser.close()
        print("Path were the screenshots are saved:", result_path)
       
def inp():
    s = input('Enter a string: ')
    main(s)
    
inp()