from main import *
import psycopg2
from db_tools import *
from Settings import user,password,host,database
cnx = psycopg2.connect(user=user, password=password, host=host, database=database)
while True:
    print("Выберите действие")
    print("1 - Найти интервалы определенной акции")
    print("2 - Установить коэфф потери и прибыли")
    print("3 - ")


    choice = int(input())

    id  = get_all_share_id(cnx)
    id_out = 0
    if choice == 1:
        print("Введите название акции")
        for i in id:
            print(i[0])
            id_out +=1
            if id_out == 16:
                print("Для выведения ещё 16 названий акций введите + ")
                choise = input()
                if choise == "+" or choise == "=":
                    id_out = 0
                else:
                    break
        act = input()
        print("С какого по какой день вы хотите посчитать")
        st = input()
        nt = input()
        find_interv(st,nt,act)
    if choice == 2:
        print("Введите коэфф потери")
        loss = input()
        print("Введите коэфф прибыли")
        profit = input()


