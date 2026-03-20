# 批量添加周易六十四卦数据 PowerShell 脚本

$dataFile = "C:\Users\25243\.openclaw\workspace\projects\zhouyi\zhouyi\data\hexagrams.json"

# 读取现有数据
$data = Get-Content $dataFile -Raw -Encoding UTF8 | ConvertFrom-Json

Write-Host "现有卦数：$($data.hexagrams.Count) 卦"
$existingIds = $data.hexagrams | ForEach-Object { $_.id }
Write-Host "现有卦 ID: $($existingIds -join ', ')"

# 20 卦完整数据（按尚书省优先顺序）
$newHexagrams = @(
    @{
        id = 3; name = "屯"; pinyin = "zhūn"; full_name = "水雷屯"; symbol = "䷂"; binary = "010001"
        upper_trigram = "坎"; lower_trigram = "震"
        judgment = "元亨利贞，勿用有攸往，利建侯"
        image = "云雷，屯。君子以经纶"
        lines = @(
            @{position = 1; text = "磐桓，利居贞，利建侯"; type = "yang"}
            @{position = 2; text = "屯如邅如，乘马班如。匪寇婚媾，女子贞不字，十年乃字"; type = "yin"}
            @{position = 3; text = "即鹿无虞，惟入于林中。君子几不如舍，往吝"; type = "yin"}
            @{position = 4; text = "乘马班如，求婚媾。往吉，无不利"; type = "yin"}
            @{position = 5; text = "屯其膏。小贞吉，大贞凶"; type = "yang"}
            @{position = 6; text = "乘马班如，泣血涟如"; type = "yin"}
        )
    },
    @{
        id = 4; name = "蒙"; pinyin = "méng"; full_name = "山水蒙"; symbol = "䷃"; binary = "001000"
        upper_trigram = "艮"; lower_trigram = "坎"
        judgment = "亨。匪我求童蒙，童蒙求我。初筮告，再三渎，渎则不告。利贞"
        image = "山下出泉，蒙。君子以果行育德"
        lines = @(
            @{position = 1; text = "发蒙，利用刑人，用说桎梏。以往吝"; type = "yin"}
            @{position = 2; text = "包蒙吉，纳妇吉，子克家"; type = "yang"}
            @{position = 3; text = "勿用取女，见金夫，不有躬。无攸利"; type = "yin"}
            @{position = 4; text = "困蒙，吝"; type = "yin"}
            @{position = 5; text = "童蒙，吉"; type = "yin"}
            @{position = 6; text = "击蒙，不利为寇，利御寇"; type = "yang"}
        )
    },
    @{
        id = 5; name = "需"; pinyin = "xū"; full_name = "水天需"; symbol = "䷄"; binary = "010111"
        upper_trigram = "坎"; lower_trigram = "乾"
        judgment = "有孚，光亨，贞吉。利涉大川"
        image = "云上于天，需。君子以饮食宴乐"
        lines = @(
            @{position = 1; text = "需于郊，利用恒，无咎"; type = "yang"}
            @{position = 2; text = "需于沙，小有言，终吉"; type = "yang"}
            @{position = 3; text = "需于泥，致寇至"; type = "yang"}
            @{position = 4; text = "需于血，出自穴"; type = "yin"}
            @{position = 5; text = "需于酒食，贞吉"; type = "yang"}
            @{position = 6; text = "入于穴，有不速之客三人来，敬之终吉"; type = "yin"}
        )
    },
    @{
        id = 6; name = "讼"; pinyin = "sòng"; full_name = "天水讼"; symbol = "䷅"; binary = "111010"
        upper_trigram = "乾"; lower_trigram = "坎"
        judgment = "有孚窒，惕中吉，终凶。利见大人，不利涉大川"
        image = "天与水违行，讼。君子以作事谋始"
        lines = @(
            @{position = 1; text = "不永所事，小有言，终吉"; type = "yin"}
            @{position = 2; text = "不克讼，归而逋，其邑人三百户，无眚"; type = "yang"}
            @{position = 3; text = "食旧德，贞厉，终吉。或从王事，无成"; type = "yin"}
            @{position = 4; text = "不克讼，复即命，渝安贞，吉"; type = "yang"}
            @{position = 5; text = "讼元吉"; type = "yang"}
            @{position = 6; text = "或锡之鞶带，终朝三褫之"; type = "yang"}
        )
    },
    @{
        id = 7; name = "师"; pinyin = "shī"; full_name = "地水师"; symbol = "䷆"; binary = "000010"
        upper_trigram = "坤"; lower_trigram = "坎"
        judgment = "贞，丈人吉，无咎"
        image = "地中有水，师。君子以容民畜众"
        lines = @(
            @{position = 1; text = "师出以律，否臧凶"; type = "yin"}
            @{position = 2; text = "在师中，吉无咎，王三锡命"; type = "yang"}
            @{position = 3; text = "师或舆尸，凶"; type = "yin"}
            @{position = 4; text = "师左次，无咎"; type = "yin"}
            @{position = 5; text = "田有禽，利执言，无咎。长子帅师，弟子舆尸，贞凶"; type = "yin"}
            @{position = 6; text = "大君有命，开国承家，小人勿用"; type = "yin"}
        )
    },
    @{
        id = 8; name = "比"; pinyin = "bǐ"; full_name = "水地比"; symbol = "䷇"; binary = "010000"
        upper_trigram = "坎"; lower_trigram = "坤"
        judgment = "吉。原筮元永贞，无咎。不宁方来，后夫凶"
        image = "地上有水，比。先王以建万国，亲诸侯"
        lines = @(
            @{position = 1; text = "有孚比之，无咎。有孚盈缶，终来有它，吉"; type = "yin"}
            @{position = 2; text = "比之自内，贞吉"; type = "yin"}
            @{position = 3; text = "比之匪人"; type = "yin"}
            @{position = 4; text = "外比之，贞吉"; type = "yin"}
            @{position = 5; text = "显比，王用三驱，失前禽。邑人不诫，吉"; type = "yang"}
            @{position = 6; text = "比之无首，凶"; type = "yin"}
        )
    },
    @{
        id = 9; name = "小畜"; pinyin = "xiǎo xù"; full_name = "风天小畜"; symbol = "䷈"; binary = "110111"
        upper_trigram = "巽"; lower_trigram = "乾"
        judgment = "亨。密云不雨，自我西郊"
        image = "风行天上，小畜。君子以懿文德"
        lines = @(
            @{position = 1; text = "复自道，何其咎，吉"; type = "yang"}
            @{position = 2; text = "牵复，吉"; type = "yang"}
            @{position = 3; text = "舆说辐，夫妻反目"; type = "yang"}
            @{position = 4; text = "有孚，血去惕出，无咎"; type = "yin"}
            @{position = 5; text = "有孚挛如，富以其邻"; type = "yang"}
            @{position = 6; text = "既雨既处，尚德载。妇贞厉，月几望。君子征凶"; type = "yang"}
        )
    },
    @{
        id = 10; name = "履"; pinyin = "lǚ"; full_name = "天泽履"; symbol = "䷉"; binary = "111011"
        upper_trigram = "乾"; lower_trigram = "兑"
        judgment = "履虎尾，不咥人，亨"
        image = "上天下泽，履。君子以辨上下，定民志"
        lines = @(
            @{position = 1; text = "素履，往无咎"; type = "yang"}
            @{position = 2; text = "履道坦坦，幽人贞吉"; type = "yang"}
            @{position = 3; text = "眇能视，跛能履。履虎尾，咥人，凶。武人贞凶"; type = "yin"}
            @{position = 4; text = "履虎尾，愬愬，终吉"; type = "yang"}
            @{position = 5; text = "夬履，贞厉"; type = "yang"}
            @{position = 6; text = "视履考祥，其旋元吉"; type = "yang"}
        )
    },
    @{
        id = 13; name = "同人"; pinyin = "tóng rén"; full_name = "天火同人"; symbol = "䷌"; binary = "111101"
        upper_trigram = "乾"; lower_trigram = "离"
        judgment = "同人于野，亨。利涉大川，利君子贞"
        image = "天与火，同人。君子以类族辨物"
        lines = @(
            @{position = 1; text = "同人于门，无咎"; type = "yang"}
            @{position = 2; text = "同人于宗，吝"; type = "yin"}
            @{position = 3; text = "伏戎于莽，升其高陵，三岁不兴"; type = "yang"}
            @{position = 4; text = "乘其墉，弗克攻，吉"; type = "yang"}
            @{position = 5; text = "同人，先号啕而后笑。大师克相遇"; type = "yang"}
            @{position = 6; text = "同人于郊，无悔"; type = "yang"}
        )
    },
    @{
        id = 14; name = "大有"; pinyin = "dà yǒu"; full_name = "火天大有"; symbol = "䷍"; binary = "101111"
        upper_trigram = "离"; lower_trigram = "乾"
        judgment = "元亨"
        image = "火在天上，大有。君子以遏恶扬善，顺天休命"
        lines = @(
            @{position = 1; text = "无交害，匪咎，艰则无咎"; type = "yang"}
            @{position = 2; text = "大车以载，有攸往，无咎"; type = "yang"}
            @{position = 3; text = "公用亨于天子，小人弗克"; type = "yang"}
            @{position = 4; text = "匪其彭，无咎"; type = "yang"}
            @{position = 5; text = "厥孚交如，威如，吉"; type = "yin"}
            @{position = 6; text = "自天佑之，吉无不利"; type = "yang"}
        )
    },
    @{
        id = 15; name = "谦"; pinyin = "qiān"; full_name = "地山谦"; symbol = "䷎"; binary = "000100"
        upper_trigram = "坤"; lower_trigram = "艮"
        judgment = "亨，君子有终"
        image = "地中有山，谦。君子以裒多益寡，称物平施"
        lines = @(
            @{position = 1; text = "谦谦君子，用涉大川，吉"; type = "yin"}
            @{position = 2; text = "鸣谦，贞吉"; type = "yin"}
            @{position = 3; text = "劳谦君子，有终吉"; type = "yang"}
            @{position = 4; text = "无不利，撝谦"; type = "yin"}
            @{position = 5; text = "不富以其邻，利用侵伐，无不利"; type = "yin"}
            @{position = 6; text = "鸣谦，利用行师，征邑国"; type = "yin"}
        )
    },
    @{
        id = 16; name = "豫"; pinyin = "yù"; full_name = "雷地豫"; symbol = "䷏"; binary = "000001"
        upper_trigram = "震"; lower_trigram = "坤"
        judgment = "利建侯行师"
        image = "雷出地奋，豫。先王以作乐崇德，殷荐之上帝，以配祖考"
        lines = @(
            @{position = 1; text = "鸣豫，凶"; type = "yin"}
            @{position = 2; text = "介于石，不终日，贞吉"; type = "yin"}
            @{position = 3; text = "盱豫，悔。迟有悔"; type = "yin"}
            @{position = 4; text = "由豫，大有得。勿疑，朋盍簪"; type = "yin"}
            @{position = 5; text = "贞疾，恒不死"; type = "yin"}
            @{position = 6; text = "冥豫，成有渝，无咎"; type = "yin"}
        )
    },
    @{
        id = 17; name = "随"; pinyin = "suí"; full_name = "泽雷随"; symbol = "䷐"; binary = "011001"
        upper_trigram = "兑"; lower_trigram = "震"
        judgment = "元亨利贞，无咎"
        image = "泽中有雷，随。君子以向晦入宴息"
        lines = @(
            @{position = 1; text = "官有渝，贞吉。出门交有功"; type = "yang"}
            @{position = 2; text = "系小子，失丈夫"; type = "yin"}
            @{position = 3; text = "系丈夫，失小子。随有求得，利居贞"; type = "yin"}
            @{position = 4; text = "随有获，贞凶。有孚在道，以明，何咎"; type = "yang"}
            @{position = 5; text = "孚于嘉，吉"; type = "yang"}
            @{position = 6; text = "拘系之，乃从维之。王用亨于西山"; type = "yang"}
        )
    },
    @{
        id = 18; name = "蛊"; pinyin = "gǔ"; full_name = "山风蛊"; symbol = "䷑"; binary = "100011"
        upper_trigram = "艮"; lower_trigram = "巽"
        judgment = "元亨，利涉大川。先甲三日，后甲三日"
        image = "山下有风，蛊。君子以振民育德"
        lines = @(
            @{position = 1; text = "干父之蛊，有子，考无咎。厉终吉"; type = "yang"}
            @{position = 2; text = "干母之蛊，不可贞"; type = "yang"}
            @{position = 3; text = "干父之蛊，小有悔，无大咎"; type = "yang"}
            @{position = 4; text = "裕父之蛊，往见吝"; type = "yin"}
            @{position = 5; text = "干父之蛊，用誉"; type = "yin"}
            @{position = 6; text = "不事王侯，高尚其事"; type = "yang"}
        )
    },
    @{
        id = 19; name = "临"; pinyin = "lín"; full_name = "地泽临"; symbol = "䷒"; binary = "000011"
        upper_trigram = "坤"; lower_trigram = "兑"
        judgment = "元亨利贞。至于八月有凶"
        image = "泽上有地，临。君子以教思无穷，容保民无疆"
        lines = @(
            @{position = 1; text = "咸临，贞吉"; type = "yang"}
            @{position = 2; text = "咸临，吉无不利"; type = "yang"}
            @{position = 3; text = "甘临，无攸利。既忧之，无咎"; type = "yin"}
            @{position = 4; text = "至临，无咎"; type = "yin"}
            @{position = 5; text = "知临，大君之宜，吉"; type = "yin"}
            @{position = 6; text = "敦临，吉无咎"; type = "yin"}
        )
    },
    @{
        id = 20; name = "观"; pinyin = "guān"; full_name = "风地观"; symbol = "䷓"; binary = "110000"
        upper_trigram = "巽"; lower_trigram = "坤"
        judgment = "盥而不荐，有孚颙若"
        image = "风行地上，观。先王以省方观民设教"
        lines = @(
            @{position = 1; text = "童观，小人无咎，君子吝"; type = "yin"}
            @{position = 2; text = "窥观，利女贞"; type = "yin"}
            @{position = 3; text = "观我生，进退"; type = "yin"}
            @{position = 4; text = "观国之光，利用宾于王"; type = "yin"}
            @{position = 5; text = "观我生，君子无咎"; type = "yang"}
            @{position = 6; text = "观其生，君子无咎"; type = "yang"}
        )
    },
    @{
        id = 21; name = "噬嗑"; pinyin = "shì kè"; full_name = "火雷噬嗑"; symbol = "䷔"; binary = "101001"
        upper_trigram = "离"; lower_trigram = "震"
        judgment = "亨，利用狱"
        image = "雷电，噬嗑。先王以明罚敕法"
        lines = @(
            @{position = 1; text = "屦校灭趾，无咎"; type = "yang"}
            @{position = 2; text = "噬肤灭鼻，无咎"; type = "yin"}
            @{position = 3; text = "噬腊肉，遇毒。小吝，无咎"; type = "yin"}
            @{position = 4; text = "噬乾胏，得金矢。利艰贞，吉"; type = "yin"}
            @{position = 5; text = "噬乾肉，得黄金。贞厉，无咎"; type = "yin"}
            @{position = 6; text = "何校灭耳，凶"; type = "yang"}
        )
    },
    @{
        id = 22; name = "贲"; pinyin = "bì"; full_name = "山火贲"; symbol = "䷕"; binary = "100101"
        upper_trigram = "艮"; lower_trigram = "离"
        judgment = "亨。小利有攸往"
        image = "山下有火，贲。君子以明庶政，无敢折狱"
        lines = @(
            @{position = 1; text = "贲其趾，舍车而徒"; type = "yang"}
            @{position = 2; text = "贲其须"; type = "yin"}
            @{position = 3; text = "贲如濡如，永贞吉"; type = "yang"}
            @{position = 4; text = "贲如皤如，白马翰如。匪寇婚媾"; type = "yin"}
            @{position = 5; text = "贲于丘园，束帛戋戋。吝，终吉"; type = "yin"}
            @{position = 6; text = "白贲，无咎"; type = "yang"}
        )
    },
    @{
        id = 23; name = "剥"; pinyin = "bō"; full_name = "山地剥"; symbol = "䷖"; binary = "100000"
        upper_trigram = "艮"; lower_trigram = "坤"
        judgment = "不利有攸往"
        image = "山附于地，剥。上以厚下安宅"
        lines = @(
            @{position = 1; text = "剥床以足，蔑贞凶"; type = "yin"}
            @{position = 2; text = "剥床以辨，蔑贞凶"; type = "yin"}
            @{position = 3; text = "剥之，无咎"; type = "yin"}
            @{position = 4; text = "剥床以肤，凶"; type = "yin"}
            @{position = 5; text = "贯鱼，以宫人宠，无不利"; type = "yin"}
            @{position = 6; text = "硕果不食，君子得舆，小人剥庐"; type = "yang"}
        )
    },
    @{
        id = 24; name = "复"; pinyin = "fù"; full_name = "地雷复"; symbol = "䷗"; binary = "000001"
        upper_trigram = "坤"; lower_trigram = "震"
        judgment = "亨。出入无疾，朋来无咎。反复其道，七日来复。利有攸往"
        image = "雷在地中，复。先王以至日闭关，商旅不行，后不省方"
        lines = @(
            @{position = 1; text = "不远复，无祗悔，元吉"; type = "yang"}
            @{position = 2; text = "休复，吉"; type = "yin"}
            @{position = 3; text = "频复，厉无咎"; type = "yin"}
            @{position = 4; text = "中行独复"; type = "yin"}
            @{position = 5; text = "敦复，无悔"; type = "yin"}
            @{position = 6; text = "迷复，凶，有灾眚。用行师，终有大败，以其国君凶。至于十年不克征"; type = "yin"}
        )
    }
)

# 添加新卦
$addedCount = 0
foreach ($hexagram in $newHexagrams) {
    if ($hexagram.id -notin $existingIds) {
        $data.hexagrams += $hexagram
        $addedCount++
        Write-Host "✓ 添加：$($hexagram.id) $($hexagram.name)" -ForegroundColor Green
    } else {
        Write-Host "⊘ 跳过（已存在）：$($hexagram.id) $($hexagram.name)" -ForegroundColor Yellow
    }
}

# 按 ID 排序
$data.hexagrams = $data.hexagrams | Sort-Object { $_.id }

# 保存
$data | ConvertTo-Json -Depth 10 | Set-Content $dataFile -Encoding UTF8

Write-Host "`n新增：$addedCount 卦" -ForegroundColor Cyan
Write-Host "总计：$($data.hexagrams.Count) 卦" -ForegroundColor Cyan
$percent = [math]::Round($data.hexagrams.Count / 64 * 100, 1)
Write-Host "完成度：$percent%" -ForegroundColor Cyan
