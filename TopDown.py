# -*- coding:utf-8 -*-
# @Time    : 2018/5/17 14:51
# @Author  : leolee
# @File    : TopDown.py
#instruction：非终结符号均用<>包围
import sys
test = False
testdirectClear = False
testRecursiveClear = False
testGetFirstSet = False
testGetFollowSet = False

inputSentence = 'begin d;\n' \
                'd;\n' \
                's\n' \
                ';s\n' \
                ' end'
inputWenFa = "<P>->begin d;<X> end\n" \
             "<X>->d;<X>\n" \
             "<X>->s<Y>\n" \
             "<Y>->;s<Y>\n" \
             "<Y>->e"

#获取文法的定义集合
def getDef(string):
    # 预处理
    # 定义集合
    Def = {}
    # 非终结符号集合
    Vt = []
    for s in string.split('\n'):
        split = s.split('->')
        Vt1 = split[0][1:-1]
        if Vt1 not in Def.keys():
            Def[Vt1] = [split[1]]
            Vt.append(Vt1)
        else:
            Def[Vt1].append(split[1])
    return Def,Vt

#直接左递归的消除
#string 输入的定义
def directClear(string):
    result = ''
    wenfa = string.split("\n")
    #初始符号
    l = wenfa[0][wenfa[0].index('<')+1:wenfa[0].index('>')]
    #判断有无直接左递归
    flag = False
    #存放没有直接左递归的定义
    list0 = []
    #存放有直接左递归的定义
    list1 = []
    for a in wenfa:
        s = a.split("->")
        #存在直接左递归
        if s[1].startswith('<'+l+'>'):
            list1.append(s[1][s[1].index('>')+1:])
        #不存在
        else:
            list0.append(s[1])
    #有左递归处理
    if len(list1) != 0:
        for a in list0:
            if not a.__eq__('e'):
                result += '<'+l+'>->'+a+'<'+l+'1>'+'\n'
            else:
                result += '<'+l+'>->'+'<'+l+'1>'+'\n'
        for a in list1:
            result += '<'+l+'1>->'+a+'<'+l+'1>\n'
        result += '<'+l+'1>->e'
    else:
        result = string
    return result

# <editor-fold desc="测试直接左递归部分">
if testdirectClear and test:
    testinput1 = "<A>-><A>c\n" \
                "<A>->b"
    testinput2 = "<T>->(<T>)\n" \
                 "<T>->a\n" \
                 "<T>->e\n" \
                 "<T>-><T>,(<T>)\n" \
                 "<T>-><T>,a\n" \
                 "<T>-><T>,"
    print directClear(testinput2)
    print "--------------直接左递归-----------------"
# </editor-fold>

#消除左递归
#string 输入的文法
#startL 开始符号
def recursiveClear(string,startL):
    #预处理
    #定义集合
    Def = {}
    #非终结符号集合
    Vt = []
    #去除左递归以后出现的新的非终结符号
    newVt = []
    # for s in string.split('\n'):
    #     split = s.split('->')
    #     Vt1 = split[0][1:-1]
    #     if Vt1 not in Def.keys():
    #         Def[Vt1] = [split[1]]
    #         Vt.append(Vt1)
    #     else:
    #         Def[Vt1].append(split[1])
    Def,Vt = getDef(string)
    for i in range(len(Vt)):
        for j in range(i):
            temp = []
            for k in range(len(Def[Vt[i]])):
                if Def[Vt[i]][k].startswith('<'+Vt[j]+'>'):
                    end = Def[Vt[i]][k][Def[Vt[i]][k].index('>')+1:]
                    for l in Def[Vt[j]]:
                        if not l.__eq__('e'):
                            temp.append(l+end)
                        else:
                            temp.append(end)
                else:
                    temp.append(Def[Vt[i]][k])
            Def[Vt[i]] = temp
        result = ''
        for m in Def[Vt[i]]:
            result += '<'+Vt[i]+'>->'+m+'\n'
        result = result[:-1]
        result = directClear(result)
        del Def[Vt[i]]
        Def[Vt[i]] = []
        results = result.split('\n')
        for m in results:
            aaa = m.split('->')
            bbb = aaa[0][1:aaa[0].index(">")]
            if(aaa[0].__eq__('<'+Vt[i]+'>')):
                Def[Vt[i]].append(aaa[1])
            else:
                if bbb not in newVt:
                    Def[bbb] = [aaa[1]]
                    newVt.append(bbb)
                else:
                    Def[bbb].append(aaa[1])
    #去除多余规则
    ruleSet = [startL]
    rulequeue = [startL]
    while len(rulequeue)>0:
        now = rulequeue[0]
        del rulequeue[0]
        for a in Def[now]:
            tmpL = a.find("<")
            tmpR = a.find(">")
            tmp = ''
            if tmpL != -1 and tmpR != -1:
                tmp = a[tmpL+1:tmpR]
                if tmp not in ruleSet:
                    ruleSet.append(tmp)
                    rulequeue.append(tmp)

    #输出文法
    output = ''
    for i in ruleSet:
        for j in Def[i]:
            output += '<'+i+'>->'+j+'\n'
    output = output[:-1]
    return output

# <editor-fold desc="测试消除左递归部分">
if testRecursiveClear and test:
    testwenfa = "<S>-><Q>c\n" \
                "<S>->c\n" \
                "<Q>-><R>b\n" \
                "<Q>->b\n" \
                "<R>-><S>a\n" \
                "<R>->a"
    print recursiveClear(testwenfa,'S')
    print "-------------消除左递归------------"
# </editor-fold>

#切分定义语句
def clip(declare):
    declare2 = declare
    lens = len(declare)
    i = 0
    clips = []
    j = 0
    while i < lens:
        if declare[i].__eq__('<'):
            clips.append('')
            i += 1
            while not declare[i].__eq__('>'):
                clips[j] += declare[i]
                i += 1
            i += 1
            j += 1
            continue
        else:
            clips.append('')
            while i < lens and not declare[i].__eq__('<'):
                clips[j] += declare[i]
                i += 1
            j += 1
    return clips

#list求集合并删除’e'
def union(list1,list2):
    tmplist = list1
    flag = False
    for i in list2:
        if i not in list1 and not i.__eq__('e'):
            tmplist.append(i)
            flag = True
    return tmplist,flag

#list求集合
def union2(list1,list2):
    tmplist = list1
    flag = False
    for i in list2:
        if i not in list1:
            tmplist.append(i)
            flag = True
    return tmplist,flag


#构造文法的FIRST集合
#string 输入的文法
def getFirstSet(string):
    # 预处理
    # 定义集合
    Def = {}
    # 非终结符号集合
    Vt = []
    #终结符号集合
    Vn = []
    Def,Vt = getDef(string)
    firstSet = {}
    for i in Vt:
        firstSet[i] = []
    #构造first集合，直到收敛
    changeFlag = True
    while changeFlag:
        changeFlag = False
        tmpflag = True
        for i in range(len(Vt)):
            for j in range(len(Def[Vt[i]])):
                declare = Def[Vt[i]][j]
                declare2 = clip(declare)
                VnFlag = True
                lens = len(declare2)
                k = 0
                while VnFlag:
                        if declare2[k] in Vt:
                            if 'e' not in firstSet[declare2[k]]:
                                VnFlag = False
                                firstSet[Vt[i]],tmpflag = union(firstSet[Vt[i]],firstSet[declare2[k]])
                                changeFlag = changeFlag or tmpflag
                            else:
                                firstSet[Vt[i]],tmpflag = union(firstSet[Vt[i]],firstSet[declare2[k]])
                                changeFlag = changeFlag or tmpflag
                        else:
                            VnFlag = False
                            firstSet[Vt[i]],tmpflag = union(firstSet[Vt[i]], [declare2[k]])
                            changeFlag = changeFlag or tmpflag
                        k += 1
    return firstSet

# <editor-fold desc="测试求First集合">
if test and testGetFirstSet:
    print getFirstSet(inputWenFa)
pass
# </editor-fold>

#构造文法的FOLLOW集合
#string 输入的文法
#s 开始符号
#firstSet:FIRST集合
def getFollowSet(string,s,firstSet):
    followSet = {}
    #定义
    Def = {}
    #非终结符号集合
    Vn = []
    Def,Vn = getDef(string)
    for i in Vn:
        followSet[i] = []
    followSet[s].append('#')
    changeFlag = True
    while changeFlag:
        changeFlag = False
        tmpflag = True
        for i in range(len(Vn)):
            for j in range(len(Def[Vn[i]])):
                declear = clip(Def[Vn[i]][j])
                for k in range(len(declear)-1,-1,-1):
                    if declear[k] in Vn:
                        if k == len(declear)-1:
                            followSet[declear[k]],tmpflag = union(followSet[declear[k]],followSet[Vn[i]])
                            changeFlag = changeFlag or tmpflag
                        else:
                            VtFlag = False
                            i = 1
                            while not VtFlag:
                                VtFlag = True
                                if i+k >= len(declear):
                                    VtFlag = False
                                    break
                                if declear[k+i] not in Vn:
                                    followSet[declear[k]],tmpflag = union(followSet[declear[k]],[declear[k+i]])
                                    changeFlag = changeFlag or tmpflag
                                else:
                                    if 'e' not in firstSet[declear[k+i]]:
                                        followSet[declear[k]],tmpflag = union(followSet[declear[k]],firstSet[declear[k+i]])
                                        changeFlag = changeFlag or tmpflag
                                    else:
                                        followSet[declear[k]],tmpflag = union(followSet[declear[k]], firstSet[declear[k + i]])
                                        changeFlag = changeFlag or tmpflag
                                        VtFlag = False
                                        i += 1
                            if not VtFlag:
                                followSet[declear[k]],tmpflag = union2(followSet[declear[k]],followSet[Vn[i]])
                                changeFlag = changeFlag or tmpflag
    return followSet

# <editor-fold desc="测试求FOLLOW集合">
if test and testGetFollowSet:
    firstSet = getFirstSet(inputWenFa)
    print getFollowSet(inputWenFa,'P',firstSet)
pass
# </editor-fold>

#递归下降分析
current = ''
firstSet = {}
followSet = {}
Def = {}
Vn = []
#向前移动
def nextt():
    s = inputSentence.split("\n")
    global current
    if current.__eq__(''):
        current = s[0]
        return True
    else:
        ind = s.index(current)
        if ind+1<len(s):
            current = s[ind+1]
            return True
        else:
            return False

def firstt():
    s = inputSentence.split("\n")
    global current
    if current.__eq__(''):
        current = s[0]
        return True
    else:
        ind = s.index(current)
        if ind - 1 > 0:
            current = s[ind - 1]
            return True
        else:
            return False

#错误处理
def error():
    global current
    print "在" + current + "附近出现错误"
    sys.exit(1)

#递归下降
#st非终结符号
def digui(st):
    global current,firstSet,followSet,Def,Vn
    flag = nextt()
    if not flag:
        error()
    if current in firstSet[st]:
        for i in Def[st]:
            if i.startswith(current):
                declear = clip(i)[1:]
                for a in declear:
                    if a in Vn:
                        digui(a)
                    else:
                        flag = nextt()
                        if not flag:
                            error()
                        if a.__eq__(current):
                            if declear.index(a) == len(declear)-1:
                                return True
                            flag = nextt()
                            if not flag:
                                error()
                        else:
                            error()
                break
    elif current in followSet[st]:
        firstt()
        return True
    else:
        error()


if __name__ == '__main__':
    newWenfa = recursiveClear(inputWenFa,"P")
    firstSet = getFirstSet(newWenfa)
    followSet = getFollowSet(newWenfa,"P",firstSet)
    Def,Vn = getDef(newWenfa)
    digui("P")
    print "分析成功"