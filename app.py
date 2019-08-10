"""
Main entrance file
"""

from flask import Flask

from router import init_router
from app.dao.dao_base import db
from data.setup_db import create_db

app = Flask(__name__)
app.config.from_object('config')

# 初始化 DB 物件
db.init_app(app)
# 初始化 router
init_router.init(app)
# 建立 DB 檔案
create_db(app)


if __name__ == '__main__':
    app.run(port=app.config['PORT'], debug=app.config['DEBUG'])
