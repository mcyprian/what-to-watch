# What to watch 

Example EPG application using Django REST framework.

Update data:

```python
In [1]: import requests

In [1]: import requests
In [2]: r = requests.post(url="http://localhost:8000/update_data/",
data={'url':"https://mcyprian.fedorapeople.org/ukazka.zip"})

In [3]: (r.status_code, r.text)
Out[3]: (200, 'Data updated!')
```

Filtering EPG entities based on genre, date and time (All query parameters are optional):
http://localhost:8000/epgentities/?date=2018-03-27&time=6:00&genre=Thriller
