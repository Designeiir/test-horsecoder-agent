import os

import requests
import json


def make_requests(url, param_key, param_value, file_name, num_requests=20):
    responses = []
    for i in range(num_requests):
        try:
            # 传递参数到 GET 请求中
            response = requests.get(url, params={param_key: param_value})
            if response.status_code == 200:
                file_path = 'log/scene-one-shot/' + file_name + '/' + str(i + 1) + '.json'
                if not os.path.exists('log/scene-one-shot/' + file_name):
                    os.makedirs('log/scene-one-shot/' + file_name)
                save_dict_to_json_file(response.json(), file_path)
            responses.append(response)
            print(f"Request {i + 1}/{num_requests} status: {response.status_code}")
        except requests.RequestException as e:
            print(f"Request {i + 1}/{num_requests} failed: {e}")
    return responses


def save_dict_to_json_file(dictionary, file_name):
    try:
        # 格式化并将字典转换为 JSON 字符串
        formatted_json = json.dumps(dictionary, indent=4, ensure_ascii=False)

        # 将格式化后的 JSON 字符串写入文件
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(formatted_json)

        print(f"Dictionary has been formatted and saved to {file_name}")
    except Exception as e:
        print(f"An error occurred: {e}")


def execute_one_sample(value, file_name):
    url = "http://localhost:5000/scene"  # 示例URL
    param_key = "layoutRequirements"
    param_value = value
    responses = make_requests(url, param_key, param_value, file_name, 1)

    # 处理响应，例如打印响应内容
    for i, response in enumerate(responses):
        if response.status_code == 200:
            print(f"Response {i + 1}: {response.json()}")
        else:
            print(f"Response {i + 1} failed with status code: {response.status_code}")



if __name__ == "__main__":
    demand_map = {'one-shot': '11 我需要一个登录界面,其中一个账户输入框,一个密码输入框,还有一个提交按钮'}
    for key in demand_map.keys():
        execute_one_sample(demand_map[key], key)
