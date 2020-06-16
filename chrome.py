from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import re
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory

class Bot:

    course = "INFO3435"
    def __init__(self,field,other):
        
        print(repr(other["dpath"]))
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {
        "download.default_directory": repr(other["dpath"]), #Change default directory for downloads
        "download.prompt_for_download": False, #To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
        })

        self.username = field["username"].get() 
        self.passw = field["passw"].get()
        self.course = field["course"].get() 
        
        self.bot = webdriver.Chrome(executable_path='D:\Jordan_Williams\Chrome download\chromedriver_win32\chromedriver.exe',options=options)
    
    def search(self):
        bot = self.bot
      
        bot.get('https://ourvle.mona.uwi.edu/?') 
        username = bot.find_element_by_xpath("//input[@name='username']")
        password = bot.find_element_by_xpath("//input[@name='password']")
        submit = bot.find_element_by_xpath("//button[@type='submit']")
        username.send_keys(self.username)
        password.send_keys(self.passw)
        submit.click()



        cancel = bot.find_element_by_xpath("//input[@value='Cancel']")
        cancel.click()

# find_element_by_css_selector
        coursebox = bot.find_elements_by_class_name("coursebox")
        for i in coursebox:
            el = i.find_element_by_css_selector("h3.coursename")
            if re.search(self.course, el.text, re.IGNORECASE):
                el.click()
                html = bot.page_source
                soup = BeautifulSoup(html,"html.parser")
                divs = soup.findAll(class_="activityinstance")
                
                for div in divs:
                    # bot.get(div.a["href"])
                    
                    if div.select("span.resourcelinkdetails"):
                        href = div.a["href"]
                        bot.get(href)
                        # print(href)

                
                break
        
            # print(el.text)

        # print(coursebox)


        print(a)




window = Tk()
window.title("Welcome to TutorialsPoint")

window.configure(background = "grey");
a = Label(window ,text = "username").grid(row = 0,column = 0)
b = Label(window ,text = "password").grid(row = 1,column = 0)
c = Label(window ,text = "course code").grid(row = 3,column = 0)
d = Label(window ,text = "choose directory to download files").grid(row = 4,column = 0)


entries = {}
other = {}
other["dpath"]=""

a1 = Entry(window,width=32)
a1.grid(row = 0,column = 1)
entries["username"] = a1

b1 = Entry(window,width=32,show="*")
b1.grid(row = 1,column = 1)
entries["passw"] = b1

c1 = Entry(window,width=32)
c1.insert(0,"comp1126")
c1.grid(row = 3,column = 1)
entries["course"] = c1


def clicked(field,other):
    field_texts = list(map(lambda x: x.get(),list(entries.values()))) + list(other.values())
    if all(field_texts):
        print("valid")
        automate = Bot(field,other) 
        automate.search()

    print("invalid")
    print(a)

def downloadf():
    other["dpath"] = askdirectory()

download = ttk.Button(window ,text="choose directory for downloaded files",command=(downloadf))
download.grid(row=4,column = 1)

btn = ttk.Button(window ,text="Submit",command=(lambda field=entries: clicked(field,other))).grid(row=5,column=0)
window.mainloop()


