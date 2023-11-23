from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FFService
from selenium.webdriver.common.by import By
import threading
import sys
import time


def try_to_agree(driver):
    try:
        btn = driver.find_element(By.CLASS_NAME, 'flag-new-messages')
        agree = btn.find_element(By.CLASS_NAME, 'button-room.agree')
        agree.click()
    except selenium.common.exceptions.NoSuchElementException:
        print("Can't agree, probably already did")

def vote_opt(driver, opt):

    polls = driver.find_elements(By.CLASS_NAME, 'thread-swipe')

    poll = polls[0]

    options = poll.find_elements(By.CLASS_NAME, 'row-label')

    opt_labels = [opt.find_element(By.TAG_NAME, "p").text for opt in options]

    if opt in opt_labels:
        ind = opt_labels.index(opt)
        options[ind].click()
        time.sleep(2)


def vote(id, target, opt):

    try:
        print(f"Thread {id} starting", flush=True)

        options = FirefoxOptions()
        service = FFService('/snap/bin/geckodriver')
        options.add_argument("-private")
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options, service=service)

        driver.get(target)

        try_to_agree(driver)

        try:
            vote_opt(driver, opt)
            print(f"Thread {id} voted!")
        except Exception as e:
            print(f"Thread {index} couldn't vote: ", e)

    finally:
        driver.quit()
        print(f"Thread {id} : browser closed", flush=True)

nb_args = 3
if len(sys.argv) != nb_args+1:
    print(f"Got {len(sys.argv) - 1} arguments, expected {nb_args - 1}")
    print("Usage: python3 bot.py <target> <opt> <nb_threads>")
    exit(1)

target = str(sys.argv[1])
opt = str(sys.argv[2])
nb_threads = int(sys.argv[3])

threads = list()
for index in range(nb_threads):
    x = threading.Thread(target=vote, args=(index, target, opt))
    threads.append(x)
    x.start()

for index, thread in enumerate(threads):
    thread.join()