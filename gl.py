week = 0
week_day = 0
#json
forbidList = {
    "forbid": [
        {
            "week_day": "周三",
            "time": "09:45-11:25"
        },
        {
            "week_day": "周一",
            "time": "09:45-11:25"
        },
        {
            "week_day": "周二",
            "time": "09:45-11:25"
        },
        {
            "week_day": "周三",
            "time": "14:30-16:10"
        }
    ]
}
forbidList1 = {
    "forbid": [
        {
            "week_day": "周三",
            "time": "07:50-11:25"
        }
    ]
}

#使用：
# js = json.dumps(gl.forbidList)
# print(js)
# jss = json.loads(js)
# for obj in jss['forbid']:
    # print(obj['week_day'])