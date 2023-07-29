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

# # 查找-cn
# with open("cn.txt", "w") as f:
#     for name in file_names:
#             if "-cn" in name:
#                 i = "geosite:" + name
#                 f.write(i + "\n")
# with open("cn.txt", "a") as f:
#     f.write("geosite:cn")


# 查找某类
def find(key):
    txtname = key + '.txt'
    with open(txtname, "w") as f:
        for name in file_names:
            if key in name:
                content = "geosite:" + str(name)
                f.write(content + "\n")

# 查找@类
def findat(key):
    txtname = key + '.txt'
    hyphen = "-" + str(key).strip("@")
    with open(txtname, "w") as f:
        for name in file_names:
            namepath = os.path.join(data_dir, name)
            if hyphen not in name:
                with open(namepath, 'r', encoding="utf-8") as txt:
                    lines = txt.read()
                    if key in lines:
                        content = "geosite:" + str(name) + str(key)
                        f.write(content + "\n")
                
# 查找所有@
def findallat(key):
    txtname = key + '.txt'
    with open(txtname, "w") as f:
        for name in file_names:
            namepath = os.path.join(data_dir, name)
            with open(namepath, 'r', encoding="utf-8") as txt:
                lines = txt.readlines()
                for line in lines:
                    if key and "#" not in line:
                        index = line.find('@')  # 查找 '@' 字符的索引位置
                        if index != -1:
                             atcontent = line[index:].rstrip()  # 获取 '@' 字符后面的内容并去除末尾的换行符
                             content = "geosite:" + str(name) + str(atcontent)
                             f.write(content + "\n")
                             break

# 给 @ 分类
def auto_classify_by_at_content(key):
    findallat(key)
    categories = {}  # 用于存储分类结果的字典
    txtfile = str(key + ".txt")

    with open(txtfile, 'r', encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()  # 去除首尾的空白字符
            index = line.find('@')
            if index != -1:
                atcontent = line[index + 1:].strip()  # 获取 '@' 后面的内容，去除首尾的空白字符
                category = categories.get(atcontent, [])  # 获取对应分类的列表，若分类不存在则创建空列表
                category.append(line)  # 将行内容添加到对应分类的列表中
                categories[atcontent] = category  # 更新分类字典

    with open(txtfile, 'w') as f:
        f.truncate(0)
        for category, lines in categories.items():
            f.write(f"*Category: {category}\n")
            for line in lines:
                f.write(f"{line}\n")
            f.write("\n")

    return categories

# 给 - 中多于1个的分类
def auto_classify_by_hyphen_content(key):
    find(key)
    txtfile = str(key + ".txt")
    categories = {}  # 用于存储分类结果的字典

    with open(txtfile, 'r', encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            # if "category" not in line:
            line = line.strip()  # 去除首尾的空白字符
            hyphen_indices = [i for i, c in enumerate(line) if c == key]  # 获取所有 - 的索引位置
            if hyphen_indices:
                last_at_index = hyphen_indices[-1]  # 获取最后一个 - 的索引位置
                hyphencontent = line[last_at_index + 1:].strip()  # 获取最后一个 - 后面的内容，去除首尾的空白字符
                category = categories.get(hyphencontent, [])  # 获取对应分类的列表，若分类不存在则创建空列表
                category.append(line)  # 将行内容添加到对应分类的列表中
                categories[hyphencontent] = category  # 更新分类字典

    txtname = "-classification.txt"
    with open(txtname, 'w') as f:
        for category, lines in categories.items():
            if len(lines) > 1:
                f.write(f"* Category: {category}\n")
                for line in lines:
                    f.write(f"{line}\n")
                f.write("\n")

    return categories


find("-ads")

find("!cn")

find("-cn")

find("category")

find("-")

findat("@ads")

findat("@cn")

auto_classify_by_at_content("@")

auto_classify_by_hyphen_content("-")
