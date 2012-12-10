#!/bin/bash
FLDR='../'
OUTPUT=$FLDR'/3Results'

cd $OUTPUT


#fields:
#1 - guid
#2 0 COUNT($1) as imps,
#3 1 SUM($1.skimlinks_count) as total_skimlinks_count,
#4 2 SUM($1.skimwords_count) as total_skimwords_count,
#5 COUNT(publisher_ids)    as publishers,
#6 COUNT(urls)             as urls,
#7 DISTICT TimeCount(views.tsm)    as real_imps, --- need to be flatterend! NOT TESTED
#8 (double) (MAX($1.tsm) - MIN($1.tsm)) / COUNT($1) as ts_interval, -- average  time interval between visits
#9 VAR($1.tsm)             as ts_variance,
#10 AVG($1.jsm)             as js_load_time,
#11 VAR($1.jsm)             as js_variance,
#12 user_agent,
#13 COUNT(domain_ids)       as count_domain_ids,
#14 domain_ids;                     --- {2134, 3452, 4363}
read -d '' CHCK <<"EOF"
(
    ("guid is wrong", "len(x)==32"),
    ("impr<1",        "int(x) > 1"),
    ("links<0",       "int(x) >= 0"),
    ("words<0",       "int(x) >= 0"),
    ("publishers<0",  "int(x) >= 0"),
    ("uls<0",         "int(x) >=0"),
    ("sesions<0",     "int(x) >= 0"),
    ("time_interv<0", "float(x) >= 0"),
    ("tsvar<0",       "float(x) >= 0"),
    ("jsav is not float",   "float(x) or True"),
    ("jsvar<0",             "float(x) >= 0"),
    ("useragent is wrong",  "str(x) or True"),
    ("domains<0",           "int(x) >= 0"),
    ("domain_ids are wrong","str(x) or True")
)
EOF

echo 'Checks: $CHCK'
C=`echo $CHCK | tr "\n" " "`

echo "Cleaning the data"
pv out_sorted.txt | ./verify-data-format -c "$C" 1> out_sorted_clean.txt 2> err_sorted.txt


