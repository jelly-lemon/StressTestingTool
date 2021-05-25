import os
import re
import sys
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter


def draw_line(x_data, y_data, x_label, y_label, title):
    # 图片比例
    plt.figure(figsize=(8, 4.5))

    # 设置坐标轴间隔
    step = x_data[1] - x_data[0]  # 计算间隔
    ax = plt.gca()
    x_major_locator = MultipleLocator(step)
    ax.xaxis.set_major_locator(x_major_locator)

    # 设置刻度小数位数
    ax = plt.subplot(111)
    yFormat = FormatStrFormatter('%d')
    ax.yaxis.set_major_formatter(yFormat)


    # 设置背景网格线
    plt.grid(axis='y', linestyle='--')

    # 设置标题
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # 绘制并显示
    plt.plot(x_data, y_data)
    for xy in zip(x_data, y_data):
        plt.annotate(text=("%d" % xy[1]), xy=xy, xytext=(0, 0), textcoords='offset points')
    plt.savefig("%s_%s_%s.png" % (x_label, y_label, title), dpi=300, bbox_inches='tight')
    plt.show()


def show_RPS_requests(rps_request_list, concurrency):
    """
    显示在指定并发量下，RPS 与请求数的折线图

    :param rps_request_list:
    :param concurrency:
    :return:
    """
    x_data = []
    y_data = []
    for t in rps_request_list:
        x_data.append(t[0])
        y_data.append(t[1])

    draw_line(x_data, y_data, x_label="requests", y_label="RPS", title="concurrency=%d" % concurrency)


def show_RPS_concurrency(rps_ccy_list, requests):
    """
    在指定请求数下，RPS 与 并发数的折线图

    :param rps_ccy_list:
    :param requests:
    :return:
    """
    x_data = []
    y_data = []
    for t in rps_ccy_list:
        x_data.append(t[0])
        y_data.append(t[1])

    draw_line(x_data, y_data, x_label="concurrency", y_label="RPS", title="requests=%d" % requests)


def show_RPS_poolsize(rps_size_list, requests, concurrency, cpu_logic_cores):
    """
    在指定请求数和并发数下，RPS 与 线程池数量的折线图

    :param rps_size_list:
    :param requests:
    :param concurrency:
    :return:
    """
    x_data = []
    y_data = []
    for t in rps_size_list:
        x_data.append(t[0])
        y_data.append(t[1])

    draw_line(x_data, y_data, x_label="thread pool size", y_label="RPS",
              title=("requests=%d,concurrency=%d,cpu logic cores=%d" % (requests, concurrency, cpu_logic_cores)))


def show_RPS_backlog(rps_backlog_list):
    """
    RPS 与 backlog 的折线图

    :param rps_backlog_list:
    :param requests:
    :param concurrency:
    :return:
    """
    x_data = []
    y_data = []
    for t in rps_backlog_list:
        x_data.append(t[0])
        y_data.append(t[1])

    draw_line(x_data, y_data, x_label="backlog", y_label="RPS", title="")


def run_stress_testing(requests, concurrency, url):
    """
    运行压力测试，返回 RPS

    :param requests:
    :param concurrency:
    :param url:
    :return:
    """
    # 【易错点】路径中有空格时，要加双引号，不能用单引号
    cmd = '"%s" -n%d -c%d %s' % (ab_path, requests, concurrency, url)
    result = os.popen(cmd).read().splitlines()
    for line in result:
        if (line.find("Requests per second") != -1):
            rps = re.findall("\d+.\d+", line)[0]
            return int(float(rps))


def RPS_requests(requests_range, concurrency, url):
    """
    测试在某一并发量下，随着请求数的增多，RPS 的变化

    :param requests_range: 请求数范围，如 (100, 2000, 100)
    :param concurrency: 并发量
    """
    start = requests_range[0]
    end = requests_range[1]
    step = requests_range[2]
    rps_list = []
    while start <= end:
        rps = run_stress_testing(start, concurrency, url)
        rps_list.append((start, rps))
        start += step

    print(rps_list)
    return rps_list

def RPS_concurrency(concurrency_range, requests, url):
    start = concurrency_range[0]
    end = concurrency_range[1]
    step = concurrency_range[2]
    rps_list = []
    while start <= end:
        rps = run_stress_testing(requests, start, url)
        rps_list.append((start, rps))
        start += step

    print(rps_list)
    return rps_list

def run_server():
    server_path = "D:\\0-2-CLion\\MiniWebServer\\cmake-build-debug\\main.exe"

def draw_data():
    data = [(200, 293.19), (400, 282.24), (600, 283.37), (800, 281.06), (1000, 281.73), (1200, 282.27), (1400, 274.97), (1600, 265.74), (1800, 275.63), (2000, 280.85), (2200, 279.46), (2400, 268.15), (2600, 278.66), (2800, 273.78), (3000, 279.17)]
    x_data = []
    y_data = []
    for t in data:
        x_data.append(t[0])
        y_data.append(t[1])

    draw_line(x_data, y_data, x_label="requests", y_label="RPS", title="concurrency=100")

ab_path = "C:\\Program Files\\httpd-2.4.47-win64-VS16\\Apache24\\bin\\ab.exe"
os.system("chcp 65001")

if __name__ == '__main__':
    # draw_data()
    # exit()

    # 判断 ab.exe 是否存在
    if not os.path.exists(ab_path):
        print(ab_path, "is not exists")
        exit()

    url = "http://127.0.0.1/"

    # 压力测试
    # requests_range = (200, 1000, 200)
    # concurrency = 200
    # rps_list = RPS_requests(requests_range, concurrency, url)
    # show_RPS_requests(rps_list, concurrency)

    # 测试并发数
    concurrency_range = (100, 1000, 100)
    requests = 1000
    rps_list = RPS_concurrency(concurrency_range, requests, url)
    show_RPS_concurrency(rps_list, requests)
