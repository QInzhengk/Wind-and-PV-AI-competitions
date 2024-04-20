from pvlib import location
from pvlib import irradiance
import pandas as pd
from matplotlib import pyplot as plt

tz = 'Asia/Shanghai'
# 哈尔滨地区纬度、经度
lat, lon = 45.739, 120.683

# 创建本地对象，存储维度、经度、时区
site = location.Location(lat, lon, tz=tz)


# 计算晴天的GHI并将其转换到阵列的平面
# 定义函数，获取某个地方的辐照度（理论标准辐照度）
def get_irradiance(site_location, date, tilt, surface_azimuth):
    # 创建一天间隔10分钟的时间序列
    times = pd.date_range(date, freq='10min', periods=6 * 24, tz=site_location.tz)
    # 使用默认的内部模型生成晴天数据
    # get_clearsky方法返回具有GHI、DNI和DHI值的数据表
    # 该函数用于计算给定地点的晴空条件下的全球横照辐射量（GHI）、直接辐射量（DNI）和散射辐射量（DHI）的估计值。可以使用不同的晴空模型，包括INEichen、HAURWITZ和SIMPLIFIED_SOLIS模型。还可以使用额外的参数进行调整。函数返回一个包含GHI、DNI和DHI的DataFrame。
    clearsky = site_location.get_clearsky(times)
    # 获取太阳方位角和天空顶点以传递到函数
    # 该函数是一个封装函数，用于计算给定时间点处的太阳天顶角、方位角等太阳位置信息。函数接受一个时间序列作为输入，以及可选的气压和温度参数。函数使用pvlib库中的get_solarposition函数进行计算，并返回一个包含太阳位置信息的数据帧。
    solar_position = site_location.get_solarposition(times=times)
    # 使用get_total_iradiance函数将GHI转换为POA
    # 该函数用于计算给定条件下太阳面板的总入射辐射量及其直射、散射和地面反射三个组成部分的值。参数包括面板倾斜角度、方位角度、太阳天顶角和太阳方位角等。函数中使用了不同模型来计算天空散射辐射量，包括等同模型、克鲁泽器模型、海德戴维斯模型、雷因德模型、金模型和佩雷斯模型。函数返回一个有序字典，包含总辐射、直射辐射、散射辐射和地面反射辐射四个参数。
    POA_irradiance = irradiance.get_total_irradiance(
        surface_tilt=tilt,
        surface_azimuth=surface_azimuth,
        dni=clearsky['dni'],
        ghi=clearsky['ghi'],
        dhi=clearsky['dhi'],
        solar_zenith=solar_position['apparent_zenith'],
        solar_azimuth=solar_position['azimuth'])

    return pd.DataFrame({'GHI': clearsky['ghi'], 'POA': POA_irradiance['poa_global']})


# 获取夏至和冬至的辐照度数据，假设倾斜25度，和朝南的阵列
summer_irradiance = get_irradiance(site, '06-21-2022', 25, 180)
winter_irradiance = get_irradiance(site, '12-22-2022', 25, 180)

# 转换时间序列为小时：分钟，方便绘图
summer_irradiance.index = summer_irradiance.index.strftime("%H:%M")
winter_irradiance.index = winter_irradiance.index.strftime("%H:%M")

plt.rcParams['figure.figsize'] = 12, 4
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams.update({"font.size": 11})
# 画夏季和冬季的 GHI  POA
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
summer_irradiance['GHI'].plot(ax=ax1, label='GHI')
summer_irradiance['POA'].plot(ax=ax1, label='POA')
winter_irradiance['GHI'].plot(ax=ax2, label='GHI')
winter_irradiance['POA'].plot(ax=ax2, label='POA')
ax1.set_xlabel('日时间序列 (夏季)')
ax2.set_xlabel('日时间序列 (冬季)')
ax1.set_ylabel('辐照度 ($W/m^2$)')
ax1.legend()
ax2.legend()
plt.show()


from pvlib import location
from pvlib import irradiance
import pandas as pd
from matplotlib import pyplot as plt

# For this example, we will be using Golden, Colorado
tz = 'MST'
lat, lon = 39.755, -105.221

# Create location object to store lat, lon, timezone
site = location.Location(lat, lon, tz=tz)


# Calculate clear-sky GHI and transpose to plane of array
# Define a function so that we can re-use the sequence of operations with
# different locations
def get_irradiance(site_location, date, tilt, surface_azimuth):
    # Creates one day's worth of 10 min intervals
    times = pd.date_range(date, freq='10min', periods=6*24,
                          tz=site_location.tz)
    # Generate clearsky data using the Ineichen model, which is the default
    # The get_clearsky method returns a dataframe with values for GHI, DNI,
    # and DHI
    clearsky = site_location.get_clearsky(times)
    # Get solar azimuth and zenith to pass to the transposition function
    solar_position = site_location.get_solarposition(times=times)
    # Use the get_total_irradiance function to transpose the GHI to POA
    POA_irradiance = irradiance.get_total_irradiance(
        surface_tilt=tilt,
        surface_azimuth=surface_azimuth,
        dni=clearsky['dni'],
        ghi=clearsky['ghi'],
        dhi=clearsky['dhi'],
        solar_zenith=solar_position['apparent_zenith'],
        solar_azimuth=solar_position['azimuth'])
    # Return DataFrame with only GHI and POA
    return pd.DataFrame({'GHI': clearsky['ghi'],
                         'POA': POA_irradiance['poa_global']})


# Get irradiance data for summer and winter solstice, assuming 25 degree tilt
# and a south facing array
summer_irradiance = get_irradiance(site, '06-20-2020', 25, 180)
winter_irradiance = get_irradiance(site, '12-21-2020', 25, 180)

# Convert Dataframe Indexes to Hour:Minute format to make plotting easier
summer_irradiance.index = summer_irradiance.index.strftime("%H:%M")
winter_irradiance.index = winter_irradiance.index.strftime("%H:%M")

# Plot GHI vs. POA for winter and summer
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
summer_irradiance['GHI'].plot(ax=ax1, label='GHI')
summer_irradiance['POA'].plot(ax=ax1, label='POA')
winter_irradiance['GHI'].plot(ax=ax2, label='GHI')
winter_irradiance['POA'].plot(ax=ax2, label='POA')
ax1.set_xlabel('Time of day (Summer)')
ax2.set_xlabel('Time of day (Winter)')
ax1.set_ylabel('Irradiance ($W/m^2$)')
ax1.legend()
ax2.legend()
plt.show()