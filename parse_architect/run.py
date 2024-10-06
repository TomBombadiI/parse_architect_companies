import requests, re, sys, csv, openpyxl, time, os, math
from bs4 import BeautifulSoup as bs

requests.packages.urllib3.disable_warnings()

workbook = openpyxl.load_workbook('results.xlsx')
worksheet = workbook.active

headers = ['Город', 'Название', 'Описание', 'Телефон', 'Сайт', 'Режим работы', 'Адрес']
# worksheet.append(headers)

cities = ['msk', '', 'abaza', 'abakan', 'abdulino', 'abinsk', 'agidel', 'aginskoe', 'agryz', 'adygeysk', 'aznakaevo', 'azov', 'ak-dovurak', 'aksay', 'alagir', 'alapaevsk', 'alatyr', 'aldan', 'aleysk', 'aleksandrov', 'aleksandrovsk', 'alekseevka', 'aleksin', 'alzamay', 'alupka', 'alushta', 'almetevsk', 'amursk', 'anadyr', 'anapa', 'angarsk', 'anzhero-sudzhensk', 'aniva', 'apatity', 'apsheronsk', 'aramil', 'argun', 'ardatov', 'ardon', 'arzamas', 'arkadak', 'armavir', 'armyansk', 'arsenev', 'arsk', 'artem', 'artemovsk', 'artemovskiy', 'arhangelsk', 'asbest', 'asino', 'astrahan', 'atkarsk', 'ahtubinsk', 'achinsk', 'asha', 'babaevo', 'babushkin', 
'bavly', 'bagrationovsk', 'baykalsk', 'baymak', 'bakal', 'baksan', 'balabanovo', 'balakovo', 'balahna', 'balashov', 'baltiysk', 'barabinsk', 'barnaul', 'barysh', 'bataysk', 'bahchisaray', 'belaya-kalitva', 'belaya-holunitsa', 'belgorod', 'belebey', 'belev', 'belinskiy', 'belovo', 'belogorsk', 'belozersk', 'belokuriha', 'belomorsk', 'beloretsk', 'belorechensk', 'beloyarskiy', 'berdsk', 'berezniki', 'berezovskiy', 'berezovskiy-kemerovo', 'beslan', 'biysk', 'bikin', 'bilibino', 'birobidzan', 'birsk', 'biryusinsk', 'blagoveschensk', 'blagoveschensk-bashkortostan', 'blagodarnyi', 'bobrov', 'bogdanovich', 'bogoroditsk', 'bogorodsk', 'bogotol', 'boguchar', 'bodaybo', 'bolgar', 'bologoe', 'bolotnoe', 'bolhov', 'bolshoy-kamen', 'bor', 'borzya', 'borisoglebsk', 'borovichi', 'borovsk', 'borodino', 'bratsk', 'bryansk', 'bugulma', 'buguruslan', 'budennovsk', 'buzuluk', 'buinsk', 'buynaksk', 'buturlinovka', 'valday', 'valuyki', 'velizh', 'velikie-luki', 'vnovgorod', 'velikiy-ustyug', 'velsk', 'venev', 'vereschagino', 'verhneuralsk', 'verhniy-tagil', 'verhniy-ufaley', 'verhnyaya-pyshma', 'verhnyaya-salda', 'verhnyaya-tura', 
'verhoture', 'vesegonsk', 'vetluga', 'vilyuysk', 'vilyuchinsk', 'vihorevka', 'vichuga', 'vladivostok', 'vladikavkaz', 'vladimir', 'volgograd', 'volgodonsk', 'volgorechensk', 'volzhsk', 'volzhskiy', 'vologda', 'volodarsk', 'volchansk', 'volsk', 'vorkuta', 'voronezh', 'vorsma', 'votkinsk', 'vuktyl', 'vyksa', 'vytegra', 'vyshniy-volochek', 'vyazemskiy', 'vyazniki', 'vyazma', 'vyatskie-polyany', 'gavrilov-posad', 'gavrilov-yam', 'gagarin', 'gadzhievo', 'gay', 'galich', 'gvardeysk', 
'gdov', 'gelendzhik', 'georgievsk', 'glazov', 'gorbatov', 'gorno-altaysk', 'gornozavodsk', 'gornyak', 'gorodets', 'gorodische', 'gorodovikovsk', 'gorohovets', 'goryachiy-klyuch', 'grayvoron', 'gremyachinsk', 'groznyi', 'gryazi', 'gryazovets', 'gubaha', 'gubkin', 'gubkinskiy', 'gudermes', 'gukovo', 'gulkevichi', 'gurevsk', 'gurevsk-kaliningrad', 'gusev', 'gusinoozersk', 'gus-hrustalnyi', 'davlekanovo', 'dagestanskie-ogni', 'dalnegorsk', 'dalnerechensk', 'danilov', 'dankov', 'degtyarsk', 'demidov', 'derbent', 'desnogorsk', 'dzhankoy', 'dzerzhinsk', 'divnogorsk', 'digora', 'dimitrovgrad', 'dmitriev-lgovskiy', 'dno', 'dobryanka', 'dolinsk', 'donetsk', 'donskoy', 'dorogobuzh', 'dubovka', 'dudinka', 'duhovschina', 'dyurtyuli', 'dyatkovo', 'evpatoriya', 'eysk', 'ekaterinburg', 'elabuga', 'elets', 'elizovo', 'elnya', 'emanzhelinsk', 'eniseysk', 'ershov', 'essentuki', 'efremov', 'zheleznovodsk', 'zheleznogorsk', 'zheleznogorsk-krasnoyarsk', 'zheleznogorsk-ilimskiy', 'zherdevka', 'zhigulevsk', 'zhizdra', 'zhirnovsk', 'zhukov', 'zhukovka', 'zavitinsk', 'zavodoukovsk', 'zavolzhsk', 'zavolzhe', 'zadonsk', 'zainsk', 'zakamensk', 'zaozernyi', 'zaozersk', 'zapadnaya-dvina', 'zapolyarnyi', 'zarechnyi-sverdlovsk', 'zarechnyi', 'zarinsk', 'zvenigovo', 'zverevo', 'zelenogorsk-krasnoyarsk', 'zelenogradsk', 'zelenodolsk', 'zelenokumsk', 'zernograd', 'zeya', 'zima', 'zlatoust', 'zlynka', 'zmeinogorsk', 'znamensk', 'ivanovo', 'ivdel', 'igarka', 'izhevsk', 'izberbash', 'izobilnyi', 'ilanskiy', 'inza', 'inkerman', 'inta', 'ipatovo', 'irbit', 'irkutsk', 'isilkul', 'iskitim', 'ishim', 'ishimbay', 'yoshkar-ola', 'kadnikov', 'kazan', 'kayerkan', 'kalach-na-donu', 'kalachinsk', 'kaliningrad', 'kalininsk', 'kaltan', 'kaluga', 'kamenka', 'kamensk-uralskiy', 'kamensk-shahtinskiy', 'kamen-na-obi', 'kameshkovo', 'kamyzyak', 'kamyshin', 'kamyshlov', 'kanash', 'kandalaksha', 'kansk', 'karabanovo', 'karabash', 'karabulak', 'karasuk', 'karachaevsk', 'karachev', 'kargat', 'kargopol', 'karpinsk', 'kartaly', 'kasimov', 'kasli', 'kaspiysk', 'katav-ivanovsk', 'kachkanar', 'kemerovo', 'kem', 'kerch', 'kizel', 'kizilyurt', 'kizlyar', 'kimovsk', 'kimry', 'kinel', 'kineshma', 'kireevsk', 'kirensk', 'kirzhach', 'kirillov', 'kirov', 'kirov-kaluga', 'kirovgrad', 'kirovo-chepetsk', 'kirovsk', 'kirs', 'kiselevsk', 'kislovodsk', 'klintsy', 'knyaginino', 'kovdor', 'kovrov', 'kovylkino', 'kogalym', 'kodinsk', 'kozelsk', 'kozlovka', 'kozmodemyansk', 'kola', 'kolpashevo', 'kolchugino', 'komsomolsk', 'komsomolsk-na-amure', 'konakovo', 'kondopoga', 'kondrovo', 'konstantinovsk', 'kopeysk', 'korablino', 'korenovsk', 'korkino', 'korocha', 'korsakov', 'koryazhma', 'kosterevo', 'kostomuksha', 'kostroma', 'kotelnikovo', 'kotelnich', 'kotlas', 'kotovo', 'kotovsk', 'kohma', 'krasavino', 'krasnoarmeisk-saratov', 'krasnovishersk', 'krasnodar', 'krasnoznamensk-kaliningrad', 'krasnokamsk', 'krasnoperekopsk', 'krasnoslobodsk', 'krasnoslobodsk-mordoviya', 'krasnoturinsk', 'krasnouralsk', 'krasnoufimsk', 'krasnoyarsk', 'krasnyi-kut', 'krasnyi-sulin', 'krasnyi-holm', 'kremenki', 
'kropotkin', 'krymsk', 'kstovo', 'kuvandyk', 'kuvshinovo', 'kudymkar', 'kuznetsk', 'kuybyshev', 'kulebaki', 'kumertau', 'kungur', 'kupino', 'kurgan', 'kurganinsk', 'kurlovo', 'kursk', 'kurchatov', 'kusa', 'kushva', 'kyzyl', 'kyshtym', 'kyahta', 'labinsk', 'labytnangi', 'lagan', 'ladushkin', 'lakinsk', 'langepas', 'lahdenpohya', 'lebedyan', 'leninogorsk', 'leninsk', 'leninsk-kuznetskiy', 'lensk', 'lermontov', 'lesnoy', 'lesozavodsk', 'lesosibirsk', 'livny', 'lipetsk', 'liski', 'lihoslavl', 'luza', 'lukoyanov', 'lyskovo', 'lysva', 'lgov', 'lyubim', 'lyudinovo', 'lyantor', 'magadan', 'magas', 'magnitogorsk', 'maykop', 'mayskiy', 'makarev', 'malaya-vishera', 'malgobek', 'maloarhangelsk', 'maloyaroslavets', 'mamadysh', 'mamonovo', 'manturovo', 'mariinsk', 'mariinskiy-posad', 'marks', 'mahachkala', 'mglin', 'megion', 'medvezhegorsk', 'mednogorsk', 'medyn', 'mezhdurechensk', 'mezen', 'melenki', 'meleuz', 'mendeleevsk', 'menzelinsk', 'miass', 'mikun', 'millerovo', 'mineralnye-vody', 'minusinsk', 'minyar', 'mirnyi', 'mirnyi-yakutsk', 'mihaylovka', 'mihailovsk-sverdlovsk', 'mihailovsk', 'michurinsk', 'mozhga', 'mozdok', 'monchegorsk', 'morozovsk', 'morshansk', 'mosalsk', 'muravlenko', 'murmansk', 'murom', 'mtsensk', 'myski', 'myshkin', 'naberezhnye-chelny', 'navashino', 'navoloki', 'nadym', 'nazarovo', 'nazran', 'nazyvaevsk', 'nalchik', 'narimanov', 'nartkala', 'naryan-mar', 'nahodka', 'nevel', 'nevinnomyssk', 'nevyansk', 'neman', 'nerehta', 'nerchinsk', 'neryungri', 'nesterov', 'neftegorsk', 'neftekamsk', 'neftekumsk', 'nefteyugansk', 'nizhnevartovsk', 'nizhnekamsk', 'nizhneudinsk', 'nizhnie-sergi', 'nizhniy-lomov', 'nnovgorod', 'nizhniy-tagil', 'nizhnyaya-salda', 'nizhnyaya-tura', 'nikolaevsk', 'nikolaevsk-na-amure', 'nikolsk-vologda', 'nikolsk', 'novaya-lyalya', 'novoaleksandrovsk', 'novoaltaysk', 'novoanninskiy', 'novovoronezh', 'novodvinsk', 'novozybkov', 'novokubansk', 'novokuznetsk', 'novokuybyshevsk', 'novomoskovsk', 'novopavlovsk', 'novorzhev', 'novorossiysk', 'novosibirsk', 'novosokolniki', 'novotroitsk', 'novouzensk', 'novoulyanovsk', 'novouralsk', 'novocheboksarsk', 'novocherkassk', 'novoshahtinsk', 'novyi-oskol', 'novyi-urengoi', 'nolinsk', 'norilsk', 'noyabrsk', 'nurlat', 'nytva', 'nyurba', 'nyagan', 'nyazepetrovsk', 'nyandoma', 'obluche', 'obninsk', 'oboyan', 'ob', 'ozersk-kaliningrad', 'ozersk', 'oktyabrsk', 'oktyabrskiy-perm', 'oktyabrskiy', 'okulovka', 'olekminsk', 'olenegorsk', 'olonets', 'omsk', 'omutninsk', 'onega', 'opochka', 'orel', 'orenburg', 'orsk', 'osa', 'osinniki', 'ostashkov', 'ostrov', 'ostrovnoy', 'otradnyi', 'ohansk', 'ohotsk', 'ocher', 'pavlovo', 'pavlovsk-voronezh', 'pallasovka', 'partizansk', 'pevek', 'penza', 'pervomaysk', 'pervouralsk', 'perevoz', 'pereslavl-zalesskiy', 'perm', 'pestovo', 'petrovsk', 'petrozavodsk', 'petropavlovsk-kamchatskiy', 'petushki', 'pechora', 'pechory', 'pionerskiy', 'pitkyaranta', 'plavsk', 'plast', 'pokrov', 'pokrovsk', 'polevskoy', 'polessk', 'polysaevo', 'polyarnye-zori', 'polyarnyi', 'porhov', 'pohvistnevo', 'pochep', 'pochinok', 'poshehone', 'pravdinsk', 'privolzhsk', 'primorsk-kaliningrad', 'primorsko-ahtarsk', 'prokopevsk', 'proletarsk', 'prohladnyi', 'pskov', 'pugachev', 'pudozh', 'pustoshka', 'puchezh', 'pytalovo', 'pyt-yah', 'pyatigorsk', 'raduzhnyi-vladimir', 'raduzhnyi', 'raychihinsk', 'rasskazovo', 'revda', 'rezh', 'rzhev', 'rodniki', 'roslavl', 'rossosh', 'rostov-yaroslavl', 'rostov', 'rtischevo', 'rubtsovsk', 'rudnya', 'ruzaevka', 'rybinsk', 'rybnoe', 'rylsk', 'ryazhsk', 'ryazan', 'saki', 'salavat', 'salehard', 'salsk', 'samara', 'saransk', 'sarapul', 'saratov', 'sarov', 'sars', 'sasovo', 'satka', 'safonovo', 'sayanogorsk', 'sayansk', 'svetlogorsk', 'svetlograd', 'svetlyi', 'svirsk', 'svobodnyi', 'sebezh', 'sevastopol', 'severobaykalsk', 'severodvinsk', 'severomorsk', 'severouralsk', 'seversk', 'sevsk', 'segezha', 'seltso', 'semenov', 'semikarakorsk', 'semiluki', 'sengiley', 'serafimovich', 'sergach', 'serdobsk', 'serov', 'sibay', 'sim', 'simferopol', 'skovorodino', 'skopin', 'slavgorod', 'slavsk', 'slavyansk-na-kubani', 'slobodskoi', 'slyudyanka', 'smolensk', 'snezhinsk', 'snezhnogorsk', 'sobinka', 'sovetsk', 'sovetsk-tula', 'sovetskaya-gavan', 'sovetskiy', 'sokol', 'solikamsk', 'sol-iletsk', 'solvychegodsk', 'soltsy', 'sorochinsk', 'sorsk', 'sortavala', 'sosnovka', 'sosnovoborsk', 'sosnogorsk', 'sochi', 'spas-klepiki', 'spassk-dalniy', 'spassk-ryazanskiy', 'srednekolymsk', 'sredneuralsk', 'stavropol', 'staraya-russa', 'staritsa', 'starodub', 'staryi-oskol', 'sterlitamak', 'strezhevoy', 'stroitel', 'strunino', 'suvorov', 'sudak', 'sudzha', 'sudogda', 'suzdal', 'suoyarvi', 'surazh', 'surgut', 'surovikino', 'susuman', 'suhinichi', 'suhoi-log', 'syzran', 'syktyvkar', 'sysert', 'sychevka', 'tavda', 'taganrog', 'tayga', 'tayshet', 'talitsa', 'talnah', 'tambov', 'tara', 'tarko-sale', 'tarusa', 'tatarsk', 'tashtagol', 'tver', 'teberda', 'teykovo', 'temnikov', 'temryuk', 'terek', 'tetyushi', 'timashevsk', 'tihoretsk', 'tobolsk', 'toguchin', 'tolyatti', 'tommot', 'tomsk', 'topki', 'torzhok', 'totma', 'trehgornyi', 'troitsk-chelyabinsk', 'trubchevsk', 'tuapse', 'tuymazy', 'tula', 'tulun', 'tura', 
'turan', 'turinsk', 'tutaev', 'tynda', 'tyrnyauz', 'tyukalinsk', 'tyumen', 'uglich', 'udachnyi', 'udomlya', 'uzhur', 'uzlovaya', 'ulan-ude', 'ulyanovsk', 'unecha', 'uray', 'uren', 'uryupinsk', 'usinsk', 'usman', 'usole', 'usole-sibirskoe', 'ussuriysk', 'ust-dzheguta', 'ust-ilimsk', 'ust-katav', 'ust-kut', 'ust-labinsk', 
'ust-ordynskiy', 'ustyuzhna', 'ufa', 'uhta', 'uchaly', 'uyar', 'fatezh', 'feodosiya', 'fokino-bryansk', 'fokino', 'frolovo', 'furmanov', 'habarovsk', 'hadyzhensk', 'hanty-mansiysk', 'harabali', 'harovsk', 'hasavyurt', 'hvalynsk', 'hilok', 'holm', 'holmsk', 'tsivilsk', 'tsimlyansk', 'chadan', 'chaykovskiy', 'chapaevsk', 'chaplygin', 'chebarkul', 'cheboksary', 'chegem', 'chelyabinsk', 'cherdyn', 'cheremhovo', 'cherepanovo', 'cherepovets', 'cherkessk', 'chermoz', 'chernogorsk', 'chernushka', 'chernyahovsk', 'chistopol', 'chita', 'chkalovsk', 'chudovo', 'chulym', 'chusovoy', 'chuhloma', 'shagonar', 'shadrinsk', 'shali', 'sharypovo', 'sharya', 'shahty', 'shahunya', 'shatsk', 'shebekino', 'shelehov', 'shenkursk', 'shilka', 'shimanovsk', 'shihany', 'shumerlya', 'shumiha', 'shuya', 'schekino', 'schigry', 'elista', 'engels', 'ertil', 'yugorsk', 'yuzha', 'yuzhno-sahalinsk', 'yuzhno-suhokumsk', 'yuzhnouralsk', 'yurga', 'yurev-polskiy', 'yurevets', 'yuryuzan', 'yuhnov', 'yadrin', 'yakutsk', 'yalta', 'yalutorovsk', 'yanaul', 'yaransk', 'yarovoe', 'yaroslavl', 'yartsevo', 'yasnogorsk', 'yasnyi']

log = ''
start_time = time.time()
def get_number_from_string(string):
  """Получает число из строки, если оно есть."""
  match = re.search(r'\d+', string)
  if match:
    return int(match.group())
  return None

def progress_bar(current, total, bar_length=20):
    """Отображает полосу загрузки в командной строке."""
    percent = round(current * 100 / total, 2)
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + ' ' * (bar_length - filled_length)
    sys.stdout.write(f'\r[{bar}] {percent}%')
    sys.stdout.flush()

def get_phone_number(contact_id):
    cookies = {
        '_ym_uid': '1727960187618746765',
        '_ym_d': '1727960187',
        '_ga': 'GA1.1.714713443.1727960188',
        'PHPSESSID': 'qmrn6ckkl97na1sjpookeuu17p',
        '_width': '1519',
        '_height': '692',
        '_ym_isad': '1',
        '_ym_visorc': 'w',
        'cf_clearance': 'glWPSeW2Rmzh2nJwmddu3lI3jqSCFmFQi_qRJZ3GDxU-1728111136-1.2.1.1-OlSl4HNaWps_TSOq_Pvg0MzN5Cqzryrqzpbv37vYgW10X5HeJzqvdFe3tLa5T3zG_PiEn64DjBvyTOtiAFdZfov7Z0R9htJvyJiRZq25hb9QtFyk7HquA8.P5_SZiY6CgllaY4ZFCmdPHVCWznN7Io2o6xNuu_SKrX0uDasjZoKVVVPetFNT4E0MOnqperE_yGPMHpC99EY9kp8LgbXpoKEjNcRkotSbg0lblHU7AIqNu42.ARNczDVjCU4Q674c8Wod58jsdSiJMQ7C9trOVHzDTrMdgs6obfe12HGPdbzahIK.0LwGeuqWg2PWb4Yq6qeApWYrgg1pMaPMUjcGnBNox37Y8xfQ5lkIWvC21sZ3B5Xg.3Faf4PuZrn0_YVbJ4vh1SBVBm8xd9CC74hZzhNqYn7x6XQRl0JqFL_q2Ds',
        '_ga_YJRM11Y9D9': 'GS1.1.1728110164.2.1.1728111411.60.0.0',
        'name_en': 'spb',
    }

    headers = {
        'accept': 'text/html, */*; q=0.01',
        'accept-language': 'ru,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '_ym_uid=1727960187618746765; _ym_d=1727960187; _ga=GA1.1.714713443.1727960188; PHPSESSID=qmrn6ckkl97na1sjpookeuu17p; _width=1519; _height=692; _ym_isad=1; _ym_visorc=w; cf_clearance=glWPSeW2Rmzh2nJwmddu3lI3jqSCFmFQi_qRJZ3GDxU-1728111136-1.2.1.1-OlSl4HNaWps_TSOq_Pvg0MzN5Cqzryrqzpbv37vYgW10X5HeJzqvdFe3tLa5T3zG_PiEn64DjBvyTOtiAFdZfov7Z0R9htJvyJiRZq25hb9QtFyk7HquA8.P5_SZiY6CgllaY4ZFCmdPHVCWznN7Io2o6xNuu_SKrX0uDasjZoKVVVPetFNT4E0MOnqperE_yGPMHpC99EY9kp8LgbXpoKEjNcRkotSbg0lblHU7AIqNu42.ARNczDVjCU4Q674c8Wod58jsdSiJMQ7C9trOVHzDTrMdgs6obfe12HGPdbzahIK.0LwGeuqWg2PWb4Yq6qeApWYrgg1pMaPMUjcGnBNox37Y8xfQ5lkIWvC21sZ3B5Xg.3Faf4PuZrn0_YVbJ4vh1SBVBm8xd9CC74hZzhNqYn7x6XQRl0JqFL_q2Ds; _ga_YJRM11Y9D9=GS1.1.1728110164.2.1.1728111411.60.0.0; name_en=spb',
        'origin': 'https://www.yp.ru',
        'priority': 'u=1, i',
        'referer': 'https://www.yp.ru/search/text/%D0%B0%D1%80%D1%85%D0%B8%D1%82%D0%B5%D0%BA%D1%82%D0%BE%D1%80/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "YaBrowser";v="24.7", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'contact_id': contact_id,
    }

    response = requests.post('https://www.yp.ru/ajax/GetPhoneByContactId', cookies=cookies, headers=headers, data=data, verify=False)

    return response.text

for i in range(850, len(cities)):
    results = []
    count = 0
    city = ''
    url = f'https://{cities[i]}.yp.ru/search/text/архитектор/' if cities[i]!='' else 'https://yp.ru/search/text/архитектор/'
    try:
        response = requests.get(url, verify=False)
        html = response.text
        soup = bs(html, 'html.parser')
    except Exception as e:
        print(f"[ERROR] {e}")
        log += f"[ERROR] {e}\n"
        open(f'log_{time.time()}.txt', 'w', encoding='utf-8').write(log)
        exit(0)

    count_block = soup.find('em', string=re.compile('компани'))
    if not count_block: 
        print(f"[WRONG] На странице ничего нет ({cities[i]}). Следующий город...")
        log += f"[WRONG] На странице ничего нет ({cities[i]}). Следующий город...\n"
        continue
    count = int(get_number_from_string(''.join(count_block.text.split())))
    city = soup.find('span', id='search_region_name').find('span').text.strip()

    print(f"[INFO] Найдено {count} компаний в городе {city}")
    log += f"[INFO] Найдено {count} компаний в городе {city}\n"
    for i in range(math.ceil(count/20)):
        try:
            url = f'{url}?page={i+1}'
            response = requests.get(url, verify=False)
            html = response.text
            soup = bs(html, 'html.parser')
        except:
            print(f"[ERROR] {e}")
            log += f"[ERROR] {e}\n"
            open(f'log_{time.time()}.txt', 'w', encoding='utf-8').write(log)
            exit(0)

        print(f"[INFO] Страница {i+1} из {count//20 + 1}. Прошло времени: {round(time.time() - start_time, 2)} сек.")
        log += f"[INFO] Страница {i+1} из {count//20 + 1}\n. Прошло времени: {round(time.time() - start_time, 2)} сек."
        rows_container = soup.find('div', id='companies')
        rows = rows_container.find_all('div', class_='row')
        rows = [row.find('div', class_='company') for row in rows if row.find('div', class_='company')]

        for i in range(len(rows)):
            row = rows[i]

            nm, desc, contact_id, link, worktime, address, phone_number = '', '', '', '', '', '', ''

            nm_block = row.find('h2', class_='company__name').find('a')
            desc_block = row.find('p', class_='company__description')
            contact_id_block = row.find('span', id='contactId')
            link_block = row.find('p', class_='company__url')
            worktime_block = row.find('p', class_='company__worktime')
            address_block = row.find('img', attrs={'src': '/images/map/location_on-24px.svg'})

            if contact_id_block and contact_id_block.text.strip() == '':
                continue

            if nm_block:
                nm = nm_block.text.strip()
            if desc_block:
                desc = desc_block.text.strip().split('.')[0].strip() + '.'
            if contact_id_block:
                contact_id = contact_id_block.text.strip()
                phone_number = get_phone_number(contact_id)
            if link_block:
                link = link_block.find('a')['href'].strip()
            if worktime_block:
                worktime = worktime_block.text.replace('Режим работы:', '').strip()
            if address_block:
                address = address_block.parent.text.strip()

            results.append({
                'Город': city,
                'Название': nm,
                'Описание': desc,
                'Телефон': phone_number,
                'Сайт': link,
                'Режим работы': worktime,
                'Адрес': address
            })
            
            progress_bar(i+1, len(rows))
        print()

    for result in results:
        row = []
        for header in headers:
            row.append(result.get(header))
        worksheet.append(row)

    workbook.save('results.xlsx')

open(f'log_{time.time()}.txt', 'w', encoding='utf-8').write(log)