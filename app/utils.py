from datetime import datetime
import pytz

def to_utc(dt: datetime, tz: str = "Asia/Kolkata") -> datetime:
    tz_obj = pytz.timezone(tz)
    local_dt = tz_obj.localize(dt)
    return local_dt.astimezone(pytz.utc)