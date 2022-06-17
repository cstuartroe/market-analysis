import pandas as pd
from typing import Optional
from datetime import date, timedelta
import pdb


class DateSeries:
    DEFAULT_COLUMN = None

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.symbol = df.index.get_level_values('Symbol')[0]

    def first_day(self) -> date:
        return self.df.index.get_level_values('Date')[0]

    def last_day(self) -> date:
        return self.df.index.get_level_values('Date')[-1]

    def seek_date(self, d: date, after: bool = True) -> pd.Series:
        for _ in range(5):
            try:
                return self.df[(self.symbol, d)]

            except IndexError:
                d = d + timedelta(days=(1 if after else -1))

        raise ValueError(f"Whoops!")

    def slice(self, start_date: date, end_date: Optional[date] = None):
        df = self.df[self.df.index.get_level_values('Date') >= start_date]

        if end_date is not None:
            df = df[df.index.get_level_values('Date') < end_date]

        return type(self)(df)

    def save(self, file):
        self.df.to_csv(file)

    def random_sample(self, column: Optional[str] = None):
        column = column or self.DEFAULT_COLUMN
        df = pd.DataFrame(index=self.df.index, columns=[column])
        df[column][:] = self.df[column].sample(
            n=len(self.df),
            replace=False,
            ignore_index=True,
        )

        return type(self)(df)

    def rolling_stat(self, transformation, window: int = 20) -> pd.DataFrame:
        df = pd.DataFrame(index=self.df.index[window - 1:], columns=['Transformed'])

        for i in range(df.size):
            df.iloc[i]['Transformed'] = transformation(self.df.iloc[i:i + window])

        return df

    def __str__(self):
        return f"{type(self)}(\n{self.df})"
