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
                    answer = receive.responseText(recMsg.Content)
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
