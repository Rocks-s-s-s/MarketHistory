def insert_to_db(date, start_lot, end_lot, cnx):
    template = ("INSERT INTO market.good_intervals"
                "(share_id, timestamp_begin, timestamp_ends)"
                "VALUES('SBER', to_timestamp('%s %s','yyyy-mm-dd hh24:mi:ss'), to_timestamp('%s %s','yyyy-mm-dd hh24:mi:ss'));")
    cursor = cnx.cursor()
    cursor.execute(template, (date, start_lot, date, end_lot))
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
