#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : anyfan

# 仅适用于淮阴师范学院（学生疫情信息收集—每日报平安）
# 1. 如有相关旅居史、接触史及发热状况，请手动上传表单并向学校汇报，配合学校防疫工作。
# 2. 所有内容禁止修改！造成相关防疫问责问题与作者无关。
# 3. 只可自己使用，禁止代他人使用或他人代使用！
# 4. 如不能遵守上述要求，请不要使用！
# 4. 如不能遵守上述要求，请不要使用！

import requests
from urllib import parse
import json
import datetime
from bs4 import BeautifulSoup
import sys


class HytcCpDaily():
    def __init__(self, hytc_id, cas_pwd):
        # 在session中发送登录请求，此后这个session里就存储了cookie。可以用print(session.cookies.get_dict())查看
        self.session = requests.Session()
        self.RtMsg = '程序未正常运行'
        self.hytc_id = hytc_id
        self.cas_pwd = cas_pwd


    def HytcLogin(self):
        # 身份验证平台
        login_url = 'https://cas.hytc.edu.cn/lyuapServer/login'
        login_data = {
            'username': self.hytc_id,
            'password': self.cas_pwd,
            'captcha': '',
            'warn': 'true',
            'lt': 'LT-1962910-0dw9MjRybLU6d2xMKhtYcA2et6cVZh-cas01.example.org',
            'execution': 'e4s1',
            '_eventId': 'submit'
        }
        # 获取登陆所需的 lt，execution 值
        resp = self.session.get(login_url)
        login_html = BeautifulSoup(
            resp.content, 'html.parser', from_encoding='utf-8')
        login_data['lt'] = login_html.find(
            'input', attrs={'name': 'lt'}).get('value')
        login_data['execution'] = login_html.find(
            'input', attrs={'name': 'execution'}).get('value')
        # 登陆身份验证系统
        resp = self.session.post(login_url, login_data)
        #判断是否登陆成功
        resp_tittle = BeautifulSoup(resp.text, 'html.parser').title.string
        if resp_tittle == '主页(学生) - 淮阴师范学院门户':
            self.RtMsg = '登陆成功'
            return True
        else:
            self.RtMsg = '登陆错误，请检查账号密码'
            return False


    def JudgeToday(self):
        # 判断是否已经填报
        self.session .get(
            'http://ehall.hytc.edu.cn/xsfw/sys/swpubapp/indexmenu/getAppConfig.do?appId=5811258723206966&appName=xsyqxxsjapp')
        resp = self.session.get(
            'http://ehall.hytc.edu.cn/xsfw/sys/swmxsyqxxsjapp/modules/mrbpa/judgeTodayHasData.do')
        jude_data = json.loads(resp.content)["data"]
        if len(jude_data):
            self.RtMsg = '今天已经签到过了'
            return False
        else:
            self.RtMsg = '正在签到'
            return True


    def GetArchives(self):
        # 获取基本信息
        resp = self.session.get(
            'http://ehall.hytc.edu.cn/xsfw/sys/xsyqxxsjapp/modules/mrbpa/mrbpabd.do')
        stu_data = json.loads(resp.content)
        if stu_data:
            stu_data = stu_data["datas"]["mrbpabd"]["rows"][0]
            print(stu_data)
            # 格式化数据 str
            stu_data = json.dumps(stu_data, ensure_ascii=False)
            stu_data = stu_data.replace("null", "\"\"")
            stu_data = stu_data.replace(" ", "")

            today = str(datetime.date.today())
            # 每天上报的基本信息
            mrqk_data = {
                "WID": "",
                "XSBH": "",
                "TBSJ": today,
                "BRJKZT_DISPLAY": "正常",
                "BRJKZT": "1",
                "SFJZ_DISPLAY": "否",
                "SFJZ": "0",
                "JTCYJKZK_DISPLAY": "正常",
                "JTCYJKZK": "1",
                "XLZK_DISPLAY": "正常",
                "XLZK": "www",
                "BY1": "",
                "QTQK": "",
                "TW": "36.7"
            }
            mrqk_data = json.dumps(mrqk_data, ensure_ascii=False)
            mrqk_data = mrqk_data.replace(" ", "")
            # 拼接表单,并进行url编码
            self.updata = {
                "JBXX": stu_data,
                "MRQK": mrqk_data
            }
            self.RtMsg = '获取信息成功'
            return True
        else:
            self.RtMsg = '获取配置信息异常'
            return False

    def UpDaily(self):
        up_data = json.dumps(self.updata, ensure_ascii=False)
        up_data = parse.quote(up_data, 'utf-8')
        up_data = "data=" + up_data
        # print(up_data)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        resp = self.session.post(
            'http://ehall.hytc.edu.cn/xsfw/sys/xsyqxxsjapp/mrbpa/saveMrbpa.do', up_data, headers=headers)

        result = json.loads(resp.content)
        if result['msg'] == '成功':
            self.RtMsg = '填报成功'
        else:
            self.RtMsg = '填报失败'


if __name__ == '__main__':
    # 学号
    hytc_id = sys.argv[1]
    # 密码
    cas_pwd = sys.argv[2]

    app = HytcCpDaily(hytc_id=hytc_id, cas_pwd=cas_pwd)
    if app.HytcLogin():
        if app.JudgeToday():
            if app.GetArchives():
                app.UpDaily()
    print(app.RtMsg)
