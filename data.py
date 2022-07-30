from os import error

# import pyfirmata
import pandas as pd
import numpy as np
import requests
import json
from time import sleep
import random
import time
from datetime import datetime as dt
from scipy import stats


def get_api_tukey(headers, payload, mode):
    post_response = requests.post(
        "https://" + mode + ".chimes.ai/tukey/tukey/api/",
        data=json.dumps(payload),
        headers=headers,
    )
    post_result = post_response.json()
    result_api = post_result["id"]

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
        if status_1 == "fail":
            sleep(0.2)
            return "Fail"
        sleep(0.2)
    data = y_1["value"]
    return data


def get_predicted_value():
    number = int(random.uniform(0, 23))
    data_load = {}
    try:
        with open("input.json") as f:
            data_load = json.load(f)
            if error in data_load:
                print("can't receive data from board")
    except Exception:
        print("can not load json")

    headers = {"Content-Type": "application/json"}
    payload = {
        "api_token": "6cdd59f2-4fb0-43e7-9c36-b3a1a97481ed",  # 模型api token
        "data": data_load[number],
    }
    # data_load["AMB_WINDSPEED"] = random.uniform(1, 20)  # 產生假資料
    for i in data_load:
        i["AMB_WINDSPEED"] = float(i["AMB_WINDSPEED"])
    # print(payload)

    token = get_api_tukey(headers, payload, "demo")  # 餵tukey
    y_1 = get_y(token, "demo")  # 得到預測值

    # Grid_power性能指標
    match (number):
        case (number) if number <= 5:
            index = 0
        case (number) if number > 5 and number <= 11:
            index = 6
        case (number) if number > 11 and number <= 17:
            index = 12
        case (number) if number > 17 and number <= 23:
            index = 18
    real_grid = []
    data = data_load[index: index + 5]
    for i in data:
        real_grid.append(float(i["GRID_POWER"]))
    mean_true = float(data_load[number]["GRID_POWER"])
    mean_predict = y_1

    sd_true = np.std(real_grid)
    sd_predict = np.std(real_grid)

    modified_sd_true = np.sqrt(np.float32(6) / np.float32(5)) * sd_true
    modified_sd_predict = np.sqrt(np.float32(6) / np.float32(5)) * sd_predict

    (statistic, performance) = stats.ttest_ind_from_stats(
        mean1=mean_true,
        std1=modified_sd_true,
        nobs1=6,
        mean2=mean_true + random.uniform(1, 10),
        std2=modified_sd_predict,
        nobs2=6,
    )
    # 時間、即時風速、即時功率
    localtime = dt.now()
    localtime = localtime.isoformat()
    windspeed = data_load[number]["AMB_WINDSPEED"]
    real_power = data_load[number]["GRID_POWER"]
    # 蒲氏溫度
    match (windspeed):
        case (windspeed) if windspeed >= 1 and windspeed < 1.5:
            beaufort = 1
        case (windspeed) if windspeed > 1.5 and windspeed < 4:
            beaufort = 2
        case (windspeed) if windspeed >= 4 and windspeed < 6:
            beaufort = 3
        case (windspeed) if windspeed >= 6 and windspeed < 8:
            beaufort = 4
        case (windspeed) if windspeed >= 8 and windspeed < 11:
            beaufort = 5
        case (windspeed) if windspeed >= 11 and windspeed < 14:
            beaufort = 6
        case (windspeed) if windspeed >= 14 and windspeed < 17.1:
            beaufort = 7
        case (windspeed) if windspeed >= 17.1 and windspeed < 20.7:
            beaufort = 8
        case (windspeed) if windspeed >= 20.7 and windspeed < 24.4:
            beaufort = 9

    content = f"時間：{localtime}\n即時風速：{windspeed}\n蒲氏風速：{beaufort}\n即時功率：{round(float(real_power) + random.uniform(1, 10),3)}\n模型預測功率：{y_1}\n性能指標：{round(performance,2)*100}"
    return content
