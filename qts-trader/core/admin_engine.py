from typing import Any
from core.acct_inst import AcctInst
from qts.log import logger_utils
from qts.tcp.server import TcpServer
from qts.model.message import MsgType,MsgHandler,Message
from qts.model.object import Position, TradeData, OrderData,AcctInfo,TickData,SubscribeRequest,OrderRequest

from enum import Enum
from typing import TypeVar, Callable,List

log = logger_utils.get_logger(__name__)


class AdminHandler:
    def __init__(self,acct_inst:AcctInst):
        self.acct_inst = acct_inst
        self.msg_handler = self.create_handler()

    def on_msg(self,req:Message)->Any:
        handler = self.msg_handler.get_handler(req.type)
        if handler is not None:  # 如果找到了handler
            try:
                rsp = handler(req.data)
                rsp_msg = Message(type=req.type,code=0,data=rsp)
                return rsp_msg
            except Exception as e:
                log.error(f"Error handling request: {e}")
                return Message(type=req.type,code=-1,data=str(e))
        else:  # 如果没有找到对应的handler
            log.warning(f"No handler found for message type: {req.type}")
            return Message(type=req.type,code=-1,data="Handler not found")

    def create_handler(self):         
        msg_handler = MsgHandler()
        @msg_handler.register(MsgType.CONNECT)
        def handle_connect(req) -> bool:
            self.acct_inst.gateway.connect()
            return True

        @msg_handler.register(MsgType.DISCONNECT)
        def handle_disconnect(req) -> bool:
            self.acct_inst.gateway.disconnect()
            return True
        
        @msg_handler.register(MsgType.SUBSCRIBE)
        def handle_subscribe(req) -> bool:
            symbol = req.get("symbol")
            sub_req = SubscribeRequest(symbol=symbol)
            self.acct_inst.gateway.subscribe(sub_req)
            return True
        
        @msg_handler.register(MsgType.GET_ACCT_INFO)
        def get_acct_info(req) -> AcctInfo:
            acct_info = self.acct_inst.acct_info
            return acct_info
        
        @msg_handler.register(MsgType.GET_ACCT_DETAIL)
        def get_acct_detail(req) -> AcctInfo:
            acct_info = self.acct_inst.acct_detail
            return acct_info

        @msg_handler.register(MsgType.GET_POSITIONS)
        def get_positions(req) -> List[Position]:
            positions = list(self.acct_inst.acct_detail.position_map.values())
            return positions


        @msg_handler.register(MsgType.GET_TRADES)
        def get_trades(req) -> List[TradeData]:
            trades = list(self.acct_inst.acct_detail.trade_map.values())
            return trades


        @msg_handler.register(MsgType.GET_ORDERS)
        def get_orders(req) -> List[OrderData]:
            orders = list(self.acct_inst.acct_detail.order_map.values())
            return orders

        @msg_handler.register(MsgType.GET_QUOTES)
        def get_quotes(req) -> List[TickData]:
            quotes = list(self.acct_inst.acct_detail.quote_map.values())
            return quotes

        @msg_handler.register(MsgType.SEND_ORDER)
        def insert_order(req:OrderRequest) -> bool:
            order = self.acct_inst.gateway.create_order(req)
            self.acct_inst.gateway.send_order(order)
            return True


        @msg_handler.register(MsgType.CANCEL_ORDER)
        def cancel_order(req) -> bool:
            return True

        return msg_handler



class AdminEngine:
    def __init__(self):
        self.tcp_server = None
        self.acct_inst = None

    def start(self, tcp_port: int, acct_inst:AcctInst):
        log.info(f"start admin engine, tcp_port:{tcp_port}")
        self.acct_inst = acct_inst
        admin_handler = AdminHandler(acct_inst)
        self.tcp_server = TcpServer(port=tcp_port,req_handler=admin_handler.on_msg,new_client_callback=self._on_new_client)
        self.tcp_server.start()

        acct_inst.add_tcp_server(self.tcp_server)

    def stop(self) -> None:
        self.tcp_server.stop()

    def _on_new_client(self):
        #每次有新客户端连接，则主动一次就绪消息
        self.acct_inst.push_msg(MsgType.ON_CONNECTED,{})
          
admin_engine = AdminEngine()
