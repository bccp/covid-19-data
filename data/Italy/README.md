# Official Covid-19 data from the Italian "Protezione Civile"

This is official data updated daily from the Italian Civil Protection Agency, the government agency that deals with the prediction, prevention and management of emergency events, and which is coordinating Italy's response.

The original data can be found at
https://github.com/pcm-dpc/COVID-19

Italy is devided in 20 administrative regions, and 109 provinces.  Aggregate data for the whole nation, as well as by region or province is provided. The .tvs files provide the following columns of daily data:

Column Header | Format / meaning
------------ | -------------
Date | YYYY-MM-DDTT18:00:00
State | always Italy
ICU | number admitted to ICU
total_hospitalized	| total Covid-19 related hospitalized
home_isolation | people in home confinment	 
positive | Total amount of current positive cases (Hospitalised patients + Home confinement)
positiveIncrease | News amount of current positive cases (Actual total amount of current positive cases - total amount of current positive cases of the previous day)	
recovered | (cumulative) total recovered	
death | (cumulative) total deaths
total_cases	| (cumulative) total Covid-19 cases
swabs | (cumulative) total tests
notes | notes
