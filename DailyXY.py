import requests
from urllib import parse
import json
import time
import sys
import datetime
import io
from bs4 import BeautifulSoup

# 学号
hytc_id = '*********'
# 密码，自己手动获取，没精力去研究RSA算法了
cas_pwd = '5bb1f6305536cd718cb68953485bd9da16a6304e84f9ad3bdfff969fc00fe2f011816e735b4a2e7dfee3e78103121c60f0bfd7137e2aede97237bb07edb1283c1640901c560601d5444b63fc71974fc6216e00d84675a907407748867d4d17bf34c89032cd9983d2ec3380326b19bce243ac123f208fe3c76d8aa6841e4ec54d'


def DailyXY():
    # return_msg = {
    #     "初始化": False,
    #     "登陆身份验证系统": False,
    #     "登陆办事大厅": False,
    #     "取填报权限": False,
    #     "获取用户信息": False,
    #     "格式化数据": False,
    #     "发送数据": False
    # }
    print('---------------------')
    print('正在初始化')
    print('---------------------')
    # 身份验证的基本信息
    login_data = {
        'username': hytc_id,
        'password': cas_pwd,
        'captcha': '',
        'warn': 'true',
        'lt': 'LT-1962910-0dw9MjRybLU6d2xMKhtYcA2et6cVZh-cas01.example.org',
        'execution': 'e4s1',
        '_eventId': 'submit'
    }

    today = str(datetime.date.today())
    # 每天上报的基本信息
    mrqk_data = {
        "WID": today+"-"+hytc_id,
        "XSBH": hytc_id,
        "TBSJ": today,
        "BRJKZT_DISPLAY": "正常",
        "BRJKZT": "1",
        "SFJZ_DISPLAY": "否",
        "SFJZ": "0",
        "JTCYJKZK_DISPLAY": "正常",
        "JTCYJKZK": "1",
        "XLZK_DISPLAY": "正常",
        "XLZK": "www",
        "BY1": "0",
        "QTQK": "",
        "TW": "36.7"
    }
    # 构造Session
    # 在session中发送登录请求，此后这个session里就存储了cookie。可以用print(session.cookies.get_dict())查看
    session = requests.Session()

    print('正在登陆身份验证系统')
    print('---------------------')

    # 身份验证域名
    login_url = 'https://cas.hytc.edu.cn/lyuapServer/login?Service=ehall.hytc.edu.cn/new/index.html'

    # 获取登陆所需的 lt，execution 值
    resp = session.get(login_url)
    login_html = BeautifulSoup(
        resp.content, 'html.parser', from_encoding='utf-8')
    login_data['lt'] = login_html.find(
        'input', attrs={'name': 'lt'}).get('value')
    login_data['execution'] = login_html.find(
        'input', attrs={'name': 'execution'}).get('value')
    # 登陆身份验证系统
    resp = session.post(login_url, login_data)

    print('正在登陆办事大厅')
    print('---------------------')
    # 登陆办事大厅,似乎可以初始化一部分cookie,不过这一步好像没什么卵用
    resp = session.get(
        'http://ehall.hytc.edu.cn/new/index.html#wechat_redirect')

    print('正在获取填报权限')
    print('---------------------')

    # 'http://ehall.hytc.edu.cn/xsfw/sys/swpubapp/indexmenu/getAppConfig.do?appId=5811258723206966&appName=xsyqxxsjapp&v=09862829349213713'  #v=09862829349213713 怎么获取还不清楚,不过可以省略该参数。
    resp = session.get(
        'http://ehall.hytc.edu.cn/xsfw/sys/swpubapp/indexmenu/getAppConfig.do?appId=5811258723206966&appName=xsyqxxsjapp')


    print('正在获取用户信息')
    print('---------------------')
    # 获取基本信息
    resp = session.get(
        'http://ehall.hytc.edu.cn/xsfw/sys/xsyqxxsjapp/modules/mrbpa/mrbpabd.do')
    jbxx_data = json.loads(resp.content)
    jbxx_data = jbxx_data["datas"]["mrbpabd"]["rows"][0]

    print('正在格式化数据')
    print('---------------------')
    # 格式化数据 str
    jbxx_data = json.dumps(jbxx_data, ensure_ascii=False)
    jbxx_data = jbxx_data.replace("null", "\"\"")
    jbxx_data = jbxx_data.replace(" ", "")
    mrqk_data = json.dumps(mrqk_data, ensure_ascii=False)
    mrqk_data = mrqk_data.replace(" ", "")

    # 拼接表单,并进行url编码,似乎不支持发送json
    data = {
        "JBXX": jbxx_data,
        "MRQK": mrqk_data
    }
    data = json.dumps(data, ensure_ascii=False)
    data = parse.quote(data, 'utf-8')
    data = "data=" + data

    print('正在发送数据')
    print('---------------------')
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    resp = session.post(
        'http://ehall.hytc.edu.cn/xsfw/sys/xsyqxxsjapp/mrbpa/saveMrbpa.do', data, headers=headers)

    result = json.loads(resp.content)
    print(result['msg'])
    print('---------------------')
    return result['msg']


# 这是本人的信息推送代码，可以删除，
def send_msg():
    msg = DailyXY()
    msg = "每日疫情信息填报--->" + msg
    url = "https://api.anyfan.top/work-wechat/?msg=" + msg
    requests.get(url)


send_msg()


# DailyXY()
