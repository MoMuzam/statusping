import urllib.request
import time

def check_website(url):
    start_time = time.time()
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


def lambda_handler(event, context):
    urls_to_check = [
        "https://www.google.com",
        "https://www.github.com"
    ]

    results = []
    for url in urls_to_check:
        result = check_website(url)
        results.append(result)
        print(result)

    return {
        "statusCode": 200,
        "results": results
    }

if __name__ == "__main__":
    fake_event = {}
    fake_context = None
    output = lambda_handler(fake_event, fake_context)
    print(output)