"""Получение количества каждого из действий по 1 товару за период"""
"""ID, дата начала, дата окончания"""
get_events_count_by_id = """WITH myconstants (ItemID, startDate, endDate) as (
       values (?, ?::DATE, ?::DATE)
    )
    SELECT
        sum(case when ecom_event_action = 'begin_checkout' then 1 else 0 end) as begin_checkout_summ,
        sum(case when ecom_event_action = 'add_to_cart' then 1 else 0 end) as add_to_cart_summ,
        sum(case when ecom_event_action = 'purchase' then 1 else 0 end) as purchase_summ,
        sum(case when ecom_event_action = 'view_item_list' then 1 else 0 end) as view_item_list_summ,
        sum(case when ecom_event_action = 'remove_from_cart' then 1 else 0 end) as remove_from_cart_summ,
        sum(case when ecom_event_action = 'view_item' then 1 else 0 end) as view_item_summ
        FROM public.wb_hack_parsed,  myconstants
        WHERE ecom_id = ItemID
        
        and (utc_event_date) between  startDate and  endDate;"""


"""Получение количества каждого из действий по 1 товару за период на каждый день"""
"""ID, дата начала, дата окончания"""
get_events_count_by_id_daily = """WITH myconstants (ItemID, startDate, endDate) as (
       values (?, ?::DATE, ?::DATE)
    )
    SELECT
    utc_event_date as date,
        sum(case when ecom_event_action = 'begin_checkout' then 1 else 0 end) as begin_checkout_summ,
        sum(case when ecom_event_action = 'add_to_cart' then 1 else 0 end) as add_to_cart_summ,
        sum(case when ecom_event_action = 'purchase' then 1 else 0 end) as purchase_summ,
        sum(case when ecom_event_action = 'view_item_list' then 1 else 0 end) as view_item_list_summ,
        sum(case when ecom_event_action = 'remove_from_cart' then 1 else 0 end) as remove_from_cart_summ,
        sum(case when ecom_event_action = 'view_item' then 1 else 0 end) as view_item_summ
    FROM public.wb_hack_parsed,  myconstants
        WHERE ecom_id = ItemID
        and (utc_event_date) between  startDate and  endDate
        GROUP BY utc_event_date
	    ORDER BY utc_event_date;"""


"""Получение стоимости товара по ID на определенную дату"""
"""Порядок параметров: ID, дата"""
get_price_by_id_date = """SELECT
ecom_price100
FROM public.items_price
Where ecom_id = ? and utc_event_time::date = ?
LIMIT 1"""


"""Цена по товару за период"""
"""ID, дата начала, дата окончания"""
get_price_by_id_period = """SELECT
min(utc_event_time::date) AS date,
MAX(ecom_price100) AS price
FROM items_price
where ecom_id = %s and utc_event_time::date between %s::date and  %s::date
group by utc_event_time::date
ORDER BY utc_event_time::date ASC"""
