config = {
    "CouchDB":{
        "HTTP":"http", 
        "USERNAME" : "Fexpert", 
        "PASSWORD": "Fexpert",
        "URL":"34.92.184.124:8100"
    },

    "ENV":"DEV",
    "System":"Mac",
    "DEV":{
        "URL":"https://hk.investing.com/stock-screener/?${Criteria}",
        # "URL":"https://hk.investing.com/stock-screener/?sp=country::39|sector::a|industry::a|equityType::a|exchange::21|eq_market_cap::2000000000,10520000000000|a52_week_high_diff::-25,0|avg_volume::25000,1460000000|last::1,1000%3EviewData.symbol;1",
        # 'Acceleration':'https://hk.investing.com/stock-screener/?sp=country::39|sector::a|industry::a|equityType::a|exchange::21|eq_market_cap::2000000000,10520000000000|a52_week_high_diff::-25,0|avg_volume::25000,1460000000|last::1,1000|',
        "Driver":{
            "Version":"83",
            "Windows":"./_driver/Windows/${Version}/chromedriver.exe",
            "Mac":"./_driver/Mac/${Version}/chromedriver"
        }
    },

    #Investing.com
    "Criteria":[
        "sp=country::39",
        "sector::a",
        "industry::a",
        "equityType::a",
        "exchange::21",
        
        "eq_market_cap::2000000000,10520000000000",
        "a52_week_high_diff::-25,0",
        "avg_volume::25000,1460000000",
        "last::1,1000",
        # "ttmrevchg_us::0,82885.98",
    ],

    #self-defined rules
    "Conditions":{
        "include":[
            '1', # Condition 1: Current Price > 150 SMA and > 200 SMA
            '2', # Condition 2: 150 SMA and > 200 SMA
            '3', # Condition 3: 200 SMA trending up for at least 1 month (ideally 4-5 months)
            '4', # Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA
            '5', # Condition 5: Current Price > 50 SMA
            '6', # Condition 6: Current Price is at least 30% above 52 week low (Many of the best are up 100-300% before coming out of consolidation)
            '7' # Condition 7: Current Price is within 25% of 52 week high
        ]
    },

    "Exceptions":[
        "0697.HK",
        "0816.HK",
        "1151.HK"
        "0960.HK",
    ],
    "WatchList":[
        "2660",
        "9988",
        "1858",
        "968",
        "1999",
        "2168",
        "2013",
        "1177",
        "2128",
        "3319",
        "1818",
        "1787",
        "241",
        "6185",
    ]

}