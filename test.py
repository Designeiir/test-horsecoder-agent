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
                file_path = 'log/one-shot-preview/' + file_name + '/' + str(i + 1) + '.json'
                if not os.path.exists('log/one-shot-preview/' + file_name):
                    os.makedirs('log/one-shot-preview/' + file_name)
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
    url = "http://localhost:5000/component"  # 示例URL
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
    demand_map = {'AntdButton': '01 我需要实现一个按钮，内容为 “hello world”，形状设置为圆形，并在一开始进行点击。',
                  'AntdTypography': '02 我需要实现一个可以复制的文本，内容为“测试”，文本需要被标记，且为斜体。',
                  'AntdAutoComplete': '03 我需要实现一个能够自动完成的输入框，并在一开始将焦点聚焦在该输入框上，失去焦点后，我需要触发逻辑弹窗。',
                  'AntdInputTextArea': '04 生成一个标准多行文本输入框,有边框,初始大小为"中",默认显示"请输入文本"',
                  'AntdComment': '05 我需要实现一条评论，内容为 “hello world”，评论用户名称为 “User”。',
                  'AntdCalender': '06 我需要一个日历，以月为单位，展示每月中的每一天，默认展示的日期是2024年8月1号，且在2024年7月19号这一天所对应的单元格中追加展示一个“上课”标签',
                  'AntdMessage': '07 我需要实现两个全局提示，第一个全局提示不自动关闭、提示用户“请注意休息”，第一个全局提示显示3秒后自动关闭、提示用户“请好好学习”',
                  'AntdNotification': '08 我需要实现一个通知提示框，标题为“通知”，内容为“明天放假”。',
                  'AntdDivider': '09 我需要实现一个在标题右边且距离为20的竖直分割线。',
                  'AntdSpace': '10 我需要设置一个纵向的间距，大小设为中等，可以自动换行',
                  'AntdBreadcrumb': '11 我需要实现一个面包屑，分隔符为“｜”。',
                  'AntdPagination': '12 我有70条数据，我希望对其进行分页展示，每页展示十条数据，可以快速跳转到某页，可以自动调整大小',
                  }
    for key in demand_map.keys():
        execute_one_sample(demand_map[key], key)
