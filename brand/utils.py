import numpy as np
import threading
from keras.models import load_model
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
# from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service

chars = ['\n', "'", 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
         'u', 'v', 'w', 'x', 'y', 'z', ' ', '_', '-', '.', '/', '&', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
         '+', '(', ')', '>', '<', '%', '`']

char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

maxlen = 33
minlen = 1
max_names = 50

model = load_model('model.h5')
model_suffix = load_model('model_suffix.h5')


def med_count(medlist):
    finallist = []
    s = Service(r"C:\Users\rajag\Desktop\chromedriver.exe")
    driver = webdriver.Chrome(service=s)
    for med in medlist:
        driver.get('https://ipindiaonline.gov.in/tmrpublicsearch/frmmain.aspx')
        wait = WebDriverWait(driver, 10)
        # time.sleep(1)
        # driver.implicitly_wait(10)
        select = Select(driver.find_element('id', 'ContentPlaceHolder1_DDLSearchType'))
        select.select_by_value('PH')
        wordmarkelem = driver.find_element(By.CSS_SELECTOR, "#ContentPlaceHolder1_TBPhonetic")
        classelem = driver.find_element(By.CSS_SELECTOR, "#ContentPlaceHolder1_TBClass")
        searchelem = driver.find_element(By.CSS_SELECTOR, "#ContentPlaceHolder1_BtnSearch")
        wordmarkelem.send_keys(med)
        classelem.send_keys("5")
        searchelem.click()
        # count = driver.find_element(By.CSS_SELECTOR, "#ContentPlaceHolder1_LblSearchDetail > table:nth-child(1) > tbody:nth-child(1) > td:nth-child(1)").text
        count = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                             "#ContentPlaceHolder1_LblSearchDetail > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1)"))).text

        count = count.split(' ')[-1]
        #         print(count)
        if int(count) > 0 and int(count) <= 80:  # range
            finallist.append(med)
    driver.close()
    return (finallist)


def sample(preds):
    """ function that sample an index from a probability array """
    preds = np.asarray(preds).astype('float64')
    preds = preds / np.sum(preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.random.choice(range(len(chars)), p=probas.ravel())


def print_name_generated(name):
    print(name, flush=True)


def print_list_generated(lst):
    print(lst, flush=True)


def generate_new_names(prefix):
    #     print("----------Generating names----------")

    # Add pre-padding of zeros in the input.
    sequence = ('{0:0>' + str(maxlen) + '}').format(prefix).lower()

    # tmp variables
    tmp_generated = prefix
    list_outputs = list()

    while (len(list_outputs) < max_names):

        # Vectorize the input of the model.
        x_pred = np.zeros((1, maxlen, len(chars)))
        for t, char in enumerate(sequence):
            if char != '0':
                x_pred[0, t, char_indices[char]] = 1

        # Predict the probabilities of the next char.
        preds = model.predict(x_pred, verbose=0)[0]

        # Chose one based on the distribution obtained in the output of the model.
        next_index = sample(preds)
        # Get the corresponding char.
        next_char = indices_char[next_index]

        # If the char is a new line character or the name start to be bigger than the longest word,
        # try to add it to the list and reset temp variables.
        if next_char == '\n' or len(tmp_generated) > maxlen:

            # If the name generated is not in the list, append it and print it.
            if tmp_generated not in list_outputs:
                list_outputs.append(tmp_generated)
            #                 print_name_generated(tmp_generated)
            # Reset tmp variables
            sequence = ('{0:0>' + str(maxlen) + '}').format(prefix).lower()
            tmp_generated = prefix
        else:

            # Append the char to the sequence that we're generating.
            tmp_generated += next_char
            # Add pre-padding of zeros to the sequence generated and continue.
            sequence = ('{0:0>' + str(maxlen) + '}').format(tmp_generated).lower()

    #     print("-----------------End-----------------")
    return list_outputs

threads = []


for prefix in ['prefix1', 'prefix2', 'prefix3', 'prefix4', 'prefix5']:
    t = threading.Thread(target=generate_new_names, args=(prefix,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
# Function invoked at the end of each epoch. Prints generated names.
# callback = LambdaCallback(on_epoch_end=generate_new_names)


# # model_instance = Model()
# prefix = "ant" # Change the prefix as one likes
#  # The number of names of na
# l1 = []
# l1 = generate_new_names(prefix)
# final_list = med_count(l1)
