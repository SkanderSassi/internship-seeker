from scraper import Seeker

def get_urls(file_name):
    urls = []
    with open(file_name, "r") as file:
        for line in file:
            urls.append(line)
    return urls
    


if __name__ == '__main__':
    
    urls = get_urls("list_of_sites.txt")
    seeker = Seeker(urls)
    seeker.launch_session()