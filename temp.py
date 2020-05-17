import requests
import config
country = "india"
meta=config.url.format(country)
res = requests.get(meta)
print(res.text)
