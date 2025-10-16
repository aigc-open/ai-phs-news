from global_config import GlobalConfig
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
from WorkWeixinRobot.work_weixin_robot import WWXRobot
from loguru import logger
import dotenv
dotenv.load_dotenv()

_info = TinyDB(storage=MemoryStorage)

class GlobalConfig_(GlobalConfig):
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = ""
    OPENAI_MODEL: str = ""
    CHAT_TYPE: str = "duckduckgo"
    WEIXIN_ROBOT_KEYS: str = "2ad85006-0d75-4b8c-bad9-f10910e9c075"
    SERPAPI_KEY: str = "0d99784bb2a8e2c89668dba0c754dfbc3a6fb3459189313e5d539b8d13d18138"
    WECHAT_APP_ID: str = ""
    WECHAT_APP_SECRET: str = ""
    WECHAT_MEDIA_ID: str = "MvcyvW-8y3M9zOIu1qlEL90czEguYAVYuQfbl2kQfFGGwOhJW1jIygQ_tN0CTSaz"

    def add_info(self, title:str, url:str, content:str):
        _info.insert({"title": title, "url": url, "content": content})

    def exist_info(self, url:str):
        return _info.contains(Query().url == url)

    


global_config = GlobalConfig_()
global_config.init_env()
