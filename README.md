# python-tableau

This repository contains 3 projects:

1. Article sentiment analysis
2. Loan data analysis
3. Transaction data analysis

The primary goal is to clean each individual dataset and use the cleaned dataset to build a static dashboard in Tableau. The dashboards can be viewed on my Tableau account. Following the link.
(https://public.tableau.com/app/profile/andrew.kitatta/vizzes

See below for more details about the projects

#### Article Sentiment Analysis

This project focuses on analyzing articles from different sources, extracting sentiment information from their titles, and deriving insights from the data. It utilizes the VADER (Valence Aware Dictionary and sEntiment Reasoner) sentiment analysis tool to assess the sentiment polarity of the article titles.

#### Overview

The primary objectives of this project are as follows:

Analyze articles from various sources stored in an Excel file (articles.xlsx).
Determine the number of articles and reactions per publisher/source.
Flag articles containing specific keywords, such as "murder" or "crash."
Assess the sentiment polarity (positive, negative, neutral) of each article title.
Save the cleaned and processed data to an Excel file (blogme_clean.xlsx).

#### Project Structure

main.py: Python script containing the code for data loading, preprocessing, sentiment analysis, and data saving.
README.md: Markdown file providing an overview of the project, instructions for running the code, and additional information.

#### Requirements

Python 3.x
pandas library
vaderSentiment library

### Usage

Clone the repository to your local machine:

git clone https://github.com/your_username/article-sentiment-analysis.git

Navigate to the project directory:

cd article-sentiment-analysis

Install the required dependencies:

pip install pandas vaderSentiment

Place the article data file (articles.xlsx) in the project directory.

Run the blogme.py script:

python blogme.py

After execution, the cleaned and processed data will be saved to blogme_clean.xlsx.


#### Loan Data Analysis

This project focuses on analyzing loan data stored in JSON format, processing it using pandas, and performing various data exploration and visualization tasks.

#### Overview

The main objectives of this project are as follows:

Read loan data from a JSON file (loan_data_json.json).
Convert the JSON data into a pandas DataFrame for analysis.
Explore the loan data, including descriptive statistics and data visualization.
Categorize FICO scores and interest rates.
Create visualizations, such as bar plots and scatter plots, to understand the data better.
Save the cleaned and processed data to a CSV file (loan_cleaned.csv).

#### Project Structure

main.py: Python script containing the code for data loading, preprocessing, analysis, and visualization.
README.md: Markdown file providing an overview of the project, instructions for running the code, and additional information.

#### Requirements

Python 3.x
pandas library
numpy library
matplotlib library

#### Usage

Clone the repository to your local machine:

git clone https://github.com/your_username/loan-data-analysis.git

Navigate to the project directory:

cd loan-data-analysis

Install the required dependencies:

pip install pandas numpy matplotlib

Place the loan data file (loan_data_json.json) in the project directory.

Run the bluebank.py script:

python bluebank.py

After execution, the cleaned and processed data will be saved to loan_cleaned.csv.


#### Transaction Data Analysis

This project involves the analysis of transaction data stored in a CSV file (transaction.csv). The data preprocessing and analysis tasks are performed using the pandas library in Python.

#### Overview

The main objectives of this project are as follows:
1.	Load the transaction data from the CSV file and preprocess it.
2.	Calculate additional metrics such as cost per transaction, sales per transaction, profit per transaction, and markup.
3.	Combine and merge datasets to enrich the transaction data with additional information.
4.	Export the cleaned and processed data to a new CSV file (ValueInc_cleaned.csv).

#### Project Structure

•	main.py: Python script containing the code for data loading, preprocessing, analysis, and export.
•	transaction.csv: CSV file containing the raw transaction data.
•	value_inc_seasons.csv: CSV file containing additional data about seasons.
•	ValueInc_cleaned.csv: CSV file containing the cleaned and processed transaction data.
•	README.md: Markdown file providing an overview of the project, instructions for running the code, and additional information.

#### Requirements

•	Python 3.x
•	pandas library

#### Usage
1.	Clone the repository to your local machine:

git clone https://github.com/your_username/transaction-data-analysis.git

2.	Navigate to the project directory:

cd transaction-data-analysis

3.	Install the required dependencies:

pip install pandas

4.	Place the transaction data file (transaction.csv) and additional data file (value_inc_seasons.csv) in the project directory.
   
5.	Run the valueinc_sales.py script:

python valueinc_sales.py 

9.	After execution, the cleaned and processed data will be saved to ValueInc_cleaned.csv.

