addColumn
dfSymbols[symbol]=[symbol,counts,dateStart,dateEnd]

addRow
dfSymbols.loc[symbol]=[symbol,counts,dateStart,dateEnd]


for i,code in enumerate(data):
    df = data[code]
    for i,row in enumerate(df.itertuples()):
        log.info( '%05d---%s' % (i,str(row)))
if(True):
    dfCodes = mt5Center.getCodes('local','mongodb')
    for i,code in enumerate(dfCodes.itertuples()):
        log.info('%05d---%s'%(i,str(code)))  