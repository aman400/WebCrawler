## A Web Crawler.
## Author : Amandeep
## version : v2.4

import urllib
import urllib.request
from bs4 import BeautifulSoup
 
class webcrawler:
    # construtor
    def __init__(self, address):
        """(str) -> None

        Constructor to initaialize member variables it takes a valid url as input.

        """
        self.tocrawl = set([])
        if not address.startswith("http://"):
            self.tocrawl.add("http://"+address)
        else:
            self.tocrawl.add(address)
        self.crawled = []
        self.crawl_web()

    # get next link in the page.
    # for manual parsing of page.
    def next_link(self, page):
        """ (str) -> str, int

        returns the first link extracted form the page
        >>> next_link('adnfjsnfsfsa <a href="http://www.google.co.in"sjnfsdfnksd')
        ('http://www.google.co.in', 39)
        """
        start_link = page.find('<a href=')

        if start_link == -1:
            return None, 0
        start_quote = page.find('"', start_link)
        end_quote = page.find('"', start_quote + 1)
        url = page[start_quote+1 : end_quote]

        return url, end_quote

    # get all links from the page.
    # for manual parsing of page.
    def get_all_links(self, page):
        """ (str) -> list of str

        returns list of links extracted from page.

        >>> find_all_links('</span><a href="http://yify-torrents.com/browse-movie/0/All/All/0/latest/2">2</a><a href="http://yify-torrents.com/browse-movie/0/All/All/0/latest/3">3</a><a href="http://yify-torrents.com/browse-movie/0/All/All/0/latest/4">4</a>')
        http://yify-torrents.com/browse-movie/0/All/All/0/latest/2
        http://yify-torrents.com/browse-movie/0/All/All/0/latest/3
        http://yify-torrents.com/browse-movie/0/All/All/0/latest/4
        
        >>> find_all_links('4</a><a href="http://yify-torrents.com/browse-movie/0/All/All/0/latest/5">5</a></span><a href="http://yify-torrents.com/browse-movie/0/All/All/0/latest/2">Next &raquo;</a><a href="http://yify-torrents.com/browse-movie/0/All/All/0/latest/166"><div class="browse-img">')
        http://yify-torrents.com/browse-movie/0/All/All/0/latest/5
        http://yify-torrents.com/browse-movie/0/All/All/0/latest/2
        http://yify-torrents.com/browse-movie/0/All/All/0/latest/166
        """
        links = []
        while True:
                link, end_pos = self.next_link(page)
                if link:
                    links.append(link)
                    page = page[end_pos:]
                else:
                    return links

    # helper member function to combine two lists into one
    def union(self, list1, list2):
        """ (list, list) -> list

             return the union of two lists.

             >>> union([1, 2, 3], [2, 3, 4])
             [1, 2, 3, 4]
             >>> union([a, b, c], [c, d, e])
             [a, b, c, d, e]
             >>> union([1, 2, 3], [4, 5, 6])
             [1, 2, 3, 4, 5, 6]
        """
        for link in list2:
            if link not in list1:
                list1.append(link)
        return list1

    # function crawl web
    def crawl_web(self):
        """ (str) -> None

             return the list of links from after crawling the seed page.

             >>> crawl_web("http://www.gmail.com")
             ['http://www.gmail.com', 'http://www.google.com/support/accounts?hl=en', 'https://accounts.google.com/TOS?loc=IN&hl=en']
             >>> crawl_web("http://www.torrentz.eu/")
             ['http://www.torrentz.eu/', 'http://torrentz-proxy.com/', 'https://torrentz.in/', 'https://torrentz.me/', 'https://torrentz.eu/']
        """
        while self.tocrawl:
            crawl_link = self.tocrawl.pop()
            if crawl_link not in self.crawled:
                try:
                    soup = self.get_page_data(crawl_link)
                    for link in soup.find_all('a'):
                        self.tocrawl.add(link.get('href'))
                    print(crawl_link)
                    self.crawled.append(crawl_link)
                except:
                    pass

    # Get data on a given page.
    def get_page_data(self, link):
        """ (str) -> str

        returns the page data after extracting it.
        """
        
        req = urllib.request.urlopen(link)
        page = str(req.read())
        soup = BeautifulSoup(page)
        return soup    

    # get all crawled links
    def get_links(self):
        return self.crawled

    # print all crawled links
    def __str__(self):
        print ("Crawled links are: ")
        for link in self.crawled:
            print (link)

link = input("Enter the link to be crawled : ")
w = webcrawler(link)
