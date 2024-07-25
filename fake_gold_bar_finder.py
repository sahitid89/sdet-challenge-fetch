import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Class to find the fake gold bar among a set of gold bars
class FakeGoldBarFinder:
    def __init__(self):
        # Initialize the Chrome WebDriver and open the target URL
        self.driver = webdriver.Chrome()
        self.driver.get("http://sdetchallenge.fetch.com")
        # Set up WebDriverWait to wait for elements to be present
        self.wait = WebDriverWait(self.driver, 10)

    def reset_scale(self):
        # Locate all elements with the ID "reset" (there are 2 elements with the ID "reset" in the given webpage)
        elements = self.driver.find_elements(By.ID, "reset")
        # Click the second reset button (The second element is the Reset button that we need)
        reset_button = elements[1]
        reset_button.click()

    def weigh(self, left_bars, right_bars):
        # Reset the scale before weighing
        self.reset_scale()

        # Enter the values for the left side of the scale
        for i, bar in enumerate(left_bars):
            self.driver.find_element(By.ID, f"left_{i}").send_keys(str(bar))

        # Enter the values for the right side of the scale
        for i, bar in enumerate(right_bars):
            self.driver.find_element(By.ID, f"right_{i}").send_keys(str(bar))

        # Click the "weigh" button to perform the weighing
        weigh_button = self.driver.find_element(By.ID, "weigh")
        weigh_button.click()
        # Wait for 2 seconds to let the result be processed
        time.sleep(2)

        # Get the result from the scale (which appears in the first reset button element)
        elements = self.driver.find_elements(By.ID, "reset")
        result_element = elements[0]
        result = result_element.text
        return result

    def select_fake_bar(self, fake_bar_number):
        # Click on the element corresponding to the fake bar number
        self.driver.find_element(By.ID, f"coin_{fake_bar_number}").click()
        # Wait for the alert to appear and then retrieve the alert message
        alert = self.wait.until(EC.alert_is_present())
        message = alert.text.strip()
        # Accept the alert
        alert.accept()
        return message

    def find_fake_bar(self):
        # Initialize list of bar numbers as strings from '0' to '8'
        bars = [str(i) for i in range(9)]

        # Recursive function to find the fake bar by dividing and weighing subsets
        def find_fake_bars(subset):
            if len(subset) == 1:
                return subset[0]
            group_size = len(subset)//3

            # Divide the bars into three groups
            group1 = subset[:group_size]
            group2 = subset[group_size:2 * group_size]

            # Weigh the first two groups against each other
            result = self.weigh(group1, group2)

            # Determine which group contains the fake bar based on the result
            if result == '=':
                return find_fake_bars(subset[2 * group_size:])
            elif result == '<':
                return find_fake_bars(group1)
            elif result == '>':
                return find_fake_bars(group2)

        # Find the fake bar and get the result message
        fake_bar = find_fake_bars(bars)
        result_message = self.select_fake_bar(fake_bar)
        weighings = self.driver.find_elements(By.CSS_SELECTOR, 'div.game-info ol li')

        # Print the results
        print(f"Fake Bar Number: {fake_bar}")
        print(f"Alert message: {result_message}")
        print(f"Number of weighing: {len(weighings)}")
        print(f"List of weighing made:")
        for i, item in enumerate(weighings):
            print(f'{i+1}. {item.text}')

    def close(self):
        # Close the browser and end the WebDriver session
        self.driver.quit()


# Create an instance of the FakeGoldBarFinder and execute the find_fake_bar method
finder = FakeGoldBarFinder()
finder.find_fake_bar()
# Close the WebDriver session
finder.close()
