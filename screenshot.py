import os

def filter_title(title):
    invalid_characters = [' ',',', ':', '/', '\\', '*', '?', '"', '<', '>', '|']
    for character in invalid_characters:
        title = title.replace(character, '_')
    return title

def screenshot(page,video):
    try:
        title = page.locator('div#title yt-formatted-string').first.inner_text()
        title = filter_title(title)
        video.evaluate('video => video.pause()')
        duration = video.evaluate('video => video.duration')
        print(f"Video: {title} and duration: {duration} seconds")
            
        count = 0
        current_time = 0
        current_dir = os.getcwd()
        result_path = f'{current_dir}\screenshots\{title}'
        
        try:    
            while current_time < duration:
                video.evaluate(f'video => video.currentTime = {current_time}')
                page.wait_for_timeout(1000)
                current_time += 10
                count += 1
                page.screenshot(path=f'{result_path}\screenshot_{count}.png')
                    
            video.evaluate(f'video => video.currentTime = {duration}')
            page.wait_for_timeout(1000)
        except Exception as e:
            print(f'Error while taking screenshots: {e}')
        print(f'Total screenshots taken: {count}')
        return result_path
    except Exception as e:
        print(f'Error detected: {e}')