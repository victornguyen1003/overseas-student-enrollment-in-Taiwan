import util
import pandas as pd # type: ignore
from IPython.display import display # type: ignore
from pathlib import Path

def main(data_dir: Path, df_save_dir: Path, plot_save_dir: Path) -> None:
    """Load, process, and visualize data.

    Args:
        data_dir: Directory containing CSV files to load
        df_save_dir: Directory to save dataframes
        plot_save_dir: Directotry to save plots
    """

    util.df_save_dir = df_save_dir
    util.plot_save_dir = plot_save_dir

    # Load, process, and consolidate data
    df = util.consolidate(data_dir)

    # Display consolidated data and summary
    display(df)
    display(df.describe())

    # Plot top 10 countries
    util.plot_top10(df)

if __name__ == "__main__":
    main(Path('../data/raw'), Path('../data/processed'), Path('../reports/figures'))