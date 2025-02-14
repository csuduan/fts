from datetime import datetime

from config import get_setting
from .ctp_td_api import CtpTdApi
from .ctp_md_api import CtpMdApi

from ..base_gateway import BaseGateway
from .lib import  *

from core.event.event import EventEngine
from model.object import AcctInfo, SubscribeRequest, OrderRequest, CancelRequest

from qts.log import logger_utils

class CtpGateway(BaseGateway):
    """
    CTP交易网关。
    """

    default_name: str = "CTP"


    exchanges: list[str] = list(EXCHANGE_CTP2VT.values())

    def __init__(self, event_engine: EventEngine, acct_info :AcctInfo) -> None:
        """构造函数"""
        super().__init__(event_engine, acct_info)

        self.td_api: "CtpTdApi" = CtpTdApi(self)
        self.md_api: "CtpMdApi" = CtpMdApi(self)

         
    def connect(self) -> None:
        '''连接接口'''
        self.td_api.connect()
        self.md_api.connect()
        self.init_query()

    def disconnect(self) -> None:
        """断开接口"""
        self.td_api.close()
        self.md_api.close()

    def subscribe(self, req: SubscribeRequest) -> None:
        """订阅行情"""
        self.md_api.subscribe(req)

    def send_order(self, req: OrderRequest) -> str:
        """委托下单"""
        return self.td_api.send_order(req)

    def cancel_order(self, req: CancelRequest) -> None:
        """委托撤单"""
        self.td_api.cancel_order(req)

    def query_account(self) -> None:
        """查询资金"""
        self.td_api.query_account()

    def query_position(self) -> None:
        """查询持仓"""
        self.td_api.query_position()




    def process_timer_event(self, event) -> None:
        """定时事件处理"""
        self.count += 1
        if self.count < 2:
            return
        self.count = 0

        func = self.query_functions.pop(0)
        func()
        self.query_functions.append(func)

        self.md_api.update_date()

    def init_query(self) -> None:
        """初始化查询任务"""
        self.count: int = 0
        self.query_functions: list = [self.query_account, self.query_position]
        #self.event_engine.register(EVENT_TIMER, self.process_timer_event)


    
