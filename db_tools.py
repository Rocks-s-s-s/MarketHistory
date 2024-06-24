def insert_to_db(date, start_lot, end_lot, cnx):
    template = ("INSERT INTO market.good_intervals "
                "(share_id, timestamp_begin, timestamp_ends) "
                "VALUES('SBER', to_timestamp(%s,'yyyy-mm-dd hh24:mi:ss'), to_timestamp(%s,'yyyy-mm-dd hh24:mi:ss'));")
    date_s = date.strftime("%Y-%m-%d")
    time_s = start_lot.strftime("%H-%M-%S")
    start_lot_s = date_s + ' ' + time_s
    time_s = end_lot.strftime("%H-%M-%S")
    end_lot_s = date_s + ' ' + time_s
    template2 = ("select * from market.good_intervals gi "
                "where share_id = 'SBER' and timestamp_begin = to_timestamp(%s,'yyyy-mm-dd hh24:mi:ss')")
    cursor = cnx.cursor()
    cursor.execute(template2,(start_lot_s,))
    res = cursor.fetchall()
    if len(res) > 0:
        return
    cursor.close()
    cursor = cnx.cursor()
    cursor.execute(template, (start_lot_s, end_lot_s))
    cnx.commit()
    cursor.close()


def get_all_share_id(cnx):
    query = ("select s.share_id "
             "from market.shares s inner join market.load_info li on s.share_id = li.share_id "
             "where li.timestamp_load < current_date-1 "
             "and s.is_history ='X'")
    cursor = cnx.cursor()
    cursor.execute(query)
    id = cursor.fetchall()
    cursor.close()
    return id
