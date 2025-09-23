import hashlib
import traceback
import time
import reply
import receive
import web
from expiringdict import ExpiringDict
import yaml

with open("config.yaml", "r") as f:
    cfg = yaml.safe_load(f)


class Handle(object):
    def responseText(message):
        message = message.strip()
        print(f"收到消息: {message}")
        return f"收到消息: {message}"
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

    cache = ExpiringDict(max_len=100, max_age_seconds=30)

    def GET(self):
        try:
            data = web.input()
            return data.echostr
        except Exception as e:
            return e

    def POST(self):
        try:
            webData = web.data()
            print("Handle Post webdata is ", webData)
            # 后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == "text":
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                print(f"Handle.cache: {Handle.cache}")
                if recMsg.MsgId in Handle.cache:
                    if Handle.cache[recMsg.MsgId] != "":
                        replyMsg = reply.TextMsg(
                            toUser, fromUser, Handle.cache[recMsg.MsgId]
                        )
                        print("成功发送")
                        return replyMsg.send()
                    else:
                        print("AI还没有处理结束，等待下一次请求")
                        time.sleep(3)
                        return "success"
                else:
                    Handle.cache[recMsg.MsgId] = ""
                    answer = Handle.responseText(recMsg.Content)
                    Handle.cache[recMsg.MsgId] = answer
                    replyMsg = reply.TextMsg(toUser, fromUser, answer)
                    time.sleep(3)
                    return "success"
            else:
                print("暂且不处理")
                return "success"
        except Exception as e:
            traceback.print_exc()
            return e
