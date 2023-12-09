# {{ conf.city }}

## [{{conf.name}}]({{conf.domain}})
{% for item in data %}
{{item.date}} [{{item.title}}]({{item.url}})
{% endfor %}


## 院校资讯