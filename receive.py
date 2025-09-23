# -*- coding: utf-8 -*-#
# filename: receive.py
import xml.etree.ElementTree as ET


def parse_xml(web_data):
    if len(web_data) == 0:
        return None
    xmlData = ET.fromstring(web_data)
    msg_type = xmlData.find("MsgType").text
    if msg_type == "text":
        return TextMsg(xmlData)
    elif msg_type == "image":
        return ImageMsg(xmlData)


class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find("ToUserName").text
        self.FromUserName = xmlData.find("FromUserName").text
        self.CreateTime = xmlData.find("CreateTime").text
        self.MsgType = xmlData.find("MsgType").text
        self.MsgId = xmlData.find("MsgId").text


class TextMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.Content = xmlData.find("Content").text


class ImageMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.PicUrl = xmlData.find("PicUrl").text
        self.MediaId = xmlData.find("MediaId").text


def responseText(message):
    message = message.strip()
    if message.startswith("/"):
        # 配置各类指令的回复
        if message == "/help":
            return (
                "我是张徊, zhyDaDa的私人助理，以下是我能为您提供的帮助指令：\n"
                "/help - 显示帮助信息\n"
                "/about - 了解我的功能和背景\n"
                "/statics - 获取统计数据\n"
            )
        elif message == "/about":
            return "我是一个基于AI的聊天助手，旨在帮助您解决问题和提供信息。"
        elif message == "/statics":
            return "当前统计数据：\n- 用户数：1234\n- 消息数：5678"
        else:
            return "未知指令，请发送 /help 获取帮助信息。"
    else:
        # 这里可以集成调用AI模型的代码
        return f"您发送了文本消息: {message}"