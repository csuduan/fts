package org.mts.admin.dao;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import org.mts.common.model.conf.AcctConf;
import org.mts.common.model.conf.QuoteConf;

import java.util.List;

@Mapper
public interface AcctMapper {
    int count();

    @Select("SELECT * FROM ACCT_CONF")
    List<AcctConf> getAcctConfs();

    @Select("SELECT * FROM QUOTE_CONF")
    List<QuoteConf> getQuoteConfs();
}
