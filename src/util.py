import pandas as pd # type: ignore
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore
from fuzzywuzzy import process # type: ignore
from mappings import colTranslation, countryTranslation, continentTranslation, manualFixes # type: ignore
from pathlib import Path

df_save_dir = str()
plot_save_dir = str()

def fuzzy_match(chineseName: str, dict: dict) -> str:
    """Match Chinese name of a country with its English name

    Args:
        chineseName (str): Chinese name of a country
        dict (dict): Chinese-english dictionary
    
    Return:
        English name of the input country
    """

    global manualFixes
    if chineseName in manualFixes:
        return manualFixes[chineseName]
    else:
        matchedName, score = process.extractOne(chineseName, dict.keys())
        return dict[matchedName]
    
def load_and_process(file_path: Path) -> pd.DataFrame:
    """Translate and standardize dataset

    Args:
        file_path: Path to CSV file
        fname: File name to save

    Returns:
        Translated and standardized dataframe
    """

    global colTranslation
    global countryTranslation
    global continentTranslation

    # Import dataset as dataframe
    df = pd.read_csv(file_path)

    # Translate col
    df = df.rename(columns=colTranslation) 
    
    # Drop uncommon programs and add total headcount for each country
    df = (
        df.assign(Others = lambda df: df.drop(columns=list(colTranslation.values())).sum(axis=1)) # Total count of uncommon programs
        .pipe(lambda df: df[list(colTranslation.values())+['Others']]) # Drop uncommon programs
        .assign(Total = lambda df: df[df.columns.difference(['Year', 'Continent', 'Country'])].sum(axis=1)) # Total count of all programs 
    ) 
    # Translate continent and country         
    df = (
        df.assign(Continent=lambda df: df['Continent'].map(continentTranslation)) # Translate continent
        .assign(Country=lambda df: df['Country'].apply(lambda x: fuzzy_match(x, countryTranslation))) # Translate country
    )  

    global df_save_dir
    fname = file_path.stem
    df.to_csv(f"{df_save_dir}/{fname}.csv", index=False)

    return df

def consolidate(data_dir: Path) -> pd.DataFrame:
    file_paths = []
    for item in data_dir.iterdir():
        if item.is_file():
            file_paths.append(item) # Append absolute path
            
    # Concat and sort
    df_consolidated = pd.concat([load_and_process(path) for path in file_paths], ignore_index=True).sort_values(['Year', 'Total'], ascending=[False, False])
    
    # Export
    global df_save_dir
    df_consolidated.to_csv(f'{df_save_dir}/consolidated_data.csv', index=False)

    return df_consolidated

def plot_top10(df: pd.DataFrame) -> None:
    """Plot a heatmap and line graphs by student type for 10 countries with the highest average number of students in Taiwan within the timeframe.

    Args:
        df: dataframe containing data to plot
    """
    
    # Find top 10 countries
    df = df.copy()
    top10 = df.groupby('Country')['Total'].mean().nlargest(10)
    dfTop10 = df[df['Country'].isin(top10.index)]

    global df_save_dir
    dfTop10.to_csv(f"{df_save_dir}/top10_country.csv", index=False)

    # Plot heatmap
    global plot_save_dir

    plt.figure(figsize=(16,8))
    sns.heatmap(
        dfTop10.pivot_table(index='Country', columns='Year', values='Total'),
        annot=True, fmt='g', cmap='Blues',
    )
    plt.title('Top 10 Countries with the Highest Average Numbers of Students in Taiwan from the Year 103 to 113', fontsize=18, fontweight='bold', loc='left')
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('')
    plt.tight_layout()

    plt.savefig(f"{plot_save_dir}/top10_country.png")
    plt.show()

    # Plot line graphs
    g = sns.FacetGrid(
        dfTop10.melt(
            id_vars=['Year', 'Country'], var_name='Student Type', value_name='Number of Students',
            value_vars=dfTop10.columns.difference(['Year', 'Continent', 'Country', 'Total'])),
        col='Student Type', col_wrap=4, sharey=False, aspect=1.25)
    g.map_dataframe(func=sns.lineplot, x='Year', y='Number of Students', hue='Country')
    g.add_legend(ncols=5, bbox_to_anchor=[0.5,1.05])
    g.figure.subplots_adjust(hspace=0.25, wspace=0.25)
    
    plt.savefig(f"{plot_save_dir}/top10_student_type.png", bbox_inches='tight', dpi=300)
    plt.show()