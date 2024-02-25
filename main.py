import pandas as pd
import mysql.connector
import time

file = open("All_Deal.txt","w")

loss = 0.99
profit = 1.01

cnx = mysql.connector.connect(user='home', password='home',
                              host='localhost',
                              database='market')

cursor = cnx.cursor()

query = ("select distinct date(sr.timestamp_begin) "
         "from market.share_rates sr "
         "order by date(sr.timestamp_begin)")

cursor.execute(query)

day = cursor.fetchall()
cursor.close()

tempate = ("select date(sr.timestamp_begin) date_tr, cast(sr.timestamp_begin as time) time_tr, sr.open_price, "
           "sr.close_price, sr.max_price, sr.min_price "
           "from market.share_rates sr "
           "where date(sr.timestamp_begin) = '<day>' "
           "order by cast(sr.timestamp_begin as time)")

for i in day:
    r = i
    cursor = cnx.cursor()
    s = tempate.replace('<day>', str(r[0]))
    cursor.execute(s)
    dats = cursor.fetchall()
    cursor.close()

    #print(r[0])

    deal = []
    start_lot = 0
    end_lot = 0
    start_lot_price = 0
    end_lot_price = 0
    open_prise = 0
    close_prise = 0
    deal_on = 0
    stop_loss = 0
    take_profit = 0
    save_close_price = 0

    for d in dats:
        open_prise = d[2]
        save_close_price =close_prise
        close_prise = d[3]
        stop_loss = int(open_prise) * loss
        take_profit = int(open_prise) * profit
        if deal_on == 0:
            deal_on = 1
            start_lot = d[1]
            start_lot_price = open_prise
        elif close_prise < stop_loss or close_prise > take_profit:
            deal_on = 0
            end_lot = d[1]
            end_lot_price = close_prise
            #print(f"     Покупка - {start_lot}, Продажа - {end_lot}, Цена покупки - {start_lot_price}, Цена продажи - {end_lot_price}")
            if end_lot_price  > start_lot_price:
                #print("append in deal (1 if)")
                deal.append([r[0],start_lot,end_lot,start_lot_price,end_lot_price])


    if deal_on == 1:
        #print(f"DEAL Покупка - {start_lot}, Продажа - {d[1]}, Цена покупки - {start_lot_price}, Цена продажи - {close_prise}")
        if end_lot_price  > start_lot_price:
            #print("append in deal (2 if")
            deal.append([r[0],start_lot,end_lot,start_lot_price,end_lot_price])

    for i in deal:
        file.write(f"{i[0]} , {i[1]} ,  {i[2]} , {i[3]} , {i[4]} \n")
        #print('ааааааааааааааааааааааааааааааааааааааааааааааааааааа')

file.close()