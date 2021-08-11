# Author : Nijatullah Mansoor
# Date: 08/11/2021


# Step1: import required library
from selenium import webdriver
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
# import Action chains
from selenium.webdriver.common.action_chains import ActionChains


# Step2: define function
def parse_product_review(product_url, num_of_review, path):
    start = time.time()
    # initializing the chromedriver
    driver = webdriver.Chrome(executable_path=path)
    driver.maximize_window()
    # setting the URL
    driver.get(product_url)

    # getting the main window handle id (some of the code below is used to close the unwanted popups)
    Main_Window = driver.current_window_handle

    # giving some time so that all elements are loaded
    time.sleep(5)

    # getting all the open window handle id's to close additional popups that are appearing
    popup_windows = driver.window_handles

    # looping through all the open  windows and closing ones that are not needed
    for winId in popup_windows:
        if winId != Main_Window:
            driver.switch_to.window(winId)
            driver.close()

    # switching to the main window
    driver.switch_to.window(Main_Window)

    # giving some time so that all elements are loaded
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="customer-reviews-header"]/div[2]/div/div[3]/a[2]/span').click()

    time.sleep(5)
    s = Select(driver.find_element_by_xpath(
        "/html/body/div[1]/div/div/div/div[1]/div/div[5]/div/div[2]/div/div[2]/div/div[2]/select"))
    s.select_by_index(2)  # this is to sort the element by most recent first we have that in index[2] position

    # getting the current url which has a specific format which will be used later
    get_url = driver.current_url

    # defining empty lists to store the parsed values

    review_date = []
    reviewer_name = []
    review_title = []
    review_description = []
    rating_given_by_user = []

    # this is where we start parsing
    for i in range(1, int(num_of_review / 20) + 1):

        # printing the number of parsed pages.
        print("Page {} of {}".format(i, int(num_of_review / 20)))

        tile_date = "November 30, 2020"  # we want review data till December of 2020 we don't before that
        if tile_date in review_date:
            break
        # forming the new url with the help which we defined earlier
        url = get_url + '&page=' + str(i)

        # opening the url
        driver.get(url)
        # giving some time so that all elements are loaded
        time.sleep(5)

        # getting product listing details
        product_review = driver.find_elements_by_class_name("Grid.ReviewList-content")

        # looping through all the product review listings we have found in the above line of code.
        for element in product_review:
            # getting the date from the review
            try:
                date = element.find_element_by_class_name("review-date-submissionTime").text
                review_date.append(date)
            except:
                review_date.append(None)

            # getting reviewver name
            try:
                name = element.find_element_by_class_name("review-footer-userNickname").text
                reviewer_name.append(name)
            except:
                reviewer_name.append(None)

            # Getting the review title
            try:
                title = element.find_element_by_class_name("review-title.font-bold").text
                review_title.append(title)
            except:
                review_title.append(None)
            # getting the review body or description
            try:
                description = element.find_element_by_class_name("review-text").text
                review_description.append(description)
            except:
                review_description.append(None)

            # getting he user rating of the product
            try:
                rating = element.find_element_by_class_name("visuallyhidden.seo-avg-rating").text
                rating_given_by_user.append(rating)
            except:
                rating_given_by_user.append(None)

    # initializing empty dataframe
    df = pd.DataFrame()

    # assigning values to dataframe columns

    df['Date'] = review_date
    df['Cutomer name'] = reviewer_name
    df['Review Title'] = review_title
    df['Review Description'] = review_description
    df['User rating'] = rating_given_by_user

    # the require time to complete the process
    end = time.time()
    print("Time Taken to Parse {} product review is:{} seconds".format(num_of_review, (end - start)))

    # quitting the driver (browser)
    driver.quit()

    # returning the data frame formed
    return df


# Let's call our function
path = r'C:\Users\nijat\Desktop\Data Science\Preparation For Interview\Technicl Skil\web Scraping\Chromedriver'
product_url = "https://www.walmart.com/ip/Clorox-Disinfecting-Wipes-225-Count-Value-Pack-Crisp-Lemon-and-Fresh-Scent-3-Pack-75-Count-Each/14898365"

dataframe = parse_product_review(product_url, 1500, path)
dataframe.to_csv("output.csv", index=False)
