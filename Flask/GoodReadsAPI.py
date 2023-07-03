from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from pyvirtualdisplay import Display
display = Display(visible=0, size=(1920, 1080))
display.start()
app = Flask(__name__)
@app.route('/execute_selenium_code', methods=['POST'])
def execute_selenium_code():
    try:
        # Get the email and password from the request's JSON payload
        url = request.json.get('url')
        
        
        # Set up the Selenium driver
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--profile-directory=Default')
        chrome_options.add_argument('--user-data-dir=~/.config/google-chrome')
        driver = webdriver.Chrome(options=chrome_options)
        driver.delete_all_cookies()
        driver.maximize_window()
        action = ActionChains(driver)
        action = webdriver.ActionChains(driver)  # You may need to adjust the driver path based on your system configuration
        #print("here")
        y=0
        df = pd.DataFrame()
        
            
        driver.get(url)
        time.sleep(15)
        
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,"//button[@aria-label='Close']"))).click()
            #driver.find_element(By.XPATH,"//button[@aria-label='Close']").click()
        except Exception as e:
            try:
                driver.find_element(By.XPATH,"//button[@aria-label='Close']").click()
            except Exception as e:
                pass
            pass
        try:
            review_button=driver.find_element(By.XPATH,"//a[contains(@href,'reviews?')]")
            #action.move_to_element(review_button).click().perform()
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", review_button)

            time.sleep(5)
            review_button.click()
            time.sleep(5)
        except Exception as e:
            try:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", review_button)
                time.sleep(5)
                review_button.click()
                time.sleep(5)
            except Exception as e:
                pass
            pass
        count=0
        while count<3:
            cards=driver.find_elements(By.XPATH,"//article[@class='ReviewCard']")
            for card in cards:
                try:
                    name = card.find_element(By.XPATH, ".//div[@data-testid='name']").text
                    url = card.find_element(By.XPATH, ".//div[@data-testid='name']//a").get_attribute('href')
                    df.at[y,"Name"]=name
                    df.at[y,"ProfileURL"]=url
                    
                except Exception as e:
                    pass
                try:
                    rating = card.find_element(By.XPATH, ".//span[contains(@aria-label,'Rating')]").get_attribute('aria-label')
                    df.at[y,"Rating"]=rating  # Add rating to the set
                except Exception as e:
                    pass
                try:
                    review = card.find_element(By.XPATH, ".//div[@data-testid='contentContainer']").text
                    df.at[y,"Review"]=review  # Add review to the set
                except Exception as e:
                    pass
                try:
                    date = card.find_element(By.XPATH, ".//span[@class='Text Text__body3']").text
                    df.at[y,"Date"]=date  # Add date to the set
                except Exception as e:
                    pass
                y=y+1
            try:  
                more=driver.find_element(By.XPATH,"//button[contains(.,'more reviews')]")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", more)
                time.sleep(2)
                print("CLicking more button")
                more.click()
            except Exception as e:
                try:
                    driver.find_element(By.XPATH,"//button[@aria-label='Close']").click()
                except Exception as e:
                    pass
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", more)
                    more.click()
                except Exception as e:
                    pass
                pass
            count=count+1
            time.sleep(5)
        

        # Display the dataframe
        df=df.drop_duplicates(subset=["ProfileURL"])
        df.to_csv("Review-test.csv")    
        return df.to_json(orient="records"), 200, 

    except Exception as e:
        # Return an error message if there was an exception
        print(e)
        response = {'message': 'Error executing Selenium code: {}'.format(str(e))}
        return jsonify(response), 500

    finally:
        # Quit the Selenium driver after execution
        driver.quit()
        display.stop()
        pass

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0', port=5000)
