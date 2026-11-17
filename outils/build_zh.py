#!/usr/bin/env python3
"""Construit data3d.json du palais chinois à partir du palais italien (structure, phrases FR, audio FR)
et des fichiers zh_<salle>.txt (contenu chinois rédigé à la main)."""
import json, re, sys, os, copy, warnings
warnings.filterwarnings("ignore")
from pypinyin import pinyin, Style, load_phrases_dict
from pinyin_to_ipa import pinyin_to_ipa
from wordfreq import zipf_frequency
import jieba
jieba.setLogLevel(60)
NAMES = {"马可": "Mǎkě", "巴黎": "Bālí", "罗马": "Luómǎ", "意大利": "Yìdàlì", "意大利语": "Yìdàlìyǔ", "米兰": "Mǐlán", "日本": "Rìběn", "苏珊娜": "Sūshānnà", "伊丽莎白": "Yīlìshābái", "艾琳": "Àilín", "拉莫娜": "Lāmònà", "露西": "Lùxī", "希克斯": "Xīkèsī", "格拉图斯": "Gélātúsī", "诺斯费拉图": "Nuòsīfèilātú", "科克": "Kēkè", "保罗": "Bǎoluó", "巴格达": "Bāgédá", "多纳": "Duōnà", "特克斯": "Tèkèsī", "斯科蒂": "Sīkēdì", "齐格弗里德": "Qígéfúlǐdé", "玛格丽特": "Mǎgélìtè", "史密斯": "Shǐmìsī", "库克": "Kùkè", "海明威": "Hǎimíngwēi", "加布里埃拉": "Jiābùlǐ'āilā", "萨维德拉": "Sàwéidélā", "兰迪斯": "Lándísī", "罗马帝国": "Luómǎ Dìguó", "露露": "Lùlu", "拉迪": "Lādí", "奥斯本": "Àosīběn", "哈马赫": "Hāmǎhè", "乌兰": "Wūlán", "利奇": "Lìqí", "山姆": "Shānmǔ", "加拉格尔": "Jiālāgé'ěr", "拿破仑": "Nápòlún", "杜立特": "Dùlìtè", "阿兰胡埃斯": "Ālánhú'āisī", "吉米": "Jímǐ", "斯图": "Sītú", "迪恩·马丁": "Dí'ēn Mǎdīng", "特丽娜": "Tèlìnà", "弗洛伦丝": "Fúluòlúnsī", "波莉": "Bōlì", "迈克": "Màikè", "德特拉弗斯": "Dé Tèlāfúsī", "德夫林": "Défūlín", "诺克": "Nuòkè", "安东尼奥": "Āndōngní'ào", "亨利": "Hēnglì", "简": "Jiǎn", "牛津": "Niújīn", "意大利": "Yìdàlì", "欧洲": "Ōuzhōu", "那不勒斯": "Nàbùlèsī", "都灵": "Dūlíng", "德国": "Déguó", "博洛尼亚": "Bóluòníyà", "美国": "Měiguó", "西班牙": "Xībānyá", "俄罗斯": "Éluósī", "中国": "Zhōngguó", "热那亚": "Rènàyà", "热那亚港": "Rènàyà Gǎng", "巴勒莫": "Bālèmò", "日本": "Rìběn", "纽约": "Niǔyuē", "希腊": "Xīlà", "英格兰": "Yīnggélán", "瑞士": "Ruìshì", "维罗纳": "Wéiluónà", "巴西": "Bāxī", "莫斯科": "Mòsīkē", "比萨": "Bǐsà", "比萨斜塔": "Bǐsà Xiétǎ", "墨西哥": "Mòxīgē", "马德里": "Mǎdélǐ", "柏林": "Bólín", "巴塞罗那": "Bāsàiluónà", "葡萄牙": "Pútáoyá", "维也纳": "Wéiyěnà", "比利时": "Bǐlìshí", "布鲁塞尔": "Bùlǔsài'ěr", "雅典": "Yǎdiǎn", "英国": "Yīngguó", "爱尔兰": "Ài'ěrlán", "日内瓦": "Rìnèiwǎ", "尼斯": "Nísī", "马赛": "Mǎsài", "斯巴达克斯": "Sībādákèsī", "曼努埃拉": "Mànnǔ'āilā", "弗兰克": "Fúlánkè", "海伦": "Hǎilún", "吉尔达": "Jí'ěrdá", "法雷尔": "Fǎléi'ěr", "肯特": "Kěntè", "埃伦": "Āilún", "帕克": "Pàkè", "玛格丽特披萨": "mǎgélìtè pīsà", "撒丁岛": "Sādīng Dǎo", "费里尼": "Fèilǐní", "米勒": "Mǐlè", "白宫": "Báigōng", "泰坦尼克号": "Tàitǎnníkè Hào", "卡布奇诺": "kǎbùqínuò", "马提尼": "mǎtíní", "埃及": "Āijí", "白雪公主": "Báixuě Gōngzhǔ", "莫吉托": "mòjítuō", "帕尔马": "Pà'ěrmǎ", "米兰": "Mǐlán", "凯西": "Kǎixī", "威尼斯": "Wēinísī", "琪琪": "Qíqí", "北见": "Běijiàn", "杰夫": "Jiéfū", "米利安": "Mǐlì'ān", "迪克森": "Díkèsēn", "马特": "Mǎtè", "本西格": "Běnxīgé", "皇家港": "Huángjiā Gǎng", "丰特努瓦": "Fēngtènǔwǎ", "本尼": "Běnní", "蒂斯代尔": "Dìsīdài'ěr", "伦菲尔德": "Lúnfēi'ěrdé", "葡萄牙人": "Pútáoyárén", "吉诺": "Jínuò", "乔伊斯": "Qiáoyīsī", "蕾妮": "Lěinī", "纳粹": "Nàcuì", "俄国人": "Éguórén", "大吉姆": "Dà Jímǔ", "弗洛伊": "Fúluòyī", "克莱恩": "Kèlái'ēn", "菲莉斯": "Fēilìsī", "赫家": "Hè jiā", "吉尔伯特": "Jí'ěrbótè", "旧金山": "Jiùjīnshān", "但丁": "Dàndīng", "佛罗伦萨": "Fóluólúnsà", "恰科": "Qiàkē", "艾哈迈德": "Àihāmàidé", "特罗布里奇": "Tèluóbùlǐqí", "艾伦": "Àilún", "哈克": "Hākè", "凯瑞": "Kǎiruì", "卡梅伦": "Kǎméilún", "朱莉娅": "Zhūlìyà", "沃尔夫": "Wò'ěrfū", "费边": "Fèibiān", "马克西穆斯": "Mǎkèxīmùsī", "安妮": "Ānnī", "斯凯勒": "Sīkǎilè", "费加罗": "Fèijiāluó", "贝丝": "Bèisī", "麦克蒂格": "Màikèdìgé", "安德森": "Āndésēn", "桑德斯": "Sāngdésī", "伦敦": "Lúndūn", "尼尔": "Ní'ěr", "沃克": "Wòkè", "克卢特": "Kèlútè", "杰西": "Jiéxī", "艾米丽": "Àimǐlì", "莱西": "Láixī", "华盛顿": "Huáshèngdùn", "胡特": "Hútè", "伊什塔尔": "Yīshítǎ'ěr", "埃丝特": "Āisītè", "科瓦尔斯基": "Kēwǎ'ěrsījī", "马可": "Mǎkě", "凯蒂": "Kǎidì", "布莱尔": "Bùlái'ěr", "加姆斯": "Jiāmǔsī", "兰格": "Lángé", "玛丽": "Mǎlì", "阿波罗": "Ābōluó", "艾伦伯里": "Àilúnbólǐ", "贾米森": "Jiǎmǐsēn", "巴克特": "Bākètè", "凯伦": "Kǎilún", "罗马": "Luómǎ", "牛津大学": "Niújīn Dàxué", "迪恩": "Dí'ēn", "马丁": "Mǎdīng", "罗宋汤": "luósòngtāng", "彗星": "huìxīng", "帕斯蒂亚": "Pàsīdìyà", "埃斯卡米洛": "Āisīkǎmǐluò", "萨姆特堡": "Sàmǔtè Bǎo", "梅萨拉": "Méisàlā", "杰拉尔德": "Jiélā'ěrdé", "克里比奇": "kèlǐbǐqí", "丽塔": "Lìtǎ", "乔希": "Qiáoxī", "赫克托": "Hèkètuō", "犹大": "Yóudà", "吉姆": "Jímǔ", "擎天柱": "Qíngtiānzhù", "内德": "Nèidé", "乔治亚": "Qiáozhìyà", "杰克": "Jiékè", "尼罗河": "Níluó Hé", "可丽饼": "kělìbǐng", "凯旋门": "Kǎixuánmén", "帕克": "Pàkè", "玛德琳": "Mǎdélín", "凯撒": "Kǎisā", "亚洲": "Yàzhōu", "珀尔": "Pò'ěr", "希尔迪": "Xī'ěrdí", "约翰逊": "Yuēhànxùn", "汤姆": "Tāngmǔ", "基奥": "Jī'ào", "布拉德": "Bùlādé", "T恤": "T xù", "瑞士": "Ruìshì", "瑞士法郎": "Ruìshì fǎláng", "小熊陈": "xiǎoxióng Chén", "三K党": "Sān K dǎng", "挪威": "Nuówēi", "格斯塔": "Gésītǎ", "贝林": "Bèilín", "波利尼西亚": "Bōlìníxīyà", "葡萄牙": "Pútáoyá", "葡萄牙语": "Pútáoyáyǔ", "西班牙": "Xībānyá", "西班牙语": "Xībānyáyǔ", "俄国": "Éguó", "中国": "Zhōngguó", "中国城": "Zhōngguóchéng", "唐人街": "Tángrénjiē", "尼古拉": "Nígǔlā", "里克": "Lǐkè", "瓦尔堡": "Wǎ'ěrbǎo", "霍尔姆": "Huò'ěrmǔ", "特纳": "Tènà", "汉斯": "Hànsī", "德国": "Déguó", "德国人": "Déguó rén", "法国": "Fǎguó", "法国人": "Fǎguó rén", "洛杉矶": "Luòshānjī", "吉尔": "Jí'ěr", "勒韦": "Lèwéi", "康苏埃洛": "Kāngsū'āiluò", "毕加索": "Bìjiāsuǒ",
         "卡门": "Kǎmén", "范妮": "Fànnī", "奈德": "Nàidé", "辛纳屈": "Xīnnàqū", "笛卡尔": "Díkǎ'ěr", "保罗": "Bǎoluó", "雨果": "Yǔguǒ", "中文": "Zhōngwén", "里昂": "Lǐ'áng", "布列塔尼": "Bùliètǎní", "玛丽亚": "Mǎlìyà", "英语": "Yīngyǔ", "莎士比亚": "Shāshìbǐyà", "俄语": "Éyǔ", "法语": "Fǎyǔ", "汉语": "Hànyǔ", "威尼斯": "Wēinísī", "比萨": "Bǐsà", "比萨斜塔": "Bǐsà xiétǎ", "美国": "Měiguó", "玛丽": "Mǎlì", "斯通曼": "Sītōngmàn", "米兰": "Mǐlán", "日本": "Rìběn", "苏珊娜": "Sūshānnà", "挪威": "Nuówēi", "格斯塔": "Gésītǎ", "贝林": "Bèilín", "波利尼西亚": "Bōlìníxīyà", "葡萄牙": "Pútáoyá", "葡萄牙语": "Pútáoyáyǔ", "西班牙": "Xībānyá", "西班牙语": "Xībānyáyǔ", "俄国": "Éguó", "中国": "Zhōngguó", "中国城": "Zhōngguóchéng", "唐人街": "Tángrénjiē", "尼古拉": "Nígǔlā", "里克": "Lǐkè", "瓦尔堡": "Wǎ'ěrbǎo", "霍尔姆": "Huò'ěrmǔ", "特纳": "Tènà", "汉斯": "Hànsī", "德国": "Déguó", "德国人": "Déguó rén", "洛杉矶": "Luòshānjī", "吉尔": "Jí'ěr", "勒韦": "Lèwéi", "康苏埃洛": "Kāngsū'āiluò", "卡昂": "Kǎ'áng"}
jieba.del_word("前来")
for nm in list(NAMES) + ["二选一", "结为", "快点儿", "得早点", "某地", "挣得", "没转过", "教了", "长这么大", "得还", "应季", "得先", "得懂得", "就算得", "踢不进", "长片", "新生儿", "是只", "倒在地上", "塑料袋子", "花花公子", "待到", "行军床", "鸟蛤", "朗姆酒", "小矮人", "白鹅", "个人物品", "逮个正着", "重写", "得加长", "加长", "夷为平地", "抢生意", "嘟嘟囔囔", "得改短", "得了流感", "三明治", "会转", "份差", "这得", "集中精神", "能不能", "搞不完", "待在", "丢不了", "到不了", "得做完", "睡得着", "救救", "求求", "听得到", "一周一周", "猜猜", "躲躲雨", "干等", "地下酒吧", "背你", "活不长", "弹钢琴", "明晚", "诗人们", "睡不着", "做得到", "劈成", "不得安宁", "教我", "说不上来", "劈柴", "做空", "钉进", "梳一梳", "系好", "还你", "推倒", "不适用", "盗窃案", "还回", "怎么着", "被炸", "打听", "量一下", "做生意", "撞到头", "抬起来", "挑起", "好闷", "自在", "被判", "抬起头来", "尝尝", "种了", "举起手来", "转过身去", "她教", "砍倒", "握握手", "每周一", "卡住", "重做", "都得", "冲他", "数一数", "长椅", "烤盘", "烤羊腿", "看台上", "浴垫", "种地", "弹吉他", "有只", "长胡子", "杯垫", "照照", "上颚", "想得到", "拿铁", "屁股墩儿", "煤气味", "病人们", "路人", "名额", "一块地", "星星", "在行", "讨回", "好觉", "记不起来", "听不清", "说起来", "做起来", "等着", "要不要", "是不是", "好不好", "对不对", "去不了", "多长时间", "没事儿", "听着", "待着", "十年前", "天哪", "想不想", "来不来", "下不下", "出不出", "有没有", "孩子们", "朋友们", "伙计们", "一起来", "在不在", "喜不喜欢", "要不", "会不会", "这么点儿", "不得不", "说说", "慢慢地", "我个人", "女人们", "打不开", "打发", "好长", "太长", "好脏", "长得", "找找", "挪挪", "台面", "找不到", "星期一", "很干", "和气"]: jieba.add_word(nm, 100000)
for w in ["我爱你", "我来", "他会", "我要", "我能", "他变", "我会", "我是", "这快", "给我发", "我怕", "带你去", "好了吗", "说得对", "我爸", "你妈", "帮帮我", "懂吗", "吃了饭", "我心", "电话响", "靠你", "今天天气", "谢谢您", "面上", "咖啡吧", "很大", "地学", "他用", "地走", "地走了"]:
    jieba.del_word(w)
for a, b in [("个", "人"), ("个", "星期"), ("个", "月"), ("讲", "个"), ("十", "个"), ("带", "你"), ("你", "去"), ("车", "去"), ("说", "得"), ("来", "得"), ("年前", "来"), ("包", "被"), ("得", "来"), ("想", "来"), ("很", "大方"), ("的", "话"), ("部", "长片"), ("意大利", "共和国"), ("歌", "唱"), ("会", "上"), ("是", "从"), ("坐", "下一班"), ("地", "下"), ("星期一", "起")]:
    jieba.suggest_freq((a, b), True)

SRC = "/home/claude/hugo-morana/pm-italien/data3d.json"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOMS = sys.argv[1].split(",") if len(sys.argv) > 1 else [r["id"] for r in json.load(open("/home/claude/hugo-morana/pm-italien/data3d.json"))["rooms"] if os.path.exists(os.path.join(HERE, "zh_" + r["id"] + ".txt"))]

# Corrections de lecture (tons neutres usuels, lectures orales)
load_phrases_dict({
    "东西": [["dōng"], ["xi"]], "事情": [["shì"], ["qing"]], "先生": [["xiān"], ["sheng"]], "孩子": [["hái"], ["zi"]],
    "晚上": [["wǎn"], ["shang"]], "早上": [["zǎo"], ["shang"]], "名字": [["míng"], ["zi"]], "道理": [["dào"], ["li"]],
    "时候": [["shí"], ["hou"]], "儿子": [["ér"], ["zi"]], "朋友": [["péng"], ["you"]], "主意": [["zhǔ"], ["yi"]],
    "运气": [["yùn"], ["qi"]], "家伙": [["jiā"], ["huo"]], "眼睛": [["yǎn"], ["jing"]], "故事": [["gù"], ["shi"]],
    "玩意儿": [["wán"], ["yì"], ["r"]], "位子": [["wèi"], ["zi"]], "部分": [["bù"], ["fen"]], "东边": [["dōng"], ["bian"]],
    "看起来": [["kàn"], ["qi"], ["lai"]], "小伙子": [["xiǎo"], ["huǒ"], ["zi"]], "辈子": [["bèi"], ["zi"]],
    "血": [["xiě"]], "爸爸": [["bà"], ["ba"]], "妈妈": [["mā"], ["ma"]], "哥哥": [["gē"], ["ge"]],
    "这边": [["zhè"], ["biān"]], "一下": [["yí"], ["xià"]],
})

NEUTRAL_EXTRA = {"认识": ["rèn","shi"], "意思": ["yì","si"], "什么": ["shén","me"], "怎么": ["zěn","me"], "这么": ["zhè","me"],
    "那么": ["nà","me"], "多么": ["duō","me"], "知道": ["zhī","dao"], "喜欢": ["xǐ","huan"], "衣服": ["yī","fu"], "地方": ["dì","fang"],
    "告诉": ["gào","su"], "舒服": ["shū","fu"], "麻烦": ["má","fan"], "客气": ["kè","qi"], "觉得": ["jué","de"], "东西": ["dōng","xi"],
    "关系": ["guān","xi"], "清楚": ["qīng","chu"], "明白": ["míng","bai"], "漂亮": ["piào","liang"], "暖和": ["nuǎn","huo"],
    "休息": ["xiū","xi"], "消息": ["xiāo","xi"], "收拾": ["shōu","shi"], "打算": ["dǎ","suan"], "时候": ["shí","hou"],
    "事情": ["shì","qing"], "先生": ["xiān","sheng"], "晚上": ["wǎn","shang"], "早上": ["zǎo","shang"], "朋友": ["péng","you"],
    "我们": ["wǒ","men"], "你们": ["nǐ","men"], "他们": ["tā","men"], "她们": ["tā","men"], "咱们": ["zán","men"], "人们": ["rén","men"],
    "爸爸": ["bà","ba"], "妈妈": ["mā","ma"], "哥哥": ["gē","ge"], "弟弟": ["dì","di"], "姐姐": ["jiě","jie"], "妹妹": ["mèi","mei"],
    "看看": ["kàn","kan"], "说说": ["shuō","shuo"], "偶尔": ["ǒu","'ěr"], "模模糊糊": ["mó","mo","hū","hū"], "小角色": ["xiǎo","jué","sè"], "角色": ["jué","sè"], "奶奶": ["nǎi","nai"], "怪物": ["guài","wu"], "爷爷": ["yé","ye"], "口袋": ["kǒu","dai"], "答案": ["dá","'àn"], "拿铁": ["ná","tiě"], "上颚": ["shàng","'è"], "杯垫": ["bēi","diàn"], "要是": ["yào","shi"], "谈谈": ["tán","tan"], "得早点": ["děi","zǎo","diǎn"], "某地": ["mǒu","dì"], "反而": ["fǎn","'ér"], "挣得": ["zhèng","de"], "没转过": ["méi","zhuàn","guo"], "教了": ["jiāo","le"], "长这么大": ["zhǎng","zhè","me","dà"], "得还": ["děi","huán"], "应季": ["yìng","jì"], "发脾气": ["fā","pí","qi"], "得先": ["děi","xiān"], "得懂得": ["děi","dǒng","de"], "问问": ["wèn","wen"], "就算得": ["jiù","suàn","děi"], "答应": ["dā","ying"], "讲讲": ["jiǎng","jiang"], "踢不进": ["tī","bu","jìn"], "长片": ["cháng","piàn"], "新生儿": ["xīn","shēng","'ér"], "是只": ["shì","zhī"], "倒在地上": ["dǎo","zài","dì","shang"], "混蛋": ["hún","dàn"], "假发": ["jiǎ","fà"], "塑料袋子": ["sù","liào","dài","zi"], "夹克": ["jiā","kè"], "花花公子": ["huā","huā","gōng","zǐ"], "天鹅绒": ["tiān","'é","róng"], "海鸥": ["hǎi","'ōu"], "芥末": ["jiè","mo"], "待到": ["dāi","dào"], "女婿": ["nǚ","xu"], "痘痘": ["dòu","dou"], "行军床": ["xíng","jūn","chuáng"], "薄荷": ["bò","he"], "鸟蛤": ["niǎo","gé"], "甘蔗": ["gān","zhe"], "朗姆酒": ["lǎng","mǔ","jiǔ"], "小矮人": ["xiǎo","'ǎi","rén"], "下巴": ["xià","ba"], "白鹅": ["bái","'é"], "裁缝": ["cái","feng"], "个人物品": ["gè","rén","wù","pǐn"], "结结巴巴": ["jiē","jie","bā","bā"], "逮个正着": ["dǎi","ge","zhèng","zháo"], "重写": ["chóng","xiě"], "打哈欠": ["dǎ","hā","qian"], "得加长": ["děi","jiā","cháng"], "加长": ["jiā","cháng"], "夷为平地": ["yí","wéi","píng","dì"], "葡萄酒": ["pú","táo","jiǔ"], "抢生意": ["qiǎng","shēng","yi"], "应付": ["yìng","fu"], "嘟囔": ["dū","nang"], "嘟嘟囔囔": ["dū","du","nāng","nāng"], "称呼": ["chēng","hu"], "得改短": ["děi","gǎi","duǎn"], "葡萄": ["pú","tao"], "得了流感": ["dé","le","liú","gǎn"], "三明治": ["sān","míng","zhì"], "狐狸": ["hú","li"], "姑姑": ["gū","gu"], "听听": ["tīng","ting"], "记号": ["jì","hao"], "会转": ["huì","zhuàn"], "份差": ["fèn","chāi"], "这得": ["zhè","děi"], "集中精神": ["jí","zhōng","jīng","shen"], "能不能": ["néng","bu","néng"], "搞不完": ["gǎo","bu","wán"], "丢不了": ["diū","bu","liǎo"], "到不了": ["dào","bu","liǎo"], "得做完": ["děi","zuò","wán"], "睡得着": ["shuì","de","zháo"], "救救": ["jiù","jiu"], "求求": ["qiú","qiu"], "碰碰运气": ["pèng","peng","yùn","qi"], "打起精神": ["dǎ","qǐ","jīng","shen"], "见见": ["jiàn","jian"], "孤儿院": ["gū","'ér","yuàn"], "听得到": ["tīng","de","dào"], "一周一周": ["yì","zhōu","yì","zhōu"], "猜猜": ["cāi","cai"], "躲躲雨": ["duǒ","duo","yǔ"], "干等": ["gān","děng"], "抱抱": ["bào","bao"], "地下酒吧": ["dì","xià","jiǔ","bā"], "不得不": ["bù","dé","bù"], "背你": ["bēi","nǐ"], "活不长": ["huó","bu","cháng"], "弹钢琴": ["tán","gāng","qín"], "睡不着": ["shuì","bu","zháo"], "献血": ["xiàn","xuè"], "笑话": ["xiào","hua"], "做得到": ["zuò","de","dào"], "劈成": ["pī","chéng"], "不得安宁": ["bù","dé","ān","níng"], "教我": ["jiāo","wǒ"], "等等": ["děng","deng"], "说不上来": ["shuō","bu","shàng","lái"], "劈柴": ["pī","chái"], "嚼": ["jiáo"], "做空": ["zuò","kōng"], "钉进": ["dìng","jìn"], "提防": ["dī","fang"], "没收": ["mò","shōu"], "缝": ["féng"], "咳嗽": ["ké","sou"], "梳一梳": ["shū","yi","shū"], "系好": ["jì","hǎo"], "还你": ["huán","nǐ"], "推倒": ["tuī","dǎo"], "不适用": ["bú","shì","yòng"], "不安": ["bù","'ān"], "盗窃案": ["dào","qiè","'àn"], "还回": ["huán","huí"], "怎么着": ["zěn","me","zhāo"], "被炸": ["bèi","zhà"], "打听": ["dǎ","ting"], "量一下": ["liáng","yí","xià"], "做生意": ["zuò","shēng","yi"], "撞到头": ["zhuàng","dào","tóu"], "挑起": ["tiǎo","qǐ"], "抬起来": ["tái","qi","lai"], "做爱": ["zuò","'ài"], "好闷": ["hǎo","mēn"], "拿来": ["ná","lai"], "砍倒": ["kǎn","dǎo"], "自在": ["zì","zai"], "被判": ["bèi","pàn"], "抬起头来": ["tái","qǐ","tóu","lai"], "尝尝": ["cháng","chang"], "种了": ["zhòng","le"], "滑倒": ["huá","dǎo"], "举起手来": ["jǔ","qǐ","shǒu","lai"], "转过身去": ["zhuǎn","guò","shēn","qu"], "流血": ["liú","xuè"], "她教": ["tā","jiāo"], "相爱": ["xiāng","'ài"], "握握手": ["wò","wo","shǒu"], "每周一": ["měi","zhōu","yī"], "卡住": ["kǎ","zhù"], "重做": ["chóng","zuò"], "都得": ["dōu","děi"], "冲他": ["chòng","tā"], "数一数": ["shǔ","yi","shǔ"], "石榴": ["shí","liu"], "长椅": ["cháng","yǐ"], "蘑菇": ["mó","gu"], "扫帚": ["sào","zhou"], "抽屉": ["chōu","ti"], "热爱": ["rè","'ài"], "烤盘": ["kǎo","pán"], "黑暗": ["hēi","'àn"], "烤羊腿": ["kǎo","yáng","tuǐ"], "姐夫": ["jiě","fu"], "看台": ["kàn","tái"], "看台上": ["kàn","tái","shang"], "浴垫": ["yù","diàn"], "种地": ["zhòng","dì"], "弹吉他": ["tán","jí","tā"], "玻璃": ["bō","li"], "有只": ["yǒu","zhī"], "苍蝇": ["cāng","ying"], "指甲": ["zhǐ","jia"], "棺材": ["guān","cai"], "夫人": ["fū","ren"], "态度": ["tài","du"], "长胡子": ["cháng","hú","zi"], "照照": ["zhào","zhao"], "想得到": ["xiǎng","dé","dào"], "跳蚤": ["tiào","zao"], "娃娃": ["wá","wa"], "婴儿": ["yīng","'ér"], "戒指": ["jiè","zhi"], "护士": ["hù","shi"], "屁股墩儿": ["pì","gu","dūnr"], "煤气味": ["méi","qì","wèi"], "名额": ["míng","'é"], "病人们": ["bìng","rén","men"], "路人": ["lù","rén"], "月亮": ["yuè","liang"], "小姐": ["xiǎo","jie"], "记性": ["jì","xing"], "公道": ["gōng","dao"], "合同": ["hé","tong"], "星星": ["xīng","xing"], "一块地": ["yí","kuài","dì"], "在行": ["zài","háng"], "分子": ["fèn","zǐ"], "重重": ["zhòng","zhòng"], "重重地": ["zhòng","zhòng","de"], "舒舒服服": ["shū","shu","fú","fú"], "模糊": ["mó","hu"], "和气": ["hé","qi"], "正经": ["zhèng","jing"], "星期二": ["xīng","qī","'èr"], "炸": ["zhá"], "进行曲": ["jìn","xíng","qǔ"], "兄弟": ["xiōng","di"], "兄弟般": ["xiōng","di","bān"], "罪恶": ["zuì","'è"], "固执": ["gù","zhi"], "尽力而为": ["jìn","lì","'ér","wéi"], "女儿": ["nǚ","'ér"], "海岸": ["hǎi","'àn"], "大方": ["dà","fang"], "结实": ["jiē","shi"], "正当": ["zhèng","dàng"], "十二": ["shí","'èr"], "快活": ["kuài","huo"], "千恩万谢": ["qiān","'ēn","wàn","xiè"], "独一无二": ["dú","yī","wú","'èr"], "机灵": ["jī","ling"], "很干": ["hěn","gān"], "恶心": ["ě","xin"], "心里": ["xīn","li"], "规矩": ["guī","ju"], "待在家里": ["dāi","zài","jiā","li"], "家里": ["jiā","li"], "待在": ["dāi","zài"], "框架": ["kuàng","jià"], "星期一": ["xīng","qī","yī"], "本案": ["běn","'àn"], "找不到": ["zhǎo","bu","dào"], "第二": ["dì","'èr"], "骄傲": ["jiāo","'ào"], "活泼": ["huó","po"], "老婆": ["lǎo","po"], "屁股": ["pì","gu"], "挪挪": ["nuó","nuo"], "胳膊": ["gē","bo"], "头发": ["tóu","fa"], "叔叔": ["shū","shu"], "找找": ["zhǎo","zhao"], "长": ["cháng"], "长得": ["zhǎng","de"], "好长": ["hǎo","cháng"], "太长": ["tài","cháng"], "脏": ["zāng"], "好脏": ["hǎo","zāng"], "亲爱": ["qīn","'ài"], "可爱": ["kě","'ài"], "打发": ["dǎ","fa"], "味道": ["wèi","dao"], "打不开": ["dǎ","bu","kāi"], "老老实实": ["lǎo","lǎo","shí","shí"], "我个人": ["wǒ","gè","rén"], "试试": ["shì","shi"], "想想": ["xiǎng","xiang"], "谢谢": ["xiè","xie"],
    "名字": ["míng","zi"], "孩子": ["hái","zi"], "儿子": ["ér","zi"], "房子": ["fáng","zi"], "位子": ["wèi","zi"], "日子": ["rì","zi"],
    "样子": ["yàng","zi"], "辈子": ["bèi","zi"], "肚子": ["dù","zi"], "桌子": ["zhuō","zi"], "椅子": ["yǐ","zi"], "妻子": ["qī","zi"],
    "部分": ["bù","fen"], "道理": ["dào","li"], "主意": ["zhǔ","yi"], "运气": ["yùn","qi"], "家伙": ["jiā","huo"], "眼睛": ["yǎn","jing"],
    "故事": ["gù","shi"], "东边": ["dōng","bian"], "西边": ["xī","bian"], "外边": ["wài","bian"], "里边": ["lǐ","bian"],
    "后边": ["hòu","bian"], "前边": ["qián","bian"], "上边": ["shàng","bian"], "下边": ["xià","bian"], "旁边": ["páng","biān"],
    "起来": ["qǐ","lai"], "出来": ["chū","lai"], "回来": ["huí","lai"], "过来": ["guò","lai"], "进来": ["jìn","lai"], "下来": ["xià","lai"],
    "上来": ["shàng","lai"], "出去": ["chū","qu"], "回去": ["huí","qu"], "过去": ["guò","qu"], "进去": ["jìn","qu"], "上去": ["shàng","qu"],
    "下去": ["xià","qu"], "玩意儿": ["wán","yìr"], "小伙子": ["xiǎo","huǒ","zi"], "看起来": ["kàn","qi","lai"], "多少": ["duō","shao"],
    "地上": ["dì","shang"], "身上": ["shēn","shang"], "头上": ["tóu","shang"], "脸上": ["liǎn","shang"], "墙上": ["qiáng","shang"],
    "桌上": ["zhuō","shang"], "床上": ["chuáng","shang"], "这个": ["zhè","ge"], "那个": ["nà","ge"], "哪个": ["nǎ","ge"],
    "一个": ["yí","ge"], "两个": ["liǎng","ge"], "几个": ["jǐ","ge"], "三个": ["sān","ge"], "整个": ["zhěng","gè"], "厉害": ["lì","hai"],
    "认得": ["rèn","de"], "记得": ["jì","de"], "值得": ["zhí","de"], "晓得": ["xiǎo","de"], "舍得": ["shě","de"], "别人": ["bié","ren"],
    "丈夫": ["zhàng","fu"], "大夫": ["dài","fu"], "姑娘": ["gū","niang"], "耳朵": ["ěr","duo"], "眉毛": ["méi","mao"],
    "便宜": ["pián","yi"], "聪明": ["cōng","ming"], "热闹": ["rè","nao"], "凉快": ["liáng","kuai"], "高兴": ["gāo","xìng"],
    "一下": ["yí","xià"], "一些": ["yì","xiē"], "一点": ["yì","diǎn"], "一点儿": ["yì","diǎnr"], "一起": ["yì","qǐ"], "一直": ["yì","zhí"],
    "一样": ["yí","yàng"], "一定": ["yí","dìng"], "一切": ["yí","qiè"], "一半": ["yí","bàn"], "一会儿": ["yí","huìr"], "这儿": ["zhèr"],
    "那儿": ["nàr"], "哪儿": ["nǎr"], "事儿": ["shìr"], "点儿": ["diǎnr"], "活儿": ["huór"], "哥们儿": ["gē","menr"], "一块儿": ["yí","kuàir"],
    "血": ["xiě"], "得": None, "招呼": ["zhāo","hu"], "窗户": ["chuāng","hu"], "钥匙": ["yào","shi"], "衣裳": ["yī","shang"], "打扮": ["dǎ","ban"], "商量": ["shāng","liang"], "认得": ["rèn","de"], "时候儿": ["shí","hour"], "怎么样": ["zěn","me","yàng"], "为什么": ["wèi","shén","me"], "那么": ["nà","me"], "这么多": ["zhè","me","duō"], "没关系": ["méi","guān","xi"], "对不起": ["duì","bu","qǐ"], "看见": ["kàn","jiàn"], "听见": ["tīng","jiàn"], "回头": ["huí","tóu"], "姑娘们": ["gū","niang","men"], "亲戚": ["qīn","qi"], "暖和": ["nuǎn","huo"], "行李": ["xíng","li"], "篮子": ["lán","zi"], "裙子": ["qún","zi"], "鞋子": ["xié","zi"], "盘子": ["pán","zi"], "嗓子": ["sǎng","zi"], "屋子": ["wū","zi"], "一静": ["yi","jìng"], "待着": ["dāi","zhe"], "聊聊": ["liáo","liao"], "瞧瞧": ["qiáo","qiao"], "黄历": ["huáng","li"], "二选一": ["èr","xuǎn","yī"], "结为": ["jié","wéi"], "眼镜": ["yǎn","jìng"], "一下子": ["yí","xià","zi"], "老黄历": ["lǎo","huáng","li"], "擤擤": ["xǐng","xing"], "莎士比亚": ["Shā","shì","bǐ","yà"], "冒昧": ["mào","mèi"], "马马虎虎": ["mǎ","mǎ","hū","hū"], "清清楚楚": ["qīng","qīng","chǔ","chǔ"], "日记": ["rì","jì"], "盘子": ["pán","zi"], "爽歪歪": ["shuǎng","wāi","wāi"], "啥": ["shá"], "快点儿": ["kuài","diǎnr"], "学生": ["xué","sheng"], "老实": ["lǎo","shi"], "了不起": ["liǎo","bu","qǐ"], "懒得": ["lǎn","de"], "玛丽亚": ["Mǎ","lì","yà"], "好笑": ["hǎo","xiào"], "好觉": ["hǎo","jiào"], "意识": ["yì","shi"], "圣诞": ["Shèng","dàn"], "聚聚": ["jù","ju"], "好玩": ["hǎo","wánr"], "罢了": ["bà","le"], "里昂": ["Lǐ","'áng"], "喂": ["wèi"], "在乎": ["zài","hu"], "记不起来": ["jì","bu","qǐ","lai"], "听不清": ["tīng","bu","qīng"], "等着": ["děng","zhe"], "说起来": ["shuō","qi","lai"], "做起来": ["zuò","qi","lai"], "看上去": ["kàn","shang","qu"], "没事儿": ["méi","shìr"], "多长时间": ["duō","cháng","shí","jiān"], "听着": ["tīng","zhe"], "门儿": ["ménr"], "去不了": ["qù","bu","liǎo"], "哦": ["ò"], "晚安": ["wǎn'ān"], "凑合": ["còu","he"], "没门儿": ["méi","ménr"], "感觉": ["gǎn","jué"], "嗯": ["ǹg"], "天啊": ["tiān","a"], "看看": ["kàn","kan"], "待会儿": ["dāi","huìr"], "看着办": ["kàn","zhe","bàn"], "说了算": ["shuō","le","suàn"], "天哪": ["tiān","na"], "帮帮": ["bāng","bang"], "在不在": ["zài","bu","zài"], "说说": ["shuō","shuo"], "偶尔": ["ǒu","'ěr"], "和气": ["hé","qi"], "正经": ["zhèng","jing"], "星期二": ["xīng","qī","'èr"], "炸": ["zhá"], "进行曲": ["jìn","xíng","qǔ"], "兄弟": ["xiōng","di"], "兄弟般": ["xiōng","di","bān"], "罪恶": ["zuì","'è"], "固执": ["gù","zhi"], "尽力而为": ["jìn","lì","'ér","wéi"], "女儿": ["nǚ","'ér"], "海岸": ["hǎi","'àn"], "大方": ["dà","fang"], "结实": ["jiē","shi"], "正当": ["zhèng","dàng"], "十二": ["shí","'èr"], "恶心": ["ě","xin"], "心里": ["xīn","li"], "规矩": ["guī","ju"], "待在家里": ["dāi","zài","jiā","li"], "家里": ["jiā","li"], "待在": ["dāi","zài"], "本案": ["běn","'àn"], "找不到": ["zhǎo","bu","dào"], "第二": ["dì","'èr"], "骄傲": ["jiāo","'ào"], "活泼": ["huó","po"], "老婆": ["lǎo","po"], "屁股": ["pì","gu"], "挪挪": ["nuó","nuo"], "胳膊": ["gē","bo"], "头发": ["tóu","fa"], "叔叔": ["shū","shu"], "找找": ["zhǎo","zhao"], "长": ["cháng"], "长得": ["zhǎng","de"], "好长": ["hǎo","cháng"], "太长": ["tài","cháng"], "脏": ["zāng"], "好脏": ["hǎo","zāng"], "亲爱": ["qīn","'ài"], "可爱": ["kě","'ài"], "打发": ["dǎ","fa"], "味道": ["wèi","dao"], "打不开": ["dǎ","bu","kāi"], "老老实实": ["lǎo","lǎo","shí","shí"], "我个人": ["wǒ","gè","rén"], "慢慢地": ["màn","màn","de"], "还是": ["hái","shi"], "这么点儿": ["zhè","me","diǎnr"], "不得不": ["bù","dé","bù"], "会不会": ["huì","bu","huì"], "要不": ["yào","bù"], "喜不喜欢": ["xǐ","bu","xǐ","huan"], "一起来": ["yì","qǐ","lái"], "谁": ["shéi"], "想不想": ["xiǎng","bu","xiǎng"], "来不来": ["lái","bu","lái"], "下不下": ["xià","bu","xià"], "出不出": ["chū","bu","chū"], "有没有": ["yǒu","mei","yǒu"], "大不了": ["dà","bu","liǎo"], "下面": ["xià","mian"], "里面": ["lǐ","mian"], "后面": ["hòu","mian"], "前面": ["qián","mian"], "外面": ["wài","mian"], "上面": ["shàng","mian"], "对面": ["duì","miàn"], "底下": ["dǐ","xia"], "顶上": ["dǐng","shang"], "右边": ["yòu","bian"], "左边": ["zuǒ","bian"], "那边": ["nà","biān"], "这样": ["zhè","yàng"], "那样": ["nà","yàng"], "什么时候": ["shén","me","shí","hou"], "有时候": ["yǒu","shí","hou"], "看上去": ["kàn","shang","qu"], "看起来": ["kàn","qi","lai"], "已经": ["yǐ","jīng"], "觉得": ["jué","de"],
}

# Affichage paramétrique : les cases à remplir entre crochets ([某人], [动词], [句子]…), le son garde « it »
# slots_zh.json : nature de chaque « … » (room:n -> [mot, [étiquettes]] ; null = hésitation, pas une case)
SLOTS = json.load(open(os.path.join(HERE, "slots_zh.json")))
LAB_PY = {"某人": "mǒurén", "某事": "mǒushì", "某物": "mǒuwù", "某处": "mǒuchù", "某地": "mǒudì", "形容词": "xíngróngcí",
          "动词": "dòngcí", "句子": "jùzi", "名词": "míngcí", "语言": "yǔyán", "数字": "shùzì", "时间": "shíjiān", "日期": "rìqī",
          "国家": "guójiā", "名字": "míngzi", "补语": "bǔyǔ", "副词": "fùcí"}
SLOT_ZH = r"某人|某事|某物|某处|某地|形容词|动词|adj\./verbe|adj\.|verbe|état|résultat|(?<![A-Za-z])V(?![A-Za-z])"
SLOT_PY = r"mǒurén|mǒushì|mǒuwù|mǒuchù|mǒudì|xíngróngcí|dòngcí|adj\./verbe|adj\.|verbe|état|résultat|(?<![A-Za-z])V(?=bù)|(?<=bù)V(?![A-Za-z])"
def brk(it, pr, key):
    a, b = re.findall(SLOT_ZH, it), re.findall(SLOT_PY, pr)
    if [LAB_PY.get(t, t) for t in a] != b:
        raise SystemExit(f"crochets : {it} / {pr}")
    n = len(re.findall("…+", it))
    if n != len(re.findall("…+", pr)):
        raise SystemExit(f"… pinyin : {it} / {pr}")
    lab = None
    if n:
        if key not in SLOTS or SLOTS[key][0] != it:
            raise SystemExit(f"slots_zh.json à refaire : {key} {it}")
        lab = SLOTS[key][1]
    if not a and not lab:
        return None
    itd = re.sub(SLOT_ZH, r"[\g<0>]", it)
    pd = re.sub(SLOT_PY, r"[\g<0>]", pr)
    if lab:
        g = iter(lab); itd = re.sub("…+", lambda m: "[" + next(g) + "]", itd)
        g = iter(lab); pd = re.sub("…+", lambda m: "[" + LAB_PY[next(g)] + "]", pd)
    pd = re.sub(r"(?<=[^\s\[(+/])\[", " [", pd)
    pd = re.sub(r"\](?=[^\s\]),.?!？。，)+/:;])", "] ", pd)
    return itd, pd

def syllables(s):
    """syllabes (pinyin à tons) par mot jieba, avec tons neutres usuels et sandhi de 一 / 不"""
    words = []
    for w in jieba.cut(s, HMM=False):
        if not w.strip():
            continue
        if w in NAMES:
            words.append(("P", NAMES[w], None)); continue
        if re.fullmatch(r"[\u4e00-\u9fff]+", w):
            if w in NEUTRAL_EXTRA and NEUTRAL_EXTRA[w]:
                syl = list(NEUTRAL_EXTRA[w])
            else:
                syl = []
                for k, seg in enumerate(pinyin(w, style=Style.TONE)):
                    syl.append(seg[0])
                # sous-chaînes connues (ex. 我们 dans 我们俩)
                for key, val in NEUTRAL_EXTRA.items():
                    if val and len(key) > 1 and key in w and len(val) == len(key):
                        i = w.index(key)
                        syl[i:i + len(key)] = val
            # 儿 de érhua
            ws = list(w)
            merged = []
            for c, p in zip(ws, syl):
                if c == "儿" and merged and len(ws) > 1 and w not in ("儿子", "女儿", "儿童") and not p.endswith("r") and p in ("ér", "er", "r"):
                    merged[-1] = (merged[-1][0], merged[-1][1] + "r")
                else:
                    merged.append((c, p))
            words.append(("H", [m[0] for m in merged], [m[1] for m in merged]))
        else:
            words.append(("P", w, None))
    # particules neutres isolées
    NEU = {"的": "de", "了": "le", "吗": "ma", "呢": "ne", "吧": "ba", "啊": "a", "着": "zhe", "过": None, "们": "men", "嘛": "ma", "呀": "ya", "啦": "la", "么": "me", "个": "ge", "地": None, "得": None}
    flat = []
    END1 = {}
    lastP = True
    for t, chars, syl in words:
        if t != "H":
            lastP = True
        if t == "H":
            w = "".join(chars)
            prevP, lastP = lastP, False
            for i, (c, p) in enumerate(zip(chars, syl)):
                if c == "个" and w not in ("个人", "个子", "个性", "个别", "整个", "个个", "我个人", "个人物品"):
                    syl[i] = p = "ge"
                if c == "地" and len(chars) == 1:
                    prev = flat[-1][0] if flat else ""
                    syl[i] = p = "dì" if prevP else "de"
                if c == "地" and len(chars) > 1 and i == len(chars) - 1 and w[-2:] not in ("土地","某地","平地","地下","种地","块地","当地","各地","本地","外地","场地","草地","陆地","工地","基地","的地","天地","此地","内地","满地","遍地","就地","原地","实地","山地","耕地","产地","墓地","营地","高地","空地","田地","园地","落地","倒地","大地","境地","余地","阵地","腹地","盆地","圣地","湿地","林地","领地","绿地","雪地","荒地","在地","上地","下地","掉地"):
                    syl[i] = p = "de"
                if c == "得" and len(chars) == 1:
                    prev = flat[-1][0] if flat else ""
                    syl[i] = p = "děi" if (prevP or prev in "我你他她您们还就也必须总在") else "de"
                if c == "得" and len(chars) > 1 and i > 0 and w not in ("获得", "取得", "赢得", "难得", "觉得", "值得", "记得", "认得", "舍得", "晓得", "显得", "懂得", "免得", "省得", "使得", "不得不", "都得", "这得", "得做完", "得先", "得懂得", "就算得", "得还", "得早点"):
                    syl[i] = p = "de"
                if c == "不" and len(chars) == 3 and i == 1 and w not in ("要不然", "要不是", "大不了", "差不多", "挺不错", "还不错", "真不错", "很不错", "不得不"):
                    syl[i] = p = "bu"
                if c == "一" and len(chars) > 1 and i == len(chars) - 1:
                    END1[len(flat)] = True
                flat.append([c, p, len(flat)])
    # sandhi 一 / 不
    for i, (c, p, _) in enumerate(flat):
        if i + 1 < len(flat):
            nc, npy, _ = flat[i + 1]
            nt = tone_of(npy) if npy not in ("ge",) else 4
            if c == "不" and nt == 4 and p != "bu":
                flat[i][1] = "bú"
            if c == "一" and END1.get(i) and p in ("yī",):
                continue
            if c == "一" and i > 0 and flat[i - 1][0] == nc and nc != "边":
                flat[i][1] = "yi"; continue
            if c == "一" and p in ("yī", "yì", "yí") and not (i > 0 and flat[i - 1][0] in "第十") and nc not in "月号日二三四五六七八九十":
                flat[i][1] = "yí" if nt == 4 else ("yì" if nt in (1, 2, 3) else p)
    k = 0
    for t, chars, syl in words:
        if t == "H":
            for i in range(len(chars)):
                syl[i] = flat[k][1]; k += 1
    return words, NEU

def py_compact(s):
    words, NEU = syllables(s)
    out = []
    for t, chars, syl in words:
        if t == "P":
            out.append(("P", chars))
            continue
        if len(chars) == 1 and chars[0] in NEU and NEU[chars[0]]:
            syl = [NEU[chars[0]]]
        if chars == ["们"] and out and out[-1][0] == "H":
            out[-1] = ("H", out[-1][1] + "men"); continue
        out.append(("H", "".join(syl)))
    txt = ""
    for t, v in out:
        if t == "P" and v and v[0].isalpha():
            txt += (" " if txt and not txt.endswith((" ", "(")) else "") + v
            continue
        if t == "P":
            v = {"，": ", ", "。": ".", "！": "!", "？": "?", "、": ", ", "；": " ; ", "：": " : ", "——": " – ", "…": "…", "（": " (", "）": ") "}.get(v, v)
            txt += v
        else:
            txt += (" " if txt and not txt.endswith((" ", "(")) else "") + v
    return re.sub(r"\s+", " ", txt).strip()

py_of = py_compact

TONES = {"āēīōūǖ": 1, "áéíóúǘ": 2, "ǎěǐǒǔǚ": 3, "àèìòùǜ": 4}
def tone_of(s):
    for k, v in TONES.items():
        if any(ch in s for ch in k):
            return v
    return 0

def ipa_of(s):
    from pypinyin.contrib.tone_convert import to_tone3
    words, NEU = syllables(s)
    seq = []
    for t, chars, syl in words:
        if t != "H":
            continue
        if len(chars) == 1 and chars[0] in NEU and NEU[chars[0]]:
            syl = [NEU[chars[0]]]
        for x in [y for z in syl for y in z.lower().split("'") if y]:
            er = x.endswith("r") and x not in ("ér", "èr", "ěr", "er")
            if er:
                x = x[:-1]
            t3 = to_tone3(x, neutral_tone_with_five=True)
            if not t3[-1].isdigit():
                t3 += "5"
            seq.append((t3, er))
    parts = []
    for p, er in seq:
        try:
            ipa = pinyin_to_ipa(p)
            ph = "".join(list(ipa)[0])
            tn = "".join(ch for ch in ph if ch in "˥˦˧˨˩")
            ph = "".join(ch for ch in ph if ch not in "˥˦˧˨˩") + ("ɻ" if er else "") + tn
            parts.append(ph)
        except Exception:
            parts.append(p)
    return "/" + " ".join(parts) + "/"

def han(s):
    return "".join(re.findall(r"[一-鿿]", s))

def zipf(s):
    h = s.split("/")[0]
    h = re.sub(r"[（(].*?[)）]", "", h)
    h = re.sub(r"某人|某事|某物|某处|做某事|某", "", h)
    h = han(h)
    if not h:
        return None, False
    toks = [t for t in jieba.cut(h) if t.strip()]
    return round(zipf_frequency(h, "zh"), 2), len(toks) > 1

VERBS = ["bouscule", "attrape", "renverse", "chatouille", "arrose", "pousse", "soulève", "avale", "embrasse", "tire par la manche",
         "éclabousse", "fait rebondir", "enroule", "réveille", "porte sur son dos", "lance", "poursuit", "salue", "frappe du gong", "souffle sur"]

def parse(room):
    path = os.path.join(HERE, f"zh_{room}.txt")
    rows = {}
    errs = []
    for line in open(path, encoding="utf8"):
        line = line.rstrip("\n")
        if not line.strip() or line.startswith("#"):
            continue
        f = line.split("|")
        if len(f) not in (9, 10):
            errs.append(f"{room} {f[0]}: {len(f)} champs")
            continue
        n = int(f[0])
        d = dict(zip(["it", "mc", "sc", "de", "fo", "eit", "eim", "im"], f[1:9]))
        if len(f) == 10:
            d["py"] = f[9]
        if d["eim"] not in d["eit"]:
            errs.append(f"{room} {n:02d}: eim « {d['eim']} » absent de « {d['eit']} »")
        if n in rows:
            errs.append(f"{room} {n:02d}: doublon")
        rows[n] = d
    return rows, errs

def main():
    src = json.load(open(SRC))
    out = {k: copy.deepcopy(v) for k, v in src.items() if k != "rooms"}
    out["langue"] = "chinois"
    out["rev"] = 1
    out["migr"] = []
    rooms = []
    allerr = []
    srcrooms = {r["id"]: r for r in src["rooms"]}
    for rid in ROOMS:
        r = copy.deepcopy(srcrooms[rid])
        rows, errs = parse(rid)
        allerr += errs
        base = rid.split("_")[0]
        r["it"] = ZH_ROOM.get(rid, ZH_ROOM.get(base, r["it"]))
        r["decor"] = DECOR.get(rid, DECOR.get(base, r["decor"]))
        nn = []
        for i, x in enumerate(r["niches"]):
            if x is None:
                nn.append(None); continue
            if i not in rows:
                allerr.append(f"{rid} {i:02d}: manquant"); nn.append(None); continue
            z = rows[i]
            y = copy.deepcopy(x)
            for k in ["co", "itd", "ito", "itp", "tv", "te", "px"]:
                y.pop(k, None)
            fd = re.sub(r"\(([a-zà-ÿ']+), (pluriel|féminin)\)", r"(\2)", x["fr"])
            if fd != x["fr"]:
                y["frd"] = fd
            y["it"] = z["it"]
            if z.get("py"):
                y["pr"] = z["py"]
            elif re.search(r"[A-Za-z+]", z["it"]):
                y["pr"] = re.sub(r"[\u4e00-\u9fff]+", lambda m: py_compact(m.group(0)), z["it"])
            else:
                y["pr"] = py_compact(z["it"])
            y["api"] = ipa_of(z["it"]) if han(z["it"]) else ""
            bd = brk(y["it"], y["pr"], f"{rid}:{i}")
            if bd:
                y["itd"], y["prd"] = bd
            y["mc"], y["sc"], y["de"], y["fo"] = z["mc"], z["sc"], z["de"], z["fo"]
            y["eit"], y["eim"] = z["eit"], z["eim"]
            y["epy"] = py_of(z["eit"])
            y["im"] = z["im"]
            zz, ax = zipf(z["it"])
            y["zi"] = zz if zz is not None else 0
            y["zie"] = y["zi"]
            y["oi"] = int(round(10 ** (y["zi"] - 1))) if y["zi"] else 0
            y["ax"] = bool(ax) or x.get("k") in ("tpl",)
            y["ai"] = None; y["am"] = None; y["ap"] = None
            nn.append(y)
        # liens n -> n+1
        for i, y in enumerate(nn):
            if y is None:
                continue
            j = next((k for k in range(i + 1, len(nn)) if nn[k]), None)
            if j is None:
                y["li"] = f"Fin de la salle : {y['im']} t'ouvre la porte de la salle suivante."
            else:
                nx = nn[j]
                v = VERBS[(i * 7 + len(rid)) % len(VERBS)]
                y["li"] = f"{y['im'][0].upper() + y['im'][1:]} {v} {nx['im']} ({nx['it']})."
        r["niches"] = nn
        rooms.append(r)
    out["rooms"] = rooms
    out["packs"] = src["packs"]
    if allerr:
        print("\n".join(allerr))
    json.dump(out, open(os.path.join(HERE, "data3d_zh.json"), "w"), ensure_ascii=False, separators=(",", ":"))
    print("ok", sum(1 for r in rooms for x in r["niches"] if x), "niches", "erreurs:", len(allerr))

ZH_ROOM = {"noms": "名词", "verbes": "动词", "adjectifs": "形容词", "pronoms": "代词", "conjonctions": "连词",
           "prepositions": "介词", "adverbes": "副词", "courantes": "常用表达", "modales": "句型表达", "incises": "插入语", "formes": "动词形式", "villes": "城市与国家", "patrons": "句型"}
DECOR = {"noms": "marché de nuit chinois", "verbes": "atelier d'artisans (hutong)", "adjectifs": "galerie de peintures à l'encre",
         "pronoms": "salon de thé", "conjonctions": "salle des ponts de jardin", "prepositions": "cour carrée (siheyuan)",
         "adverbes": "salle d'opéra de Pékin", "courantes": "foire du temple (庙会)", "modales": "foire du temple (庙会)", "incises": "académie des lettrés (书院)", "formes": "pavillon des miroirs de bronze (铜镜阁)", "villes": "salle des cartes et du compas (舆图)", "patrons": "cabinet du maître bâtisseur (营造司)"}

if __name__ == "__main__":
    main()
