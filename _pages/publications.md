---
layout: page
permalink: /publications/
title: publications
description: Bibliometrics can be found on <a href=https://scholar.google.com/citations?user=-NPCrhcAAAAJ>Google Scholar</a>.<br>* indicates co-ﬁrst authorship.
years: [2023, 2022, 2021, 2020, 2019]
nav: true
nav_order: 1
---
<!-- _pages/publications.md -->
<div class="publications">

{%- for y in page.years %}
  <h2 class="year">{{y}}</h2>
  {% bibliography -f papers -q @*[year={{y}}]* %}
{% endfor %}

</div>
