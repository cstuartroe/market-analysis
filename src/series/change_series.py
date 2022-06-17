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

    def dca(self, dollars_per_trading_day: int = 1) -> CumulativeGainSeries:
        df = pd.DataFrame(index=self.df.index, columns=['Gain'])

        last_value = 1

        for i, (change,) in self.df.iterrows():
            last_value = last_value*change + dollars_per_trading_day

            df.at[i, 'Gain'] = last_value

        return CumulativeGainSeries(df)
