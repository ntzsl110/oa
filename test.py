import os

print(os.path.splitext("file.xls")[0])
print("a")
# path = os.path.abspath("./downloads")
# file = int(
#     len([
#         lists for lists in os.listdir(path)
#         if os.path.isfile(os.path.join(path, lists))
#     ]))

# def numbers(dir):
#     number = 0
#     for root, dirname, filenames in os.walk(dir):
#         for filename in filenames:
#             print(filename)
#             if os.path.splitext(filename)[1] in ['.xlsx', '.xls']:
#                 number += 1
#     return number

# print(numbers(path))

# links = browser.find_elements((By.XPATH, "//td[@id='file_name']/a"))
# for link in links:
#     files = file_counts(dir)
#     link.click()
#     while file_counts(dir) > files:
#         sleep(1)
#     sleep(5)

# email['notRead'] == '未读邮件' and
# batchdownload_btn = browser.element_is_exist((By.XPATH, "//div[@id='batchdownload_btn' and contains(@style,'display:none')]"))

#
# if batchdownload_btn:
#     browser.click((By.XPATH, "//td[@id='file_name']/a"))
# else:
#     browser.click((By.XPATH, "//td[@id='file_name']/a"))
# rows = browser.find_elements((By.XPATH, "/html/body/form/table[@class='listTable']/tbody/tr"))
# rows = browser.find_elements((By.XPATH, "//tbody[@id='itemContainer']/tr"))
# print(rows)

# html = driver.page_source   # 获取网页html
# doc = pq(html)

# driver.switch_to.default_content()   # 切换到默认frame

# sleep(2)
