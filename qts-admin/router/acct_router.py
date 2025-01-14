from fastapi import APIRouter, Request
from pydantic import BaseModel, Extra
from utils import log_utils
from common.resp import resp_success

from core.acct import acct_mgr

router = APIRouter(prefix='/v1/acct')


@router.get('/conf/list')
async def get_configs():
    '''
    返回配置账户列表
    :return:
    '''
    list = acct_mgr.get_acct_confs()
    return resp_success(list)


@router.put('/conf')
async def get_configs(config):
    '''
    添加账户配置
    :return:
    '''
    return resp_success()


@router.delete('/conf')
async def get_configs(acct_id: str):
    '''
    删除账户配置
    :return:
    '''
    return resp_success()


@router.get('/inst/list')
async def get_acct_list():
    '''
    返回账户实例列表
    :return:
    '''
    list = acct_mgr.get_acct_infos()
    return resp_success(list)


@router.get('/inst/detail')
async def get_acct_detail(acct_id: str):
    '''
    返回账户实例详情
    :param acct_id: 账户编号
    :return:
    '''
    detail = {}

    return resp_success(detail)


@router.post('/inst/start')
async def start_acct():
    pass


@router.post('/inst/stop')
async def stop_acct():
    pass


@router.post('/inst/connect')
async def connect_acct(acct_id: str):
    acct_mgr.get_acct_inst(acct_id).connect()
    pass


@router.post('/inst/disconnect')
async def disconnect_acct(acct_id: str):
    acct_mgr.get_acct_inst(acct_id).disconnect()
    pass
