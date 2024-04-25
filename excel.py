import pandas as pd

# 创建表格数据
def excel(data, name):
    # 创建DataFrame对象
    df = pd.DataFrame(data)
    # 写入Excel文件

    df.to_excel(f'{name}.xlsx')
    # 显示表格
