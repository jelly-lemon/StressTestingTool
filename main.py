import os
import re
import sys
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator


def show_RPS(rps_list, concurrency):
    x_data = []
    y_data = []
    for t in rps_list:
        x_data.append(t[0])
        y_data.append(t[1])

    # 设置坐标轴间隔
    step = x_data[1] - x_data[0]    # 计算间隔
    ax = plt.gca()
    x_major_locator = MultipleLocator(step)
    ax.xaxis.set_major_locator(x_major_locator)

    # 设置标题
    plt.title("concurrency=%d" % concurrency)
    plt.xlabel("requests")
    plt.ylabel("RPS")

    # 绘制并显示
    plt.plot(x_data, y_data)
    plt.show()


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
            return (requests, float(rps))



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
        rps_list.append(rps)
        start += step

    print(rps_list)
    return rps_list



ab_path = "C:\\Program Files\\httpd-2.4.47-win64-VS16\\Apache24\\bin\\ab.exe"
os.system("chcp 65001")

if __name__ == '__main__':
    # 判断 ab.exe 是否存在
    if not os.path.exists(ab_path):
        print(ab_path, "is not exists")
        exit()

    concurrency = 100
    # run_stress_testing(100, 100, "http://127.0.0.1/")
    rps_list = RPS_requests((100, 300, 100), concurrency, "http://127.0.0.1/")
    show_RPS(rps_list, concurrency)




