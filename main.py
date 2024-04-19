import psycopg2
from db_tools import insert_to_SQL
from meny import loss, profit, act, st, nt
from meny import cnx
file = open("All_Deal.txt", "w")




#loss = 0.99
#profit = 1.01
def find_interv():


    cursor = cnx.cursor()

    query = ("select distinct date(sr.timestamp_begin) "
         "from market.share_rates sr "
         "where share_id = '<act>' "
         "order by date(sr.timestamp_begin)")
    query = query.replace('<act>',act)
    cursor.execute(query)

    #days = cursor.fetchall()[31:34]
    #days = cursor.fetchall()

    days = [st,nt]

    #cursor.close()

    #query = ("select date(sr.timestamp_begin) date_tr, cast(sr.timestamp_begin as time) time_tr, sr.open_price, "
    #     "sr.close_price, sr.max_price, sr.min_price "
    #     "from market.share_rates sr "
    #     "where date(sr.timestamp_begin) = %s "
    #     "and share_id = '<act>' "
    #     "order by cast(sr.timestamp_begin as time)")
    #query = query.replace('<act>',act)
    for day in days:
        cursor = cnx.cursor()
        #Почему это работает?
        cursor.execute(query, (day[0],))
        dates = cursor.fetchall()
        #print(f"Считаны данные дня - {day[0]}")
        cursor.close()
        deal = []
        start_lot = 0
        end_lot = 0
        start_lot_price = 0
        end_lot_price = 0
        open_prise = 0
        close_prise = 0
        in_progress = 0
        stop_loss = 0
        take_profit = 0
        save_close_price = 0
        i = 1
        orders = []
    for date in dates:
        open_prise = date[2]
        orders.append(date)
        save_close_price = close_prise
        close_prise = date[3]
        stop_loss = int(open_prise) * loss
        take_profit = int(open_prise) * profit
        if in_progress == 0:
            in_progress = 1
            start_lot = date[1]
            start_lot_price = open_prise
        elif close_prise < stop_loss or close_prise > take_profit:
            in_progress = 0
            end_lot = date[1]
            end_lot_price = close_prise
            if end_lot_price > start_lot_price:
                deal.append([day[0], start_lot, end_lot, start_lot_price, end_lot_price])
                insert_to_SQL(date[0],start_lot,end_lot,cnx)
                #break
        #print(i, date)
        i += 1
        if in_progress == 1:
            if end_lot_price > start_lot_price:
                deal.append([day[0], start_lot, end_lot, start_lot_price, end_lot_price])

        for i in deal:
            file.write(f"{i[0]}, {i[1]}, {i[2]}, {i[3]}, {i[4]}\n")
        #Тех прирывание при нахождении хоть одной строки
        #if len(deal)>0:
            #break
file.close()
