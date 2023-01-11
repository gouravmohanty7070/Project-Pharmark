# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense
# from tensorflow.keras.layers import LSTM
from keras.layers import (
    LSTM,
    Dense,
    Dropout,
    Sequential,
)
from tensorflow import keras
import pandas as pd
import numpy as np

def get_name_of_country_and_make_data(country:str) -> pd.DataFrame:
    df = pd.read_csv("brand_name.csv")
    names = list(df["Country"].drop_duplicates())

    # TODO: check if this is working
    country = country
    country = country.upper()
    try:
        if country not in names:
            raise Exception
    except:
        country = "INDIA"
        print("Invalid country name so changed to INDIA by default")
    df_train = df[df["Country"] == country]["Drug name"]
    df_train = df_train.drop_duplicates()
    return df_train

def make_prefix_model_and_save(country:str):
    chars = [
        "\n",
        "'",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        " ",
        "_",
        "-",
        ".",
        "/",
        "&",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "0",
        "+",
        "(",
        ")",
        ">",
        "<",
        "%",
        "`",
    ]

    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))

    col_one_list = get_name_of_country_and_make_data(country=country).tolist()
    col_one_list = [i.lower() for i in col_one_list]
    col_one_list = [i.split(" ") for i in col_one_list]
    col_one_list = [i[0] for i in col_one_list]
    col_one_list = set(col_one_list)

    lines = col_one_list
    lines = [line for line in lines if len(line)!=0]

    maxlen = len(max(lines, key=len)) + 30
    minlen = len(min(lines, key=len))

    steps = 1
    sequences = []
    next_chars = []

    for line in lines:
        # pre-padding with zeros
        s = (maxlen - len(line))*'0' + line
        sequences.append(s)
        next_chars.append('\n')
        for it,j in enumerate(line):
            if (it >= len(line)-1):
                continue
            s = (maxlen - len(line[:-1-it]))*'0' + line[:-1-it]
            sequences.append(s)
            next_chars.append(line[-1-it])

    # Vectorization
    x = np.zeros((len(sequences), maxlen, len(chars)), dtype=np.bool)
    y = np.zeros((len(sequences), len(chars)), dtype=np.bool)
    for i, seq in enumerate(sequences):
        for t, char in enumerate(seq):
            if char != '0':
                x[i, t, char_indices[char]] = 1
        y[i, char_indices[next_chars[i]]] = 1

    # model 
    model = Sequential()
    model.add(LSTM(64, input_shape=(maxlen, len(chars))))
    model.add(Dropout(0.3))
    model.add(Dense(len(chars), activation='softmax'))
    opt = keras.optimizers.Adam(learning_rate=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=opt)
    model.fit(x, y, batch_size=128, epochs=10, verbose=2)

    model.save(f'model_prefix_{country}.h5')
    print('Model saved')

def return_model(data,country):
    if (data=="prefix"):
        make_prefix_model_and_save(country=country)
    else:
        make_suffix_model_and_save(country=country)

# For Suffix 
def make_suffix_model_and_save(country:str):
    chars = [
        "\n",
        "'",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        " ",
        "_",
        "-",
        ".",
        "/",
        "&",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "0",
        "+",
        "(",
        ")",
        ">",
        "<",
        "%",
        "`",
    ]

    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))

    col_one_list = get_name_of_country_and_make_data(country=country).tolist()
    col_one_list = [i.lower() for i in col_one_list]
    col_one_list = [i.split(" ") for i in col_one_list]
    col_one_list = [i[0] for i in col_one_list]
    col_one_list = set(col_one_list)

    lines = col_one_list
    lines = [line for line in lines if len(line)!=0]

    maxlen = len(max(lines, key=len)) + 30
    minlen = len(min(lines, key=len))

    steps = 1
    sequences = []
    next_chars = []
        
    # Reverse the text
    lines = [line[::-1] for line in lines]

    # Print the reversed names generated splited
    def print_name_generated(name):
        print(name[::-1], flush=True)
    def print_list_generated(lst):
        print([l[::-1] for l in lst], flush=True)


    steps = 1
    sequences = []
    next_chars = []

    for line in lines:
        # pre-padding with zeros
        s = (maxlen - len(line))*'0' + line
        sequences.append(s)
        next_chars.append('\n')
        for it,j in enumerate(line):
            if (it >= len(line)-1):
                continue
            s = (maxlen - len(line[:-1-it]))*'0' + line[:-1-it]
            sequences.append(s)
            next_chars.append(line[-1-it])
            
    x = np.zeros((len(sequences), maxlen, len(chars)), dtype=np.bool)
    y = np.zeros((len(sequences), len(chars)), dtype=np.bool)
    for i, seq in enumerate(sequences):
        for t, char in enumerate(seq):
            if char != '0':
                x[i, t, char_indices[char]] = 1
        y[i, char_indices[next_chars[i]]] = 1

    prefix = ""
    max_names = 10
        
    model = Sequential()
    model.add(LSTM(64, input_shape=(maxlen, len(chars))))
    model.add(Dense(len(chars), activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr=0.01))
    history = model.fit(x, y, batch_size=128, epochs=10, verbose=2, callbacks=[callback])

    # Insert a suffix of your business name (could be empty):
    suffix = "don"
    # Insert how many names you'd like to generate:
    max_names = 10

    # This reverse the prefix 
    prefix = suffix[::-1]
    # generate_new_names()
    # later, it will be reversed again in the print function

    model.save(f'model_prefix_{country}.h5')
    print('Model saved')