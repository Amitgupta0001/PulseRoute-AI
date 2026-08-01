import pandas as pd


class DataExplorer:

    @staticmethod
    def explore(df: pd.DataFrame, name: str):

        print("=" * 70)
        print(name.upper())

        print("=" * 70)

        print("Rows :", df.shape[0])

        print("Columns :", df.shape[1])

        print()

        print(df.dtypes)

        print()

        print("Missing Values")

        print(df.isnull().sum())

        print()

        print(df.head())