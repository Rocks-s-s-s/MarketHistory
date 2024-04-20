def insert_to_db(date, start_lot, end_lot, cnx):
    template = ("INSERT INTO market.good_intervals"
             "(share_id, timestamp_begin, timestamp_ends)"
             "VALUES('SBER',to_timestamp('<date1> <time1>','yyyy-mm-dd hh24:mi:ss'),to_timestamp('<date2> <time2>','yyyy-mm-dd hh24:mi:ss'));")
    s = template.replace('<time1>',str(start_lot))
    s = s.replace('<time2>', str(end_lot))
    s = s.replace('<date1>', str(date))
    s = s.replace('<date2>', str(date))
    #print(s)
    cursor = cnx.cursor()
    cursor.execute(s)
    cnx.commit()
    cursor.close()

def get_all_share_id(cnx):
    query = ("select s.share_id "
    "from market.shares s inner join market.load_info li on s.share_id = li.share_id " 
    "where li.timestamp_load < current_date-1 "
    "and s.is_history ='X'")
    #query = ("select distinct  share_id "
    #        "FROM market.shares "
    #        "order by share_id")
    cursor = cnx.cursor()
    cursor.execute(query)
    id = cursor.fetchall()
    cursor.close()
    return id