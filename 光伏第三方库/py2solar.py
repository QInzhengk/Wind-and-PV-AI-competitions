from pysolar import radiation
from pysolar.solar import get_altitude, get_azimuth
import datetime
import pytz

# 设置经纬度和时区
lat = 39.9
lon = 116.4
tz = pytz.timezone('Asia/Shanghai')

# 获取当前时间和太阳高度角、方位角
dt = datetime.datetime.now(tz)
altitude = get_altitude(lat, lon, dt)
azimuth = get_azimuth(lat, lon, dt)

# 输出结果
print("当前时间: ", dt)
print("太阳高度角: ", altitude)
print("太阳方位角: ", azimuth)

latitude_deg = 42.206  # positive in the northern hemisphere
longitude_deg = -71.382  # negative reckoning west from prime meridian in Greenwich, England
date = datetime.datetime(2007, 2, 18, 15, 13, 1, 130320, tzinfo=datetime.timezone.utc)
altitude_deg = get_altitude(latitude_deg, longitude_deg, date)
radiation.get_radiation_direct(date, altitude_deg)
