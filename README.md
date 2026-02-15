# Obsidian-to-Hexo
把obsidian的md文档转移到hexo的post目录并做好对hexo的适配。
Migrate Obsidian Markdown documents to the Hexo 'posts' directory and optimize them for Hexo compatibility.

You need to edit the address at the beginning of each python files.

### move.py
move.py moves mds to certain files you selected and images to another file. At the same time, it adds

---
title:...
date:...
---

to the beginning of md to adapt to hexo.

### image.py
image.py turns images form ![[]] in obsidian into !()[] form in hexo, and revises the address of images that moved by move.py. 

### revise.py
revise.py turns 
$$
...
$$
into
<p>
$$
...
$$
</p>
so that hexo could recognize it.

### pin.py
pin.py adds pinned:10 to the beginning yaml parts.The value could be editted at the beginning part.

### more.py
more.py adds <!-- more --> after the first paragraph.

### cate.py
cate.py adds categories and tags for md.
