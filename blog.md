---
layout: page
title: BLOG
permalink: /blog/
weight: 1
---

# Blog

Thoughts on linguistics, data science, academic life, and computational methods.

## Recent Posts

{% for post in site.posts %}
- **{{ post.date | date: "%B %d, %Y" }}** — [{{ post.title }}]({{ post.url }})
  {% if post.tags.size > 0 %}
  <br>*Tags:* {% for tag in post.tags %}`{{ tag }}`{% unless forloop.last %}, {% endunless %}{% endfor %}
  {% endif %}
{% endfor %}

## Tags

{% assign tags = site.tags | sort %}
{% for tag in tags %}
- [{{ tag[0] }}](#{{ tag[0] | slugify }}) ({{ tag[1].size }})
{% endfor %}

{% for tag in tags %}
### {{ tag[0] }}
{% for post in tag[1] %}
- **{{ post.date | date: "%B %d, %Y" }}** — [{{ post.title }}]({{ post.url }})
{% endfor %}
{% endfor %}