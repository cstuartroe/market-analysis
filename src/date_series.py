import pandas as pd
from typing import Optional
from datetime import date, timedelta


class DateSeries:
    DEFAULT_COLUMN = None

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def first_day(self) -> date:
        return self.df['Date'].iloc[0]

    def last_day(self) -> date:
        return self.df['Date'].iloc[-1]

    def seek_date(self, d: date, after=True) -> pd.Series:
        for _ in range(5):
            row = self.df[self.df['Date'] == d]

            if row.empty:
                d = d + timedelta(days=(1 if after else -1))
            else:
                return row

        raise ValueError(f"Whoops!")

    def slice(self, start_date: date, end_date: Optional[date] = None):
        df = self.df[self.df['Date'] >= start_date]

        if end_date is not None:
            df = df[df['Date'] < end_date]

        return type(self)(df)

    def max(self, column: Optional[str] = None):
        column = column or self.DEFAULT_COLUMN

        return self.df[column].max()
