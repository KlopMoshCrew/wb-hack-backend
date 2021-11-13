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
