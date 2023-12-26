import requests
import pandas as pd
pd.options.mode.chained_assignment = None 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
sns.set_style("whitegrid")

##################################################################################################################################

# idescat.cat

##################################################################################################################################

## Maria's analysis in Catalonia

years = ['2018', '2019', '2020', '2021', '2022']
Maria_abs_freq, Maria_total_position, Maria_girls_position, Maria_total_percent, Maria_girls_percent = [], [], [], [], []

for year in years :

    url = f'https://api.idescat.cat/onomastica/v1/nadons/dades.json?id=40683&t={year}&lang=es'
    response = requests.get(url)
    data_json = response.json() 

    Maria_abs_freq.append(data_json['onomastica_nadons']['ff']['f']['pos1']['v']) # abs freq name Maria over the names of childs born in Catalonia in {year}
    Maria_total_position.append(data_json['onomastica_nadons']['ff']['f']['rank']['total']) # rank of name Maria over the names of childs born in Catalonia in {year}
    Maria_girls_position.append(data_json['onomastica_nadons']['ff']['f']['rank']['sex']) # rank of name Maria over the names of girls born in Catalonia in {year}
    Maria_total_percent.append(data_json['onomastica_nadons']['ff']['f']['pos1']['w']['total']) # % of childs born in Catalonia in {year} whose name is Maria
    Maria_girls_percent.append(data_json['onomastica_nadons']['ff']['f']['pos1']['w']['sex'])  # % of girls born in Catalonia in {year} whose name is Maria

Maria_dict = dict()
Maria_dict['years'] = years
Maria_dict['Maria_abs_freq'] = Maria_abs_freq
Maria_dict['Maria_total_position'] = Maria_total_position
Maria_dict['Maria_girls_position'] = Maria_girls_position
Maria_dict['Maria_total_percent'] = Maria_total_percent
Maria_dict['Maria_girls_percent'] = Maria_girls_percent

Maria_df = pd.DataFrame(Maria_dict)

for col_name in Maria_df.columns :
    if col_name in ['Maria_abs_freq', 'Maria_total_position', 'Maria_girls_position'] :
        Maria_df[col_name] = Maria_df[col_name].astype('int64')
    elif col_name in ['Maria_total_percent', 'Maria_girls_percent'] :
        Maria_df[col_name] = Maria_df[col_name].astype('float64')

#################################################################

### Table

print('--------------------------------------------------------------------------------------------------------')
print('Maria\'s analysis in Catalonia\n')
print(Maria_df)
print('--------------------------------------------------------------------------------------------------------\n')

#################################################################

### Plots

selected_columns = [x for x in Maria_df.columns if x != 'years']
titles = ["Absolute Frequencies Maria in Catalonia", "Ranking: Maria total position in Catalonia",
          "Ranking: Maria girls position in Catalonia", "Maria total % in Catalonia", "Maria girls % in Catalonia"]

# Define the number of rows and columns for the matrix plot
num_cols = 2  # You can adjust the number of columns as needed
num_rows = int(np.ceil(len(selected_columns) / num_cols))

# Create a subplot with the specified number of rows and columns
fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 13))

# Flatten the axes array to make it easier to iterate
axes = axes.flatten()

colors = sns.color_palette("tab10", len(selected_columns))

# Loop through each 'geo' and create a subplot in the matrix
for (i, col_name), color, title in zip(enumerate(selected_columns), colors, titles) :
    ax = axes[i]  # Get the current axis
    sns.barplot(x="years", y=col_name, data=Maria_df, color=color, ax=ax)
    ax.set_title(f"{title}", fontsize=13)
    xticks_index = np.arange(0, len(Maria_df), 1)
    ax.set_xticks(xticks_index)
    ax.tick_params(axis='x', rotation=0)
    ax.set_xlabel('Year')
    ax.set_ylabel('')

# Remove any unused subplots in case the number of 'geo' values is less than num_rows * num_cols
for j in range(len(selected_columns), num_rows * num_cols):
    fig.delaxes(axes[j])

plt.suptitle('Maria\'s born in Catalonia - Statistical information - Last five years (2018-2022)', fontsize=15, y=0.95) # Establishing a general tittle for the plot.
plt.subplots_adjust(hspace=1, wspace=0.3) # Adjust vertical (hspace) and horizontal (wspace) spacing
fig.savefig('Marias_Catalonia' + '.jpg', format='jpg', dpi=550)
# plt.tight_layout()
plt.show()

##################################################################################################################################

## Maria's analysis in Catalonia by city (comarca)

print('Maria\'s analysis in Catalonia by city (comarca)\n')

years = ['2018', '2019', '2020', '2021', '2022']
Maria_df_dict = dict()

for com_id in range(0, 42): # 42 = len(data_json['onomastica_nadons']['ff']['f']) - 1

    Maria_abs_freq, Maria_total_position, Maria_girls_position, Maria_total_percent, Maria_girls_percent = [], [], [], [], []

    for year in years :

        url = f'https://api.idescat.cat/onomastica/v1/nadons/dades.json?id=40683&class=com&t={year}&lang=es'
        response = requests.get(url)
        data_json = response.json() 

        Maria_abs_freq.append(data_json['onomastica_nadons']['ff']['f'][com_id]['pos1']['v']) # abs freq name Maria over the names of childs born in comarca {com_id} in {year}
        Maria_total_position.append(data_json['onomastica_nadons']['ff']['f'][com_id]['rank']['total']) # rank of name Maria over the names of childs born in comarca {com_id} in {year}
        Maria_girls_position.append(data_json['onomastica_nadons']['ff']['f'][com_id]['rank']['sex']) # rank of name Maria over the names of girls born in comarca {com_id} in {year}
        Maria_total_percent.append(data_json['onomastica_nadons']['ff']['f'][com_id]['pos1']['w']['total']) # % of childs born in comarca {com_id} in {year} whose name is Maria
        Maria_girls_percent.append(data_json['onomastica_nadons']['ff']['f'][com_id]['pos1']['w']['sex'])  # % of girls born in comarca {com_id} in {year} whose name is Maria

    Maria_dict = dict()
    Maria_dict['years'] = years
    Maria_dict['Maria_abs_freq'] = Maria_abs_freq
    Maria_dict['Maria_total_position'] = Maria_total_position
    Maria_dict['Maria_girls_position'] = Maria_girls_position
    Maria_dict['Maria_total_percent'] = Maria_total_percent
    Maria_dict['Maria_girls_percent'] = Maria_girls_percent  
    com = data_json['onomastica_nadons']['ff']['f'][com_id]['c']['content']
    Maria_df_dict[com] = pd.DataFrame(Maria_dict)

#################################################################

###  Catalonia city (comarca) with more Maria\'s born by year

Maria_abs_freq_year = dict()

for year in ['2018', '2019', '2020', '2021', '2022']  :

    Maria_abs_freq_city = dict()

    for com in Maria_df_dict.keys() :

        value =  Maria_df_dict[com].loc[Maria_df_dict[com]['years'] == year, 'Maria_abs_freq'].iloc[0]

        if value != '_' : # To avoid the cities with missing value.
        
            Maria_abs_freq_city[com] = value

    Maria_abs_freq_year[year] = Maria_abs_freq_city


Maria_abs_freq_values = dict()
Maria_abs_freq_index = dict()
city_max_Maria = dict()
years =  ['2018', '2019', '2020', '2021', '2022'] 

for year in years :

    Maria_abs_freq_values[year] = np.array([x for x in Maria_abs_freq_year[year].values()], dtype=int)
    Maria_abs_freq_index[year] = np.array([x for x in Maria_abs_freq_year[year].keys()])
    city_max_Maria[year] = Maria_abs_freq_index[year][np.argmax(Maria_abs_freq_values[year])]
    print(f'Catalonia city (comarca) with more Maria\'s born in {year} -->', city_max_Maria[year])

#################################################################

### Plots

# Define the number of rows and columns for the matrix plot
num_cols = 3  # You can adjust the number of columns as needed
num_rows = int(np.ceil(len(years) / num_cols))

# Create a subplot with the specified number of rows and columns
fig, axes = plt.subplots(num_rows, num_cols, figsize=(20, 30))

# Flatten the axes array to make it easier to iterate
axes = axes.flatten()

colors = sns.color_palette("tab10", len(years))

# Loop through each 'geo' and create a subplot in the matrix
for i, color, year in zip(range(0,len(years)), colors, years) :

    ax = axes[i]  # Get the current axis
    sns.barplot(x=Maria_abs_freq_values[year], y=Maria_abs_freq_index[year], color=color, ax=ax)
    ax.set_title(f"{year}", fontsize=13)
    ax.tick_params(axis='x', rotation=0)
    ax.set_xlabel('Count')
    ax.set_ylabel('Cities')

# Remove any unused subplots in case the number of 'geo' values is less than num_rows * num_cols
for j in range(len(years), num_rows * num_cols):
    fig.delaxes(axes[j])

plt.suptitle('Absolute Frequencies Maria by Catalonia cities (comarcas) - Last five years (2018-2022)', fontsize=14, y=0.91) # Establishing a general tittle for the plot.
plt.subplots_adjust(hspace=0.5, wspace=0.37) # Adjust vertical (hspace) and horizontal (wspace) spacing
# fig.savefig('Marias_Areas_Catalonia' + '.jpg', format='jpg', dpi=550)
# plt.tight_layout()
plt.show()

##################################################################################################################################

## Gender info for the childs born in Catalonia in the last nine years (2014-2022)

def try_float(x):   
    try:
        return float(x)
    except ValueError:
        return None

url = 'https://www.idescat.cat/indicadors/?id=aec&n=15237&fil=43&lang=en'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table')

columns = table.find(class_="cap") 
columns_html = columns.select("thead th")
columns_list = []

for i in range(1,len(columns_html)) :
    columns_list.append(columns.select("thead th")[i].text)

columns_list = ['Year'] + columns_list
tr_list = table.select('tr')
useful_info_index = range(1,(len(tr_list)-3))

rows = dict()
for i , r in enumerate(useful_info_index) :
    text_data = tr_list[r].text
    row_data = text_data.replace('\n', ' ').split()
    row_data = [x.replace(',', '.') for x in row_data]
    row_data = [try_float(x) for x in row_data]
    row_data = [x for x in row_data if x != None]
    rows[i] = row_data

df = pd.DataFrame(rows)
df = df.T
df.columns = columns_list
df['Year'] = df['Year'].astype('int')
df['Boys_prop'] = round(df['Boys'] / df['Total'], 3)
df['Girls_prop'] = round(df['Girls'] / df['Total'], 3)

#################################################################

### Table

print('--------------------------------------------------------------------------------------------------------')

print('Gender info for the childs born in Catalonia in the last nine years (2014-2022)\n')
print(df)

print('--------------------------------------------------------------------------------------------------------')

#################################################################

### Plots

selected_columns = [x for x in df.columns if x in ['Boys_prop', 'Girls_prop']]

# Define the number of rows and columns for the matrix plot
num_cols = 2  # You can adjust the number of columns as needed
num_rows = int(np.ceil(len(selected_columns) / num_cols))

# Create a subplot with the specified number of rows and columns
fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5))

# Flatten the axes array to make it easier to iterate
axes = axes.flatten()

colors = sns.color_palette("tab10", len(selected_columns))
titles = ['Girls', 'Boys']

# Loop through each 'geo' and create a subplot in the matrix
for i, color, col_name, title in zip(range(0,len(selected_columns)), colors, selected_columns, titles) :
    ax = axes[i]  # Get the current axis
    sns.barplot(x="Year", y=col_name, data=df, color=color, ax=ax)
    ax.set_title(f"{title}", fontsize=14)
    xticks_index = np.arange(0, len(df), 1)
    ax.set_xticks(xticks_index)
    ax.tick_params(axis='x', rotation=0)
    ax.set_xlabel('Year')
    ax.set_ylabel(' ')
    ax.set_ylim([0.45, 0.54])

# Remove any unused subplots in case the number of 'geo' values is less than num_rows * num_cols
for j in range(len(selected_columns), num_rows * num_cols):
    fig.delaxes(axes[j])

plt.suptitle('Relative frequencies of the gender of childs born in Catalonia - Last nine years (2014-2022)', fontsize=15, y=0.97) # Establishing a general tittle for the plot.
plt.subplots_adjust(hspace=0.6, wspace=0.3) # Adjust vertical (hspace) and horizontal (wspace) spacing
# fig.savefig('Gender_born_Catalonia' + '.jpg', format='jpg', dpi=550)
# plt.tight_layout()
plt.show()


##################################################################################################################################
# EXTRA ANALYSIS
##################################################################################################################################

print('--------------------------------------------------------------------------------------------------------')

print('EXTRA ANALYSIS')

print('--------------------------------------------------------------------------------------------------------')


## Maria's analysis in Catalonia by province

years = ['2018', '2019', '2020', '2021', '2022']
Maria_df_dict = dict()

for prov_id in range(0, 4): # 4 = len(data_json['onomastica_nadons']['ff']['f']) - 1

    Maria_abs_freq, Maria_total_position, Maria_girls_position, Maria_total_percent, Maria_girls_percent = [], [], [], [], []

    for year in years :

        url = f'https://api.idescat.cat/onomastica/v1/nadons/dades.json?id=40683&class=prov&t={year}&lang=es'
        response = requests.get(url)
        data_json = response.json() 

        Maria_abs_freq.append(data_json['onomastica_nadons']['ff']['f'][prov_id]['pos1']['v']) # abs freq name Maria over the names of childs born in province {prov_id} in {year}
        Maria_total_position.append(data_json['onomastica_nadons']['ff']['f'][prov_id]['rank']['total']) # rank of name Maria over the names of childs born in province {prov_id} in {year}
        Maria_girls_position.append(data_json['onomastica_nadons']['ff']['f'][prov_id]['rank']['sex']) # rank of name Maria over the names of girls born in province {prov_id} in {year}
        Maria_total_percent.append(data_json['onomastica_nadons']['ff']['f'][prov_id]['pos1']['w']['total']) # % of childs born in province {prov_id} in {year} whose name is Maria
        Maria_girls_percent.append(data_json['onomastica_nadons']['ff']['f'][prov_id]['pos1']['w']['sex'])  # % of girls born in province {prov_id} in {year} whose name is Maria

    Maria_dict = dict()
    Maria_dict['years'] = years
    Maria_dict['Maria_abs_freq'] = Maria_abs_freq
    Maria_dict['Maria_total_position'] = Maria_total_position
    Maria_dict['Maria_girls_position'] = Maria_girls_position
    Maria_dict['Maria_total_percent'] = Maria_total_percent
    Maria_dict['Maria_girls_percent'] = Maria_girls_percent  
    prov = data_json['onomastica_nadons']['ff']['f'][prov_id]['c']['content']
    Maria_df_dict[prov] = pd.DataFrame(Maria_dict)

#################################################################

### Tables

print('Maria\'s analysis in Catalonia by province')

for prov in Maria_df_dict.keys():
    
    print('--------------------------------------------------------------------------------------------------------')
    print(prov)
    print(Maria_df_dict[prov])

print('--------------------------------------------------------------------------------------------------------')

#################################################################

### Catalonia province with more Maria's born in 2022

Maria_abs_freq_2022 = dict()

for prov in Maria_df_dict.keys():
    Maria_abs_freq_2022[prov] = Maria_df_dict[prov].loc[Maria_df_dict[prov]['years'] == '2022', 'Maria_abs_freq'].iloc[0]

Maria_abs_freq_2022_values = np.array([x for x in Maria_abs_freq_2022.values()], dtype=int)
Maria_abs_freq_2022_index = np.array([x for x in Maria_abs_freq_2022.keys()])
prov_max_Maria_2022 = Maria_abs_freq_2022_index[np.argmax(Maria_abs_freq_2022_values)]
print('Catalonia province with more Maria\'s born in 2022 -->', prov_max_Maria_2022)
print('--------------------------------------------------------------------------------------------------------')

#################################################################

### Plots

Maria_df_dict['Barcelona'] = Maria_df_dict['Barcelona'].drop([3], axis=0)

for prov in Maria_df_dict.keys() :
    for col_name in Maria_df_dict[prov].columns :
        if col_name in ['Maria_abs_freq', 'Maria_total_position', 'Maria_girls_position'] :
            Maria_df_dict[prov][col_name] = Maria_df_dict[prov][col_name].astype('int64')
        elif col_name in ['Maria_total_percent', 'Maria_girls_percent'] :
            Maria_df_dict[prov][col_name] = Maria_df_dict[prov][col_name].astype('float64')

provinces = Maria_df_dict.keys()

# Define the number of rows and columns for the matrix plot
num_cols = 2  # You can adjust the number of columns as needed
num_rows = int(np.ceil(len(provinces) / num_cols))

# Create a subplot with the specified number of rows and columns
fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 13))

# Flatten the axes array to make it easier to iterate
axes = axes.flatten()

colors = sns.color_palette("tab10", len(provinces))

# Loop through each 'geo' and create a subplot in the matrix
for i, color, prov in zip(range(0,len(provinces)), colors, provinces) :
    ax = axes[i]  # Get the current axis
    sns.barplot(x="years", y='Maria_abs_freq', data=Maria_df_dict[prov], color=color, ax=ax)
    ax.set_title(f"{prov}", fontsize=13)
    xticks_index = np.arange(0, len(Maria_df_dict[prov]), 1)
    ax.set_xticks(xticks_index)
    ax.tick_params(axis='x', rotation=0)
    ax.set_xlabel('Year')
    ax.set_ylabel('Count')

# Remove any unused subplots in case the number of 'geo' values is less than num_rows * num_cols
for j in range(len(provinces), num_rows * num_cols):
    fig.delaxes(axes[j])

plt.suptitle('Absolute Frequencies Maria by Catalonia provinces - Last five years (2018-2022)', fontsize=15, y=0.95) # Establishing a general tittle for the plot.
plt.subplots_adjust(hspace=0.5, wspace=0.3) # Adjust vertical (hspace) and horizontal (wspace) spacing
# fig.savefig('Marias_Provinces_Catalonia' + '.jpg', format='jpg', dpi=550)
# plt.tight_layout()
plt.show()

##################################################################################################################################

## Maria's analysis in Catalonia by area (region)

years = ['2018', '2019', '2020', '2021', '2022']
Maria_df_dict = dict()

for at_id in range(0, 8): # 8 = len(data_json['onomastica_nadons']['ff']['f']) - 1

    Maria_abs_freq, Maria_total_position, Maria_girls_position, Maria_total_percent, Maria_girls_percent = [], [], [], [], []

    for year in years :

        url = f'https://api.idescat.cat/onomastica/v1/nadons/dades.json?id=40683&class=at&t={year}&lang=es'
        response = requests.get(url)
        data_json = response.json() 

        Maria_abs_freq.append(data_json['onomastica_nadons']['ff']['f'][at_id]['pos1']['v']) # abs freq name Maria over the names of childs born in comarca {com_id} in {year}
        Maria_total_position.append(data_json['onomastica_nadons']['ff']['f'][at_id]['rank']['total']) # rank of name Maria over the names of childs born in comarca {com_id} in {year}
        Maria_girls_position.append(data_json['onomastica_nadons']['ff']['f'][at_id]['rank']['sex']) # rank of name Maria over the names of girls born in comarca {com_id} in {year}
        Maria_total_percent.append(data_json['onomastica_nadons']['ff']['f'][at_id]['pos1']['w']['total']) # % of childs born in comarca {com_id} in {year} whose name is Maria
        Maria_girls_percent.append(data_json['onomastica_nadons']['ff']['f'][at_id]['pos1']['w']['sex'])  # % of girls born in comarca {com_id} in {year} whose name is Maria

    Maria_dict = dict()
    Maria_dict['years'] = years
    Maria_dict['Maria_abs_freq'] = Maria_abs_freq
    Maria_dict['Maria_total_position'] = Maria_total_position
    Maria_dict['Maria_girls_position'] = Maria_girls_position
    Maria_dict['Maria_total_percent'] = Maria_total_percent
    Maria_dict['Maria_girls_percent'] = Maria_girls_percent  
    at = data_json['onomastica_nadons']['ff']['f'][at_id]['c']['content']
    Maria_df_dict[at] = pd.DataFrame(Maria_dict)

#################################################################

### Tables

print('Maria\'s analysis in Catalonia by area (region)')

for at in Maria_df_dict.keys():

    print('--------------------------------------------------------------------------------------------------------')
    print(at)
    print(Maria_df_dict[at])

print('--------------------------------------------------------------------------------------------------------')

#################################################################

### Catalonia region with more Maria\'s born in 2022

selected_at = [x for x in Maria_df_dict.keys() if x != 'Alt Pirineu i Aran']

Maria_abs_freq_2022 = dict()

for at in selected_at :
    Maria_abs_freq_2022[at] = Maria_df_dict[at].loc[Maria_df_dict[at]['years'] == '2022', 'Maria_abs_freq'].iloc[0]

Maria_abs_freq_2022_values = np.array([x for x in Maria_abs_freq_2022.values()], dtype=int)
Maria_abs_freq_2022_index = np.array([x for x in Maria_abs_freq_2022.keys()])
prov_max_Maria_2022 = Maria_abs_freq_2022_index[np.argmax(Maria_abs_freq_2022_values)]
print('Catalonia area with more Maria\'s born in 2022 -->', prov_max_Maria_2022)

#################################################################

### Plots

for at in selected_at :
    for col_name in Maria_df_dict[at].columns :
        if col_name in ['Maria_abs_freq', 'Maria_total_position', 'Maria_girls_position'] :
            Maria_df_dict[at][col_name] = Maria_df_dict[at][col_name].astype('int64')
        elif col_name in ['Maria_total_percent', 'Maria_girls_percent'] :
            Maria_df_dict[at][col_name] = Maria_df_dict[at][col_name].astype('float64')

# Define the number of rows and columns for the matrix plot
num_cols = 2  # You can adjust the number of columns as needed
num_rows = int(np.ceil(len(selected_at) / num_cols))

# Create a subplot with the specified number of rows and columns
fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 13))

# Flatten the axes array to make it easier to iterate
axes = axes.flatten()

colors = sns.color_palette("tab10", len(selected_at))

# Loop through each 'geo' and create a subplot in the matrix
for i, color, at in zip(range(0,len(selected_at)), colors, selected_at) :
    ax = axes[i]  # Get the current axis
    sns.barplot(x="years", y='Maria_abs_freq', data=Maria_df_dict[at], color=color, ax=ax)
    ax.set_title(f"{at}", fontsize=13)
    xticks_index = np.arange(0, len(Maria_df_dict[at]), 1)
    ax.set_xticks(xticks_index)
    ax.tick_params(axis='x', rotation=0)
    ax.set_xlabel('Year')
    ax.set_ylabel('Count')

# Remove any unused subplots in case the number of 'geo' values is less than num_rows * num_cols
for j in range(len(selected_at), num_rows * num_cols):
    fig.delaxes(axes[j])

plt.suptitle('Absolute Frequencies Maria by Catalonia areas - Last five years (2018-2022)', fontsize=15, y=0.95) # Establishing a general tittle for the plot.
plt.subplots_adjust(hspace=2.5, wspace=0.3) # Adjust vertical (hspace) and horizontal (wspace) spacing
# fig.savefig('Marias_Areas_Catalonia' + '.jpg', format='jpg', dpi=550)
# plt.tight_layout()
plt.show()

