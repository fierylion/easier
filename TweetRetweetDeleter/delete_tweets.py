#Inspiration from kalebu

import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import logging
class DeleteTweets:
    def __init__(self, username, password, from_tweet_message):
        self.username = username
        self.password = password  # for security you can use os.getenv method
        self.message = from_tweet_message # tweet message that the program should start deleting from
        self.driver = webdriver.Chrome()
        self.website = 'https://www.twitter.com/login'
        logging.basicConfig(level=logging.INFO)
        self.driver.implicitly_wait(10)
        self.main()





    def deleteTweet(self, tweet):
        # passed as a verified tweet only
        tweet.find_element(By.CSS_SELECTOR, 'div[aria-label="More"]').click()
        # select delete from more menu
        self.driver.find_element(By.CSS_SELECTOR, '#layers div[role="menuitem"]').click()
        # confirm the delete
        self.driver.find_element(By.CSS_SELECTOR, '#layers div[data-testid="confirmationSheetConfirm"').click()
        logging.info('Element Deleted Successfully')

    def deleteRetweet(self, retweet):
        # passed a verified retweet
        # click unretweet
        retweet.find_element(By.CSS_SELECTOR, 'div[data-testid="unretweet"]').click()
        # confirm retweet
        self.driver.find_element(By.CSS_SELECTOR, 'div[data-testid="unretweetConfirm"]').click()
        logging.info('Retweet Deleted')

    def isRetweet(self, post):
        regex = re.compile(r'You Retweeted')
        return True if (regex.search(post.text)) else False

    def moveToWantedTweet(self):
        while True:
            try:
                # ele = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"] *:contains("an irony.")')
                divs = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"]')
                ele = None
                found = False
                for div in divs:
                    if self.message in div.text: # check if the message is in specific tweet
                        ele = div
                        found = True
                        break
                if not found:
                    raise NoSuchElementException
                self.driver.execute_script('arguments[0].setAttribute("data-mark", "")', ele)
                ele = self.driver.find_element(By.CSS_SELECTOR, "[data-mark]")
                self.driver.execute_script('arguments[0].scrollIntoView(true);', ele)
                logging.info('Target element marked')
                return '[data-mark]'
            except NoSuchElementException:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)  #move to next tweet

    def main(self):
        self.driver.get(self.website)
        self.driver.find_element(By.CSS_SELECTOR, 'input[name="text"]').send_keys(self.username)
        # click next
        buttons = self.driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
        next_button = None
        for button in buttons:
            if "Next" in button.text:
                next_button = button
                break
        if next_button:
            next_button.click()
        else:
            logging.info("Next button not found")

        # enter password
        self.driver.find_element(By.CSS_SELECTOR, 'input[autocomplete="current-password"]').send_keys(self.password)
        # click next
        buttons = self.driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
        next_button = None
        for button in buttons:
            if "Log in" in button.text:
                next_button = button
                break
        if next_button:
            next_button.click()
        else:
            logging.info("Log in button not found")
        time.sleep(3)
        # go to profile
        self.driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Profile"]').click()
        time.sleep(5)
        # find elements under
        tweetUnder = self.moveToWantedTweet()
        while True:
            tweets = self.driver.find_elements(By.CSS_SELECTOR, f'{tweetUnder}+div[data-testid="cellInnerDiv"]')

            time.sleep(2)
            for tweet in tweets:
                if (tweet.text == ""):
                    self.driver.execute_script('arguments[0].remove()', tweet)
                    continue
                if (self.isRetweet(tweet)):
                    self.deleteRetweet(tweet)
                    logging.info('retweet deleted')
                    time.sleep(1)
                else:
                    try:
                        self.deleteTweet(tweet)
                        logging.info('Tweet deleted')
                    except:
                        logging.info('Not a tweet')
                    time.sleep(1)


program = DeleteTweets('daniel_mawalla', '*{1601}*#', 'This is')