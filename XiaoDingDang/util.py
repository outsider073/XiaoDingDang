from decimal import Decimal
from win32com import client as win32
import os


def NumChange(value):
    if not isinstance(value, (Decimal, str, int)):
        raise ValueError("Not a Decimal Number!")
        # 汉字金额字符定义
    dunit = ('角', '分')
    num = ('零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖')
    iunit = ['元', '拾', '佰', '仟', '万', '拾', '佰', '仟', '亿', '拾', '佰', '仟', '万', '拾', '佰', '仟']
    # 转换为Decimal，并截断多余小数
    if not isinstance(value, Decimal):
        value = Decimal(value).quantize(Decimal('0.01'))
    # 转化为字符串
    s = str(value)
    if len(s) > 19:
        raise ValueError('Too large value!')
    istr, dstr = s.split('.')  # 小数部分和整数部分分别处理
    istr = istr[::-1]  # 翻转整数部分字符串
    so = []  # 用于记录转换结果
    # 零
    if value == 0:
        return num[0] + iunit[0]

    haszero = False  # 用于标记零的使用
    if dstr == '00':
        haszero = True  # 如果无小数部分，则标记加过零，避免出现“圆零整”
    # 处理小数部分
    # 分
    if dstr[1] != '0':
        so.append(dunit[1])
        so.append(num[int(dstr[1])])
    else:
        so.append('整')  # 无分，则加“整”
    # 角
    if dstr[0] != '0':
        so.append(dunit[0])
        so.append(num[int(dstr[0])])
    elif dstr[1] != '0':
        so.append(num[0])  # 无角有分，添加“零”
        haszero = True  # 标记加过零了
    # 无整数部分
    if istr == '0':
        if haszero:  # 既然无整数部分，那么去掉角位置上的零
            so.pop()
        so.reverse()  # 翻转
        return ''.join(so)
    # 处理整数部分
    for i, n in enumerate(istr):
        n = int(n)
        if i % 4 == 0:  # 在圆、万、亿等位上，即使是零，也必须有单位
            if i == 8 and so[-1] == iunit[4]:  # 亿和万之间全部为零的情况
                so.pop()  # 去掉万
            so.append(iunit[i])
            if n == 0:  # 处理这些位上为零的情况
                if not haszero:  # 如果以前没有加过零
                    so.insert(-1, num[0])  # 则在单位后面加零
                    haszero = True  # 标记加过零了
            else:  # 处理不为零的情况
                so.append(num[n])
                haszero = False  # 重新开始标记加零的情况
        else:  # 在其他位置上
            if n != 0:  # 不为零的情况
                so.append(iunit[i])
                so.append(num[n])
                haszero = False  # 重新开始标记加零的情况
            else:  # 处理为零的情况
                if not haszero:  # 如果以前没有加过零
                    so.append(num[0])
                    haszero = True
                    # 最终结果
    so.reverse()
    return ''.join(so)


def DocumentConverter(template, output, mark_dict, visible=False):
    word = win32.gencache.EnsureDispatch("Word.Application")
    if not os.path.isfile(template):
        return False
    if os.path.isfile(output):
        os.remove(output)
    document = word.Documents.Open(template)
    word.Visible = visible
    word.DisplayAlerts = False
    for mark in mark_dict.keys():
        word.Selection.HomeKey(Unit=6)
        word.Selection.Find.Text = mark
        word.Selection.Find.Replacement.Text = mark_dict[mark]
        word.Selection.Find.MatchCase = True
        word.Selection.Find.Execute(Replace=2, Forward=2)
    document.SaveAs(output)
    word.Quit()
    return True


if __name__ == '__main__':
    print(NumChange(123000))
    print(NumChange('0.01'))
    print(NumChange(100000000))
    print(NumChange('124'))
    # DocumentConvertererter("D:\\test.docx", "D:\\test2.docx", {"@mark1": 123, "@mark2": "ABC"}, True)
