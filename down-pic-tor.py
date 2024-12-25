from bs4 import BeautifulSoup
import requests
import time
import os

def download_torrent(url, save_path):
    # 发送HTTP GET请求到指定的URL
    response = requests.get(url, stream=True)

    # 确保请求成功
    if response.status_code == 200:
        # 从响应头中获取文件名
        if 'Content-Disposition' in response.headers:
            content_disposition = response.headers['Content-Disposition']
            # 提取filename
            file_name = content_disposition.split('filename=')[-1].strip('"')
        else:
            # 如果未找到filename，使用默认名称
            file_name = 'default.torrent'

        # 如果保存路径不存在，创建该路径
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # 生成完整的文件路径
        file_path = os.path.join(save_path, file_name)

        # 将响应内容写入文件
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"文件已成功下载并保存到: {file_path}")
    else:
        print(f"下载失败，HTTP状态码: {response.status_code}")

def download_image(url, save_path, filename):
    # 发送HTTP GET请求到指定的URL
    response = requests.get(url, stream=True)

    # 确保请求成功
    if response.status_code == 200:
        # 如果保存路径不存在，创建该路径
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # 生成完整的文件路径
        file_path = os.path.join(save_path, filename)

        # 将响应内容写入文件
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"文件已成功下载并保存到: {file_path}")
    else:
        print(f"下载失败，HTTP状态码: {response.status_code}")



for page in range(1, 2, 1):
    r = requests.get(f"http://bbs.sex169.org/forum.php?mod=forumdisplay&fid=192&page={page}")

    if r.status_code != 200:
        raise Exception()

    html_doc = r.text

    soup = BeautifulSoup(html_doc, "html.parser")
    h2_nodes = soup.find_all("a", class_="s xst")

    for h2_node in h2_nodes:
        print("mov:" + "http://bbs.sex169.org/" + h2_node["href"])

        #time.sleep(5)
        R = requests.get("http://bbs.sex169.org/" + h2_node["href"])

        if R.status_code != 200:
            raise Exception()
        html = R.text

        soup1 = BeautifulSoup(html, "html.parser")
        tolinks = soup1.find_all("span")
        piclinks = soup1.find_all("img", class_="zoom")

        for piclink in piclinks:
            print( "pic:" + piclink["src"])
            src = piclink["src"]
            save_path = f"./pic and tor/page_46"
            filename = os.path.basename(piclink["src"])
            http = "http"
            if http in piclink["src"]:
                download_image(src, save_path, filename)

        for tolink in tolinks:
            tols = tolink.find_all("a")
            for tol in tols:
                target = tol.get('target')
                if target:
                    print("bt:"+"http://bbs.sex169.org/" + tol["href"])
                    src = "http://bbs.sex169.org/" + tol["href"]
                    # 动态生成保存路径
                    save_path = f"./pic and tor/page_46"
                    download_torrent(src, save_path)