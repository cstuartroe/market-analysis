import pandas as pd
from .date_series import DateSeries
from .cumulative_gain_series import CumulativeGainSeries


class ChangeSeries(DateSeries):
    DEFAULT_COLUMN = "Change"

    def gain(self) -> float:
        return self.df['Change'].product()

    def leverage(self, factor: float) -> "ChangeSeries":
        df = pd.DataFrame()
        df['Change'] = self.df['Change'].transform(lambda x: (x-1)*factor + 1)

        return ChangeSeries(df)

    def cumulative(self) -> CumulativeGainSeries:
        df = pd.DataFrame()
        df['Gain'] = self.df['Change'].cumprod()

        return CumulativeGainSeries(df)
