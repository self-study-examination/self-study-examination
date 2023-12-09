# 全国高等教育自学考试各省份通知公告汇总

{% for item in list %}
## {{ item.conf.city }}
更新时间：{{item.time}}

### [{{item.conf.name}}]({{item.conf.domain}})
{% for d in item.data %}
{{d.date}} [{{d.title}}]({{d.url}})
{% endfor %}

{% endfor %}
