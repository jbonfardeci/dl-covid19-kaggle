import re
import json

def authors_to_list(s:str):
    def _trim(s):
        return re.sub("(^\s+|\s+$)", "", s)

    def _to_dict(s):
        if s.find(',') > -1:
            names = list( map(_trim, s.split(',')) )
            return {
                "first": names[1],
                "last": names[0]
            }

        return {
            "first": None,
            "last": _trim(s)
        }

    if s == None or len(_trim(s)) == 0:
        return []

    if s.find("[") > -1:
        lst = json.loads(s.replace('\'', '"'))
        return list( map(_to_dict, lst) )

    elif s.find(";") > -1:
        return list( map(_to_dict, s.split(';')) )
    else:
        return _to_dict(s)
    
    return s

s = "['Zhang, Dan', 'Lou, Xiuyu', 'Yan, Hao', 'Pan, Junhang', 'Mao, Haiyan', 'Tang, Hongfeng', 'Shu, Yan', 'Zhao, Yun', 'Liu, Lei', 'Li, Junping', 'Chen, Jiang', 'Zhang, Yanjun', 'Ma, Xuejun']"
s2 = "Cao, Yanan; Li, Lin; Feng, Zhimin; Wan, Shengqing; Huang, Peide; Sun, Xiaohui; Wen, Fang; Huang, Xuanlin; Ning, Guang; Wang, Weiqing"
s3 = "McCall, Becky"
s4 = "['Yang, Haitao', 'Xie, Weiqing', 'Xue, Xiaoyu', 'Yang, Kailin', 'Ma, Jing', 'Liang, Wenxue', 'Zhao, Qi', 'Zhou, Zhe', 'Pei, Duanqing', 'Ziebuhr, John', 'Hilgenfeld, Rolf', 'Yuen, Kwok Yung', 'Wong, Luet', 'Gao, Guangxia', 'Chen, Saijuan', 'Chen, Zhu', 'Ma, Dawei', 'Bartlam, Mark', 'Rao, Zihe']"
s5 = "['Yang, Haitao', 'Xie, Weiqing', 'Xue, Xiaoyu', 'Yang, Kailin', 'Ma, Jing', 'Liang, Wenxue', 'Zhao, Qi', 'Zhou, Zhe', 'Pei, Duanqing', 'Ziebuhr, John', 'Hilgenfeld, Rolf', 'Yuen, Kwok Yung', 'Wong, Luet', 'Gao, Guangxia', 'Chen, Saijuan', 'Chen, Zhu', 'Ma, Dawei', 'Bartlam, Mark', 'Rao, Zihe']"
# print(authors_to_list(s))
# print(authors_to_list(s2))
# print(authors_to_list(s3))
print(authors_to_list(s5))