import os
import requests
from random import randint
import re
from bs4 import BeautifulSoup


class PicSaver:
    """
    Class PicSaver download last or random pic from https://xkcd.com
    """

    def __init__(self, homedir=(os.getcwd()+'/')):
        self.SoupError = None
        self.default_url = "https://xkcd.com"
        self.url = self.default_url
        self.plate = homedir
        self.pname = ''
        self.pling = ''

    def make_soup(self):
        try:
            response = requests.get(self.url).text
        except:
            print('Problem with airstatic or atmoshere')
            self.SoupError = True
        else:
            self.soup = BeautifulSoup(response, "lxml")

    def soup_take_home(self):
        if self.plink and self.pname:
            data = requests.get(self.plink)
            if data.status_code == 200:
                with open(self.plate+self.pname+".png", "wb") as f:
                    f.write(data.content)

    def eat_soup(self):
        node = self.soup.find(id="comic")
        self.plink = node.find("img")["src"].replace('//', 'https://')
        self.pname = node.find("img")["alt"]

    def find_ing(self):
        self.make_soup()
        if not self.SoupError:
            sort_ing = self.soup.find('div', id="middleContainer").text
            pattern = r"{}/(\d+)".format(self.default_url)
            s = int(re.search(pattern, sort_ing).group(1))
            num = randint(1, s)
            self.url = self.default_url+"/"+str(num)
            self.heat_soup()

    def heat_soup(self):
        self.make_soup()
        if not self.SoupError:
            self.eat_soup()
            self.soup_take_home()
            print('Soup with name: "{}" served.'.format(self.pname))

    def soup_day(self):
        self.url = self.default_url
        self.heat_soup()


if __name__ == "__main__":
    r = PicSaver()
    while True:
        d = input('What are you prefer: soup of day, or something'
                  + ' interesting? [1:2]: ')
        if d == '2':
            r.find_ing()
            break
        elif d == '1':
            r.soup_day()
            break
        else:
            print('NO spam')
