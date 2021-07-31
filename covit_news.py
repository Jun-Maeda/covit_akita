from bs4 import BeautifulSoup
import requests
import json

# 更新を通知する


def new_bs():
    url = "https://www.pref.akita.lg.jp/pages/archive/47957"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    old_file = "covit_news.txt"

    # 今回取り込んだ情報を取り出す
    new_elem = str(soup.select(".p-page-title"))

    # 前回のデータを取り込む
    try:
        with open(old_file) as f:
            old_elem = f.read()
    except:
        old_elem = ""

    if new_elem == old_elem:
        return False
    else:
        with open(old_file, "w") as f:
            f.write(new_elem)
        return True

# 感染者情報が更新されたら通知


def info_get():
    url = "https://www.pref.akita.lg.jp/pages/archive/47957"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    old_file = "covit_info.txt"

    # 今回取り込んだ情報を取り出す
    new_elem = soup.select(
        "#top > div.l-site-container > main > article > div > div.p-page-body > table > tbody")

    # 前回のデータを取り込む
    try:
        with open(old_file) as f:
            old = f.read()
    except:
        old = ""

    # スクレイピングデータの取得
    datas = new_elem[0].select("tr")
    # 一番最初の症例数のみ取得
    first_data = datas[0].select("td")[0].get_text()

    # 前回取り込んだ症例数と違う場合のみ実行
    if first_data == old:
        return False
    else:
        for data in datas:
            count_num = data.select("td")[0].get_text()
            day = data.select("td")[1].get_text()
            area = data.select("td")[4].get_text()
            # 症例数が前回取り込んだ数と同じになるまで実行
            if count_num is not old and old is not "":
                print(f"{count_num} 判明日：{day}　　場所：{area}")
        with open(old_file, "w") as f:
            f.write(first_data)
            print(url)
            return True


# jsonファイルを読み込む
def json_read():
    file = open('info.json', 'r')
    info = json.load(file)
    print(info)


if __name__ == "__main__":
    json_read()
