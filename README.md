# Telugu GPT-2

This project is a comprehensive pipeline for training a GPT-2 model for the Telugu language. The process involves scraping data from various sources, cleaning and preparing the data, training a custom tokenizer, and finally, training the GPT-2 model itself. This could be adapted to fit any new language as long as data is prepared properly. Dataset used to train the small model was 832.95 MB. This is barely anything and it will be expanded in the future to use HuggingFace's public datasets. 

## Project Overview

The project is structured into the following key stages:

1.  **Data Scraping:** Data is collected from multiple sources to create a diverse and comprehensive dataset for training the language model.
2.  **Data Cleaning and Preparation:** The scraped data is cleaned and preprocessed to make it suitable for training.
3.  **Tokenizer Training:** A custom Byte-Level BPE (Byte-Pair Encoding) tokenizer is trained on the cleaned data.
4.  **GPT-2 Model Training:** The GPT-2 model is trained from scratch using the custom tokenizer and the prepared dataset.

## 1. Data Scraping

The data scraping process is designed to gather a large corpus of Telugu text from various online sources. The project includes scrapers for the following:

*   **Eenadu News:** A sophisticated scraper is used to collect news articles from the Eenadu website. This scraper is designed to be robust and avoid detection by using:
    *   **Proxy Rotation:** It uses a list of proxies to make requests from different IP addresses.
    *   **Random User-Agents:** It rotates user-agents to mimic different browsers.
*   **TeluguOne Books:** A scraper is included to download books from the TeluguOne Grandalayam. You can also access the source download [here](https://drive.google.com/file/d/1MDiP-_S2RtAN7c9TLnKi8I2pxIgONIP0/view). This was not created from me, but from another source. DO NOT TRUST IT TO BE CLEAN.
*   **Andhrajyothy News:** Another scraper is used to fetch news articles from the Andhrajyothy website. You can access a scraped source [here](https://drive.google.com/file/d/1IbqM335M7imzG-2ZV0d8-JbRqCnyAii3/view). This was not created from me, but from another source. DO NOT TRUST IT TO BE CLEAN. Scraper me now be outdated, will maybe push an update later.
*   **Future datasets:** You can pull datasets from [hugging face's dataset page](https://huggingface.co/datasets) and use ```load_dataset()``` function to add it. 

The scrapers are located in the `scrapers` directory. The `eenadu` scraper, in particular, is a good example of a well-designed and resilient web scraper.

### Frameworks and Libraries

The scraping process primarily utilizes the following Python libraries:

*   `requests`: For making HTTP requests to the websites.
*   `BeautifulSoup4`: for parsing HTML and extracting data.
*   `PyYAML`: For managing configuration settings.
*   `fake-useragent`: To generate random user-agent strings.

## 2. Data Cleaning and Preparation

Once the data is scraped, it needs to be cleaned and prepared for training. The `scrapers/clean.py` and `scrapers/utf8_join.py` scripts are used for this purpose. These scripts perform tasks such as:

*   Removing HTML tags and other non-textual elements.
*   Normalizing the text.
*   Joining the cleaned text from different sources into a single file.

## 3. Tokenizer Training

A custom tokenizer is needed for this language model, as it defines the vocabulary and because GPT2's tokenizer was built for the English language. Since the model has most likely never seen a charachter of Telugu before, it is important to use our own tokenizer to understand the charachters. This project uses a Byte-Level BPE tokenizer.

The `tokenizer.py` script is responsible for training the tokenizer. It uses the `tokenizers` library from Hugging Face to train the tokenizer on the cleaned dataset. The trained tokenizer is then saved to the `telugu-gpt2-tokenizer` directory.

## 4. GPT-2 Model Training

The core of the project is the training of the GPT-2 model. The `tuner.py` script handles this process. It uses the `transformers` library from Hugging Face to:

*   **Configure the Model:** A `GPT2Config` object is created to define the architecture of the model, including the vocabulary size, number of layers, and other hyperparameters.
*   **Load the Dataset:** The cleaned and tokenized dataset is loaded using the `datasets` library.
*   **Train the Model:** The `Trainer` class is used to train the model on the prepared dataset. The training process is configured with various parameters, such as the batch size, learning rate, and number of epochs.
*   **Save the Model:** The trained model is saved to the `telugu-gpt2-small` directory, along with the tokenizer and configuration files.
*   **WANDB Progress:** Use WandB to track your model progress.

## How to Run

To run this project, you would typically follow these steps:

1.  **Install Dependencies:** Install the required libraries from the `requirements.txt` files in the scraper directories.
2.  **Scrape Data:** Run the scraper scripts to collect the data or collect data from your own sources.
3.  **Clean Data:** Run the cleaning scripts to prepare the data for training.
4.  **Train Tokenizer:** Run the `tokenizer.py` script to train the custom tokenizer.
5.  **Train Model:** Run the `tuner.py` script to train the GPT-2 model.

## Results

The model, in its current state, shows some promise but is not yet capable of generating coherent and meaningful text. The generated text, when prompted with "తెలుగు భాషలో పురాణాలు" (Puranas in Telugu language), is mostly a collection of disconnected words and phrases. This is likely due to the small size of the training dataset (832.95 MB). While the model has learned some vocabulary and basic sentence structure, it lacks the deeper understanding of the language needed to generate high-quality text. The output shows that the model can produce Telugu characters and some words, but it fails to form grammatically correct or contextually relevant sentences. Increasing the size and diversity of the training data is the most critical next step to improve the model's performance. However, this presents a significant challenge as the current model was trained on a single 4060 Ti GPU and took 68 hours and 38 minutes of compute time. Scaling the data further will necessitate more powerful computing resources for the training to be feasible.

## Conclusion

This project demonstrates a complete pipeline for building a language model for a low-resource language like Telugu. It covers all the essential steps, from data collection to model training, and utilizes modern and powerful libraries to achieve this. The resulting model can be used for various NLP tasks, such as text generation, translation, and sentiment analysis.
