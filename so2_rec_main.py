import tkinter as tk
from tkinter import ttk
import pickle

class ComboSet(tk.Frame):
    def __init__(self,master=None,entname=None,xpos=None,ypos=None,workdict=None,nowworking=None):
        tk.Frame.__init__(self,master)
        self.label = tk.Label(master,text=entname,width=20)
        if nowworking is None:
            self.combobox = ttk.Combobox(master,state='readonly',postcommand=lambda:self.UpdateBox1(workdict))
        else:
            self.combobox = ttk.Combobox(master,state='readonly',postcommand=lambda:self.UpdateBox2(nowworking))
        self.label.grid(row=ypos+1,column=xpos)
        self.combobox.grid(row=ypos+2,column=xpos)
    def UpdateBox1(self,workdict):
        self.combobox['values'] = tuple(workdict.keys())
    def UpdateBox2(self,nowworking):
        tmplist = []
        for i,x in enumerate(nowworking):
            worktypetmp = x['作業名']
            repeatnumtmp = x['回数']
            tmpstr = str(i)+':'+str(worktypetmp)+':'+str(repeatnumtmp)+"回"
            tmplist.append(tmpstr)
        self.combobox['values'] = tuple(tmplist)

class EntrySet(tk.Frame):
    def __init__(self,master=None,entname=None,xpos=None,ypos=None):
        tk.Frame.__init__(self,master)
        self.label = tk.Label(master,text=entname,width=20)
        self.entry = tk.Entry(master)
        self.label.grid(row=ypos+1,column=xpos)
        self.entry.grid(row=ypos+2,column=xpos)

class ScalableEntrySet(tk.Frame):
    def __init__(self,master=None,entname=None,xpos=None,ypos=None):
        tk.Frame.__init__(self,master)
        self.entrylist = []
        self.label = tk.Label(master,text=entname,width=20)
        self.addbutton = tk.Button(master,text='+',height=1,command=lambda:self.AddEntry(master,xpos,ypos))
        self.removebutton = tk.Button(master,text='-',height=1,command=lambda:self.RemoveEntry())
        self.label.grid(row=ypos+1,column=xpos,columnspan=2)
        self.addbutton.grid(row=ypos,column=xpos)
        self.removebutton.grid(row=ypos,column=xpos+1)
    def AddEntry(self,master,xpos,ypos):
        self.entrylist.append(tk.Entry(master))
        listlen = len(self.entrylist) -1
        self.entrylist[listlen].grid(row=int(listlen+ypos+2),column=xpos,columnspan=2)
        print('addentry_pushed')
    def RemoveEntry(self):
        try:
            listlen = len(self.entrylist) -1
            self.entrylist[listlen].destroy()
            self.entrylist.pop()
            print('removeentry_pushed')
        except:
            print('removeentry not worked')

class ItemEntrySet(tk.Frame):
    def __init__(self,master=None,entname1=None,entname2=None,xpos=None,ypos=None):
        tk.Frame.__init__(self,master)
        self.namenumset = []
        self.x = 0
        self.namelabel = tk.Label(master,text=entname1,width=20)
        self.numlabel = tk.Label(master,text=entname2,width=20)
        self.addbutton = tk.Button(master,text='+',height=1,command=lambda:self.AddEntry(master,xpos,ypos))
        self.removebutton = tk.Button(master,text='-',height=1,command=lambda:self.RemoveEntry())
        self.addbutton.grid(row=ypos,column=xpos)
        self.removebutton.grid(row=ypos,column=xpos+1)
        self.namelabel.grid(row=ypos+1,column=xpos)
        self.numlabel.grid(row=ypos+1,column=xpos+1)
    def AddEntry(self,master,xpos,ypos):
        self.namenumset.append([tk.Entry(master), tk.Entry(master)])
        listlen = len(self.namenumset) -1
        self.namenumset[listlen][0].grid(row=int(listlen+ypos+2),column=xpos)
        self.namenumset[listlen][1].grid(row=int(listlen+ypos+2),column=xpos+1)
        print('addentry_pushed')
    def RemoveEntry(self):
        try:
            listlen = len(self.namenumset) -1
            self.namenumset[listlen][0].destroy()
            self.namenumset[listlen][1].destroy()
            self.namenumset.pop()
            print('removeentry_pushed')
        except:
            print('removeentry not worked')



class AddWorkType(tk.LabelFrame):
    def __init__(self,master=None,workdict=None):
        tk.LabelFrame.__init__(self,master,text='作業追加')
        self.nameset = EntrySet(self,entname='作業名',xpos=0,ypos=0)
        self.inoutset = EntrySet(self,entname='屋内/屋外',xpos=1,ypos=0)
        self.jobtypeset = EntrySet(self,entname='職種/業種',xpos=2,ypos=0)
        self.sucupset = ScalableEntrySet(self,entname='成功率アップ条件',xpos=3,ypos=0)
        self.gainupset = ScalableEntrySet(self,entname='獲得量アップ条件',xpos=5,ypos=0)
        self.needtimeset = EntrySet(self,entname='必要時間',xpos=7,ypos=0)
        self.needitemset = ItemEntrySet(self,entname1='必要アイテム',entname2='数量',xpos=8,ypos=0)
        self.gettableset = ScalableEntrySet(self,entname='獲得可能アイテム',xpos=10,ypos=0)
        self.entrybutton = tk.Button(self,text='登録',command=lambda:self.AddWorkTypeToDict(workdict)).grid(row=0,column=12)
        self.entrybutton = tk.Button(self,text='test',command=lambda:self.Test(workdict)).grid(row=1,column=12)
    def AddWorkTypeToDict(self,workdict):
        workname=self.nameset.entry.get()
        workdict[workname] = {}
        workdict[workname]["屋内/屋外"] = self.inoutset.entry.get()
        workdict[workname]["業種/職種"] = self.jobtypeset.entry.get()
        workdict[workname]["成功率アップ条件"] = []
        for x in self.sucupset.entrylist:
            workdict[workname]["成功率アップ条件"].append(x.get())
        workdict[workname]["獲得量アップ条件"] = []
        for x in self.gainupset.entrylist:
            workdict[workname]["獲得量アップ条件"].append(x.get())
        workdict[workname]["作業時間"] = self.needtimeset.entry.get()
        workdict[workname]["必要アイテム"] = {}
        for x,y in self.needitemset.namenumset:
            workdict[workname]["必要アイテム"][x.get()] = y.get()
        workdict[workname]["獲得可能アイテム"] = []
        for x in self.gettableset.entrylist:
            workdict[workname]['獲得可能アイテム'].append(x.get())
        workdict[workname]["作業データ"] = []

    def Test(self,workdict):
        print(workdict)
        print(tuple(workdict.keys()))

class AddGettable(tk.LabelFrame):
    def __init__(self,master=None,workdict=None):
        tk.LabelFrame.__init__(self,master,text='獲得可能アイテム追加')
        self.worklist = ComboSet(self,entname='作業名',xpos=0,ypos=0,workdict=workdict)
        self.gettableset = ScalableEntrySet(self,entname='獲得可能アイテム',xpos=1,ypos=0)
        self.entrybutton = tk.Button(self,text='追加',command=lambda:self.EntryGettable(workdict)).grid(row=0,column=3)
        self.entrybutton2 = tk.Button(self,text='test',command=lambda:self.Test(workdict)).grid(row=1,column=3)
    def Test(self,workdict):
        print(workdict)
        print(tuple(workdict.keys()))
        print(self.worklist.combobox.get())
    def EntryGettable(self,workdict=None):
        workname = self.worklist.combobox.get()
        for x in self.gettableset.entrylist:
            workdict[workname]['獲得可能アイテム'].append(x.get())

class AddLostData(tk.LabelFrame):
    def __init__(self,master=None,workdict=None,nowworking=None):
        tk.LabelFrame.__init__(self,master,text='作業開始時入力')
        self.worklist = ComboSet(self,entname='作業名',xpos=0,ypos=0,workdict=workdict)
        self.workset = tk.Button(self,command=lambda:self.SetWork(worktype=self.worklist.combobox.get(),workdict=workdict),text='set').grid(row=4,column=0)
        self.repeatnum = EntrySet(self,entname='回数',xpos=1,ypos=0)
        self.lostitemset = ItemEntrySet(self,entname1='消耗アイテム',entname2='数量',xpos=2,ypos=0)
        self.entrybutton = tk.Button(self,text='登録',command=lambda:self.EntryNowWork(nowworking)).grid(row=0,column=4)
        self.entrybutton2 = tk.Button(self,text='test',command=lambda:self.Test(workdict)).grid(row=1,column=4)
    def Test(self,workdict):
        print(workdict)
        print(tuple(workdict.keys()))
        print(self.worklist.combobox.get())
    def SetWork(self,worktype=None,workdict=None):
        print(worktype)
        print(workdict[worktype]['必要アイテム'].keys())
        for itemname in workdict[worktype]['必要アイテム'].keys():
            print(itemname)
            self.lostitemset.AddEntry(self,xpos=2,ypos=0)
            self.lostitemset.namenumset[len(self.lostitemset.namenumset)-1][0].insert(tk.END,itemname)
    def EntryNowWork(self,nowworking=None):
        if (self.repeatnum.entry.get() != ''):
            tmpdict = {}
            tmpdict["作業名"] = self.worklist.combobox.get()
            tmpdict['回数'] = self.repeatnum.entry.get()
            self.repeatnum.entry.delete(0,tk.END)
            tmpdict["消費アイテム"] = {}
            for x,y in self.lostitemset.namenumset:
                tmpdict["消費アイテム"][x.get()] = y.get()
                y.delete(0,tk.END)
            nowworking.append(tmpdict)
            print(nowworking)
        else:
            print('回数が入力されていない')


class AddGetData(tk.LabelFrame):
    def __init__(self,master=None,workdict=None,nowworking=None):
        tk.LabelFrame.__init__(self,master,text='作業完了時入力')
        self.worklist = ComboSet(self,entname='作業名:回数',xpos=0,ypos=0,nowworking=nowworking)
        self.workset = tk.Button(self,command=lambda:self.SetWork(worktype=self.worklist.combobox.get().split(":")[1],workdict=workdict,nowworking=nowworking,repnum=self.worklist.combobox.get().split(":")[2].rstrip('回')),text='set').grid(row=4,column=0)
        self.repeatnum = EntrySet(self,entname='回数',xpos=1,ypos=0)
        self.sucupset = ItemEntrySet(self,entname1='成功率アップ条件',entname2='適正程度',xpos=2,ypos=0)
        self.gainupset = ItemEntrySet(self,entname1='獲得量アップ条件',entname2='適正程度',xpos=4,ypos=0)
        self.gotitemset = ItemEntrySet(self,entname1='獲得アイテム',entname2='数量',xpos=6,ypos=0)
        self.entrybutton = tk.Button(self,text='登録',command=lambda:self.EntryNowWork(nowworking=nowworking,workdict=workdict)).grid(row=1,column=8)
    def SetWork(self,worktype=None,workdict=None,nowworking=None,repnum=None):
        print(worktype)
        self.repeatnum.entry.insert(tk.END,repnum)
        for sucup in workdict[worktype]['成功率アップ条件']:
            print(sucup)
            self.sucupset.AddEntry(self,xpos=2,ypos=0)
            self.sucupset.namenumset[len(self.sucupset.namenumset)-1][0].insert(tk.END,sucup)
        for gainup in workdict[worktype]['獲得量アップ条件']:
            print(gainup)
            self.gainupset.AddEntry(self,xpos=4,ypos=0)
            self.gainupset.namenumset[len(self.gainupset.namenumset)-1][0].insert(tk.END,gainup)
        for gotitem in workdict[worktype]['獲得可能アイテム']:
            print(gotitem)
            self.gotitemset.AddEntry(self,xpos=6,ypos=0)
            self.gotitemset.namenumset[len(self.gotitemset.namenumset)-1][0].insert(tk.END,gotitem)
    def EntryNowWork(self,nowworking=None,workdict=None):
        tmpdict = {}
        tmpx = int(self.worklist.combobox.get().split(':')[0])
        workname = self.worklist.combobox.get().split(':')[1]
        tmpdict['回数'] = self.repeatnum.entry.get()
        tmpdict['成功率アップ条件適正程度'] = {}
        for x,y in self.sucupset.namenumset:
            tmpdict["成功率アップ条件適正程度"][x.get()] = y.get()
        tmpdict['獲得量アップ条件適正程度'] = {}
        for x,y in self.gainupset.namenumset:
            tmpdict["獲得量アップ条件適正程度"][x.get()] = y.get()
        tmpdict['消費アイテム'] = {}
        tmpdict['消費アイテム'] = nowworking[tmpx]['消費アイテム']
        tmpdict['獲得アイテム'] = {}
        for x,y in self.gotitemset.namenumset:
            tmpdict["獲得アイテム"][x.get()] = y.get()
        workdict[workname]['作業データ'].append(tmpdict)
        nowworking.pop(tmpx)
        print(workdict)


class MenuFrame(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master, relief='ridge',borderwidth=2)
        self.inputs = tk.Button(self,text='inputs',width=6).pack(side="left")
        self.outputs = tk.Button(self,text='outputs',width=6).pack(side="left")

class InputField(tk.LabelFrame):
    def __init__(self,master=None,workdict=None,nowworking=None):
        tk.LabelFrame.__init__(self,master, text='データ入力')
        self.add_work_type_field = AddWorkType(self,workdict)
        self.add_add_gettable_to_workdict_field = AddGettable(self,workdict)
        self.add_work_lost_data_field = AddLostData(self,workdict,nowworking)
        self.add_work_get_data_field = AddGetData(self,workdict,nowworking)
        self.savebutton = tk.Button(self,text='保存',command=lambda:self.PickleDatas(workdict=workdict,nowworking=nowworking))
        self.add_work_type_field.pack()
        self.add_add_gettable_to_workdict_field.pack()
        self.add_work_lost_data_field.pack()
        self.add_work_get_data_field.pack()
        self.savebutton.pack()

    def PickleDatas(self,workdict=None,nowworking=None):
        with open('datas.pkl','ab') as wf:
            pickle.dump((workdict,nowworking),wf)

class MainFrame(tk.Frame):
    def __init__(self,master=None,workdict=None,nowworking=None):
        tk.Frame.__init__(self, master)
        self.menuframe = MenuFrame(self)
        self.menuframe.pack()
        self.inputfield = InputField(self,workdict,nowworking)
        self.inputfield.pack()
try:
    with open('datas.pkl','rb') as rf:
        pickled = pickle.load(rf)
except:
    with open('datas.pkl','w') as wf:
        wf.write('')
        pickled = ({},[])
workdict = pickled[0]
nowworking = pickled[1]
mainframe = MainFrame(workdict=workdict,nowworking=nowworking)
mainframe.pack()
mainframe.mainloop()
