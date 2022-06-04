import requests
from enum import Enum
from datetime import date, datetime
from typing import Optional
from io import BytesIO
import pandas as pd
from dataclasses import dataclass


# Gotta suppress those security protocols somehow!
WSJ_HEADERS = {'Host': 'www.wsj.com', 'User-Agent': 'Chrome', 'Accept': '*/*'}
WSJ_DATE_FORMAT = "%m/%d/%Y"
DEFAULT_START_DATE = date(1970, 1, 1)


class SecurityCategory(Enum):
    MUTUAL_FUND = "mutualfund"
    INDEX_FUND = "index"
    ETF = "etf"
    FX = "fx"
    STOCK = "stock"


@dataclass
class PriceSeriesParams:
    symbol: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    category: Optional[SecurityCategory] = None


def get_wsj_url(category: SecurityCategory, symbol: str):
    if category is SecurityCategory.STOCK:
        infix = symbol
    else:
        infix = f"{category.value}/{symbol}"

    return f'https://www.wsj.com/market-data/quotes/{infix}/historical-prices/download'


def _wsj_request(p: PriceSeriesParams):
    if p.category is None:
        for category in SecurityCategory:
            p.category = category  # TODO avoid mutation
            res = _wsj_request(p)

            # if the category is wrong, WSJ will still 200 but the table will be empty
            if len(res.text) > 100:
                return res

    url = get_wsj_url(p.category, p.symbol)

    start_date: date = p.start_date or DEFAULT_START_DATE

    end_date: date = p.end_date or date.today()

    return requests.get(
        url,
        stream=True,
        headers=WSJ_HEADERS,
        params={
            "num_rows": 100000.958333333333,
            "range_days": 100000.958333333333,
            "startDate": start_date.strftime(WSJ_DATE_FORMAT),
            "endDate": end_date.strftime(WSJ_DATE_FORMAT),
        }
    )


def _download_historical_data(p: PriceSeriesParams) -> BytesIO:
    response = _wsj_request(p)

    f = BytesIO()
    for chunk in response.iter_content(chunk_size=4096):
        if chunk:  # filter out keep-alive new chunks
            f.write(chunk)
    f.seek(0)

    return f


def download_historical_data_as_pd(p: PriceSeriesParams) -> pd.DataFrame:
    buf = _download_historical_data(p)

    df = pd.read_csv(buf, skipinitialspace=True)
    # Reverse the order of rows, so older data is on top
    df = df.loc[::-1].reset_index(drop=True)
    df['Date'] = df['Date'].transform(lambda date_string: datetime.strptime(date_string, '%m/%d/%y').date())

    return df
