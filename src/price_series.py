from datetime import date
from typing import Optional
import pandas as pd
from .download import SecurityCategory, PriceSeriesParams, download_historical_data_as_pd
from .date_series import DateSeries
from .change_series import ChangeSeries
from .cumulative_gain_series import CumulativeGainSeries


class PriceSeries(DateSeries):
    DEFAULT_COLUMN = "Close"

    @classmethod
    def download(
            cls,
            symbol: str,
            start_date: Optional[date] = None,
            end_date: Optional[date] = None,
            category: Optional[SecurityCategory] = None,
    ) -> "PriceSeries":
        p = PriceSeriesParams(symbol=symbol, start_date=start_date, end_date=end_date, category=category)

        return cls(df=download_historical_data_as_pd(p))

    def to_changes(self, column=DEFAULT_COLUMN) -> ChangeSeries:
        changes_df = pd.DataFrame()
        changes_df['Date'] = self.df['Date'].iloc[1:]
        changes_df['Change'] = (self.df[column]/self.df[column].shift(1)).iloc[1:]

        return ChangeSeries(changes_df)

    def cumulative(self, column=DEFAULT_COLUMN) -> CumulativeGainSeries:
        cumulative_df = pd.DataFrame()
        cumulative_df['Date'] = self.df['Date'].iloc[1:]
        start_value = self.df[column].iloc[0]
        cumulative_df['Gain'] = self.df[column].iloc[1:].transform(lambda x: x/start_value)

        return CumulativeGainSeries(cumulative_df)
