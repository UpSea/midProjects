import pandas as pd
from pytz import common_timezones

now = pd.Timestamp('now')
local_now = now.tz_localize('UTC')
rng = pd.date_range('20120301 00:00',periods=15,freq='D')
local_rng = pd.date_range('20120301 00:00',periods=15,freq='D',tz='US/Mountain')
i = 8