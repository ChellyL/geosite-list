import os
import urllib.request
import zipfile

# 下载zip文件
url = "https://github.com/v2fly/domain-list-community/archive/refs/heads/master.zip"
filename = "master.zip"
urllib.request.urlretrieve(url, filename)

# 解压缩zip文件
with zipfile.ZipFile(filename, 'r') as zip_ref:
    zip_ref.extractall()

# 读取data文件夹中所有文件名
data_dir = os.path.join(os.getcwd(), "domain-list-community-master", "data")
file_names = sorted(os.listdir(data_dir))

# 将文件名写入txt文件
with open("geosite.txt", "w") as f:
    for name in file_names:
        name = "geosite:" + name
        f.write(name + "\n")

# 查找@cn
with open("@cn.txt", "w") as f:
    for i in file_names:
        ipath = os.path.join(data_dir, i)
        with open(ipath, 'r', encoding="utf-8") as txt:
            lines = txt.read()
            if "@cn" in lines:
                i = "geosite:" + i
                f.write(i + "\n")

# 查找-cn
with open("cn.txt", "w") as f:
    for name in file_names:
            if "-cn" in name:
                i = "geosite:" + i + "-cn"
                f.write(i + "\n")
with open("cn.txt", "a") as f:
    f.write("geosite:cn")


# 查找某类
def find(key):
    txtname = key + '.txt'
    with open(txtname, "w") as f:
        for name in file_names:
            if key in name:
                content = "geosite:" + str(name)
                f.write(content + "\n")


find("ads")

find("!cn")

find("category")
