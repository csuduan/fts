package org.qts.trader.gateway.tora;

import org.qts.common.entity.acct.AcctDetail;
import org.qts.trader.gateway.MdGateway;

import java.util.List;

public class ToraMdGateway implements MdGateway {


    public ToraMdGateway(AcctDetail acctInfo) {

    }

    @Override
    public void subscribe(String symbol) {

    }

    @Override
    public void connect() {

    }

    @Override
    public void close() {

    }

    @Override
    public List<String> getSubscribedSymbols() {
        return null;
    }

    @Override
    public boolean isConnected() {
        return false;
    }
}
