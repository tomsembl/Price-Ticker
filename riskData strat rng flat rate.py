#intoTheCryptoverse historical.json https://app.intothecryptoverse.com/charts/risk

import json, random
data = json.load(open("GitHub/Price-Ticker/riskHistorical.json"))["data"]["series"]
period = ["2020-11-21","2021-12-30"]
period = ["2016-12-21","2018-01-12"]
period = ["2016-12-21","2021-12-30"]
print(period)
data = [x for x in data if x["d"] >= period[0] and x["d"] <= period[1]]
bestWorth = 0
finalWorth = False
bestBuySellAmounts = [0 for x in range(11)]#[0, 0, 0, -3954, 1019, -17123, 11412, -13986, -5989, -6276, 0]#[0,0,3000,1000,0,0,-2000,-4000,-7000,-30000,0]
minRisk = min([int(float(x["btc_risk"])*10) for x in data])
maxRisk = max([int(float(x["btc_risk"])*10) for x in data])
while True:
    # fiat = 0
    # btcPrice = float(data[0]["btc_usd"])
    # totalWorth = 126000
    # btc = totalWorth / btcPrice
    fiat = 126000
    btc = 0
    totalWorth = fiat
    scaler = random.uniform(0,1000)
    newBuySellAmounts = sorted([x+int(random.uniform(-scaler,scaler))  if i>=minRisk and i<=maxRisk else 0 for i,x in enumerate(bestBuySellAmounts)],reverse=True)
    #print(buySellAmounts)
    tradeHistory = []
    for i,x in enumerate(data):
        isDCADay = i % 7 == 0
        if isDCADay:
            btcPrice = float(x["btc_usd"])
            risk = float(x["btc_risk"])
            riskInt = int(risk*10)
            if riskInt > maxRisk: maxRisk = riskInt
            if riskInt < minRisk: minRisk = riskInt
            buySellAmount = newBuySellAmounts[riskInt]
            enoughMoney = fiat - buySellAmount > 0
            enoughBtc = btc + buySellAmount/btcPrice > 0
            doTrade = enoughMoney and enoughBtc
            if doTrade:
                btc += buySellAmount/btcPrice
                stack = btc * btcPrice
                fiat -= buySellAmount
            #else: break
            trade = {"date":x["d"],"price":btcPrice,"risk":round(risk,2),"fiat":round(fiat,2),"trade":round(buySellAmount,2) if doTrade else 0,"btc":round(btc,5)}
            tradeHistory.append(trade)
        finalWorth = fiat#btc * btcPrice + fiat
    if not finalWorth: continue
    if bestWorth < finalWorth:
        bestWorth = finalWorth
        bestBuySellAmounts = newBuySellAmounts
        #for x in tradeHistory: print(x)
        bestList = [x if i>=minRisk and i<=maxRisk else 0 for i,x in enumerate(bestBuySellAmounts)]
        print(f"New best worth: {bestWorth:.2f}, buySellAmounts: {bestList} endDate: {x['d']}")
        print([x for x in tradeHistory if "2020-11-20" < x["date"] <= "2020-11-27"])

    #New best worth: 458733.87, buySellAmounts: [0, 4440, 3326, 1291, 567, -331, -999, -9838, -10611, 0, 0] endDate: 2024-02-27