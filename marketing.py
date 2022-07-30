from os import error
import random
from numpy import number
import requests
import json
from time import sleep


def get_api_tukey(headers, payload, mode):
    post_response = requests.post(
        "https://" + mode + ".chimes.ai/tukey/tukey/api/",
        data=json.dumps(payload),
        headers=headers,
    )
    post_result = post_response.json()
    result_api = post_result["id"]
    print(post_result)
    return result_api


def get_response_tukey(result_api, mode):
    url = "https://" + mode + ".chimes.ai/tukey/tukey/api/" + result_api + "/"
    calculation = requests.get(url)
    calculation_result = calculation.json()
    answer = calculation_result["data"]
    return answer


def get_y(token, mode):
    status_1 = ""
    while status_1 != "success":
        y_1 = get_response_tukey(token, mode)
        status_1 = y_1["status"]
        print(status_1)
        if status_1 == "fail":
            sleep(0.2)
            return "Fail"
        print(y_1)
        sleep(2)
    data = y_1["prob"][0]["是"]
    return data


def get_predicted_value():
    data_load = {}
    try:
        with open("marketing_test.json", encoding="utf-8") as f:
            data_load = json.load(f)
            if error in data_load:
                print("can't receive data from board")
    except Exception:
        print("can not load json")
    number = int(random.uniform(0, 99))
    data = data_load[number]
    del data["Data_Analysis"]

    headers = {"Content-Type": "application/json"}
    payload = {
        "api_token": "fc446a89-7924-40ef-8f88-8c81fc68413f",  # 模型api token
        "data": data,
    }

    token = get_api_tukey(headers, payload, "staging")  # 餵tukey
    y_1 = get_y(token, "staging")  # 得到預測值
    print(y_1)

    sex = data["sex"]
    status = data["subscriber_status"]
    time = data["subscribe_time"]
    industry = data["industry"]
    job = data["job_levels"]
    id = number
    return f"客戶資訊：客戶編號：{id}\n性別：{sex}\n訂閱狀態：{status}\n訂閱期數：{time}\n產業：{industry}\n職位：{job}\n購買機率：{round(y_1*100)}%"
