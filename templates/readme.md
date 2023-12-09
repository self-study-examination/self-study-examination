# 全国高等教育自学考试资讯库

{% for item in config %}
## [{{item.city}}]({{item.output}})
[{{item.name}}]({{item.domain}})

{% endfor %}