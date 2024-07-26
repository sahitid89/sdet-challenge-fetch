# Documentation for 'fake_gold_bar_finder' Python Script

## Overview
This Python script automates a web-based challenge to identify a fake gold bar from a set of 9 bars. All the bars weigh the same except for the fake bar which weighs less than the others. The script uses Selenium, a web automation tool, to interact with a web application where the challenge is hosted.

## Prerequisites
### Software Requirements
1. **Python**: Ensure you have Python installed on your machine. You can download it from the official Python website.

2. **Web Browser**: The script uses Google Chrome for browser automation. Download and install Google Chrome.

3. **ChromeDriver**: Selenium requires a WebDriver to interface with the browser. For Chrome, download ChromeDriver that matches your version of Chrome.

### Python Libraries
The script requires the selenium library. To install it, open your terminal or command prompt and run:
```
pip install selenium
```

## Code Explanation
### Imports

```
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
```

- **time**: Provides time-related functions.
+ **webdriver** from **selenium**: Allows interaction with web browsers.
* **By**: Provides various strategies to locate elements on a webpage.
- **WebDriverWait** and **expected_conditions as EC**: Used for waiting until certain conditions are met.


### Class Definition: FakeGoldBarFinder
#### Constructor: __init__()

```
def __init__(self):
    self.driver = webdriver.Chrome()
    self.driver.get("http://sdetchallenge.fetch.com")
    self.wait = WebDriverWait(self.driver, 10)
```

+ Initializes a new instance of the Chrome browser with the specified path to ChromeDriver.
- Navigates to the challenge URL (http://sdetchallenge.fetch.com).
* Sets up a WebDriverWait to handle waiting for elements or conditions.

Note: In the above code snippet, if **self.driver = webdriver.Chrome()** doesn't work due to restricted environment or vpn settings, you will have to download ChromeDriver that matches your version of Chrome. Replace self.driver = webdriver.Chrome() with below code. Replace '/path/to/chromedriver' with the actual path where you saved the ChromeDriver executable.
  ```
  self.driver = webdriver.Chrome(executable_path='/path/to/chromedriver')
  ```

#### Method: reset_scale()
```
def reset_scale(self):
    elements = self.driver.find_elements(By.ID, "reset")
    reset_button = elements[1]
    reset_button.click()
```

Locates and clicks the "reset" button to prepare the scale for weighing.

#### Method: weigh(left_bars, right_bars)

```
def weigh(self, left_bars, right_bars):
    self.reset_scale()

    for i, bar in enumerate(left_bars):
        self.driver.find_element(By.ID, f"left_{i}").send_keys(str(bar))

    for i, bar in enumerate(right_bars):
        self.driver.find_element(By.ID, f"right_{i}").send_keys(str(bar))

    weigh_button = self.driver.find_element(By.ID, "weigh")
    weigh_button.click()
    time.sleep(2)

    elements = self.driver.find_elements(By.ID, "reset")
    result_element = elements[0]
    result = result_element.text
    return result
```

+ Resets the scale and inputs the bars to be weighed.
- Clicks the "weigh" button and waits for the result.
* Returns the result of the weighing operation (<, =, or >).

#### Method: select_fake_bar(fake_bar_number)

```
def select_fake_bar(self, fake_bar_number):
    self.driver.find_element(By.ID, f"coin_{fake_bar_number}").click()
    alert = self.wait.until(EC.alert_is_present())
    message = alert.text.strip()
    alert.accept()
    return message
```

+ Clicks on the bar identified as fake and confirms the result through an alert box.
- Returns the alert message.

#### Method: find_fake_bar()

```
def find_fake_bar(self):
    bars = [str(i) for i in range(9)]

    def find_fake_bars(subset):
        if len(subset) == 1:
            return subset[0]
        group_size = len(subset)//3

        group1 = subset[:group_size]
        group2 = subset[group_size:2 * group_size]

        result = self.weigh(group1, group2)

        if result == '=':
            return find_fake_bars(subset[2 * group_size:])
        elif result == '<':
            return find_fake_bars(group1)
        elif result == '>':
            return find_fake_bars(group2)

    fake_bar = find_fake_bars(bars)
    result_message = self.select_fake_bar(fake_bar)
    weighings = self.driver.find_elements(By.CSS_SELECTOR, 'div.game-info ol li')
    print(f"Fake Bar Number: {fake_bar}")
    print(f"Alert message: {result_message}")
    print(f"Number of weighing: {len(weighings)}")
    print(f"List of weighing made:")
    for i, item in enumerate(weighings):
        print(f'{i+1}. {item.text}')

```

+ Uses a recursive approach to determine which bar is fake based on the weighing results.
  Divide the bars into three groups of three bars each. Weigh two groups against each other. If they balance, the fake bar is in the third group. If they don't balance, the lighter side contains the fake bar. Divide the remaining group of three bars into three single bars. Weigh two bars against each other. If they balance, the fake bar is the one not weighed. If they don't balance, the lighter bar is the fake one.
+ Selects the identified fake bar and retrieves the result.
+ Prints the results including the fake bar number, alert message, number of weighings, and details of each weighing.

#### Method: close()
```
def close(self):
    self.driver.quit()
```

+ Closes the browser and ends the Selenium session.

### Execution
To run the script, save it to a file named fake_gold_bar_finder.py and run using python3
```
python3 fake_gold_bar_finder.py
```







