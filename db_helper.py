import pymysql
import yaml


class DBHelper:
    def __init__(self):
        with open("config.yaml", "r", encoding='utf-8') as f:
            cfg = yaml.safe_load(f)
        db_config = cfg['database']
        
        self.conn = pymysql.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['db_name'],
            charset="utf8mb4",
        )
        self.cursor = self.conn.cursor()

    def create_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS msg_history (
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            to_user VARCHAR(64),
            from_user VARCHAR(64),
            create_time VARCHAR(32),
            msg_type VARCHAR(16),
            msg_id VARCHAR(64),
            content TEXT,
            pic_url VARCHAR(256),
            media_id VARCHAR(128)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_msg(self, to_user, from_user, create_time, msg_type, msg_id, content=None, pic_url=None, media_id=None):
        sql = """
        INSERT INTO msg_history (to_user, from_user, create_time, msg_type, msg_id, content, pic_url, media_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(
            sql, (to_user, from_user, create_time, msg_type, msg_id, content, pic_url, media_id)
        )
        self.conn.commit()

    def insert_image_msg(self, to_user, from_user, create_time, msg_type, msg_id, pic_url, media_id):
        self.insert_msg(
            to_user=to_user,
            from_user=from_user,
            create_time=create_time,
            msg_type=msg_type,
            msg_id=msg_id,
            content=None,
            pic_url=pic_url,
            media_id=media_id
        )

    def get_msgs(self, limit=100):
        sql = "SELECT * FROM msg_history ORDER BY id DESC LIMIT %s"
        self.cursor.execute(sql, (limit,))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
