import re

#flag———————————————————————————————
#待处理的文本
main_file = '待处理词库.txt'
#文本编码
encode = 'utf-8'
#是否要自动调频
autoWeight = False
defaultWeight = 1
#出现相同编码的汉字，如果出现权重冲突，选择权重相加模式还是取大值
weightPlusMode = False
#输出格式，默认为rime格式
printCraft = 'rime'
#默认为小鹤双拼
codeCraft = 'doublepy'
#默认扩展名是txt
file_exp = '.txt'
file_name = '输出_词库'
#默认换行格式
file_splitlines = '\n'
#如果是双拼，是否输出空格
doublepy_space = True
space_stuff = ' '
#是否重编码
reCode = False
#是否增加辅助码
mul_wubi = True#多重形码
wubiCode = True
wubiSplit = '['
#是否输出错误日志
error_log = False
error_print = True
simple_relookWubi = False
#分散打印还是分开打印
ffsj = False

#加载字库-----------------------------------------------------------
#辅助码反查
if wubiCode:
    relook_wubi_file = open("辅助码反查.txt",'r', encoding=encode)
    relook_wubi_date = relook_wubi_file.read().splitlines()
    relook_wubi_file.close()
#单字重编码反查
if reCode:
    relook_recode_file = open("单字反查.txt",'r', encoding=encode)
    relook_recode_date = relook_recode_file.read().splitlines()
    relook_recode_file.close()
#字频反查
if autoWeight:
    relook_weight_6763_file = open("6763字频.txt",'r', encoding=encode)
    relook_weight_6763_date = relook_weight_6763_file.read().splitlines()
    relook_weight_6763_file.close()
    
    relook_weight_file = open("字频反查.txt",'r', encoding=encode)
    relook_weight_date = relook_weight_file.read().splitlines()
    relook_weight_file.close()
#待处理的来源词库
date_file= open(main_file,'r', encoding=encode)
date = date_file.read().splitlines()
date_file.close()


#分拣字库——————————————————————————————
#反查
relookWubi = {}
relookRecode = {}
relookWeight6763 = {}
relookWeight = {}
#双拼单字
singleChracter = {}
#其他类型单字
singleChracterOther = {}
#简码
easyCode = {}
easyCode2 = {}
#词库
word2 = {}
word2Other = {}
word3 = {}
word3Other = {}
wordMore = {}
wordMoreOther = {}
#超级简拼
phraseWord = {}
#正则
pat_code = re.compile(r'[a-zA-Z;_\']+')
pat_chracter = re.compile(r'[^a-z,A-Z,\t,\d,\n,\s,%,\[]+')
pat_chracter_weight = re.compile(r'[\d]+')

#加载字库
def load():
    print('加载词库中……')
    
    #加载辅助码
    if wubiCode:
        print('加载反查词库中：')
        for i in relook_wubi_date:
            try:
                chracter = pat_chracter.search(i).group(0)
                code = pat_code.search(i).group(0)
                #print('\r','%s\t%s'%(chrater,code),end='',flush=True)
                insert_dic(relookWubi,chracter,code)
            except:
                print('fail loading',i)
        print('完成。')
        
    #加载重编码
    if reCode:
        print('加载重编码单字词库：')
        for i in relook_recode_date:
            chracter = pat_chracter.search(i).group(0)
            code = pat_code.search(i).group(0)
            insert_dic(relookRecode,chracter,code)
        print('完成。')
        
    #加载字频
    if autoWeight:
        print('加载字频权重：')
        for i in relook_weight_date:
            chracter = pat_chracter.search(i).group(0)
            code = pat_code.search(i).group(0)
            weight = pat_chracter_weight.search(i).group(0)
            insert_dic(relookWeight,chracter,code,weight)
        for i in relook_weight_6763_date:
            chracter = pat_chracter.search(i).group(0)
            weight = pat_chracter_weight.search(i).group(0)
            insert_dic(relookWeight6763,chracter,'',weight)
        print('完成。')

    #加载待处理的来源字库
    print('加载待处理字库中……')
    for i in date:
        try:
            chracter = pat_chracter.search(i).group(0)
            code = pat_code.search(i).group(0)
            try:
                if reCode:
                    if len(chracter) == 1:
                         code = relook_recode(chracter,code)
            except:
                if error_print:
                    print('%s重编码失败'%(chracter))
                if error_log:
                    print_dic((chracter,code,defaultWeight),'重编码失败____error')#写入——————————
            try:
                if autoWeight:
                    try:
                        weight = relook_6763_weight(chracter,code)
                    except:
                        weight = relook_weight(chracter,code)
                else:
                    try:
                        weight = pat_chracter_weight.search(i).group(0)
                    except:
                        weight = defaultWeight
            except:
                if error_print:
                    print('%s未查询到字频'%(chracter))
                weight = pat_chracter_weight.search(i).group(0)
                if error_log:
                    print_dic((chracter,code,weight),'未查询到字频____error')#写入——————————
                weight = defaultWeight
        except:
            print('待处理字库加载失败%s'%(i))
        #送入分拣器
        sorting(chracter,code,weight)
    print('完成。')
    return True

#插入字典条目
def insert_dic(dic,chracter,code,weight=defaultWeight):
    #如果插入的字典是五笔字典
    #if dic == relookWubi:
     #   try:
      #      for i in range(len(dic[chracter])):
       #         if simple_relookWubi:
        #            if len(code) <= len(dic[chracter][i][0]):
        #                if dic[chracter][i][0][0:len(code)]  != code:
     #                       dic[chracter].append((code,int(weight)))
      #              else:
       #                 if code[0:len(dic[chracter][i][0])]  != dic[chracter][i][0]:
        #                    dic[chracter].append((code,int(weight)))
         #               else:
          #                  dic[chracter][i][0] = code
           #     else:
           #         dic[chracter].append((code,int(weight)))
      #  except:
       #     dic[chracter] = [(code,int(weight))]
    #return True
    try:
        for i in range(len(dic[chracter])):
            #如该码已经存在
            if dic[chracter][i][0] == code:
                if weightPlusMode:
                    dic[chracter][i][1] += weight
                else:
                    if dic[chracter][i][1] < weight:
                        dic[chracter][i][1] = weight
                return True
        dic[chracter].append([code,int(weight)])
    except:
        dic[chracter] = [[code,int(weight)]]
        return True
    
#查询辅助码
def relook_wubi(chracter,code=''):
    if len(chracter) == 1:
        if mul_wubi:
            return relookWubi[chracter]
        else:
            return [(relookWubi[chracter][0][0],defaultWeight)]
    else:
        pass


#查询字频权重
def relook_weight(chracter,code=''):
    weight = defaultWeight
    for i in relookWeight[chracter]:
        if code == i[0]:
            weight = i[1]
            break
        else:
            if i[1] > weight:
                weight = i[1]
    return weight

#查询字频权重
def relook_6763_weight(chracter,code=''):
    if relook_recode(chracter)[0][0] == code:
        weight = defaultWeight
        for i in relookWeight6763[chracter]:
            weight = i[1]
    else:
        weight = relook_weight(chracter,code)
    return weight

#查询单字重编码
def relook_recode(chracter,code=''):
    try:
        if len(chracter) == 1:
            for i in relookRecode[chracter]:
                if code == i[0]:
                    return code
                else:
                    pass
            return relookRecode[chracter]
        else:
            pass
    except:
        if error_print:
            print('%s未查询到重编码'%(chracter))
        if error_log:
            print_dic((chracter,code,defaultWeight),'未查询到重编码____error')#写入——————————
        return code

#添加空格同辅助码
def add_space_wubi(chracter,code):
    code_len = len(code)
    res_list = []
    if code_len == (len(chracter)*2):
        res = ''
        #如果字数大于2
        if code_len>=4:
            segment_code = []
            #编码首编码
            first_new_code = []
            #code加上辅助码后的片段
            segment_new_code = []
            #code加上辅助码后的片段的转存
            res_new_code = []
            res = ''
            for i in range(2,code_len+2,2):
                segment_code = code[(i-2):i]
                if wubiCode:
                    postion = int((i-2)/2)
                    chracter_i = chracter[postion]
                    #如果字数大于4--------------------------------------------------------------
                    if code_len >=6:
                        time = str(i/2)
                        #---------------------------------------------------------------------------
                        res += segment_code + wubiSplit + relook_wubi(chracter_i)[0][0]
                        if doublepy_space:
                                res += space_stuff
                        if i == code_len:
                            res_list.append(res)
                            return res_list
                    #如果字数小于4
                    else:
                        for wubi_i in relook_wubi(chracter_i):
                            time = str(i/2)
                            #---------------------------------------------------------------------------
                            new_code = segment_code + wubiSplit + wubi_i[0]
                            if doublepy_space:
                                new_code+=space_stuff
                            if i == 2:
                                first_new_code.append(new_code)
                            else:
                                for first_new_code_i in  first_new_code:
                                    tempt_code = first_new_code_i+new_code
                                    segment_new_code.append(tempt_code)
                                for segment_new_code_i in segment_new_code:
                                    res_new_code.append(segment_new_code_i)
                                segment_new_code = []
                                if wubi_i == relook_wubi(chracter_i)[len(relook_wubi(chracter_i))-1]:
                                    first_new_code = res_new_code
                                    res_new_code = []
                                    if i == code_len:
                                         res_list = first_new_code
                                         return res_list
                #如果的不用加五笔
                else:
                    if doublepy_space:
                        res = res + segment_code + space_stuff
                        if i == code_len:
                            res_list.append(res)
                            return res_list
                    else:
                        res = code
                        res_list.append(res)
                        return res_list
        else:
            if wubiCode:
                relook_wubi_i = relook_wubi(chracter)
                if type(relook_wubi_i) == list:
                    for wubi_i in relook_wubi_i:
                        res = code + wubiSplit + wubi_i[0]
                        if doublepy_space:
                                    res+=space_stuff
                        res_list.append(res)
                elif type(relook_wubi_i) == str:
                    res = code + wubiSplit + relook_wubi_i
                    if doublepy_space:
                        res+=space_stuff
                    res_list.append(res)
            else:
                res = code
                if doublepy_space:
                    res+=space_stuff
                res_list.append(res)
    else:
        res = code
        res_list.append(res)
    return res_list

#双拼分拣过滤装置
def sorting(chracter,code,weight=defaultWeight):
    if type(code) == list:
        for code_i in code:
            sorting(chracter,code_i[0],weight)
        return True
    code_len = len(code)
    try:
        code = add_space_wubi(chracter,code)
    except:
        if error_print:
            print('%s %s编码调整失败'%(chracter,code))
        if error_log:
            print_dic((chracter,code,weight),'编码调整失败____date')#写入——————————
        return False
    if type(code) == list:
        for code_i in code:
            sorting_insert(chracter,code_i,code_len,weight)
    else:
        sorting_insert(chracter,code,code_len,weight)
    
def sorting_insert(chracter,code,code_len,weight=defaultWeight):
    #code = code[0:2]
    #if code[0:2] != 'ob':
    #    return True
    #print('\r','%s\t%s'%(chracter,code),end='',flush=True)
    if len(chracter) == 1:
        if code_len == 1:
            insert_dic(easyCode,chracter,code,weight)
        elif code_len == 2:
            insert_dic(singleChracter,chracter,code,weight)
        else:
            insert_dic(singleChracterOther,chracter,code,weight)
    elif len(chracter) == 2:
        if code_len < 4:
            insert_dic(easyCode2,chracter,code,weight)
        elif code_len == 4:
            insert_dic(word2,chracter,code,weight)
        elif code_len > 4:
            insert_dic(word2Other,chracter,code,weight)
    elif len(chracter) == 3:
        if code_len < 6:
            insert_dic(phraseWord,chracter,code,weight)
        elif code_len == 6:
            insert_dic(word3,chracter,code,weight)
        elif code_len > 6:
            insert_dic(word3Other,chracter,code,weight)
    else:
        if code_len < (len(chracter)*2):
            insert_dic(phraseWord,chracter,code,weight)
        elif code_len == (len(chracter)*2):
            insert_dic(wordMore,chracter,code,weight)
        elif code_len > (len(chracter)*2):
            insert_dic(wordMoreOther,chracter,code,weight)
    return True
            
#最终的输出格式-----------------------------------------------------------------------
def res_form(chracter,code,weight=defaultWeight):
    if printCraft == 'rime':
        return '%s\t%s\t%s'%(chracter,code,str(weight))
    elif printCraft == 'rime_梨子':
        code = code.replace("xm[g ","XG[ ")
        code = code.replace("ui[p ","UP[ ")
        code = code.replace("jb[wc ","JW[ ")
        code = code.replace("zi[p ","ZP[ ")
        code = code.replace("ji[e ","JE[ ")
        code = code.replace("vs[tkh ","OT[ ")
        code = code.replace("rf[wt ","RW[ ")
        code = code.replace("mw[vfi ","MV[ ")
        code = code.replace("ww[o ","WY[ ")
        code = code.replace("he[tk ","HT[ ")
        code = code.replace("wh[m ","WM[ ")
        code = code.replace("zi[b ","ZB[ ")
        code = code.replace("aa[b ","AB[ ")
        code = code.replace("ui[jf ","UJ[ ")
        code = code.replace("wu[tr ","WT[ ")
        code = code.replace("fg[","FS[")
        code = code.replace("vw[","OW[")
        code = code.replace("ve[","OE[")
        code = code.replace("vr[","OR[")
        code = code.replace("va[","OA[")
        code = code.replace("vs[","OS[")
        code = code.replace("vd[","OD[")
        code = code.replace("vf[","OF[")
        code = code.replace("vz[","OZ[")
        code = code.replace("vx[","OX[")
        code = code.replace("vc[","OC[")
        code = code.replace("vv[","OV[")
        code = code.replace("vg[","OG[")
        code = code.replace("ao[","AC[")
        code = code.replace("ah[","AM[")
        code = code.replace("aj[","AN[")
        code = code.replace("uy[","AY[")
        code = code.replace("uu[","AU[")
        code = code.replace("ui[","US[")
        code = code.replace("uo[","AO[")
        code = code.replace("uh[","AH[")
        code = code.replace("uj[","AJ[")
        code = code.replace("uk[","AK[")
        code = code.replace("ul[","AL[")

        code = code.replace("yy[","EY[")
        code = code.replace("yu[","EU[")
        code = code.replace("yi[","EI[")
        code = code.replace("yo[","EO[")
        code = code.replace("yh[","EH[")
        code = code.replace("yj[","EJ[")
        code = code.replace("yk[","EK[")

        code = code.replace("ei[","EW[")
        code = code.replace("eh[","EM[")

        # code = code.replace("iy[","EY[")
        # code = code.replace("iu[","EU[")
        # code = code.replace("ii[","EI[")
        # code = code.replace("io[","EO[")
        # code = code.replace("ih[","EH[")
        # code = code.replace("ij[","EJ[")
        # code = code.replace("ik[","EK[")
        # code = code.replace("il[","EL[")
        code = code.lower()
        if weight != 1:
            weight = str(weight) + '%'
            res_code = '%s\t%s\t%s'%(chracter,code,str(weight))
            res_code = res_code.replace(" 	","	")
            return res_code
        else:
            res_code = '%s\t%s\t'%(chracter,code)
            res_code = res_code.replace(" 	","	")
            return res_code
    elif printCraft == '纯汉字':
        return '%s'%(chracter)
    elif printCraft == '搜狗细胞词库':
        pass
    elif printCraft == '百度输入法':
        pass
    elif printCraft == '微软快捷短语':
        pass
    elif printCraft == '正则运算式':
        return '- derive/^(%s)%s(%s)%s$/$1$2/   #%s'%(code[0],code[1:2],code[3],code[4:(len(code)-1)],chracter)
    elif printCraft == 'other':
        pass

#拆分字典格式，便于输出
def transeform_dic(dic):
    result = []
    for charcter in dic.keys():
        for i in dic[charcter]:
            result.append(res_form(charcter,i[0],i[1]))
    return result

#打印字典
def print_dic(dic,file_name=file_name):
    file_name = file_name+file_exp
    file_handle=open(file_name,mode='a',encoding=encode)
    try:
        if type(dic[0]) == str and len(dic) == 3:
            tempt_dic = {}
            tempt_dic[dic[0]]=[(dic[1],dic[2])]
            dic = transeform_dic(tempt_dic)
    except:
        pass
    if type(dic) == dict:
        dic = transeform_dic(dic)
    else:
        pass
    for i in dic:
        file_handle.write(i)
        file_handle.write(file_splitlines)
    callback = file_handle.close()
    return True

#打印全部字典 
def printer():
    print('正在打印')
    if ffsj == True:
        print_dic(singleChracter)
        print_dic(singleChracterOther,'other')
        print_dic(word2)
        print_dic(word2Other,'else')
        print_dic(word3)
        print_dic(word3Other,'else')
        print_dic(wordMore)
        print_dic(wordMoreOther,'else')
        
        print_dic(transeform_dic(easyCode),'easyCode_1')
        print_dic(transeform_dic(easyCode2),'easyCode2')
        print_dic(transeform_dic(phraseWord),'phraseWord')
    else:
        print_dic(singleChracter)
        print_dic(singleChracterOther)
        print_dic(word2)
        print_dic(word2Other)
        print_dic(word3)
        print_dic(word3Other)
        print_dic(wordMore)
        print_dic(wordMoreOther)
        
        print_dic(transeform_dic(easyCode))
        print_dic(transeform_dic(easyCode2))
        print_dic(transeform_dic(phraseWord))

    try:
        pass
    except:
        pass

#主进程——————————————————————————————
def main():
    print('处理器1.0 —— by lizi')
    print('仅支持繁体，不支持带英文的词组如：U盘')
    load()
    printer()
    return True

if main():
    input('处理完成、输入任意键退出：')
