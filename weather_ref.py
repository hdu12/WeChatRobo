from weather_mapping import weather_mapping
import requests
import json
def weather_ref():         
      locat="121.47,31.23"
      apikey = ''
      url = f'https://api.caiyunapp.com/v2.6/{apikey}/{locat}/daily.json'

      city ="上海"
      response = requests.get(url)
      weather_data = json.loads(response.content.decode())
      temperature_min = weather_data['result']['daily']['temperature'][0]['min']
      temperature_max = weather_data['result']['daily']['temperature'][0]['max']
      summary = weather_data['result']['daily']['skycon'][0]['value']
      summary=weather_mapping.get(summary, "未知天气")
      humidity_min = weather_data['result']['daily']['humidity'][0]['min']
      humidity_max = weather_data['result']['daily']['humidity'][0]['max']
      sendAll = f"\n{city}今天的天气：{summary}\n温度：{temperature_min}℃ ~ {temperature_max}℃\n湿度：{humidity_min*100}% ~ {humidity_max*100}%"
      return(sendAll)

def weather_real():
   locat="121.47,31.23"
      # 填入你的开发者密钥
   apikey = ''
   city ="上海"
# 拼接API请求URL
   url = f'https://api.caiyunapp.com/v2.6/{apikey}/{locat}/weather'

# 发送GET请求获取响应数据
   response = requests.get(url)

# 解析JSON格式数据
   data = response.json()
   print(data)
# 提取当前天气信息
   current_weather = data['result']['realtime']['skycon']
   current_weather=weather_mapping.get(current_weather, "未知天气")
# 提取当前温度湿度信息
   current_temperature = data['result']['realtime']['temperature']
   current_humidity = data['result']['realtime']['humidity']

   sendAll = f"\n{city}现在的天气：{current_weather}\n温度：{current_temperature}℃\n湿度：{current_humidity*100:.1f}%"
   return(sendAll)