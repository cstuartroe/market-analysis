from typing import Optional

from .date_series import DateSeries


class CumulativeGainSeries(DateSeries):
    DEFAULT_COLUMN = "Gain"

    def total_gain(self, column: Optional[str] = None):
        column = column or self.DEFAULT_COLUMN
        return self.df[column][-1]
