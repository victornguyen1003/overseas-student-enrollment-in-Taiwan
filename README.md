# Overseas Student Enrollment in Taiwan: Data Wrangling & Visualization
This project engineered an automated ETL pipeline that standardizes and visualized a decade of Ministry of Education (MOE) records of overseas student enrollment in Taiwan into a longitudinal database for trend and composition analysis.

## Setup
**Install the required Python libraries:**
```bash
pandas numpy matplotlib seaborn fuzzywuzzy
```
**Place all these files in your project folder:**
- countryTranslation.csv
- config.py
- utils.py
- main.ipynb

## References
Dataset: [政府資訊開放平台](https://data.gov.tw/en/datasets/6289)

Country name Chinese-English translation: [中華民國證券投資信託暨顧問商業同業公會](https://members.sitca.org.tw/OPF/K0000/files/F/01/%E5%9C%8B%E7%A8%85%E5%B1%80%E5%9C%8B%E5%AE%B6%E4%BB%A3%E7%A2%BC%E8%A1%A8%E5%8F%8A%E5%8D%80%E5%9F%9F%E5%B0%8D%E6%87%89%E8%A1%A8.xls)
