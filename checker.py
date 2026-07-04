import urllib.request
import time

def check_website(url):
    start_time = time.time()  # records the current time
    try:
        response = urllib.request.urlopen(url, timeout=5)
        status_code = response.status
    except Exception as e:
        status_code = None

    end_time = time.time()
    response_time_ms = round((end_time - start_time) * 1000)

    return {
        "url": url,
        "status_code": status_code,
        "response_time_ms": response_time_ms
    }

if __name__ == "__main__":
    urls = ["https://www.google.com", "https://www.thissitedoesnotexist12345.com"]
    for url in urls:
        result = check_website(url)
        print(result)