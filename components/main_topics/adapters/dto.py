from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional, Union

import pandas as pd


@dataclass
class MessagesTable:
    data: Optional[Dict[int, Dict[str, Union[datetime, str]]]]

    def __len__(self):
        return len(self.data.keys())

    def to_df(self):
        return pd.DataFrame.from_dict(self.data, orient='index')


@dataclass
class DateTopics:
    date: Optional[datetime]
    top_keywords: pd.Series
