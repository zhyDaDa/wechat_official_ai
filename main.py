import web
import os
from handle import Handle
from db_helper import DBHelper

# 初始化数据库
db = DBHelper()
db.create_table()  # 确保表已创建

# 将数据库实例传递给 Handle 类
Handle.db = db

class Index:
    def GET(self):
        html_path = os.path.join(os.path.dirname(__file__), 'html', 'index.html')
        with open(html_path, 'r', encoding='utf-8') as f:
            return f.read()

class Admin:
    def GET(self):
        try:
            # 从数据库获取消息
            msgs = db.get_msgs(limit=50)
            
            # 动态生成HTML表格
            table_rows = ""
            for msg in msgs:
                table_rows += "<tr>"
                # msg is a tuple, access by index
                table_rows += f"<td>{msg[0]}</td>" # id
                table_rows += f"<td>{msg[1]}</td>" # to_user
                table_rows += f"<td>{msg[2]}</td>" # from_user
                table_rows += f"<td>{msg[3]}</td>" # create_time
                table_rows += f"<td>{msg[4]}</td>" # msg_type
                table_rows += f"<td>{msg[5]}</td>" # msg_id
                table_rows += f"<td>{msg[6] or ''}</td>" # content
                table_rows += f"<td>{msg[7] or ''}</td>" # pic_url
                table_rows += "</tr>"

            # 读取HTML模板并插入表格
            html_path = os.path.join(os.path.dirname(__file__), 'html', 'admin.html')
            with open(html_path, 'r', encoding='utf-8') as f:
                template = f.read()
            
            return template.replace("<!-- DATA_TABLE -->", table_rows)
        except Exception as e:
            return f"数据库查询出错: {e}"

urls = (
    '/', 'Index',
    '/admin', 'Admin',
    '/wx', 'Handle',
)

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()