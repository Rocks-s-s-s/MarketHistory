#Аксиомы и импорты кода
import psycopg2
from db_tools import *
from Settings import user,password,host,database
cnx = psycopg2.connect(user=user, password=password, host=host, database=database)
file = open("All_Deal.txt", "w")
loss = 0.99
profit = 1.01

#Функции

def find_interv(st,nt,act):
    print("Find on")

    cursor = cnx.cursor()

    #Считывание всех доступных дней для выбранного инструмента
    query = ("select distinct date(sr.timestamp_begin) "
            "from market.share_rates sr "
            "where share_id = '<act>' "
            "order by date(sr.timestamp_begin)")
    query = query.replace('<act>',act)
    cursor.execute(query)

    days = cursor.fetchall()[st:nt]
    #days = cursor.fetchall()

    #days = days[st,nt]

    #cursor.close()

    #В данном запросе мы выбираем все дни для данной акции

    query = ("select date(sr.timestamp_begin) date_tr, cast(sr.timestamp_begin as time) time_tr, sr.open_price, "
         "sr.close_price, sr.max_price, sr.min_price "
         "from market.share_rates sr "
         "where date(sr.timestamp_begin) = %s "
         "and share_id = '<act>' "
         "order by cast(sr.timestamp_begin as time)")
    query = query.replace('<act>',act)
    for day in days:
        cursor = cnx.cursor()
        #Почему это работает?
        print(day[0])
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
    print("Find off")


#Менюшка

while True:
    print("Выберите действие")
    print("1 - Найти интервалы определенной акции")



    choice = int(input())

    id  = get_all_share_id(cnx)
    id_out = 0
    i1 = ""
    i2 = ""
    i3 = ""
    i4 = ""
    i5 = ""
    if choice == 1:
        print("Введите название акции")
        for i in id:
            id_out +=1
            print(i[0])
            if id_out == 16:
                id_out = 0
                print("Для ввода названия акции напишите 1 | Для вывода ещё 16 названий акций напишите 2 |  Для остановки напишите 3")
                choise = int(input())
                if choise == 1:
                    print("Введите акцию")
                    act = input()

                    print("С какого по какой день вы хотите посчитать")
                    st = int(input())
                    nt = int(input())
                    find_interv(st, nt, act)
                    break
                if choise == 2:
                    print("two")
                if choise == 3:
                    print("3")
                    break
    if choice == 2:
        print("Введите коэфф потери")
        loss = input()
        print("Введите коэфф прибыли")
        profit = input()




