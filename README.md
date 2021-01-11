# 每日疫情信息填报

> 此脚本只适用于淮阴师范学院（2021）

## 修改`DailyXY.py`里面两个变量即可使用

 `hytc_id`学号
 `hytc_id`身份验证平台的密钥

默认每日填报温度`36.7`，具体可以自己修改。

## 密钥的获取

### 推荐方法

登陆 [https://cas.hytc.edu.cn/lyuapServer/login](https://cas.hytc.edu.cn/lyuapServer/login)，输入用户名密码，浏览器按`F12`打开控制台,点到`Network`页面，然后登陆。登陆成功后在`Network`栏中拉到最上面点击`login`页面，在`Header`页面中拉到最后点击`Form Data`，里面的`password`值就是密钥了。

### 本地转换（建议先确定密码能否登陆在使用）

直接点击该项目下的`index.html`,输入密码既可转为密钥。

例如你的密码是`123456`，那么获取的登陆密钥就是

```text
479bc0586418f4ee1d7771942808eebc6fa0622ff40c31681977daa3963d26e7fee31835274225ce3025273df1800934710111de7082bd3a8de1d0e9fc3d8d89f9f0bd161a832986576c7d8d2f555e5f0a63aa67f2cad490254412efb373b926dea056959fd0f977ca745ea4944e6247840c725c033f7f7bb2c0dcb29bfc6495
```

## 使用

```python
pip3 install beautifulsoup4
python3 DailyXY.py
```

每天设置自动运行的方法再此就不在阐述

## 其他

- github 已经有今日校园的自动填报仓库了，为什么不直接拿来用？

  我也想啊，但是学校的填报接口对接的是自己域名下的接口，貌似他们给的版本是无法提交数据的，或者是我太笨不会用。
  
- 为什么代码写的那么烂？

  本人不是计算机专业的，仅仅是因为懒的提交，就在网上现学现卖写的此脚本
