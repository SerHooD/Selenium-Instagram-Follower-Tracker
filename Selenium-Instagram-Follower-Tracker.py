from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from PyQt5 import QtWidgets
from _projectForm import Ui_MainWindow
import time
import sys

class  myApp(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(myApp,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btnLogin.clicked.connect(self.handleLogin)

    def handleLogin(self):
        self.ui.lblResult.setText("Loading............................") 
        QtWidgets.QApplication.processEvents()
        username = self.ui.lineUsername.text() 
        password = self.ui.linePassword.text()  
        
        self.user = Instagram(username, password)
        loginStat = self.user.singIn()
        
        if loginStat == 1:
            self.ui.lblResult.setText("Logged in")
        else:
            self.ui.lblResult.setText(loginStat)      
        followerList = self.user.getFollowers()

        if isinstance(followerList, list):
            for follower in followerList:
                self.ui.followerList.addItem(follower.text)
            self.ui.lblResult.setText("Followers fetched.")
            self.user.quit()

        elif followerList == 0:
            self.ui.lblResult.setText("Login Failed. Try Again")
            self.user.quit()  

        else:
            self.ui.lblResult.setText(f"Error fetching followers")
            self.user.quit()
 
class Instagram:
    def __init__(self,username,password):
        self.browser = webdriver.Chrome()
        self.username = username
        self.password = password
        self.wait = WebDriverWait(self.browser, 10)
        

    def singIn(self):

        try:
            self.browser.get("https://www.instagram.com/")
            
            usernameInput = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='loginForm']/div/div[1]/div/label/input")))
            usernameInput.send_keys(self.username)
            
            passwordInput = self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='loginForm']/div/div[2]/div/label/input")))
            passwordInput.send_keys(self.password)
            passwordInput.send_keys(Keys.ENTER)
            
             
            return 1  # Logged in
       
        except Exception as e:
            print("Error:", e)
            return e  # Other errors
        
    def getFollowers(self):
        
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[8]/div/span/div/a/div"))).click()
            self.wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/header/section[3]/ul/li[2]/div/a"))).click()          
            
            jsCommand = """
                page = document.querySelector(".x1rife3k");
                page.scrollTo(0,page.scrollHeight);
                var pageEnd = page.scrollHeight;
                return pageEnd;
                """
            pageEnd = 0
            
            while True:
                last = pageEnd
                time.sleep(1)
                pageEnd = self.browser.execute_script(jsCommand)
                
                if last == pageEnd:
                    followersLst = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div/div/div/div/div/div/div/div/div/div/a/div/div/span")))
                    return followersLst
        
        except:
            return 0
    
    def quit(self):
        self.browser.quit()

app= QtWidgets.QApplication(sys.argv)
win = myApp()
win.show()
sys.exit(app.exec_())
