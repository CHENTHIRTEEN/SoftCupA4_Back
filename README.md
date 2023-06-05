### :house_with_garden:第12届中国软件杯A4
### :school:南信大-龙王山风电小分队后端代码仓库

### **:bread:前置需求**
+ python==3.7
+ Django==3.2
+ djangorestframework
+ ……
相关pypi包已经在requirement.txt中列出

### :mag:目录结构
```
./
│  README.md
│  requirements.txt
│  
└─A4_Back
    │  db.sqlite3
    │  manage.py
    │  
    ├─A4_Back
    │  │  asgi.py
    │  │  settings.py
    │  │  urls.py
    │  │  wsgi.py
    │  │___init__.py
    │        
    └─apitest
        │  admin.py
        │  apps.py
        │  models.py
        │  tests.py
        │  urls.py
        │  views.py
        │___init__.py
```

### :dizzy: 使用方式
```bash
git clone https://github.com/CHENTHIRTEEN/SoftCupA4_Back.git
cd SoftCupA4_Back
pip install -r requirement.txt
cd A4_Back
python manage.py runserver
```

### :fries: TODO
- [x] 搭建项目框架
- [x] 跨域配置
- [ ] 删除requirement中的冗余包
- [ ] 接口撰写
- [ ] 机器学习推理接入 