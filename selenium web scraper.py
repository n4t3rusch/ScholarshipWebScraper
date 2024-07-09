#selenium web scraper initialization
import tkinter as tk
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#holds the body of the code most functionality is found in this class
class scraper:
    def __init__(self, expected_amount: int, deadline: str, xGender: int, xStudyLocation: int, xLiveLocation: int, xLevel: int, xAward: int,
                award_passto: str, gender_passto:str, level_passto: str, study_passto: str, live_passto: str, results_widget):
        #final resting place of scholarship info
        self.results_widget = results_widget

        #driver initialization
        self.s = Service('C:/Users/natha/OneDrive/Documents/vscode/AlgsFinal-Project/chromedriver.exe')
        self.driver = webdriver.Chrome(service = self.s)
        self.driver.get("https://www.careeronestop.org/toolkit/training/find-scholarships.aspx")
        
        #defines used for checking length of fields 
        self.INTYPE_SIZE = self.getLength("//*[@id='collapseAwardType']/li")
        self.AWARD_TYPE_SIZE = self.getLength("//*[@id='collapseLevelofStudy']/li")
        self.INGEN_SIZE = self.getLength("//*[@id='collapseGenderSpecific']/li")
        self.KEYWORD_LENGTH = 20 #MAX AMOUNT OF CHARACTERS WE HAVE ALOTED
        self.NUM_STUDY_LOCATIONS = self.getLength("//*[@id='collapseWhereYouWillStudy']/li")
        self.NUM_LIVE_LOCATIONS = self.getLength("//*[@id='collapseWhereYouLive']/li")
        
        #Provided by user to help rate scholarships based off of their deadlines
        self.EXPECTED_AMOUNT = expected_amount
        self.DEADLINE = deadline

        #used for rating of scholarships
        self.RETLEVEL = 0
        self.RETAWARD = 0
        self.RETGENDER = 0
        self.RETLOCATION = 0
        
        #provided by user to rate the different aspects of scholarships 
        self.impGender = xGender
        self.impStudyLocation = xStudyLocation
        self.impLiveLocation = xLiveLocation
        self.impLevel = xLevel
        self.impAward = xAward
       
       #helper dictionary to translate strings to their numeric counterparts
        self.month_to_number = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12
        }

        self.ratings={(self.LevelofStudy2, level_passto):xLevel, 
                    (self.getAwardType2, award_passto):xAward, 
                    (self.getGender2, gender_passto):xGender, 
                    (self.getStudyLocation2, study_passto):xStudyLocation, 
                    (self.getLiveLocation2, live_passto):xLiveLocation
     }

        #dictionary to allow for calculation of month differences
        self.numDeadline = self.month_to_number.get(deadline.lower(), 12)  # Default to December if not found
        
        #final array to hold all scholarships
        self.scholarships = [] 

    #runs functions based on user rating 
    def dynamicExecution(self):
        for (method, param), rating in sorted(self.ratings.items(), key=lambda item: item[1], reverse=True):
            method(param)
        return
    
    #parses levels of study to get correct level of study
    def LevelofStudy2(self, instudy: str):
        count = 1
        UL_XPATH = "//*[@id='collapseLevelofStudy']"
        try:
            UL_elements = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, UL_XPATH))
            )
        #UL_elements = self.driver.find_element(By.XPATH, UL_XPATH)
        except: 
            self.RETLEVEL -= self.impLevel
            return
        
        li_elements = UL_elements.find_elements(By.TAG_NAME, 'li')
        for element in li_elements:
            if instudy in element.text:
                input_xpath = f"//*[@id='collapseLevelofStudy']/li[{count}]/a"
                break
            else:
                count += 1  
        try: 
            raw = self.driver.find_element(By.XPATH, input_xpath)
            raw.click()
            self.RETLEVEL += self.impLevel
        except:
            self.RETLEVEL -= self.impLevel
        return
    
    #parses award types to get correct award type
    def getAwardType2(self, awardType: str):
        count = 1
        UL_XPATH = "//*[@id='collapseAwardType']"
        try:
            UL_elements = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, UL_XPATH))
            )
        except:
            self.RETAWARD -= self.impAward
            return
        
        li_elements = UL_elements.find_elements(By.TAG_NAME, 'li')
        for element in li_elements:
            if awardType in element.text:
                input_xpath = f"//*[@id='collapseAwardType']/li[{count}]/a"
                break
            else:
                count += 1 
        try: 
            raw = self.driver.find_element(By.XPATH, input_xpath)
            raw.click()
            self.RETAWARD += self.impAward
        except:
            self.RETAWARD -= self.impAward
        return
     
    #gets correct gender by parsing 
    def getGender2(self, inGen: str):
        count = 1
        UL_XPATH = "//*[@id='collapseGenderSpecific']"
        try:
            UL_elements = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, UL_XPATH))
            )
            #UL_elements = self.driver.find_element(By.XPATH, UL_XPATH)
        except:
            self.RETGENDER -= self.impGender
            return
        
        li_elements = UL_elements.find_elements(By.TAG_NAME, 'li')
        for element in li_elements:
            print(element.text)
            if inGen in element.text:
                input_xpath = f"//*[@id='collapseGenderSpecific']/li[{count}]/a"
                break
            else:
                count += 1 
        try: 
            raw = self.driver.find_element(By.XPATH, input_xpath)
            raw.click()
            self.RETGENDER += self.impGender
        except:
            self.RETGENDER -= self.impGender
        return

    #enters users preferred keyword
    def enterKeyword(self, keyword: str): 
        if(len(keyword) < self.KEYWORD_LENGTH):
            entry_XPATH = '//*[@id="SFInputbox"]'
            box = self.driver.find_element(By.XPATH, entry_XPATH)
            button = self.driver.find_element(By.XPATH, '//*[@id="btnDynamicSearch"]')
            box.send_keys(keyword)
            button.click()
        return

    #gets correct live location based off parsing
    def getLiveLocation2(self, location: str):
        try:
            but_xpath = '//*[@id="WhereYouLive-more"]/a'
            button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, but_xpath)))
            #button = self.driver.find_element(By.XPATH, but_xpath)
            button.click()
        except:
            pass
        
        UL_XPATH = '//*[@id="collapseWhereYouLive"]'
        try:
            UL_elements = self.driver.find_element(By.XPATH, UL_XPATH)
        except:
            self.RETLOCATION -= self.impLiveLocation
            return    
        
        count = 1
        li_elements = UL_elements.find_elements(By.TAG_NAME, 'li')
        for element in li_elements:
            if location in element.text:
                locationxpath = f"//*[@id='collapseWhereYouLive']/li[{count}]/a"
                raw = self.driver.find_element(By.XPATH, locationxpath)
                break
            else:
                count += 1 
        try: 
            raw.click()
            self.RETLOCATION += self.impLiveLocation
        except:
            self.RETLOCATION -= self.impLiveLocation
        return
    
    #parses for correct study location
    def getStudyLocation2(self, location: str):
        try:
            but_xpath = '//*[@id="WhereYouWillStudy-more"]/a'
            button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, but_xpath)))
            button.click()
        except:
            pass

        UL_XPATH = '//*[@id="collapseWhereYouWillStudy"]'
        try:
            UL_elements = self.driver.find_element(By.XPATH, UL_XPATH)
        except:
            self.RETLOCATION -= self.impStudyLocation
            return    
        count = 1
        li_elements = UL_elements.find_elements(By.TAG_NAME, 'li')
        for element in li_elements:
            if location in element.text:
                locationxpath = f"//*[@id='collapseWhereYouWillStudy']/li[{count}]/a"
                raw = self.driver.find_element(By.XPATH, locationxpath)
                break
            else:
                count += 1 
        try: 
            raw.click()
            self.RETLOCATION += self.impStudyLocation
        except:
            self.RETLOCATION -= self.impStudyLocation
        return
    
    #parses scholarships and saves them to scholarship element
    def parseScholarships(self):
        tr_elements = self.driver.find_elements(By.TAG_NAME, 'tr')

        for tr in tr_elements[1:]: 
            td_elements = tr.find_elements(By.TAG_NAME, 'td')
            name = td_elements[0].text
            level = td_elements[1].text
            type = td_elements[2].text
            amount = td_elements[3].text
            deadline = td_elements[4].text
            self.scholarships.append(scholarship(name, level, type, amount, deadline))

        self.rateScholarships()
        return
    
    #calculates difference between expected month and actual month of Deadline
    def calculateDifference(self, expected: int, actual: str):
        intExpected = self.month_to_number.get(expected.lower(), 12)
        intACTUAL = self.month_to_number.get(actual.lower(), 12)
        return (intACTUAL - intExpected)
    
    #rates scholarships based on previous specified catagories if they ran or not
    def rateScholarships(self):
        for scholarship in self.scholarships: 
            final = 0 

            diff = self.calculateDifference(self.DEADLINE, scholarship.DEADLINE)

            try:
                cleaned_amount = scholarship.AMOUNT.replace('$', '').replace(',', '')
                amount = int(float(cleaned_amount))
                if(self.EXPECTED_AMOUNT == amount):
                    final += 3
                else:
                    final -= 3
            except:
                final -= 3
                pass

            final = self.RETAWARD + self.RETGENDER + self.RETLEVEL + self.RETLOCATION + diff
            if(final < 0):
                final = 1
            scholarship.score = final

        self.sortScholarships()
    
    #wrapper for mergesort 
    def sortScholarships(self): 
        self.mergeSort(self.scholarships, 0, len(self.scholarships) - 1)

    #sorts the entire scholarships list based of their different scores
    def merge(self, arr, l, m, r):
    
        L = arr[l:m+1]
        R = arr[m+1:r+1]

        i = 0  # Initial index of first subarray
        j = 0  # Initial index of second subarray
        k = l  # Initial index of to be sorted subarray

        while i < len(L) and j < len(R):
            if L[i].score >= R[j].score:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

    def mergeSort(self, arr, l, r):
        if l < r:
            m = l + (r - l) // 2  
            self.mergeSort(arr, l, m)
            self.mergeSort(arr, m + 1, r)
            self.merge(arr, l, m, r)
    
    #helper to get length of field
    def getLength(self, XPATH):
        elements = self.driver.find_elements(By.XPATH, XPATH)
        return len(elements)
    
    #kills scraper
    def close(self):
        self.driver.close()

    #returns final url of scraper
    def getURL(self):
        print(self.driver.current_url)
    
    #helper to print scholarship items
    def print(self): 
        for scholarships in self.scholarships:
            info = (f'NAME AND INFO: {scholarships.NAME}\n'
                    f'LEVEL: {scholarships.LEVEL}\n'
                    f'TYPE: {scholarships.TYPE}\n'
                    f'AMOUNT: {scholarships.AMOUNT}\n'
                    f'DEADLINE: {scholarships.DEADLINE}\n'
                    f'SCORE: {scholarships.score}\n\n')
            self.results_widget.insert(tk.END, info)

#objects that will be places in the scholarship array
class scholarship:
    def __init__(self, name: str, level: str, type: str, amount: str, deadline: str):
        self.NAME = name
        self.LEVEL = level
        self.TYPE = type
        self.AMOUNT = amount
        self.DEADLINE = deadline
        self.score = 0

#Function from which all the gui calls are put into the scraper instance
def run(): 
    #sets up scraper init
    scraperinst = scraper(amount_entry.get(), 
                      deadline_entry.get(), 
                      int(gender_rank_var.get()), 
                      int(college_location_rank_var.get()), 
                      int(location_rank_var.get()),
                      int(study_rank_var.get()),
                      int(award_rank_var.get()),
                      str(award_var.get()),
                      str(gender_var.get()),
                      str(study_var.get()),
                      str(college_location_var.get()),
                      str(location_var.get()),
                      results_text)
    
    #Runs scraper functions
    scraperinst.enterKeyword(keyword_entry.get())
    scraperinst.dynamicExecution()
    scraperinst.parseScholarships()
    scraperinst.print()
    #print(scraperinst.getURL())
    scraperinst.close()
    return 

# Create main window
root = tk.Tk()
root.title("Scholarship Selector")

# Window size
window_width = 500
window_height = 500

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate position
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

# Set the position of the window to the center of the screen
root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

# Location section
location_label = tk.Label(root, text="Where you live:")
location_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
location_var = tk.StringVar()
location_menu = tk.OptionMenu(root, location_var, "US", "International", "Hawaii", "Ohio",
                              "California", "West Virginia", "Michigan", "Vermont", "Texas", "Washington",
                              "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
                              "Alaska", "Nebraska", "Florida", "Minnesota", "North Carolina", "Oregon",
                              "Idaho", "Pennsylvania", "Connecticut", "Virginia", "Illinois", "Montana",
                              "Alabama", "New Jersey", "Massachusettes", "Wisconsin", "Indiana",
                              "Maine", "Maryland", "New Mexico", "New York", "Rhode Island", "Tennesee",
                              "Nevada", "Georgia", "Puerto Rico", "Arizona", "Kentucky", "District of Columbia", "New Hampshire",
                              "Arkansas", "Delaware", "Louisiana", "South Carolina", "Colorado", "Iowa", "Missouri", "Kansas", "Mississippi",
                              "South Dakota", "Oklahoma", "North Dakota", "Utah", "Wyoming", "Guam")
location_menu.grid(row=0, column=1, padx=5, pady=5,sticky='w')

location_rank_label = tk.Label(root, text="Rank (1-5):")
location_rank_label.grid(row=0, column=2, padx=5, pady=5)
location_rank_var = tk.StringVar()
location_rank_menu = tk.OptionMenu(root, location_rank_var, "1", "2", "3", "4", "5")
location_rank_menu.grid(row=0, column=3, padx=5, pady=5)

# College Location section
college_location_label = tk.Label(root, text="College Location:")
college_location_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
college_location_var = tk.StringVar()
college_location_menu = tk.OptionMenu(root, college_location_var, "US", "International", "California", "Ohio",
                              "Michigan", "Alaska", "Florida", "Texas", "Hawaii", "Alabama"
                              "Idaho", "New York", "Massachusetts", "Virginia", "North Carolina", "Wisconsin",
                              "Tennesee", "Pennsylvania", "Washington", "Iowa", "Illinois", "Minnesota",
                              "Georgia", "West Virginia", "Nebraska", "New Jersey", "District of Columbia",
                              "Oregon", "Indiana", "Puerto Rico", "Kentucky", "Kansas",
                              "Nevada", "South Carolina", "Colorado", "Connecticut", "Maryland", "Louisiana",
                              "Arizona", "Rhode Island", "Maine", "Montana", "New Mexico", "Missouri", "New Hampshire",
                              "North Dakota", "Arkansas", "Mississippi", "Oklahoma", "Vermont", "South Dakota", 
                              "Wyoming", "Delaware", "Utah","Guam")


college_location_menu.grid(row=1, column=1, padx=5, pady=5, sticky='w')

college_location_rank_label = tk.Label(root, text="Rank (1-5):")
college_location_rank_label.grid(row=1, column=2, padx=5, pady=5)
college_location_rank_var = tk.StringVar()
college_location_rank_menu = tk.OptionMenu(root, college_location_rank_var, "1", "2", "3", "4", "5")
college_location_rank_menu.grid(row=1, column=3, padx=5, pady=5)

# Gender section
gender_label = tk.Label(root, text="Gender:")
gender_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
gender_var = tk.StringVar()
gender_menu = tk.OptionMenu(root, gender_var, "Male", "Female")
gender_menu.grid(row=2, column=1, padx=5, pady=5, sticky='w')

gender_rank_label = tk.Label(root, text="Rank (1-5):")
gender_rank_label.grid(row=2, column=2, padx=5, pady=5)
gender_rank_var = tk.StringVar()
gender_rank_menu = tk.OptionMenu(root, gender_rank_var, "1", "2", "3", "4", "5")
gender_rank_menu.grid(row=2, column=3, padx=5, pady=5)

# Level of Study section
study_label = tk.Label(root, text="Level of Study:")
study_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
study_var = tk.StringVar()
study_menu = tk.OptionMenu(root, study_var,"Bachelor's Degree", "Graduate Degree", "Professional Development", 
                           "Vocational", "Associates Degree", "High School")
study_menu.grid(row=3, column=1, padx=5, pady=5, sticky='w')

study_rank_label = tk.Label(root, text="Rank (1-5):")
study_rank_label.grid(row=3, column=2, padx=5, pady=5)
study_rank_var = tk.StringVar()
study_rank_menu = tk.OptionMenu(root, study_rank_var, "1", "2", "3", "4", "5")
study_rank_menu.grid(row=3, column=3, padx=5, pady=5)

# Award Type section
award_label = tk.Label(root, text="Award Type:")
award_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')
award_var = tk.StringVar()
award_menu = tk.OptionMenu(root, award_var, "Scholarship", "Fellowship", "Grant", "Prize", "Public Grant", "Loan")
award_menu.grid(row=4, column=1, padx=5, pady=5, sticky='w')

award_rank_label = tk.Label(root, text="Rank (1-5):")
award_rank_label.grid(row=4, column=2, padx=5, pady=5)
award_rank_var = tk.StringVar()
award_rank_menu = tk.OptionMenu(root, award_rank_var, "1", "2", "3", "4", "5")
award_rank_menu.grid(row=4, column=3, padx=5, pady=5)

# Deadline section
deadline_label = tk.Label(root, text="Expected Deadline in Month Format:")
deadline_label.grid(row=5, column=0, padx=5, pady=5, sticky='w')
deadline_entry = tk.Entry(root)
deadline_entry.grid(row=5, column=1, columnspan=3, padx=5, pady=5, sticky='w')

#keyword entry
keyword_label = tk.Label(root, text="Enter Keyword Under 20 characters:")
keyword_label.grid(row=7, column=0, padx=5, pady=5, sticky='w')
keyword_entry = tk.Entry(root)
keyword_entry.grid(row=7, column=1, columnspan=3, padx=5, pady=5, sticky='w')

# Desired Amount section
amount_label = tk.Label(root, text="Desired Amount:")
amount_label.grid(row=6, column=0, padx=5, pady=5, sticky='w')
amount_entry = tk.Entry(root)
amount_entry.grid(row=6, column=1, columnspan=3, padx=5, pady=5, sticky='w')

results_text = tk.Text(root, height=10, width=75)
results_text.grid(row=10, column=0, columnspan=7, padx=5, pady=5)

# Submit button
submit_button = tk.Button(root, text="Submit", command=run)
submit_button.grid(row=9, column=0, columnspan=4, padx=5, pady=5)

root.mainloop()