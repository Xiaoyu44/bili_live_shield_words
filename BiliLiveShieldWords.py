# coding: utf-8
# <DATA BEGIN>
import re
# 拼音对应的常用汉字
hz_xi="夕兮吸汐西希析昔茜奚唏栖息悉惜淅犀晰腊锡皙溪嘻嬉窸稀蹊蟋曦习席袭洗喜戏系细隙"
hz_jin_jing="巾今斤金矜津筋禁仅尽紧堇谨锦劲进近浸烬晋京径经荆惊晶睛鲸井景净竞竟靓敬静境镜颈精浄警"
hz_pin_ping="拼贫频品聘乒平评凭坪屏瓶苹萍"
hz_ba="八巴扒叭坝把吧芭爸拔疤笆粑耙罢捌跋靶魃霸"
hz_jiu="九久旧纠臼究鸠玖灸咎疚韭赳柩酒阄救厩就揪啾舅鹫"
hz_jiu_1="九久纠究鸠玖灸韭赳阄揪啾"
hz_bai="白百伯佰拜柏掰" # 排除：败摆
hz_du_1="度渡镀肚杜堵睹赌读渎犊椟独毒嘟督笃妒" # 排除：竺都
hz_du_2="度渡镀肚杜堵睹独毒都"
hz_liu_lu="六刘柳浏流留琉硫碌溜馏遛榴瘤卢庐芦陆卤虏炉录鸬赂鹿颅绿鲁禄鲈路噜撸辘戮橹璐鹭露" # 重复：六碌
hz_si_shi="四司丝死寺似私祀伺饲驷食思斯肆嗣厮撕嘶十尸士氏什示矢石史市失仕世式师时识始饰视鸤虱实驶事势使侍诗试施恃柿是蚀拭适室狮拾屎峙舐轼逝硕匙释湿谥弑誓嗜噬螫" # 重复：似食
#hz_wei="卫为韦未危伪伟围纬尾违苇位委味畏威娓维惟唯帷萎偎谓尉喂猥痿微蔚薇魏巍"
hz_wei_1="卫未位味畏维萎谓尉喂蔚"
hz_wei_2="为伟围维唯魏"
hz_wei_3="为未伪纬苇委味畏维惟萎谓尉蔚"
hz_ni="尼拟泥妮昵逆倪匿腻溺霓" # 排除：你呢
hz_ma="马妈吗码玛蚂犸麻嘛骂蟆抹"
#hz_bo="卜伯驳拨波泊勃柏玻剥饽钵铂菠啵脖舶博渤搏箔播薄簸"
hz_fa="乏发伐法罚阀砝"
hz_lun="仑伦论抡沦纶囵轮"
hz_gong="公工功供宫攻恭弓躬龚蚣拱巩汞共贡"
hz_chan_1="产铲蝉婵禅󠀠掺缠馋潺󠀠"
hz_an_1="安按鞍案氨岸俺庵"
hz_qing="轻庆亲青请情清晴顷倾卿磬罄擎"
hz_feng_1="风枫凤丰封奉峰"

pm=r".,!?+*/#%&^$`(){}…@~\"\'\\;:<>|=·。，！？；：￥“”‘’—（）【】「」\-\[\]" # 常见标点符号，用于正则表达式的[]内，不得用于words内
ja="\u3040-\u309F\u30A0-\u30FF" # 日文假名，用于正则表达式的[]内
cn="\u4E00-\u9FA5" # 汉字，用于正则表达式的[]内
sp="\U000E0020" # 旧版机制填充符，已由U+0592改为U+E0020
safe_pat=re.compile(r"[\d%s]"%cn) # 正则模式: 匹配数字或汉字

fill = lambda s,n: s+sp*(n-len(s)+s.count(" ")) #函数：使用填充符来填补字符串s，使其中的非空格字符数等于n
add_filler = lambda x: x.group()+sp # 函数：在匹配项后插入填充符
add_space = lambda x: x.group()+" " # 函数：在匹配项后插入空格
insert_filler = lambda x: x.group()[0]+sp+x.group()[1:] # 函数：在匹配项的第一个字符后插入填充符
insert_space = lambda x: x.group()[0]+" "+x.group()[1:] # 函数：在匹配项的第一个字符后插入空格
insert_both = lambda x: x.group()[0]+sp+" "+x.group()[1:] # 函数：在匹配项的第一个字符后依次插入填充符和空格

# 屏蔽词列表
words =  [ 
    # 1.0保护性处理
    "视频", "公主", "超市", "毕业", "人大", "洗澡", "东西", "尿尿", "蛋蛋", "屁股", "内裤",
    "小学生", "dps", "n#1i#2m",

    ### 一般屏蔽词（易变动）   1.0版本，填充字符即可解决
    "即位", "在任", "下台", "倒台", "候选", "上位", "票选", "换届",
    "总理", "总统", "纪委", "政府", "议会", "特首", "书记", "团派",
    "修正", "特权", "政策", "提案", "出访", "审查", "官腔",
    "安门", "赤字", "民众", "民意", "康米", "阶层", "权斗", "中特",
    "生事", "游行", "颠覆", "煽动", "乱暴", "动乱", "政变", "落马", "侵略",
    "分裂", "抗议", "罢工", "冷战", "圣战", "革命", "起义", "抗争", "厌世", "卖国",
    "军队", "部队", "萨德", "履带", "卫兵", "警察", "八路", "番号", "兵团", "公安",
    "囚禁", "捆绑", "割腕", "剥削", "鞭尸", "灌肠", "嗑药", "罂粟", "吗啡", "砒霜󠀠󠀠",
    "中出", "高潮", "诱惑", "双飞", "梆硬", "女同", "男同", "体位", "吉尔", "乳房",
    "喘气", "喘息", "娇喘", "呻吟", "处男", "绅士", "性癖", "裸镜", "半裸", "口活",
    "胖次", "罩杯", "嘿咻", "吹气", "掏耳", "助眠", "耳语", "脏病", "开冲", "炮友",
    "勃起", "出轨", "黑化", "痴汉", "进裙", "爽爆", "无修", "带套", "猥亵", "阴处",
    "肉便", "玩逼", "看腿", "御姐", "迷途", "无码", "裙底", "换妻", "胸罩", "露沟",
    "脱光", "丝袜", "漏点", "媚药", "很太", "热舞", "发情", "交配", "浪叫", "早泄",
    "膝下", "胯下", "扶她", "看片", "凸起", "全裸", "日狗", "裸照", "几把", "抽插󠀠",
    "袭胸", 
    "肥猪", "嘴臭", "拉屎", "撤硕", "低俗", "憨批", "傻吊", "喷粪", "屎会󠀠", "我日",
    "碧池", "禽兽", "畜生", "吃屎", "智障", "杂种", "猥琐", "废物", "愚民", "歧视",
    "台湾", "香港", "澳门", "日吹", "徐州", "高丽",
    "油管", "推特", "新浪", "抖音", "优酷", "虎牙", "斗鱼", "战旗", "飞稻",
    "皇帝", "皇宫", "庙堂", "磕头", "安乐", "包养", "清真", "还愿", "黑魂", "如龙",
    "赌博", "扑克", "彩票", "博彩", "菠菜", "借贷", "贷款", "网贷", "传销", "贿赂",
    "新冠", "防疫", "疫情", "硫酸", "草酸", "甲烷", "煤气", "氨水", "氨气", 
    "四六", "五四", "七一", "七五", "九八", "双十",
    "即为", "豪迈", "触摸", "慎重", "三尺", "鲍鱼", "河蟹", "洗地", "家宝", "外溢",
    "代打", "躺平", "要素", "上吊", "读错", "下乡", "闪灵", "集资", "奥运", "种台",
    "盗取", "茅台", "痔疮", "利益", "不办", "变质", "维他", "别来", "刑啊", "真主",
    "秃鹰", "细腻", "泼墨", "发酵", "快排", "匕首", "紫砂", "漏牛", "墙外",
    "动森", "映画", "老母", "青蛙", "口误", "连睡", "内设", "平总", "纹身", "毒圈",
    "黑幕", "猎奇", "冲塔", "逆行", "太安", "弹舌", "螳臂", "挡车", "全套", "费肾",
    "牛芝", "比心", "横幅", "饭友", "尚气", "赛艇", "催吐", "月经", "接单", "山路",
    "小熊", "尼维", "吼哇", "吼啊", "膜导", "长者", "長者", "郭嘉", "台国",
    "与正", "蒂亚", "稻上", "飞草", "熊学", "伐龙", "家明", "马云", "唐可", "泽东",
    "小瓶", "晓平", "超良", "虫也", "虫合", "换声", "代开", "网球", "发票", "惊悚",
    "追思", "佐助", "腊肉", "抑郁", "发漂", "咧嘴", "莉娅", "丽娅", "汪洋", "楚晨",
    "冈本", "太君", "入赘", "度良", "哄睡", "三胖", "多震", "迪迦", "觅食", "讽刺",
    "张为", "清场", "喷水", "西氏", "泌尿", "嫁衣", "骑脸", "攻正󠀠", "発射", "颅内",
    "扩列", "瘠薄", "暗网", "舆论", "神坛", "川普", "空降", "洗白", "透过", "大鸟",
    "上贡", "恩来", "入肉", "夜勤", "病栋", "外围", "老八", "猫王", "不厚", "有沟󠀠",
    "橄榄", "分尸", "膜包󠀠", "葱油󠀠", "领主", "天包", "气弹", "烟弹", "微冲", "殉教",
    "a片" , "造f" , "抖m" , "妹y" , "h漫" , "h肉", "约p",  "文g" ,
    "ロリ", "はま", "ハマ", "しな", "シナ", "くま", "エロ",

    "gc", "hw", "hk", "qd", "rh", "zf",
    "abs", "cjp", "cnm", "cov", "cum", "gay", "ghs", "hhd", "hso", "kui", "lsp", "nmb", "nmd", "ntr", "ply", "roc", "scp", "soe", "tmd", "usl", "wic", "wjb", "xxd",
    "anal", "arms", "bear", "biss", "dang", "drug", "frog", "fuck", "hath", "knee", "kuma", "liya", "loli", "nmsl", "ommc", "rori", "sina", "tank", "winn", "xxoo",
    "anmen", "baidu", "bajiu", "bitch", "ching", "elder", "luoli", "nword", "obama", "ruler", "sager", "secom", "shina", "wenny",
    "antifa", "fangyi", "father", "hentai", "heroin", "huanqi", "panzer", "reddit", "remake", "signal", "tianan", "tiktok", "twitch",
    "bigboss", "excited", "youtube", "exciting", "nekopara", "onedrive", "zhongguo", "hanzheng", "revolution", "neverforget",
    "64", "73", "404", "535", "586", "604", "718", "809", "817", "881", "918", "1926", "1953", "1979", "1989", "j8", "g20", "r19", "5km", "9ping",
    
    "自由门", "咖啡因", "死灵魂", "白衬衫", "生理期", "空气炮", "黑历史", "一本道", "养老金", "给我爬",
    "被传染", "网易云", "爱奇艺", "支付宝", "劈腿男", "缘之空", "一起死", "稻田上", "安眠药", "接班人", 
    "纪念日", "为自由", "绞肉机", "女菩萨", "毕业歌", "老鼠台", "网上搜", "别洗了", "理事长", "慢一拍",
    "脱衣服", "我要射", "小柜子", "奇酷比", "比基尼", "好日子", "吃粑粑", "大裤衩", "黑裤子", "色相头󠀠",
    "妖妖灵", "蛋炒饭", "异教徒", "跑得快", "牺牲品", "劳动法", "未成年", "小红书", "你的奶", "皮燕子󠀢",
    "麻酥酥", "兼职加", "水好多", "滚出去", "黄段子", "给我滚", "没衣服", "玻璃心", "不过审", "东京热",
    "色蝴蝶", "色天使", "色宝石", "振动棒", "震动棒", "战车道", "臂当车", "小黄油", "小黄书", "炸学校", 
    "小幸运", "换平台", "顶不住", "顶得住", "按回车", "找爸爸", "欧金金", "拼多多", "熊出没", "上床了",
    "有神明", "一直播", "看名字", "报警了", "被墙了", "大三元", "不作为", "再教育", "背锅侠", "遮羞布",
    "求救信", "这垃圾", "咀嚼音", "被消灭", "鲨了你", "家暴男", "胸好大", "死很多", "一夜情", "一刀切",
    "开黄腔", "空心菜", "硬起来", "踩油门", "是喷子", "吸血鬼", "爱发电", "灭火器", "没毕业", "按摩棒",
    "十字弓", "走后门", "敏感词", "委员会", "委員会", "检察院", "起风了", "都在笑", "乡下人", "一秒钟",
    "黑社会", "大哥哥", "搞黄色", "元老院", "没死成", "号不要", "我想舔", "打手枪", "太刑了", "赶紧死",
    "小鸟酱󠀠", "卖中国", "趣直播", "我冲了", "就去日", "乳制品", "想要舔", "拆腻子󠀠", "兴奋剂", "熊兔子",
    "小叽叽", "你全家", "不识字", "性器官", "是爱吃󠀢", "分钟吃", "是平的", "大白腿", "皮肤病", "歪脖子",
    "我在场", "到床上", "续一波",
    "李医生", "右大人", "梦大师", "金小姐", "刘先生", "熊先生", "马老师",
    "水龙敬", "清水健", "斯大林", "特朗普",
    "【萝莉", "就这？", "是sb"  , "nm呢" , "bb弹"  ,
    "四一二", "五三五", "八一七", "九一八", "九九六", "一九二六", "一九五三", 
    "自由之门", "继续前进", "并肩同行", "焕然一新", "二氧化碳", "阿里巴巴", "恐怖分子", "恐怖份子", "田所浩二", "蒙古上单",
    "身经百战", "黑框眼镜", "谈笑风生", "无可奉告", "微小的事", "活不下去", "飘飘欲仙", "分割人生", "坟头蹦迪", "b站员工" ,
    "我是黄金", "没有敌人", "少女之心", "奥斯曼人", "孩子的鞋", "花花公子", "不想回忆", "最大限度", "那个男人", "那位大人", 
    "脑子瓦特", "恐怖漫画", "乡关何处", "最后一课", "狼吞虎咽", "时间机器", "疲劳驾驶", "区别对待", "小学程度", "贤者时间",
    "的混合物", "波涛汹涌", "报复社会", "官方签约", "我还活着", "贤者模式", "侃侃而谈", "约德尔人", "社会主义", "要开会了",
    "健身教练", "为所欲为", "人生经验", "银河联邦", "活塞运动", "再来一次", "夫目前犯", "自产自销", "贫富差距", "遥遥领先",
    "中国制造", "中国大妈", "中国特色", "就是中国", "时光老人", "满口谎言", "加急名单", "正中下怀", "直接取消", "口吐芬芳", 
    "菜鸡互啄", "丝绸之路", "画了个圈", "苍天已死", "黄天当立", "下体一凉󠀠", "贤者时间󠀠", "张开双腿", "我的很大", "你忍一下",
    "浅尝辄止", "经济问题",
    "逃生2", "黎明杀", "黑暗之魂", "求生之路", "上古卷轴", "侠盗飞车", "尸体派对", "动物之森", "生化危机",
    "9禁", "31年", "80年代", "110吗", "1月23", "7月1日", "7月5日", "7月13", "8月17日", "10月16日", "12月28", "十月十", #汉字格式的日期也会被屏蔽，这里没写出来
    "命运共同体", "这就是中国", "克里斯托弗", "东京食尸鬼", "心动文学社", "满嘴跑火车", "纯洁的白色", "悲伤的自由",
    "你是你我是我", "南无阿弥陀佛", "热爱105度", "三国演义西游记",

    ### 多字符间隔屏蔽词
    "性#1[骚騷]#1扰", "奥#1数#1[魔默]", "一#1口#1[气吃喝]", "不#1[想配]#1活", "收#1[妹弟女]#1[妹弟儿]", "[色涩]#1咪#1咪", r"[?+\-]#1[1一]#1[秒s]", "[大小]#1吊#1子", "[掌当]#1权#1者", "[来冲]#1一#1发",
    "[一二三四五六]#1代#1目", "[哥姐弟妹爸妈爷奶儿女]#1[哥姐弟妹爸妈爷奶儿女]#1[日操]",
    "下#1面#2[松紧毛]", "回#1来#3谢", "观#1众#3v", "还#1没#3封", "不#1要#3要", "中#1国#4熊", "[姐妹姑]#1[姐妹娘]#5[逼b]", "弟#1弟#6大", "护#1照#6办", "飞#1机#6好", "有#1一#6账",
    "射#2出#1来", "湿#2视#2频", "[01]#2找#2[01]",
    "[逼b]#3看#1吗", "[搜艘馊嗖]#3这#1个", "投#3比#1赛", "看#3[头昵内签i]#1[像称裤名d]", "戴#3绿#1帽", "吃#3菊#1花", "摸#3[下屁]#1[面屁股]", "我#3好#1痒", "h#3动#1[画漫]", "[加减]#3[1一]#1秒", "6#3月#24", "黄#3漫#1画",
    "同#3性#3恋", "道#3上#3飞", "名#3字#3看", "我#3是#3处", "下#3面#3好", "习#3d#3d", "看#3[洗爱]#3[澡爱]", "干#3一#3发", "听#3国#3歌", "[爱操干草]#3萝#1莉", "少#3女#3[下自]", "打#3飞#3机", "直#3播#3[日草艹操曰]", r"的#3[没免]#4[穿钱费\d]",
    "射#4身#1上", "童#4收#1养", "买#4烟#1花", "[删关]#4评#1论", "改#4中#1国", "找#4小#1姐", "天#4[%s]#4[门们闷]"%hz_an_1, "萝#4莉#4控", "正#4太#4控", "加#4速#4器", "不#4换#4届", "[%s]#4大#4大"%hz_xi, 
    "[你尼]#4[妈马吗码蚂玛犸麻嘛母m家]#4[死币比逼必痹猪狗bp]", "[大小妈姐妹哥弟一二三四五六七八九]#4[小姐妹哥弟一二三四五六七八九]#5[在来做进]",
    "手#5指#5插", "徐#5上#5爽", "谢#5日#5双", "下#5面#5痒", "崔#5塔#5娜", "[包许张]#5[含艾]#5[雪莉丽]", "[左右徐]#5上#5觉", "安#5玩#5娜", "[索爱艾]#5男#5枪", "王#5锤#5石", "金#5塔#5姆", "给#5草#5了",
    "[马周]#5上#5[文梦琴]", "[鲁撸露打]#5一#5发", "[徐许]#5[上玩日]#5[碧双霜雪]", "[马就]#5[想上]#5[鲁撸噜门们]", "日#5[和河]#5[吗马码玛蚂犸]",
    "[%sail百败掰摆柏伯噜]#6[就上去还点被了射让]#4[来射车有点出被入抽]"%hz_du_1, "[日草艹操干曰死烧解透跳杀骂唱]#6[你尼拟我他她它女]#5[妈马吗码蚂玛犸嘛母m家]",
    "文#6古#6花", "看#6地#6方", "不#6钱#6[啊3]", "[谢x]#6s#6w", "有#6黄#6色", "微#6信#9[0-9a-z_]",
    "点#1点#1点", "大#1大#1大#1大#1大", "啪#2啪#2啪","娅#6娅#6娅", "加#1速#1加#1速", "嘀#1哩#1嘀#1哩", "[啪绿弯湾内色涩瑟哑娅撸噗鼠丫套]#1\\1",
    
    "找#1工#1作#3加", "准#1备#3纸#1巾", "都#1是#3衣#1服", "那#1个#4[老奶]#1[太奶]", "羊#1羊#4结#1婚", "学#1生#4学#1生",
    "看#1我#5名#1字", "妈#1妈#6唱#1歌", "不#1论#6生#1死", "时#1间#6老#1人", "[姐妹哥]#1[姐妹哥]#6大#1腿",
    "[01]#2还#1是#2[01]", "权#2利#2斗#2争", "你#3画#3我#3猜", "闭#3关#3锁#3国", "不#3穿#3衣#3服", "不#3穿#3内#1裤", "了#3没#3浪#3费", "看#3我#3i#1d", 
    "看#6我#6[头昵]#6[像称]", "清#6透#6世#6界", "在#6家#6寂#6寞", "买#6信#1用#1卡", "想#1要#1的#4来#1拿", "想#6p#1a#1p#1a", "一#6个#6人#6寂#6寞", "想#1要#1的#4来#1拿", "不#1要#6这#1种#1事#1情", "1#10#3月#31#10",
    "a#6j#6p", "s#2e#2x", "t#6l#6y", "v#4b#3o", "v#2p#2n", "x#4j#4p", "x#6y#6z", "a#3s#3m#3r", "b#1o#3k#1i", "f#6l#6d#6f", "n#3t#1o#1p", "r#64#60#63", "w#1w#1w#1[.,·`。，、]",
    "n#2t#2t#1o#1p", "n#4d#4i#4p#4w", "r#6i#6o#6t#6s", "w#4e#4i#4b#4o", "t#6m#6m#6s#6m#6e", "y#4a#4y#4e#4a#4e",
    "1#1[68]#1禁", "7#1[.]#15", "1#1[.]#12#13", "1#18#1[c厘]#1[m米]", "9#6m#6k", "1#32#33#34#35#36#37#38#39#30",
    "[.,。·、]#1[cf]", "[.]#1g#1a", "[.，]#1t#1k", "[.,。，·、]#2c#2n", "[.]#6c#6c", "[.,。，·、]#2c#2o#2m", "[.]#5s#5i#5t#5e",
    "i#1s#1i#1s", "m#1a#1m#1a", "m#1i#1m#1i", "n#1i#1c#1o#1n#1i#1c#1o", "[dp]#1i#1l#1i#1\\1#1i#1l#1i", 
    
    "暴#1[饮食动乱徒民雷]", "被#1[透上轮]", "称#1[王皇帝神]", "初#1[心生]", "大#1[麻吊弔胸波奶胃法选]", "点#1[1cfl]", "腐#1[败敗]", "国#1[会歌难动运]", "果#1[体母加照]",
    "好#1[爸爹]", "黄#1[图游]", "回#1[逼b]", "魂#1[一二三123]", "鸡#1[儿脖头]", "金#1[砖三四]", "精#1[美日湛子]", "就#1[职職]", "卖#1[春肉批逼b]", "奶#1[头汁水大]", "乃#1[子兹滋大]", "闹#1[大事剧]", "虐#1[待杀殺]",
    "人#1[肉兽日]", "乳#1[头首量水摇沟]", "色#1[情图欲狼批逼b]", "涩#1[气批片p]", "射#1[爆爽]", "死#1[吧法ね]", "舔#1[你您他她它脚]", "跳#1[楼崖蛋河海]", "天#1[安朝谴]",
    "微#1[博搏勃]", "[想给]#1[日草艹曰射操]", "选#1[举民票战]", "野#1[爹妈味]", "榨#1[干汁]", "自#1[残省重刎]",
    "[狂猛]#1吃", "[犬蛋刁]#1大", "[包白草操]#1粉", "[一尼泥]#1哥", "[中终阿啊]#1共", "[走扒]#1光", "[美米韩冲]#1国",
    "[两二2]#1会", "[看叫烧做]#1鸡", "[调传宗]#1教", "[吞吃受]#1精", "[兄弟妹足]#1控", "[工重给]#1口", "[湿射硬支]#1了", "[逼b]#1里", "[你送死]#1妈", "[批阴]#1毛", "[之纸拆]#1那", "[玩双晕]#1奶", "[施受]#1虐", "[处下熟幼痴]#1女",
    "[欧猫毛]#1派", "[费捞洗水]#1钱", "[左右]#1倾", "[军鸣催藏点]#1人", "[贫平双爆]#1乳", "[黑白]#1丝", "[杀去爽干操草爹妈饿想该作求毒]#1死", 
    "[肉性]#1欲", "[条包孢窑梯秃矮棒牛稻]#1子", "[谢謝]#1罪",
    "[插吸]#1[你他她它]", "[红紅]#1[魔通]", "[鸡己几寄性基]#1[吧巴八8⑧]",
    "网#2恋", "巨#2乳", "自#2尽", "涩#2情", "翻#2墙", "蓝#2灯", "人#2权", "[逼b]#2[真黑毛美]", "[黑美傻沙煞撒]#2[逼比笔鼻b]",
    "支#3那", "去#3搜", "共#3[产妻]", "毛#3东", "手#3[银冲]", "涩#3图", "肉#3棒", "邪#3教", "果#3聊", "裸#3体", "[粉吃吸]#3奶", "内#3射", "子#3宫", "排#3卵", "艾#3薇", "舔#3耳", "光#3光", "法#3功", "大#3熊", "陪#3睡", "望#3桥",
    "自#3[杀殺慰]", "鸡#3[巴八8⑧鸡]", "[涩色]#3网", "被#3[日草艹操曰]", "[习習吊弔]#3大", "[草艹操]#3[逼b]", "[逼b]#3内", "[下压]#3注", "[六6]#3中","[色卖h]#3片", "[做作坐座]#3[爱暖]", "[加+]#3[微薇v]", 
    "六#4四", "八#4九", "车#4震", "援#4交", "后#4入", "流#4世", "主#4席", "赤#4毒", "孤#4儿", "倒#4车", "约#4炮", "共#4共", "前#4妻", "看#4胸", "包#4力", "[阴陰]#4道",
    "明#4[泽z]", "近#4[苹评]", "[小进]#4平", "[连再]#4任", "吃#4[比逼币笔]", "[日草艹操干曰]#4[姐妹奶姨吊弔妇]", 
    "留#5水", "性#5[爱交]", "威#5雄",
    "罗#6莉", "萝#6[利俐]", "丽#6丽", "宽#6衣", "枪#6[买卖]", "刀#6卖", "卖#6刀", "震#6好", "维#6尼", "敲#6锅", "胸#6腿", "彭#6s", "[彭澎p]#6帅", "[逼b]#6紧", "[习習]#6[近进]", "[黄璜簧皇色]#6[网站片]",
    "习#8下", "幼#8[比逼b]", "越#9共", "[买卖]#9枪",
    
    ### 拼音/部首组合相关
    "[%s]#1[一1]#1下"%(hz_du_2),
    "[%s]#3大#1大"%(hz_xi),
    "[%s]#3没#1了"%(hz_ma),
    "[%s摆败干]#3[一1]#4下"%(hz_bai), # 顺带处理"干#3一#3下"
    "[两量凉梁良粮粱]#4[加家架假甲嫁佳贾驾茄夹+]#4[和河何呵喝核合盒贺禾荷]", #待补充
    "[裸棵菓粿踝]#1聊",
    "[%s]#1[%s]"%(hz_wei_1,hz_ni),
    "[%s]#1尼"%(hz_wei_2),
    "[%s]#3博"%(hz_wei_3),
    "[%s]#1[%s读赌]"%(hz_bai,hz_du_2),
    "[%sq]#1[%s分f]"%(hz_qing,hz_feng_1), # 对填充符要求较高
    "[%s败]#2调#2查"%(hz_bai),
    "[百白]#3[度渡镀查d]",
    "[%s伪]#3娘"%(hz_du_1),
    "[形型刑邢行]#1[%s]"%(hz_pin_ping),
    "[%scx]#2[%s呼砰怦秤抨]"%(hz_xi,hz_pin_ping),
    "[%s]#2p"%(hz_xi),
    "[%s8⑧]#3[%s]"%(hz_ba,hz_jiu),
    "[%s]#3[9⑨]"%(hz_ba),
    "[%scx]#3[%s青蜻箐]"%(hz_xi,hz_jin_jing), # 注：此规则无视全角空格
    "[%s青蜻箐斥芹斩析祈折所]#3[%s呼乎砰怦秤抨p]"%(hz_jin_jing,hz_pin_ping), 
    "[%s6⑥]#3[%s舍捨]"%(hz_liu_lu,hz_si_shi),
    "[%s]#3[4④]"%(hz_liu_lu),
    "[xw]#3[%s]"%(hz_jiu_1),
    "康#6[买卖麦脉埋迈霾]",
   
    ### 字母+汉字（仅作简单处理）
    "si法", "你ma", "mei药", "媚yao", "吃shi", "发xiao", "刷ins", "被ri", "tb直播", "[大小]#1jj", "lu#2发", "加#4qq", "gong#4gong", "くるみ#3ぽんちお",
    "[微薇]#4bo", "dio#3[大小]", "diao#3[大小]", "ri#1[我你]", "d#3u#3娘", "天#4a#1n#4[门们闷]",

    ### 以下词汇屏蔽已失效
    # "领袖", "领导", "大会", "会议", "疫情", "和谐", "许愿", "退钱", "厕所", "巨人", "人妻", "伞兵", "屏蔽",
    # "神社", "改变", "签约", "失望", "控制", "节奏", "赤裸", "天城", "成都", "爸爸", "没封", "电竞",
    # "黑手", "集会", "光荣", "虾膜", "成人", "中央", "万岁", "萝莉", "没了", "死了", "上街",
    # "选拔", "月半", "淘宝", "试看", "百年", "庆典", "广场", "小乳", "人大",
    # "痒", "爬", "奠", "6年", "71", "1921", "av", "g7", "ma", "sb", "tg", "yuan", "100kg",
    # "不习惯", "发不出", "就去泡", "莉莉安", "不唱歌", "甜蜜蜜",
    # "风平浪静", "老不死的", "特别待遇",
    # "好#4胸", "吉儿", "黄#4红",
]

# 反屏蔽处理规则字典，键为正则匹配表达式（字符串, pat），值为处理结果（字符串或函数, rep）
rules = {
    ### 连续半角空格处理（务必作为rules的第一项）
    " +" :" ",
    ### 单字/特殊字符
    "(?<![花牡虾海车香])蛤(?![蜊蚧子蜃])":"haᐟ", "蛤": "geᐟ",
    "翠": "翆", "骚": "騷", "尻": "𡱧", "淫":"yinᐟ", "岿": "巍", "屌": "吊", "党": "dαngᘁ", "慎": "shenᐠ", "贱": "賎", "婊": "biaoᘁ", "焯": "chaoᐠ",
    "[àáâãäåÀÁÂÃÄÅāǎ]": "a", "[èéêëÈÉÊËēě]": "e", "[ìíîïÌÍÎÏīǐ]": "i", "[òóõôöÒÓÔÕÖōǒ]": "o", "[ùúûüÙÚÛÜūǔ]": "u", "[ǖǘǚǜü]": "v",
    "⑤": "(5)", "⑥": "(6)", "⑧": "(8)", "⑨": "(9)", "⑩": "(10)", "０": "0", "５": "5", "６": "6", "９": "9", "×": "x", "❤": "♡", "🎶": "♬", "♀": "",
    "Ⅰ": "I", "Ⅱ": "II", "Ⅲ": "III", "Ⅳ": "IV", "±": "+-",
    ### 英文特殊处理规则
    r"(?ia)(?<!\w)t(?: ?w| ?a ?m)(?! ?\w)": insert_filler,
    r"(?ia)(?<!\w)x ?i(?! ?\w)": insert_filler,
    r"(?ia)(?<!\w)(i ?l ?i ?)(b ?i ?l ?i ?b)(?! ?\w)": lambda x: x.group(1)+sp+x.group(2),
    r"(?a)(?<!\w)8 ?.? ?(?=9(?! ?\w))": lambda x: fill(x.group(),3),
    r"6[ %s]*4"%pm: insert_filler,
    r"A ?V": insert_filler,
    ### 中文特殊处理规则
    r"[草艹操日曰干扣](?=[ %s]*[你您我他她它比笔逼妈父母]|时光|女儿|螃蟹)"%pm: add_filler,
    r"(?i)[%sg洪哄烘](?=[ %s]*[%sc期妻7])"%(hz_gong,pm,hz_chan_1): add_filler,
    r"幼(?=(?: ?[^\s幼]){0,2} ?[比逼b])": "youᐠ",  # 幼#8[比逼b]  短间隔处理方式
    r"越(?=(?: ?[^\s越]){0,3} ?共)": "yueᐠ",       # 越#9共      短间隔处理方式
    r"[买卖](?=(?: ?[^\s买卖]){0,3} ?枪)": lambda x: "mai"+("ᘁ" if x.group()=="买" else "ᐠ"), # [买卖]#9枪  短间隔处理方式
    r"猎(?= ?人.*?电 ?影)": add_filler, # 猎#1人#13电#1影
    r"[买卖].*?硬(?= ?币)": add_filler,
    r"(小 ?学|[初高] ?中|年 ?级)(?=.*?[外语书政])": insert_filler, # 格式：甲#1乙#9丙(#1丁)
    r"(上? ?[舰船] ?长?|[总提] ?督|大 ?航 ?海)(?=(?: ?[^\s送]){0,4}送)": lambda x: sp.join(x.group()),
    r"[习習](?=.*?[平苹])": "Χiᐟ",
    r"炼(?=.*?铜)": "lianᐠ",
    r"[撸噜] ?[^\s撸噜]?(?= ?一.*?下)": lambda x: fill(x.group(),3),
    r"(?i)[习習].*?a ?p ?p": lambda x: x.group()[:-1]+sp+x.group()[-1],
    r"(?i)([六6⑥]|l ?i ?u)(.*?)([四肆4④]|s ?i)": lambda x: (x.group(1)+fill(x.group(2),4)+x.group(3)) if x.group(1)+x.group(3)!="64" else x.group(),
    r"(?i)([%s] ?|f ?a? ?)([%s会能弄冷案]|l ?u ?n)"%(hz_fa,hz_lun): insert_filler,
    r"(?ia)[加+](?: ?[^\s加+]){0,5}(?= ?[微薇v].*?\w)": lambda x: fill(x.group(),7), # [加+]#6[微薇v]#11[0-9a-z_]
    ### 保护型处理规则
    r"[习習]": add_filler,
    r"(?i)r(?= ?i(?: ?[^\si]){0,6}?[你您尼我他她它])": add_filler,
    r"(?i)n(?= ?i(?: ?[^\si]){0,6}?[妈吗玛马嘛母家娘姐妹奶])": add_filler,
    r"(?i)t(?= ?a(?: ?[^\sa]){0,6}?[妈吗玛马嘛母家娘姐妹奶])": add_filler,
    
    ### 2.0版本屏蔽字，填充机制不适用，一般需要加空格
    "鲶": "鯰", "龅": "齙", "雑": "杂", "捋": " 捋", "猥": "weiᘁ",
    "尼嚎": "你好", "铸 ?币": f"鋳{sp}币", "壁ドン": "壁咚", "症候群": "综合征",
    "人妖": "人yaoᐨ", "咖喱 ?人": "咖喱renᐟ", "巨婴": "juᐠ婴", "弱智": "ruoᐠ智", "傻 ?子": "shaᘁ子", "奶 ?子": "naiᘁ子", "(?<!繁)琐":"suoᘁ", "(?<![小文])丑": "chouᘁ", "(?<!愚)蠢(?!蠢|欲动)": "chunᘁ",
    "臭(?=[小老八弟])": "臭",
    r"变(?=\S?态)": "変",
    r"恶(?=\S?[心啊吧吗嘛么])": "悪",
    r"母(?=的|亲[呢吗嘛])": "⺟",
    r"((?:[嘴脸鼻眼脑舌肚腿病胖矮肥笨傻蠢丑]|学生)\S{0,6}?)样": lambda x: x.group(1)+"様",
    r"(?<!\s)([真太很好挺]|有一?点)(?=[^\s不]{0,3}[烦怪脏臭疯吓吵恶悪])": lambda x: " "+x.group(),
    r"(?<![\s\d%s])死(?![\s%s])"%(cn,cn): "si",
    "声音(?=.{0,3}[好真挺太很偏点])": "声⾳",
    "司马(?![懿光])": "司⻢",
    "[点个]胖": insert_space, # 优先于list_1进行处理
}

# 根据周围字符情况，在左侧/右侧/中间加空格。
list_1=[
    "全家", "柴犬", "狒狒", "猩猩", "双亲", "股间", "倚老", "猴子?",
    "弱狗", "彩笔", "活该", "闭嘴", "大妈", "肥仔", "整容", "死宅", "病弱",
    "老太婆", "神经质", "死鱼眼", "大舌头", "好表现", "个样子?", "痴呆症?",
    "睁[开眼]", "残[疾障]", "脑[子袋]", "难[看听]", "小[偷丑]",
    "[病摔]死", "[矮崽]子", 
    "[长胖矮肥笨傻蠢丑][得的成]", "垃圾[桶袋箱站]?(?!游戏)",
    "(?<![小狗])狗(?![狗头熊仔])", "滚(?![滚动轴雪])",
    r"[真太很好挺点个][^\s不真太很好挺点个]{0,3}(?:[胖矮肥傻笨蠢病丑废逊挫土]|老(?!师))",
]

# 周围无空格/汉字/数字时，在中间加空格。
list_2=[
    "爹妈", "废柴", "肥宅", "妇女", "基佬", "好走", "娘子", "免费", "脏话", "下巴",
    "必死", "沙子", "马娘", "比个", "[真好]菜", "呕吐?",
    "孤勇者", "丑小鸭", "脏东西", "蠢蠢的?",
    "断[手脖]", "作[文者]", "菜[鸟鸡]", "傻[瓜子]", "[男女]妖|妖[怪精]?",
    "[村病]人", "[吐病]了", "[有狗]狗", "说话[好真]?难?",
]

# 在中间加填充符和空格。
list_3=[
    "人渣", "渣[男女]", "牲畜", "坦克", "上香", "快死", "[波啵玻簸][鸡及击几机肌姬󠀠基箕唧]",
]

# 在右侧加空格。
list_4=[
    r"[日草艹操干曰死烧解透跳杀](?=\S{0,3}[你您拟尼我他她它]\S{0,3}[妈马吗码蚂玛犸嘛母m家])",
    r"的(?=[嘴脸鼻眼舌肚腿])",
    r"[嘴脸鼻眼脑舌肚腿][子睛头巴蛋]?(?=\S{0,6}?[猴狗猪胖矮肥丑烦笨傻蠢怪废臭土大睁肿垃混脏逊滚糊挫碾吓怕像歪])",
    r"[你您他她这那][个们么样种些人]?的?(?=[^\s这那]{0,3}?[嘴脸鼻眼脑舌肚货猴狗猪胖矮肥丑烦笨傻蠢怪臭土歪睁肿垃混废脏丫逊滚挫碾鬼Pp])",
    r"[你您]们?\S?(?=[是比]个(?!好)|\S{0,3}年轻|[^\s吓笑]{0,6}[死滚])",
    r"样的?(?=\S{0,3}?[嘴脸鼻眼脑舌肚作])",
    r"像(?=\S{0,6}?[嘴脸鼻眼脑舌肚])",
    r"[嘴脑脸](?=\S?[跟还你])",
    r"没[有了]?(?=[妈马码蚂玛犸娘眼]|头?脑)",
    r"没[了似]?(?=吗)",
    r"你们?家(?=没)",
    r"[妈马吗码蚂玛犸嘛娘](?=[^\s妈吗嘛]?没)",
    r"(有[^\s生]{0,3})(?=(?<!中二)病)",
    r"[%s你您]们?(?=[^\s的]?[%s娘母])"%(hz_ni,hz_ma),
    r"[%s](?=\S?[%s您])"%(hz_ma,hz_ni),
    r"死(?=\S{0,3}[狗猪吧吗嘛啊呢哦呀么啦])",
    r"[病笨傻蠢臭胖矮肥狗猪猴土烦脏妈][蛋了味]?(?=[^\s妈笨傻蠢臭胖狗脏]{0,3}[成样吧吗嘛啊呢哦呀么啦](?!\s))",
    r"[菜笨傻胖肥臭](?=\S{0,2}[狗猪逼比笔币Bb])",
    r"吃(?=\S{1,2}饼)",
    r"作[^\s\d%s]*?(?=吧)"%cn,
    r"[要怪](?=\S{0,3}[脸鼻])",
    r"脸.{0,6}(?=吓)",
    r"碾碎?(?=\S{0,3}你)",
    r"大的?(?=[^\s墙]{0,6}壁)",
    r"[一条](?=狗)",
    r"[你您他她这那个]\S?小(?=偷)",
]

# 二次处理时，若周围无空格，则在右侧加空格。
str_ex="猴猩驴"+"脸鼻眼肚腿"+"胖矮肥烦笨怪废睁混脏菜残"+"跟睁作妇"

# 二次处理时，在中间加填充符。
ex_words=[]

# 二次处理规则汇总字典。
# 从LyricDanmu v1.5.0a开始， 可根据ex_rules对被屏蔽过一次的弹幕进行二次处理，降低再次被屏蔽的几率。
ex_rules={
    "臭": "臭", "恶": "悪", "变": "変", "猪": "猪", "样": "様", "女": "女", "鬼": "⿁", "母": "⺟", "日": "⽇", "马": "⻢", "铸": "鋳",
    "滚": "gunᘁ", "妖": "yaoᐨ", "傻": "shaᘁ", "圾": "ji", "死": "si", "炸": "zhaᐠ", "嘴": "zuiᘁ", "舌": "sheᐟ",
    "呕": "ouᘁ", "吐": "tuᐠ", "逼": "Ⲃiᐨ", "琐": "suoᘁ", "挫": "cuoᐠ", "渣": "zhaᐨ",
    "病 ?": "Ⲃingᐠ", "蠢 ?": "chunᘁ", "丑 ?": "chouᘁ", "脑 ?":"naoᘁ", "垃 ?": "laᐨ", "狗( ?狗)*": "gouᘁ", 
    r"[这那][么样様种些个是]?的?(?!\s)": add_space,
    r"[你您他她它]们?(?![\s这那])": add_space,
    r"(?<![\s吗嘛啊吧呢哦呀啦])[吗嘛啊吧呢哦呀啦]": lambda x: " "+x.group(),
    r"[%s]{4,}[^\r\n】]*(?=】?$)"%ja: lambda x: x.group()+" 1", #处理长日语假名夹杂着少量汉字的情况
}

def add_space_1(x:re.Match):
    text, pre, suf = x.group(), x.group("pre"), x.group("suf")
    if suf and re.search(safe_pat, suf):
        return text if suf[0] == " " else text + " "
    if pre and re.search(safe_pat, pre):
        return " " + text
    if len(text)<=1:
        return text + " 1"
    return text[0] + " " + text[1:]

for word in list_1:     rules[r"(?:^|(?<=(?P<pre>\S)))"+word+r"(?=(?P<suf> ?\S{0,3}))"]=add_space_1
for word in list_2:     rules[fr"(?<![\s\d{cn}]){word}(?![\s\d{cn}])"]=insert_space
for word in list_3:     rules[word]=insert_both
for word in list_4:     rules[word]=add_space
for char in str_ex:     ex_rules[r"(?<!\s)"+char+r"(?!\s)"]=add_space

# <DATA END>
