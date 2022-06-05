import pandas as pd
from typing import Optional
from datetime import date, timedelta


class DateSeries:
    DEFAULT_COLUMN = None

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.symbol = df.index.get_level_values('Symbol')[0]

    def first_day(self) -> date:
        return self.df.index.get_level_values('Date')[0]

    def last_day(self) -> date:
        return self.df.index.get_level_values('Date')[-1]

    def seek_date(self, d: date, after=True) -> pd.Series:
        for _ in range(5):
            try:
                return self.df[(self.symbol, d)]

            except IndexError:
                d = d + timedelta(days=(1 if after else -1))

        raise ValueError(f"Whoops!")

    def slice(self, start_date: date, end_date: Optional[date] = None):
        df = self.df[self.df.index.get_level_values('Date') >= start_date]

        if end_date is not None:
            df = self.df[self.df.index.get_level_values('Date') < end_date]

        return type(self)(df)

    def save(self, file):
        self.df.to_csv(file)

    def __str__(self):
        return f"{type(self)}(\n{self.df})"
