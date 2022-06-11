import pandas as pd
import numpy as np
from src.series import ChangeSeries


def preceding_changes(
        cs: ChangeSeries,
        days: int,
) -> pd.DataFrame:
    cumul = cs.cumulative().df

    out = pd.DataFrame()
    out['Date'] = cs.df['Date'].iloc[days + 1:]
    out['Preceding'] = cumul['Gain'].shift(1)/cumul['Gain'].shift(days + 1)
    out['Daily'] = cs.df['Change']

    return out


def correlation_p(list1, list2):
    """Performs a permutation test to assess confidence of correlation"""
    list1 = np.array(list1)
    list2 = np.array(list2)

    num_tests = 500

    r = np.corrcoef(list1, list2)[0, 1]
    random_rs = []
    for i in range(num_tests):
        np.random.shuffle(list1)
        np.random.shuffle(list2)
        random_rs.append(np.corrcoef(list1, list2)[0, 1])

    num_rs_greater = len([random_r for random_r in random_rs if abs(random_r) > abs(r)])
    return num_rs_greater/num_tests
