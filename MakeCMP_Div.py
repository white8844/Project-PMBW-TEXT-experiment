import GetCMP, GetDivision
import os,re

#批量构造CMP整体对比文本
def MakeCMP(jpdirpath,chdirpath,encoding = 'utf-16',mknewdir = False):
    jpfileslist = os.listdir(jpdirpath)
    chfileslist = os.listdir(chdirpath)
    jptxtfilelist = []
    chtxtfilelist = []
    for filepath in jpfileslist:
        if '.txt' in filepath:
            jptxtfilelist.append(filepath)
    for filepath in chfileslist:
        if '.txt' in filepath:
            chtxtfilelist.append(filepath)
    jp_ch_dict = {jptxtfilelist[i]:chtxtfilelist[i] for i in range(len(jptxtfilelist))}#方便批量构造CMP
    for jpfilepath in jp_ch_dict:
        chfilepath = chdirpath + "/"+ jp_ch_dict[jpfilepath]
        jpfilepath = jpdirpath + "/" + jpfilepath
        cmpfilepath = GetCMP.CMP(jpfilepath,chfilepath,encoding=encoding,mknewdir=mknewdir)
    finda = re.findall(r'(.*)/(.*)',cmpfilepath)
    CMP_path = finda[0][0]
    return CMP_path

#批量分片经由CPM处理过后的整体文本
def DivCMP(CMPdirpath,blocknums = 2,encoding = 'utf-16',mknewdir = False):
    if CMPdirpath[-1]!="/":#补充路径尾部缺失的/方便后续拼接操作
        CMPdirpath += "/"
    filelist = os.listdir(CMPdirpath)
    CMPlist = []
    for filepath in filelist:
        if ".txt" in filepath:
            if "CMP" in filepath:
                try:
                    int(filepath[0])
                except ValueError:#按命名规则，必须开头是CMP的才是可分片的整体文本
                    CMPlist.append(filepath)
    for CMPpath in CMPlist:
        CMPpath = CMPdirpath + CMPpath
        with open(CMPpath,"r",encoding='utf-16')as f:
            GetDivision.txtDivision_byBlock(f.readlines(), CMPpath, blocknums = blocknums,
                                            encoding=encoding,mknewdir = mknewdir)

#批量将分块文本重新组合复原
def Div_Restore(CMPdirpath,blocknums = 2,encoding = 'utf-16',fmnewdir = False):
    if CMPdirpath[-1]!="/":#补充路径尾部缺失的/方便后续拼接操作
        CMPdirpath += "/"
    filelist = os.listdir(CMPdirpath)
    CMPlist = []
    for filepath in filelist:
        if ".txt" in filepath:
            if "CMP" in filepath:
                try:
                    int(filepath[0])
                except ValueError:#按命名规则，必须开头是CMP的才是可分片的整体文本
                    CMPlist.append(filepath)
    for CMPpath in CMPlist:
        CMPpath = CMPdirpath + CMPpath
        GetDivision.txtCombine_byBlock(CMPpath,blocknums = blocknums,encoding = encoding,fmnewdir = fmnewdir)

#批量将CMP文本只保留翻译部分
def MakeCMP_TH(CMPdirpath,encoding = 'utf-16',mknewdir = False):
    if CMPdirpath[-1]!="/":#补充路径尾部缺失的/方便后续拼接操作
        CMPdirpath += "/"
    filelist = os.listdir(CMPdirpath)
    CMPlist = []
    for filepath in filelist:
        if ".txt" in filepath:
            if "CMP" in filepath:
                try:
                    int(filepath[0])
                except ValueError:#按命名规则，必须开头是CMP的才是可分片的整体文本
                    CMPlist.append(filepath)
    for CMPpath in CMPlist:
        CMPpath = CMPdirpath + CMPpath
        GetCMP.KeepTH(CMPpath,encoding = encoding,mknewdir = mknewdir)

if __name__ == "__main__":#This is just for code testing
    for i in range(2,4):
        num = str(i)
        nstr = num + '_extr'
        jpdir = 'B(JP)'
        chdir = 'B(CH)'
        jpdirpath = jpdir + nstr
        chdirpath = chdir + nstr
        blocknums = 2
        encoding = 'utf-16'
        CMPdirpath = MakeCMP(jpdirpath,chdirpath,encoding = encoding,mknewdir = True)
        DivCMP(CMPdirpath,blocknums = blocknums,encoding = encoding,mknewdir = True)
        Div_Restore(CMPdirpath,blocknums = blocknums,encoding = encoding,fmnewdir = True)
        MakeCMP_TH(CMPdirpath,encoding = encoding,mknewdir = True)
