def detect_ad(page):
    try:
        ad_preview_button = page.locator('.ytp-preview-ad').first
        if(ad_preview_button.is_visible()):
            page.wait_for_timeout(5000)
                
        ad_skip_button = page.locator('.ytp-skip-ad-button')
        if ad_skip_button.is_visible():
            ad_skip_button.click()
            print("Ad skipped")
        else:
            print("No ads to skip")
    except Exception as e:
        print(f"Error while detecting ads: {e}")
   
def ad_skipper(page):
    try:
        ad_check_interval = 1000
        max_check_time = 60000
        checked_time = 0
        while checked_time < max_check_time:
            detect_ad(page)
            page.wait_for_timeout(ad_check_interval)
            checked_time += ad_check_interval

            if not page.locator('.ytp-preview-ad').is_visible() and not page.locator('.ytp-skip-ad-button').is_visible():
                break
    except Exception as e:
        print(f"Error while skipping ads: {e}")