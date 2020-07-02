from selenium import webdriver
from bs4 import BeautifulSoup
import time
import datetime
import json

class Publication():
    def publication(self, url_publication):
        self.publication_url = url_publication


class Credentials():
    def credentials(self, username, password):
        self.username = username
        self.password = password


class InstagramBoot(Credentials, Publication):
    def __init__(self):
        self.friends = []

        option = webdriver.ChromeOptions()
        option.add_argument('lang=pt-br')

    def getFriends(self):

        # access profile
        time.sleep(8)
        profileBox = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/a/img')
        profileBox.click()

        # access friend's list
        time.sleep(4)
        followingBox = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a')
        followingBox.click()

        # scroll friend's list
        value = 500
        for i in range(25):
            value += 60000
            jsScript1 = f"element = document.getElementsByClassName('isgrP');element[0].scroll(10,{value});"
            self.driver.execute_script(jsScript1)
            time.sleep(1)

        # get friends
        html_source = self.driver.page_source
        soup_html = BeautifulSoup(html_source, 'html.parser')
        tagA_href = soup_html.find_all("a", {"class": "FPmhX notranslate _0imsa"})
        for tag_a in tagA_href:
            href_splited = tag_a['href'].split("/")
            self.friends.append(href_splited[1])

    def accessInstragram(self):
        self.driver = webdriver.Chrome(executable_path=r'./chromedriver')
        self.driver.get('https://www.instagram.com/')

        self.start_time = datetime.datetime.utcnow()

        time.sleep(3)
        userBox = self.driver.find_element_by_name('username')
        time.sleep(1)
        userBox.click()
        userBox.send_keys(self.username)

        passBox = self.driver.find_element_by_name('password')
        time.sleep(1)
        passBox.click()
        passBox.send_keys(self.password)

        time.sleep(1)
        loginBox = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[4]/button')
        loginBox.click()

        time.sleep(5)

    def create_publication(self, type, comment_text=None, range_number=None):
        time.sleep(3)
        self.driver.get(self.publication_url)
        count_errors_total = 0
        count_errors_followed = 0
        count_success = 0

        if type == "friend_list":
            for friend in self.friends:
                time.sleep(3)
                commentElement = self.driver.find_element_by_class_name('Ypffh')
                commentElement.click()

                commentElement2 = self.driver.find_element_by_class_name('Ypffh')
                commentElement2.send_keys(friend)

                buttonSubmitElement = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/section[3]/div/form/button')
                buttonSubmitElement.click()
                time.sleep(5)

        if type == "only_comment":
            if comment_text != None:
                for i in range(10000):
                    try:
                        time.sleep(3)
                        commentElement = self.driver.find_element_by_class_name('Ypffh')
                        commentElement.click()

                        commentElement2 = self.driver.find_element_by_class_name('Ypffh')
                        commentElement2.send_keys(comment_text)

                        buttonSubmitElement = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/section[3]/div/form/button')
                        buttonSubmitElement.click()
                        time.sleep(10)

                        count_errors_followed = 0
                        count_success += 1

                        end_time = datetime.datetime.utcnow()
                        div_time = end_time - self.start_time
                        print(f"SUCESSO - {div_time}: Registrados {count_success} comentários bem sucedidos")
                    except:
                        count_errors_total += 1
                        count_errors_followed += 1
                        end_time = datetime.datetime.utcnow()
                        div_time = end_time - self.start_time

                        if count_errors_followed >= 3:
                            print(f"ERRO - {div_time} : Registrados {count_errors_followed} erros seguidos e {count_errors_total} bloqueios totais. Aguardando 300 segundos")
                            time.sleep(300)
                        else:
                            print(f"ERRO - {div_time} : Registrados {count_errors_followed} erros seguidos e {count_errors_total} bloqueios totais. Aguardando 60 segundos")
                            time.sleep(60)
                        try:
                            self.driver.get(self.publication_url)
                        except:
                            print("ERRO 001 VERIFICAR")


if __name__ == '__main__':
    #get credentials
    with open('credencials.json', 'r') as json_file:
        json_data = json.loads(json_file.read())
        username = json_data['username']
        password = json_data['password']

    instagramBot = InstagramBoot()

    instagramBot.credentials(username, password)
    instagramBot.accessInstragram()

    # get friend's list?
    #instagramBot.getFriends()

    instagramBot.publication('https://www.instagram.com/p/CBeXwX5Dt5_/')
    instagramBot.create_publication(type="only_comment", comment_text="Here have a comment!", range_number=10000)
