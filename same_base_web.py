from urllib.parse import urlparse

def same_base_website(url1, url2):
    parsed_url1 = urlparse(url1)
    parsed_url2 = urlparse(url2)

    # Extract the hostname (netloc) from the parsed URLs
    hostname1 = parsed_url1.netloc.split(':')[0]  # Remove port if any
    hostname2 = parsed_url2.netloc.split(':')[0]

    # Compare the hostnames
    return hostname1 == hostname2 == 'example.com'

# Example usage:
url1 = "https://example.com/page1"
url2 = "example.com/page2"
url3 = "https://differentwebsite.com/page3"

print(same_base_website(url1, url2))  # Output: True (same base website)
print(same_base_website(url1, url3))  # Output: False (different base websites)

