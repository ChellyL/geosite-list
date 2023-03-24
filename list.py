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
file_names = os.listdir(data_dir)

# 将文件名写入txt文件
with open("file_names.txt", "w") as f:
    for name in file_names:
        f.write(name + "\n")
