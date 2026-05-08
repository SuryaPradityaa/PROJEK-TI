"""Training data multilingual untuk model intent chatbot BaliGuide."""

TRAINING_DATA_MULTILINGUAL = [
    # ==========================================
    # GREETINGS / SALAM (MULTILINGUAL)
    # ==========================================

    # --- INDONESIAN ---
    ("halo", "salam"),
    ("hai", "salam"),
    ("selamat pagi", "salam"),
    ("selamat siang", "salam"),
    ("selamat sore", "salam"),
    ("selamat malam", "salam"),
    ("assalamualaikum", "salam"),
    ("permisi", "salam"),
    ("apa kabar", "salam"),
    ("gimana kabarnya", "salam"),
    ("halo bali guide", "salam"),
    ("hai bali guide", "salam"),
    ("selamat datang", "salam"),
    ("salam kenal", "salam"),
    ("perkenalkan nama saya", "salam"),
    ("saya turis pertama kali", "salam"),
    ("butuh info wisata", "salam"),
    ("ada yang bisa dibantu", "salam"),

    # --- ENGLISH ---
    ("hello", "salam"),
    ("hi", "salam"),
    ("hi there", "salam"),
    ("good morning", "salam"),
    ("good afternoon", "salam"),
    ("good evening", "salam"),
    ("good night", "salam"),
    ("how are you", "salam"),
    ("how do you do", "salam"),
    ("nice to meet you", "salam"),
    ("pleased to meet you", "salam"),
    ("i'm new here", "salam"),
    ("i'm a tourist", "salam"),
    ("can you help me", "salam"),
    ("i need information", "salam"),
    ("tourism information", "salam"),
    ("hello bali guide", "salam"),
    ("hi bali guide", "salam"),
    ("what's up", "salam"),
    ("hey", "salam"),
    ("hey there", "salam"),

    # --- JAPANESE (NIHONGO) ---
    ("こんにちは", "salam"),  # konnichiwa
    ("こんばんは", "salam"),  # konbanwa
    ("おはようございます", "salam"),  # ohayou gozaimasu
    ("はじめまして", "salam"),  # hajimemashite
    ("よろしくお願いします", "salam"),  # yoroshiku onegaishimasu
    ("すみません", "salam"),  # sumimasen
    ("こんにちは、バリガイド", "salam"),  # konnichiwa, bali guide
    ("観光情報を教えてください", "salam"),  # kankou jouhou o oshiete kudasai
    ("バリの観光スポットを教えて", "salam"),  # bali no kankou supotto o oshiete
    ("初めまして", "salam"),  # hajimemashite
    ("お元気ですか", "salam"),  # ogenki desu ka
    ("助けてください", "salam"),  # tasukete kudasai

    # --- MANDARIN CHINESE ---
    ("你好", "salam"),  # nǐ hǎo
    ("早上好", "salam"),  # zǎo shàng hǎo
    ("下午好", "salam"),  # xià wǔ hǎo
    ("晚上好", "salam"),  # wǎn shàng hǎo
    ("晚安", "salam"),  # wǎn ān
    ("很高兴认识你", "salam"),  # hěn gāo xìng rèn shí nǐ
    ("初次见面", "salam"),  # chū cì jiàn miàn
    ("我是第一次来巴厘岛", "salam"),  # wǒ shì dì yī cì lái bā lí dǎo
    ("请问有什么可以帮忙的", "salam"),  # qǐng wèn yǒu shén me kě yǐ bāng máng de
    ("我需要旅游信息", "salam"),  # wǒ xū yào lǚ yóu xìn xī
    ("巴厘岛旅游指南", "salam"),  # bā lí dǎo lǚ yóu zhǐ nán
    ("你好吗", "salam"),  # nǐ hǎo ma
    ("请帮助我", "salam"),  # qǐng bāng zhù wǒ

    # --- KOREAN ---
    ("안녕하세요", "salam"),  # annyeonghaseyo
    ("안녕", "salam"),  # annyeong
    ("좋은 아침이에요", "salam"),  # joeun achimieyo
    ("좋은 저녁이에요", "salam"),  # joeun jeonyeogieyo
    ("처음 뵙겠습니다", "salam"),  # cheoeum boepgesseumnida
    ("도와주세요", "salam"),  # dowajuseyo
    ("관광 정보가 필요해요", "salam"),  # gwangwang jeongboga pillyohae yo
    ("발리 관광지 추천해주세요", "salam"),  # balli gwangwangji chucheon haejuseyo
    ("안녕하세요, 발리 가이드", "salam"),  # annyeonghaseyo, balli gaideu
    ("처음이에요", "salam"),  # cheoeumieyo
    ("어떻게 지내세요", "salam"),  # eotteoke jinaeseyo

    # --- FRENCH ---
    ("bonjour", "salam"),
    ("bonsoir", "salam"),
    ("salut", "salam"),
    ("enchanté", "salam"),
    ("ravi de vous rencontrer", "salam"),
    ("je suis nouveau ici", "salam"),
    ("je suis touriste", "salam"),
    ("pouvez-vous m'aider", "salam"),
    ("j'ai besoin d'informations", "salam"),
    ("guide touristique de bali", "salam"),
    ("bonjour bali guide", "salam"),
    ("comment allez-vous", "salam"),
    ("s'il vous plaît aidez-moi", "salam"),

    # --- GERMAN ---
    ("hallo", "salam"),
    ("guten morgen", "salam"),
    ("guten tag", "salam"),
    ("guten abend", "salam"),
    ("gute nacht", "salam"),
    ("schön dich kennenzulernen", "salam"),
    ("ich bin neu hier", "salam"),
    ("ich bin tourist", "salam"),
    ("können sie mir helfen", "salam"),
    ("ich brauche informationen", "salam"),
    ("bali reise guide", "salam"),
    ("hallo bali guide", "salam"),
    ("wie geht es dir", "salam"),
    ("bitte helfen sie mir", "salam"),

    # --- SPANISH ---
    ("hola", "salam"),
    ("buenos días", "salam"),
    ("buenas tardes", "salam"),
    ("buenas noches", "salam"),
    ("encantado", "salam"),
    ("soy nuevo aquí", "salam"),
    ("soy turista", "salam"),
    ("¿puedes ayudarme?", "salam"),
    ("necesito información", "salam"),
    ("guía turística de bali", "salam"),
    ("hola bali guide", "salam"),
    ("¿cómo estás?", "salam"),
    ("por favor ayúdame", "salam"),

    # --- ARABIC ---
    ("مرحبا", "salam"),  # marhaban
    ("صباح الخير", "salam"),  # sabah al-khair
    ("مساء الخير", "salam"),  # masa al-khair
    ("أنا جديد هنا", "salam"),  # ana jadid huna
    ("أنا سائح", "salam"),  # ana sai'h
    ("هل يمكنك مساعدتي", "salam"),  # hal yumkinuka musa'adati
    ("أحتاج معلومات", "salam"),  # ahtaj ma'lumat
    ("دليل سياحي لبلي", "salam"),  # dalil sayahi li bali
    ("مرحبا بالي غايد", "salam"),  # marhaba bali guide
    ("كيف حالك", "salam"),  # kayfa haluk
    ("من فضلك ساعدني", "salam"),  # min fadlik sa'idni

    # --- RUSSIAN ---
    ("привет", "salam"),  # privet
    ("доброе утро", "salam"),  # dobroe utro
    ("добрый день", "salam"),  # dobryy den'
    ("добрый вечер", "salam"),  # dobryy vecher
    ("здравствуйте", "salam"),  # zdrastvuyte
    ("приятно познакомиться", "salam"),  # priyatno poznakomit'sya
    ("я новичок здесь", "salam"),  # ya novichok zdes'
    ("я турист", "salam"),  # ya turist
    ("можете ли вы мне помочь", "salam"),  # mozhete li vy mne pomoch'
    ("мне нужна информация", "salam"),  # mne nuzhna informatsiya
    ("путеводитель по бали", "salam"),  # putevoditel' po bali
    ("привет бали гайд", "salam"),  # privet bali guide
    ("как дела", "salam"),  # kak dela
    ("пожалуйста помогите мне", "salam"),  # pozhaluysta pomogite mne

    # ==========================================
    # BEACH / PANTAI (MULTILINGUAL)
    # ==========================================

    # --- INDONESIAN ---
    ("pantai", "pantai"),
    ("ke pantai", "pantai"),
    ("saya mau ke pantai", "pantai"),
    ("rekomendasi pantai", "pantai"),
    ("pantai bagus", "pantai"),
    ("pantai sepi", "pantai"),
    ("pantai untuk keluarga", "pantai"),
    ("pantai sunset", "pantai"),
    ("snorkeling", "pantai"),
    ("diving", "pantai"),
    ("surfing", "pantai"),
    ("berenang di laut", "pantai"),
    ("beach club", "pantai"),
    ("jetski", "pantai"),
    ("parasailing", "pantai"),
    ("kuta beach", "pantai"),
    ("nusa dua", "pantai"),
    ("sanur beach", "pantai"),
    ("uluwatu", "pantai"),
    ("jimbaran", "pantai"),
    ("seminyak", "pantai"),
    ("canggu", "pantai"),
    ("amed", "pantai"),
    ("bias tugel", "pantai"),
    ("virgin beach", "pantai"),
    ("blue lagoon", "pantai"),
    ("pantai bulan madu", "pantai"),

    # --- ENGLISH ---
    ("beach", "pantai"),
    ("to the beach", "pantai"),
    ("i want to go to the beach", "pantai"),
    ("beach recommendations", "pantai"),
    ("good beach", "pantai"),
    ("quiet beach", "pantai"),
    ("family beach", "pantai"),
    ("sunset beach", "pantai"),
    ("snorkeling", "pantai"),
    ("diving", "pantai"),
    ("surfing", "pantai"),
    ("swimming in the sea", "pantai"),
    ("beach club", "pantai"),
    ("jet ski", "pantai"),
    ("parasailing", "pantai"),
    ("kuta beach", "pantai"),
    ("nusa dua beach", "pantai"),
    ("sanur beach", "pantai"),
    ("uluwatu beach", "pantai"),
    ("jimbaran beach", "pantai"),
    ("seminyak beach", "pantai"),
    ("canggu beach", "pantai"),
    ("amed beach", "pantai"),
    ("virgin beach", "pantai"),
    ("blue lagoon", "pantai"),
    ("honeymoon beach", "pantai"),

    # --- JAPANESE ---
    ("ビーチ", "pantai"),  # bīchi
    ("ビーチに行く", "pantai"),  # bīchi ni iku
    ("ビーチをおすすめ", "pantai"),  # bīchi o osusume
    ("良いビーチ", "pantai"),  # yoi bīchi
    ("静かなビーチ", "pantai"),  # shizukana bīchi
    ("家族向けビーチ", "pantai"),  # kazoku mukai bīchi
    ("サンセットビーチ", "pantai"),  # sansetto bīchi
    ("シュノーケリング", "pantai"),  # shunōkeringu
    ("ダイビング", "pantai"),  # daibingu
    ("サーフィン", "pantai"),  # sāfin
    ("海で泳ぐ", "pantai"),  # umi de oyogu
    ("ビーチクラブ", "pantai"),  # bīchi kurabu
    ("ジェットスキー", "pantai"),  # jetto sukī
    ("パラセーリング", "pantai"),  # para sēringu
    ("クタビーチ", "pantai"),  # kuta bīchi
    ("ヌサドゥア", "pantai"),  # nusa du a
    ("サヌール", "pantai"),  # sanūru
    ("ウルワツ", "pantai"),  # uruwatsu
    ("ジンバラン", "pantai"),  # jinbaran
    ("スミニャック", "pantai"),  # suminyakku
    ("チャング", "pantai"),  # changu
    ("アメッド", "pantai"),  # ameddo
    ("ヴァージンビーチ", "pantai"),  # vājin bīchi
    ("ブルーラグーン", "pantai"),  # burū ragūn
    ("ハネムーンビーチ", "pantai"),  # hanemūn bīchi

    # --- MANDARIN ---
    ("海滩", "pantai"),  # hǎi tān
    ("去海滩", "pantai"),  # qù hǎi tān
    ("我想去海滩", "pantai"),  # wǒ xiǎng qù hǎi tān
    ("海滩推荐", "pantai"),  # hǎi tān tuī jiàn
    ("好海滩", "pantai"),  # hǎo hǎi tān
    ("安静海滩", "pantai"),  # ān jìng hǎi tān
    ("家庭海滩", "pantai"),  # jiā tíng hǎi tān
    ("日落海滩", "pantai"),  # rì luò hǎi tān
    ("浮潜", "pantai"),  # fú qián
    ("潜水", "pantai"),  # qián shuǐ
    ("冲浪", "pantai"),  # chōng làng
    ("在海里游泳", "pantai"),  # zài hǎi lǐ yóu yǒng
    ("海滩俱乐部", "pantai"),  # hǎi tān jù lè bù
    ("喷气式滑雪", "pantai"),  # pēn qì shì huá xuě
    ("滑翔伞", "pantai"),  # huá xiáng sǎn
    ("库塔海滩", "pantai"),  # kù tǎ hǎi tān
    ("努沙杜瓦", "pantai"),  # nǔ shā dù wǎ
    ("萨努尔", "pantai"),  # sà nǔ ěr
    ("乌鲁瓦图", "pantai"),  # wū lǔ wǎ tú
    ("金巴兰", "pantai"),  # jīn bā lán
    ("塞米尼亚克", "pantai"),  # sài mǐ ní yà kè
    ("昌古", "pantai"),  # chāng gǔ
    ("阿梅德", "pantai"),  # ā méi dé
    ("处女海滩", "pantai"),  # chǔ nǚ hǎi tān
    ("蓝色泻湖", "pantai"),  # lán sè xiè hú
    ("蜜月海滩", "pantai"),  # mì yuè hǎi tān

    # --- KOREAN ---
    ("해변", "pantai"),  # haebyeon
    ("해변에 가다", "pantai"),  # haebyeon-e gada
    ("해변에 가고 싶어요", "pantai"),  # haebyeon-e gago sipeoyo
    ("해변 추천", "pantai"),  # haebyeon chucheon
    ("좋은 해변", "pantai"),  # joeun haebyeon
    ("조용한 해변", "pantai"),  # joyonghan haebyeon
    ("가족 해변", "pantai"),  # gajok haebyeon
    ("일몰 해변", "pantai"),  # ilmol haebyeon
    ("스노클링", "pantai"),  # seunokeulling
    ("다이빙", "pantai"),  # daibing
    ("서핑", "pantai"),  # seoping
    ("바다에서 수영", "pantai"),  # badaeseo suyeong
    ("비치 클럽", "pantai"),  # bichi keulleop
    ("제트 스키", "pantai"),  # jeteu seuki
    ("패러세일링", "pantai"),  # paereoseilling
    ("쿠타 해변", "pantai"),  # kuta haebyeon
    ("누사 두아", "pantai"),  # nusa du a
    ("사누르", "pantai"),  # sanuru
    ("울루와투", "pantai"),  # ulluwatu
    ("짐바란", "pantai"),  # jimbalan
    ("세미냑", "pantai"),  # seminyak
    ("창구", "pantai"),  # changgu
    ("아메드", "pantai"),  # amedeu
    ("버진 비치", "pantai"),  # beojin bichi
    ("블루 라군", "pantai"),  # beullu lagun
    ("허니문 비치", "pantai"),  # heonimun bichi

    # ==========================================
    # NATURE / ALAM (MULTILINGUAL)
    # ==========================================

    # --- INDONESIAN ---
    ("alam", "alam"),
    ("wisata alam", "alam"),
    ("gunung", "alam"),
    ("air terjun", "alam"),
    ("trekking", "alam"),
    ("hiking", "alam"),
    ("hutan", "alam"),
    ("sawah", "alam"),
    ("danau", "alam"),
    ("gunung batur", "alam"),
    ("gunung agung", "alam"),
    ("gunung rinjani", "alam"),
    ("air terjun gitgit", "alam"),
    ("air terjun aling aling", "alam"),
    ("air terjun sekumpul", "alam"),
    ("taman nasional", "alam"),
    ("petualangan alam", "alam"),
    ("camping", "alam"),
    ("river tubing", "alam"),
    ("sunrise", "alam"),
    ("sunset", "alam"),

    # --- ENGLISH ---
    ("nature", "alam"),
    ("nature tourism", "alam"),
    ("mountain", "alam"),
    ("waterfall", "alam"),
    ("trekking", "alam"),
    ("hiking", "alam"),
    ("forest", "alam"),
    ("rice field", "alam"),
    ("lake", "alam"),
    ("mount batur", "alam"),
    ("mount agung", "alam"),
    ("mount rinjani", "alam"),
    ("gitgit waterfall", "alam"),
    ("aling aling waterfall", "alam"),
    ("sekumpul waterfall", "alam"),
    ("national park", "alam"),
    ("nature adventure", "alam"),
    ("camping", "alam"),
    ("river tubing", "alam"),
    ("sunrise", "alam"),
    ("sunset", "alam"),

    # --- JAPANESE ---
    ("自然", "alam"),  # shizen
    ("自然観光", "alam"),  # shizen kankou
    ("山", "alam"),  # yama
    ("滝", "alam"),  # taki
    ("トレッキング", "alam"),  # torekkingu
    ("ハイキング", "alam"),  # haikingu
    ("森", "alam"),  # mori
    ("田んぼ", "alam"),  # tanbo
    ("湖", "alam"),  # mizuumi
    ("バトゥール山", "alam"),  # batouru san
    ("アグン山", "alam"),  # agun san
    ("リンジャニ山", "alam"),  # rinjani san
    ("ギットギット滝", "alam"),  # gittogitto taki
    ("アリングアリング滝", "alam"),  # aringgaring taki
    ("セクンプル滝", "alam"),  # sekunpuru taki
    ("国立公園", "alam"),  # kokuritsu kouen
    ("自然探検", "alam"),  # shizen tanken
    ("キャンプ", "alam"),  # kyampu
    ("リバーチュービング", "alam"),  # riba chubingu
    ("日の出", "alam"),  # hinode
    ("日の入り", "alam"),  # hi no iri

    # --- MANDARIN ---
    ("自然", "alam"),  # zì rán
    ("自然旅游", "alam"),  # zì rán lǚ yóu
    ("山", "alam"),  # shān
    ("瀑布", "alam"),  # bào bù
    ("徒步旅行", "alam"),  # tú bù lǚ xíng
    ("远足", "alam"),  # yuǎn zú
    ("森林", "alam"),  # sēn lín
    ("稻田", "alam"),  # dào tián
    ("湖泊", "alam"),  # hú pō
    ("巴杜尔山", "alam"),  # bā dù ěr shān
    ("阿贡山", "alam"),  # ā gòng shān
    ("林贾尼山", "alam"),  # lín jiǎ ní shān
    ("吉吉特瀑布", "alam"),  # jí jí tè bào bù
    ("阿陵阿陵瀑布", "alam"),  # ā líng ā líng bào bù
    ("塞孔普尔瀑布", "alam"),  # sài kǒng pǔ ěr bào bù
    ("国家公园", "alam"),  # guó jiā gōng yuán
    ("自然冒险", "alam"),  # zì rán mào xiǎn
    ("露营", "alam"),  # lù yíng
    ("河上漂流", "alam"),  # hé shàng piāo liú
    ("日出", "alam"),  # rì chū
    ("日落", "alam"),  # rì luò

    # ==========================================
    # CULTURE / BUDAYA (MULTILINGUAL)
    # ==========================================

    # --- INDONESIAN ---
    ("budaya", "budaya"),
    ("wisata budaya", "budaya"),
    ("pura", "budaya"),
    ("temple", "budaya"),
    ("sejarah", "budaya"),
    ("museum", "budaya"),
    ("tari", "budaya"),
    ("adat", "budaya"),
    ("tradisi", "budaya"),
    ("upacara", "budaya"),
    ("kecak", "budaya"),
    ("legong", "budaya"),
    ("wayang kulit", "budaya"),
    ("seni", "budaya"),
    ("heritage", "budaya"),
    ("religi", "budaya"),

    # --- ENGLISH ---
    ("culture", "budaya"),
    ("cultural tourism", "budaya"),
    ("temple", "budaya"),
    ("historical", "budaya"),
    ("museum", "budaya"),
    ("dance", "budaya"),
    ("tradition", "budaya"),
    ("ceremony", "budaya"),
    ("kecak dance", "budaya"),
    ("legong dance", "budaya"),
    ("shadow puppet", "budaya"),
    ("art", "budaya"),
    ("heritage", "budaya"),
    ("religious", "budaya"),

    # --- JAPANESE ---
    ("文化", "budaya"),  # bunka
    ("文化観光", "budaya"),  # bunka kankou
    ("寺院", "budaya"),  # jiin
    ("歴史", "budaya"),  # rekishi
    ("博物館", "budaya"),  # hakubutsukan
    ("踊り", "budaya"),  # odori
    ("伝統", "budaya"),  # dentou
    ("儀式", "budaya"),  # gishiki
    ("ケチャダンス", "budaya"),  # kecha dansu
    ("レゴンダンス", "budaya"),  # regon dansu
    ("影絵芝居", "budaya"),  # kagee shibai
    ("芸術", "budaya"),  # geijutsu
    ("遺産", "budaya"),  # isan
    ("宗教", "budaya"),  # shukyou

    # --- MANDARIN ---
    ("文化", "budaya"),  # wén huà
    ("文化旅游", "budaya"),  # wén huà lǚ yóu
    ("寺庙", "budaya"),  # sì miào
    ("历史", "budaya"),  # lì shǐ
    ("博物馆", "budaya"),  # bó wù guǎn
    ("舞蹈", "budaya"),  # wǔ dǎo
    ("传统", "budaya"),  # chuán tǒng
    ("仪式", "budaya"),  # yí shì
    ("凯查舞", "budaya"),  # kǎi chá wǔ
    ("莱贡舞", "budaya"),  # lái gòng wǔ
    ("皮影戏", "budaya"),  # pí yǐng xì
    ("艺术", "budaya"),  # yì shù
    ("遗产", "budaya"),  # yí chǎn
    ("宗教", "budaya"),  # zōng jiào

    # ==========================================
    # FOOD / KULINER (MULTILINGUAL)
    # ==========================================

    # --- INDONESIAN ---
    ("kuliner", "kuliner"),
    ("makan", "kuliner"),
    ("restoran", "kuliner"),
    ("makanan khas", "kuliner"),
    ("seafood", "kuliner"),
    ("warung", "kuliner"),
    ("cafe", "kuliner"),
    ("babi guling", "kuliner"),
    ("ayam betutu", "kuliner"),
    ("nasi campur", "kuliner"),
    ("lawar", "kuliner"),
    ("sate lilit", "kuliner"),
    ("bebek betutu", "kuliner"),
    ("pisang goreng", "kuliner"),
    ("kopi luwak", "kuliner"),
    ("jimbaran seafood", "kuliner"),

    # --- ENGLISH ---
    ("food", "kuliner"),
    ("cuisine", "kuliner"),
    ("restaurant", "kuliner"),
    ("local food", "kuliner"),
    ("seafood", "kuliner"),
    ("warung", "kuliner"),
    ("cafe", "kuliner"),
    ("babi guling", "kuliner"),
    ("ayam betutu", "kuliner"),
    ("nasi campur", "kuliner"),
    ("lawar", "kuliner"),
    ("sate lilit", "kuliner"),
    ("bebek betutu", "kuliner"),
    ("fried banana", "kuliner"),
    ("kopi luwak", "kuliner"),
    ("jimbaran seafood", "kuliner"),

    # --- JAPANESE ---
    ("グルメ", "kuliner"),  # gurume
    ("料理", "kuliner"),  # ryouri
    ("レストラン", "kuliner"),  # resutoran
    ("郷土料理", "kuliner"),  # kyoudoryouri
    ("シーフード", "kuliner"),  # shifudo
    ("ワルン", "kuliner"),  # warun
    ("カフェ", "kuliner"),  # kafe
    ("バビグリング", "kuliner"),  # babi guringu
    ("アヤムベトゥトゥ", "kuliner"),  # ayamu betutu
    ("ナシカンプル", "kuliner"),  # nashi kampuru
    ("ラワール", "kuliner"),  # rawaru
    ("サテリリット", "kuliner"),  # sate riritt
    ("ベベックベトゥトゥ", "kuliner"),  # bebe kku betutu
    ("揚げバナナ", "kuliner"),  # age banana
    ("コピルワク", "kuliner"),  # kopi ruwaku
    ("ジンバランシーフード", "kuliner"),  # jinbaran shifudo

    # --- MANDARIN ---
    ("美食", "kuliner"),  # měi shí
    ("美食", "kuliner"),  # měi shí
    ("餐厅", "kuliner"),  # cān tīng
    ("当地美食", "kuliner"),  # dāng dì měi shí
    ("海鲜", "kuliner"),  # hǎi xiān
    ("瓦隆", "kuliner"),  # wǎ lóng
    ("咖啡馆", "kuliner"),  # kā fēi guǎn
    ("烤乳猪", "kuliner"),  # kǎo rǔ zhū
    ("巴厘鸡", "kuliner"),  # bā lí jī
    ("印尼炒饭", "kuliner"),  # yìn ní chǎo fàn
    ("沙拉", "kuliner"),  # shā lā
    ("串烧肉", "kuliner"),  # chuàn shāo ròu
    ("巴厘鸭", "kuliner"),  # bā lí yā
    ("炸香蕉", "kuliner"),  # zhà xiāng jiāo
    ("麝香猫咖啡", "kuliner"),  # shè xiāng māo kā fēi
    ("金巴兰海鲜", "kuliner"),  # jīn bā lán hǎi xiān

    # ==========================================
    # ENTERTAINMENT / HIBURAN (MULTILINGUAL)
    # ==========================================

    # --- INDONESIAN ---
    ("hiburan", "hiburan"),
    ("taman hiburan", "hiburan"),
    ("waterpark", "hiburan"),
    ("wahana", "hiburan"),
    ("atraksi", "hiburan"),
    ("fun park", "hiburan"),
    ("water bomb", "hiburan"),
    ("flying fox", "hiburan"),
    ("banana boat", "hiburan"),
    ("paintball", "hiburan"),
    ("go kart", "hiburan"),
    ("mini golf", "hiburan"),
    ("bowling", "hiburan"),

    # --- ENGLISH ---
    ("entertainment", "hiburan"),
    ("amusement park", "hiburan"),
    ("water park", "hiburan"),
    ("rides", "hiburan"),
    ("attractions", "hiburan"),
    ("fun park", "hiburan"),
    ("water bomb", "hiburan"),
    ("flying fox", "hiburan"),
    ("banana boat", "hiburan"),
    ("paintball", "hiburan"),
    ("go kart", "hiburan"),
    ("mini golf", "hiburan"),
    ("bowling", "hiburan"),

    # --- JAPANESE ---
    ("エンターテイメント", "hiburan"),  # entateimento
    ("遊園地", "hiburan"),  # yuuenchi
    ("ウォーターパーク", "hiburan"),  # woota paaku
    ("乗り物", "hiburan"),  # norimono
    ("アトラクション", "hiburan"),  # aturakushon
    ("ファンパーク", "hiburan"),  # fan paaku
    ("ウォーターボム", "hiburan"),  # wootaa bomu
    ("フライングフォックス", "hiburan"),  # furaingu fokkusu
    ("バナナボート", "hiburan"),  # banana boot
    ("ペイントボール", "hiburan"),  # peinto booru
    ("ゴーカート", "hiburan"),  # goo kaato
    ("ミニゴルフ", "hiburan"),  # mini gorufu
    ("ボウリング", "hiburan"),  # bouringu

    # ==========================================
    # RECOMMENDATIONS / REKOMENDASI (MULTILINGUAL)
    # ==========================================

    # --- INDONESIAN ---
    ("rekomendasi", "rekomendasi"),
    ("saran", "rekomendasi"),
    ("tempat terbaik", "rekomendasi"),
    ("wisata populer", "rekomendasi"),
    ("destinasi terkenal", "rekomendasi"),
    ("spot instagramable", "rekomendasi"),
    ("tempat foto bagus", "rekomendasi"),
    ("wisata viral", "rekomendasi"),
    ("trending spots", "rekomendasi"),

    # --- ENGLISH ---
    ("recommend", "rekomendasi"),
    ("suggest", "rekomendasi"),
    ("best places", "rekomendasi"),
    ("popular tourism", "rekomendasi"),
    ("famous destinations", "rekomendasi"),
    ("instagram worthy", "rekomendasi"),
    ("good photo spots", "rekomendasi"),
    ("viral attractions", "rekomendasi"),
    ("trending places", "rekomendasi"),

    # --- JAPANESE ---
    ("おすすめ", "rekomendasi"),  # osusume
    ("提案", "rekomendasi"),  # teian
    ("最高の場所", "rekomendasi"),  # saikou no basho
    ("人気観光地", "rekomendasi"),  # ninki kankouchi
    ("有名な目的地", "rekomendasi"),  # yuumeina mokutekichi
    ("インスタ映えスポット", "rekomendasi"),  # insuta bae supotto
    ("良い写真場所", "rekomendasi"),  # yoi shashin basho
    ("バイラルアトラクション", "rekomendasi"),  # bairaru aturakushon
    ("トレンドスポット", "rekomendasi"),  # torendo supotto

    # --- MANDARIN ---
    ("推荐", "rekomendasi"),  # tuī jiàn
    ("建议", "rekomendasi"),  # jiàn yì
    ("最佳地点", "rekomendasi"),  # zuì jiā dì diǎn
    ("热门旅游地", "rekomendasi"),  # rè mén lǚ yóu dì
    ("著名目的地", "rekomendasi"),  # zhù míng mù dì dì
    ("适合拍照的景点", "rekomendasi"),  # shì hé pāi zhào de jǐng diǎn
    ("好的摄影地点", "rekomendasi"),  # hǎo de shè yǐng dì diǎn
    ("热门景点", "rekomendasi"),  # rè mén jǐng diǎn
    ("潮流景点", "rekomendasi"),  # cháo liú jǐng diǎn

    # ==========================================
    # BUDGET / MURAH & MAHAL (MULTILINGUAL)
    # ==========================================

    # --- INDONESIAN ---
    ("murah", "murah"),
    ("budget", "murah"),
    ("gratis", "murah"),
    ("hemat", "murah"),
    ("terjangkau", "murah"),
    ("low budget", "murah"),
    ("free entrance", "murah"),

    ("mahal", "mahal"),
    ("premium", "mahal"),
    ("mewah", "mahal"),
    ("luxury", "mahal"),
    ("eksklusif", "mahal"),
    ("high end", "mahal"),
    ("vip", "mahal"),

    # --- ENGLISH ---
    ("cheap", "murah"),
    ("budget", "murah"),
    ("free", "murah"),
    ("affordable", "murah"),
    ("low budget", "murah"),
    ("free entrance", "murah"),

    ("expensive", "mahal"),
    ("premium", "mahal"),
    ("luxury", "mahal"),
    ("exclusive", "mahal"),
    ("high end", "mahal"),
    ("vip", "mahal"),

    # ==========================================
    # LOCATIONS / LOKASI (MULTILINGUAL)
    # ==========================================

    # --- INDONESIAN ---
    ("ubud", "lokasi"),
    ("kuta", "lokasi"),
    ("seminyak", "lokasi"),
    ("nusa dua", "lokasi"),
    ("sanur", "lokasi"),
    ("uluwatu", "lokasi"),
    ("jimbaran", "lokasi"),
    ("canggu", "lokasi"),
    ("gianyar", "lokasi"),
    ("denpasar", "lokasi"),
    ("karangasem", "lokasi"),
    ("buleleng", "lokasi"),
    ("tabanan", "lokasi"),
    ("bangli", "lokasi"),
    ("klungkung", "lokasi"),
    ("jembrana", "lokasi"),

    # --- ENGLISH ---
    ("ubud tourism", "lokasi"),
    ("kuta tourism", "lokasi"),
    ("seminyak tourism", "lokasi"),
    ("nusa dua tourism", "lokasi"),
    ("sanur tourism", "lokasi"),
    ("uluwatu tourism", "lokasi"),
    ("jimbaran tourism", "lokasi"),
    ("canggu tourism", "lokasi"),
    ("gianyar tourism", "lokasi"),
    ("denpasar tourism", "lokasi"),
    ("karangasem tourism", "lokasi"),
    ("buleleng tourism", "lokasi"),
    ("tabanan tourism", "lokasi"),
    ("bangli tourism", "lokasi"),
    ("klungkung tourism", "lokasi"),
    ("jembrana tourism", "lokasi"),

    # ==========================================
    # HELP / BANTUAN (MULTILINGUAL)
    # ==========================================

    # --- INDONESIAN ---
    ("tolong", "bantuan"),
    ("bantu", "bantuan"),
    ("bingung", "bantuan"),
    ("tidak tahu", "bantuan"),
    ("butuh bantuan", "bantuan"),
    ("rekomendasikan", "bantuan"),

    # --- ENGLISH ---
    ("help", "bantuan"),
    ("please help", "bantuan"),
    ("i'm confused", "bantuan"),
    ("i don't know", "bantuan"),
    ("i need help", "bantuan"),
    ("recommend for me", "bantuan"),

    # ==========================================
    # GENERAL QUESTIONS / PERTANYAAN UMUM (MULTILINGUAL)
    # ==========================================

    # --- INDONESIAN ---
    ("apa saja wisata di bali", "pertanyaan_umum"),
    ("bali punya apa aja", "pertanyaan_umum"),
    ("destinasi wisata bali", "pertanyaan_umum"),
    ("tempat menarik di bali", "pertanyaan_umum"),
    ("atraksi wisata bali", "pertanyaan_umum"),

    # --- ENGLISH ---
    ("what tourist attractions in bali", "pertanyaan_umum"),
    ("what does bali have", "pertanyaan_umum"),
    ("bali tourist destinations", "pertanyaan_umum"),
    ("interesting places in bali", "pertanyaan_umum"),
    ("bali tourist attractions", "pertanyaan_umum"),

]