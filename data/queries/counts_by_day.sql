select
	 date_trunc('day', r.dt_start) as date
	,count(distinct(r.account)) as raffle_count
	,count(distinct(r.account)) - count(distinct(l.account))  as raffles_net_cancels
	,count(distinct(s.account)) as scraped_count
	,count(distinct(b.account)) as raffles_bought_count
	,count(distinct(l.account)) as cancels_count
	,count(distinct(e.account)) as ends_count
	,count(distinct(w.account)) as wins_count
From raffles r
	left join raffles_scraped s on r.account = s.account
	left join buys b on r.account = b.account
	left join cancels l on r.account = l.account
	left join endings e on r.account = e.account
	left join winners w on r.account = w.account
group by date
order by date desc