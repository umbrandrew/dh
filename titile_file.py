import os
import xlrd


class Main():
    def __init__(self) -> None:
        self.kk={}
    
    def cat_dict(self):
        #返回类目表格标题
        self.fileLists=[]
        for s in os.listdir():
            if s.find(".xls")>0:
                files=s.split(".xls")
                file=files[0]  
                self.fileLists.append(file)
        kk=dict(zip(range(len(self.fileLists)), self.fileLists))
        return kk
        # return dict(zip(range(len(self.fileLists)), self.fileLists))

    def get_sheet_name(self):
        self.kk = self.cat_dict()
        print (self.kk)
        a=int(input('请选择主类目：'))
        ws_name=self.kk[a]+'.xls'
        ws=xlrd.open_workbook(ws_name)
        ws_dic=dict(zip(range(len(ws.sheet_names())), ws.sheet_names()))
        print(ws_dic)
        b=int(input('请输入子类目'))
        wor_sheet=ws.sheet_by_index(b)
        return wor_sheet


if __name__=='__main__':
    get_list= Main()
    wssn=Main.get_sheet_name(get_list)
    print(wssn)


        
                





