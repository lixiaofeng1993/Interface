# coding:utf-8
import xlrd
from common.logger import Log


class ExcelUtil:
    def __init__(self, excel_path, sheet_name="Sheet1"):
        self.data = xlrd.open_workbook(excel_path)
        self.table = self.data.sheet_by_name(sheet_name)
        self.keys = self.table.row_values(0)  # 获取第一行作为key值
        self.rowNum = self.table.nrows  # 获取总行数
        self.colNum = self.table.ncols  # 获取总列数
        self.log = Log()

    def dict_data(self):
        if self.rowNum <= 1:
            self.log.error("总行数小于1")
        else:
            r = []
            j = 1
            for i in list(range(self.rowNum - 1)):  # 去掉行首 self.rowNum - 1
                s = {'rowNum': i + 2}
                values = self.table.row_values(j)  # 从第二行取对应values值
                for x in list(range(self.colNum)):
                    s[self.keys[x]] = values[x]
                r.append(s)
                j += 1
            return r  # 返回list包含的dict数据


if __name__ == "__main__":
    filepath = "D:\work\Interface_framework\data\demo_api.xlsx"
    sheetName = "Sheet1"
    data = ExcelUtil(filepath, sheetName)
    print(data.dict_data())
