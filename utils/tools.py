import os


def file_counts(dir, file_type=['.xlsx', '.xls']):
    """判断指定文件夹下文件数量

    Args:
        dir (string): 目录
        file_type (list): 指定文件类型

    Returns:
        int: 文件数量
    """
    number = 0
    for root, dirname, filenames in os.walk(dir):
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() in file_type:
                number += 1
    return number


if __name__ == '__main__':
    print()
