import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def countries(list_of_countries):
    for itr in list(list_of_countries):
        print(itr)


def all_countries(list_of_countries):
    return list(list_of_countries)


def maximum_infection(county):
    print(filtered_covid_data.loc[county].diff().max())


# Initializing the dataset
covid_data_csv = pd.read_csv("Datasets/covid19_Confirmed_dataset.csv")   # Importing the csv dataset
# print(covid_data_csv.head())          # print the first 5 values of dataset (default)
# print(covid_data_csv.shape)           # Describe the shape of the data set

covid_data_csv.drop(["Lat", "Long", "Province/State"], axis=1, inplace=True)     # Removing the useless columns inplace
# print(covid_data_csv.head())          # print the first 5 values of dataset (default)
# print(covid_data_csv.shape)           # Describe the shape of the data set

filtered_covid_data = covid_data_csv.groupby("Country/Region").sum()       # Grouping the dataset according to countries
# print(filtered_covid_data.head())          # print the first 5 values of dataset (default)
# print(filtered_covid_data.shape)           # Describe the shape of the data set

# countries(filtered_covid_data.index)            # Print all the countries


plt.figure(figsize=(12, 6))


# Plot the graph of the Total covid cases vs Date
plt.subplot(1, 2, 1)
filtered_covid_data.loc["India"].plot()                 # India
filtered_covid_data.loc["China"].plot()                 # China
filtered_covid_data.loc["United Kingdom"].plot()        # United Kingdom
plt.ylabel("Total cases")
plt.xlabel("Date")

plt.legend()

# Plot the graph of the Cases of covid per day vs Date
plt.subplot(1, 2, 2)
filtered_covid_data.loc["India"].diff().plot()              # India
filtered_covid_data.loc["China"].diff().plot()              # China
filtered_covid_data.loc["United Kingdom"].diff().plot()     # United Kingdom
plt.ylabel("Cases per day")
plt.xlabel("Date")

plt.legend()
plt.show()

# Maximum recorded cases on single date
# maximum_infection("India")
# maximum_infection("China")
# maximum_infection("United Kingdom")

# Adding a column : maximum number recorded on single date
Countries = all_countries(filtered_covid_data.index)
max_infection_rate = []
for i in Countries:
    max_infection_rate.append(filtered_covid_data.loc[i].diff().max())

filtered_covid_data["max_infection_rate"] = max_infection_rate

# print(filtered_covid_data.head())
# print(filtered_covid_data.shape)

# Creating a new data table with only maximum number recorded on single date column

covid_data = pd.DataFrame(filtered_covid_data["max_infection_rate"])
# print(covid_data.head())
# print(covid_data.shape)

# Working with the World Happiness Report, Manipulating the data according to owr need

whr_data_csv = pd.read_csv("Datasets/worldwide_happiness_report.csv")
# print(whr_data_csv.head())
# print(whr_data_csv.shape)

# Removing useless columns
whr_data_csv.drop(["Overall rank", "Score", "Generosity", "Perceptions of corruption"], axis=1, inplace=True)
# print(whr_data_csv.head())
# print(whr_data_csv.shape)

whr_data_csv.set_index("Country or region", inplace=True)
# print(whr_data_csv.head())
# print(whr_data_csv.shape)

# Joining both the data into single data using join

joined_data = covid_data.join(whr_data_csv, how="inner")
# print(final_data.head())
# print(final_data.shape)

# Importing the data of deaths due to covid19
death_data_csv = pd.read_csv("Datasets/covid19_deaths_dataset.csv")
# print(death_data_csv.head())
# print(death_data_csv.shape)

# Filtering the data

death_data_csv.drop(["Lat", "Long", "Province/State"], axis=1, inplace=True)         # Removing useless columns
# print(death_data_csv.head())
# print(death_data_csv.shape)

filtered_death_data = death_data_csv.groupby("Country/Region").sum()        # Grouping data according to countries
# print(filtered_data_csv.head())
# print(filtered_data_csv.shape)

# Plotting Graphs

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
filtered_death_data.loc["India"].plot()                 # India
filtered_death_data.loc["China"].plot()                 # China
filtered_death_data.loc["United Kingdom"].plot()        # United Kingdom
plt.title("Total Deaths vs Date")
plt.legend()

plt.subplot(1, 2, 2)
filtered_death_data.loc["India"].diff().plot()              # India
filtered_death_data.loc["China"].diff().plot()              # China
filtered_death_data.loc["United Kingdom"].diff().plot()     # United Kingdom
plt.title("Deaths vs Date")
plt.legend()

plt.show()

# Adding max_death_rate column in the joined_data
max_death_rate = []
for i in Countries:
    max_death_rate.append(filtered_death_data.loc[i].diff().max())

filtered_death_data["max_death_rate"] = max_death_rate
# print(filtered_death_data.head())
# print(filtered_death_data.shape)

#  Creating a new data table with only column : maximum death recorded on single date
covid_death = pd.DataFrame(filtered_death_data["max_death_rate"])
# print(covid_death.head())

# Joining the data together
final_data = covid_death.join(joined_data, how="inner")
# print(final_data.head())
# print(final_data.shape)

# Evaluating the relationship between each parameter of the data set
correlation_matrix = final_data.corr()          # Gives the correlation matrix
sns.heatmap(final_data.corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)    # Visualize Correlation matrix
plt.title('Correlation Matrix')
plt.show()


# Data Relation Visualization
plt.figure(figsize=(16, 8))

# Plotting GDP vs Maximum infection rate
plt.subplot(2, 2, 1)
plt.title("GDP per capita vs Maximum infection rate")
x = final_data["GDP per capita"]
y = final_data["max_infection_rate"]
sns.scatterplot(x=x, y=np.log(y))
sns.regplot(x=x, y=np.log(y))

# Plotting Social support vs Maximum infection rate
plt.subplot(2, 2, 2)
plt.title("Social support vs Maximum infection rate")
x = final_data["Social support"]
y = final_data["max_infection_rate"]
sns.scatterplot(x=x, y=np.log(y))
sns.regplot(x=x, y=np.log(y))

# Plotting Healthy life expectancy vs Maximum infection rate
plt.subplot(2, 2, 3)
plt.title("Healthy life expectancy vs Maximum infection rate")
x = final_data["Healthy life expectancy"]
y = final_data["max_infection_rate"]
sns.scatterplot(x=x, y=np.log(y))
sns.regplot(x=x, y=np.log(y))

# Plotting Freedom to make life choices vs Maximum infection rate
plt.subplot(2, 2, 4)
plt.title("Freedom to make life choices vs Maximum infection rate")
x = final_data["Freedom to make life choices"]
y = final_data["max_infection_rate"]
sns.scatterplot(x=x, y=np.log(y))
sns.regplot(x=x, y=np.log(y))

plt.tight_layout()
plt.show()

# Data Relation Visualization
plt.figure(figsize=(16, 8))

# Plotting GDP vs Maximum infection rate
plt.subplot(2, 2, 1)
plt.title("GDP per capita vs Maximum Death rate")
x = final_data["GDP per capita"]
y = final_data["max_death_rate"]
sns.scatterplot(x=x, y=np.log(y))
sns.regplot(x=x, y=y)

# Plotting Social support vs Maximum infection rate
plt.subplot(2, 2, 2)
plt.title("Social support vs Maximum Death rate")
x = final_data["Social support"]
y = final_data["max_death_rate"]
sns.scatterplot(x=x, y=np.log(y))
sns.regplot(x=x, y=y)

# Plotting Healthy life expectancy vs Maximum infection rate
plt.subplot(2, 2, 3)
plt.title("Healthy life expectancy vs Maximum Death rate")
x = final_data["Healthy life expectancy"]
y = final_data["max_death_rate"]
sns.scatterplot(x=x, y=np.log(y))
sns.regplot(x=x, y=y)

# Plotting Freedom to make life choices vs Maximum infection rate
plt.subplot(2, 2, 4)
plt.title("Freedom to make life choices vs Maximum Death rate")
x = final_data["Freedom to make life choices"]
y = final_data["max_death_rate"]
sns.scatterplot(x=x, y=np.log(y))
sns.regplot(x=x, y=y)

plt.tight_layout()
plt.show()
