import undetected_chromedriver as uc
import pandas as pd
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

class GoogleReviewBot:
    
    def __init__(self,mailaddress,password,comment):
        self.mailaddress = mailaddress
        self.password = password
        self.comment = comment
        self.completedAccounts = open("./data/completedAccounts.csv","a")
        self.initialize()

    def initialize(self):
        self.i = 0
        PlaceURL = "https://www.google.com/search?q=empire+state+building&biw=1920&bih=841&tbm=lcl&sxsrf=AOaemvKtJq3ct8p65NL3BUMpvXtXXWJ2Ww%3A1641592752932&ei=sLfYYZmvONiRxc8PwLqiiA8&oq=empire+state&gs_l=psy-ab.1.1.35i39k1j0i433i67k1j0i512k1l7j0i67k1.63774.65241.0.67175.12.10.0.0.0.0.384.1764.0j1j5j1.7.0....0...1c.1.64.psy-ab..5.7.1764...0i512i433k1j0i512i433i131k1j0i512i457k1.0.-OO0zl_w5LU#lrd=0x89c259a9b3117469:0xd134e199a405a163,3,,,&rlfi=hd:;si:15074921902713971043,l,ChVlbXBpcmUgc3RhdGUgYnVpbGRpbmdIn6MFWicQAhgAGAEYAiIVZW1waXJlIHN0YXRlIGJ1aWxkaW5nKgIIAjICZW6SARJ0b3VyaXN0X2F0dHJhY3Rpb24,y,IYrXyp60Thk;mv:[[40.74862047731903,-73.98542683213199],[40.74826052268097,-73.98590196786799]]" #ENTER YOUR LINK HERE
        self.driver = uc.Chrome()
        self.driver.delete_all_cookies()
        self.urls = ["https://accounts.google.com/signin/v2/identifier?hl=tr&passive=true&continue=https%3A%2F%2Fwww.google.com%2Fsearch%3Fq%3Dgoogle%26oq%3Dgoogle%26aqs%3Dchrome.0.69i59l3j0i271l2j69i60j69i65j69i60.706j0j1%26sourceid%3Dchrome%26ie%3DUTF-8&ec=GAZAAQ&flowName=GlifWebSignIn&flowEntry=ServiceLogin",PlaceURL]
        self.driver.get(self.urls[self.i])
        
    def _login(self):
        try:
            login=self.driver.find_element(By.ID,"identifierId")
            login.send_keys(self.mailaddress)
            button1 = self.driver.find_element(By.ID,("identifierNext"))
            sleep(1)
            button1.click()
            sleep(1)
            password=self.driver.find_element(By.NAME,("password")) 
            password.send_keys(self.password)
            sleep(1)
            button2= self.driver.find_element(By.ID,"passwordNext")
            button2.click()
            sleep(3)
        except:
            print("There is a problem in LogIn.")
            pass
         
    def _comment(self):
        try:
            self.i +=1
            self.driver.get(self.urls[self.i])        
            sleep(3)
            WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"/html/body/div[18]/iframe")))
            self.driver.find_element(By.XPATH,("/html/body/div[1]/c-wiz/div/div/div/div/div[1]/div[3]/div[2]/div[3]/div[1]/textarea")).send_keys("Comment")
            elem=WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#yDmH0d > c-wiz > div > div > div > div > div.O51MUd > div.l5dc7b > div.DTDhxc.eqAW0b > div.euWHWd.aUVumf > div > div:nth-child(5)")))
            self.driver.execute_script("arguments[0].click();", elem)
            sleep(1)
            button = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#ZRGZAf > span")))
            button.click()
            sleep(1)
            self.completedAccounts.write(self.mailaddress + "-" + self.password + "\n")
            self.driver.close()
        except:
            print("There is a problem in Comment.")
            pass

    @staticmethod
    def GetUserInfo(mailaddressFile,passwordsFile,commentsFile):
        get_MailAdresses=pd.read_csv(mailaddressFile).sample(frac=1,random_state=0)
        get_Passwords=pd.read_csv(passwordsFile).sample(frac=1,random_state=0)
        get_Comments=pd.read_csv(commentsFile).sample(frac=1,random_state=0)
        num = min(len(get_MailAdresses),len(get_Passwords),len(get_Comments))
        UserInfo= get_MailAdresses
        UserInfo["mailaddress"] = get_MailAdresses.values
        UserInfo["password"] = get_Passwords.values
        UserInfo["comment"] = get_Comments.values
        UserInfo.index = range(num)
        return UserInfo
    
    
if __name__ == "__main__":
    mailaddressFile = "./data/mailaddresses.csv"
    passwordsFile = "./data/passwords.csv"
    commentsFile = "./data/comments.csv"
    UserInfoDF = GoogleReviewBot.GetUserInfo(mailaddressFile, passwordsFile,commentsFile)
    for num in range(len(UserInfoDF)):
        UserInfoSeries = UserInfoDF.loc[num]
        GRB = GoogleReviewBot(*UserInfoSeries)
        try:
            GRB._login()
            GRB._comment()
        except:
            print("There is a problem.")
            pass
