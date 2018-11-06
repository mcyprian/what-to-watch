# What to watch 

Example EPG application using Django REST framework.

Data update:

```python
In [1]: import requests

In [2]: r = requests.post(url="http://localhost:8000/api/update_data/", data={'url':"https://mcyprian.fedorapeople.org/ukazka.zip"})

In [3]: (r.status_code, r.text)
Out[3]: (200, 'Data updated!')
```

Filtering EPG entities based on genre, actor, date and time (All query parameters are optional):
```
<hostname>/api/epgentities/?date=2018-03-27&time=6:00&genre=Thriller&actor=John%20Travolta
```


Visit ```<hostname>/docs/``` to see the API documentation.
>>>>>>> 3695ae8... fixup! Update README
