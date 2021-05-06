import sys
from webbrowser import open
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from form_ui import Ui_MainWindow


class MiniGG(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 필요 변수 초기 셋팅
        self.this_version = "1.2"
        self.cid = ""  # POST 호출에 필요한 데이터
        self.version = ""  # 패치 버전 정보
        self.get_img_version = ""  # 패치 버전 정보이나 이미지 링크에 포함되는 별도의 패치 버전
        self.skill_list = []  # 스킬 이미지 파일 이름 정보
        self.champ_dic = {}  # 챔피언 이름 데이터 (한글, 영문 모두 포함)
        # 텍스트 레이블 변수 목록 (초기화 대상)
        self.total_label_ObjList = [self.spell_rate_1, self.spell_rate_2, self.spell_rate_3,
                                    self.spell_rate_4, self.spell_rate_5, self.spell_rate_6,
                                    self.shoes_rate_1, self.shoes_rate_2,
                                    self.shoes_rate_3, self.shoes_rate_4,
                                    self.lune_rate_1, self.lune_rate_2,
                                    self.lune_rate_3, self.lune_rate_4,
                                    self.skill_rate_1, self.skill_rate_2,
                                    self.skill_rate_3, self.skill_rate_4,
                                    self.skill_name_1, self.skill_name_2, self.skill_name_3,
                                    self.skill_name_4, self.skill_name_5, self.skill_name_6,
                                    self.startitem_rate_1, self.startitem_rate_2,
                                    self.startitem_rate_3, self.startitem_rate_4,
                                    self.item_rate_1, self.item_rate_2, self.item_rate_3,
                                    self.item_rate_4, self.item_rate_5, self.item_rate_6, self.skill_1_to_3]
        # 이미지 레이블 변수 목록 (초기화 대상)
        self.total_img_ObjList = [self.spell_img_1, self.spell_img_2, self.spell_img_3,
                                  self.spell_img_4, self.spell_img_5, self.spell_img_6,
                                  self.shoes_img_1, self.shoes_img_2,
                                  self.lune_img_1, self.lune_img_2,
                                  self.lune_img_3, self.lune_img_4,
                                  self.skill_img_1, self.skill_img_2, self.skill_img_3,
                                  self.skill_img_4, self.skill_img_5, self.skill_img_6,
                                  self.startitem_img_1, self.startitem_img_2, self.startitem_img_3,
                                  self.startitem_img_4, self.startitem_img_5, self.startitem_img_6,
                                  self.item_img_1, self.item_img_2, self.item_img_3,
                                  self.item_img_4, self.item_img_5, self.item_img_6,
                                  self.item_img_7, self.item_img_8, self.item_img_9,
                                  self.det_lune_1, self.det_lune_2, self.det_lune_3, self.det_lune_4,
                                  self.det_lune_5, self.det_lune_6, self.det_lune_7, self.det_lune_8,
                                  self.det_lune_9, self.det_lune_10, self.det_lune_11]

        # 초기화 후 실행될 함수 or 시그널 연결
        self.move_center()  # 화면 중앙 배치
        self.make_champion_map()  # self.champ_dic 에 챔피언 이름 데이터를 저장하는 함수
        self.get_version()  # 이미지 링크에 포함되는 패치 버전 정보를 받아오는 함수
        self.listWidget.itemDoubleClicked.connect(self.checkbox_state_and_set_pos)  # ListWidget 시그널 연결 (DbClicked)
        # self.comboBox.currentTextChanged.connect(self.checkbox_state_and_set_pos)  # 미사용 (중복 실행 이슈가 존재함.)
        self.checkBox.stateChanged.connect(self.checkbox_changed)  # checkBox 시그널 연결 (위의 중복 실행 이슈 대안)

    # 화면 중앙 배치
    def move_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 텍스트, 이미지 레이블 데이터 초기화 (재검색 시 최상단에 실행)
    def init_label_data(self):
        for obj in self.total_img_ObjList:
            obj.clear()

        for label_obj in self.total_label_ObjList:
            label_obj.setText("-")

    # 챔피언 이름 (한글, 영문) 데이터 저장
    def make_champion_map(self):
        find_url = "http://fow.kr/champs"
        page = urlopen(find_url).read()
        soup = BeautifulSoup(page, 'lxml')
        champion_name = soup.select("div.champ_list > ul a")

        for i in range(len(champion_name)):
            eng_name = champion_name[i]['href'].split('/')[-1]
            kor_name = champion_name[i].select('li')[0]['rname']
            self.champ_dic[kor_name] = eng_name

    # 이미지 링크에 포함되는 패치 버전 정보 저장
    def get_version(self):
        version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
        version_page = urlopen(version_url).read().decode()
        self.get_img_version = version_page.split(',')[0].replace("[", "").replace('"', '')

    # checkBox 체크 여부 판별 후 포지션 셋팅
    def checkbox_state_and_set_pos(self):
        champ_url = "http://fow.kr/champs/"
        champ_name = self.listWidget.currentItem().text().replace(' ', '')
        champ_url += self.champ_dic[champ_name]

        position = ""
        page = urlopen(champ_url).read()
        soup = BeautifulSoup(page, 'lxml')

        self.cid = soup.select('div.build_select.build_select_on')[0]['cid']
        self.version = soup.select('div.build_select.build_select_on')[0]['ver']

        # 챔피언 포지션 자동인식
        if self.checkBox.isChecked() is True:
            position = soup.select('div.build_select.build_select_on')[0]['pos']
            if position == "TOP":
                self.comboBox.setCurrentIndex(0)
            elif position == "JUNGLE":
                self.comboBox.setCurrentIndex(1)
            elif position == "MIDDLE":
                self.comboBox.setCurrentIndex(2)
            elif position == "DUO_CARRY":
                self.comboBox.setCurrentIndex(3)
            elif position == "DUO_SUPPORT":
                self.comboBox.setCurrentIndex(4)

            self.champion_selected(champ_name, position)
        else:  # 챔피언 포지션 자동인식 해제
            cur_pos = self.comboBox.currentText()
            if cur_pos == "탑":
                position = "TOP"
            elif cur_pos == "정글":
                position = "JUNGLE"
            elif cur_pos == "미드":
                position = "MIDDLE"
            elif cur_pos == "원거리 딜러":
                position = "DUO_CARRY"
            elif cur_pos == "서포터":
                position = "DUO_SUPPORT"
            elif cur_pos == "칼바람":
                self.all_random_game(champ_name)

            if cur_pos != "칼바람":
                self.champion_selected(champ_name, position)

    # checkBox 변동 시그널
    def checkbox_changed(self):
        if self.checkBox.isChecked() is False:
            self.comboBox.setEnabled(True)
            QMessageBox.about(self, "정보", "포지션 자동 인식을 해제합니다. \n\n포지션을 선택하고 챔피언을 더블클릭 하면 검색이 가능합니다.")
        else:
            self.comboBox.setEnabled(False)

    # 이미지 레이블에 이미지 삽입
    def input_img_data(self, img_url, obj):
        # 개선된 화질의 이미지를 불러오기 위해서 라이엇 공식 API 사용(아이템만 해당)
        if "items3" in img_url:
            img_url = img_url.replace("http://z.fow.kr/items3/", "http://ddragon.leagueoflegends.com/cdn/"
                                      + self.get_img_version + "/img/item/")

        # 이미지 데이터 로딩
        image_string = urlopen(img_url).read()
        image = QPixmap()
        image.loadFromData(image_string)
        image = image.scaled(41, 41)  # 크기 조절
        obj.setPixmap(image)

    # 스킬 이미지 파일 이름 저장
    def skill_name_build(self, champ_name):
        self.skill_list = []  # 초기화 필수
        get_skill_name_url = "http://ddragon.leagueoflegends.com/cdn/10.9.1/data/ko_KR/champion/" \
                             "" + self.champ_dic[champ_name] + ".json"
        page = urlopen(get_skill_name_url).read().decode("UTF-8")

        for i in range(1, 5):
            self.skill_list.append(page.split('spells')[1].split('"image":{"full":"')[i].split('"')[0])

    # 챔피언이 선택되었을 경우 데이터 로드 (소환사의 협곡)
    def champion_selected(self, champ_name, pos):
        # 텍스트, 이미지 레이블 데이터 초기화 실행
        self.init_label_data()

        # 1. 필요 데이터 셋팅 (이미지 링크가 POST 방식이므로 파라미터가 필요함)
        get_info_url = "http://fow.kr/api_new_ajax.php"
        values = {'action': 'champ_build',
                  'cid': self.cid,
                  'pos': pos,
                  'ver': self.version}
        # 파라미터는 UTF-8 형식으로 인코딩하여 전송해야한다.
        param = urlencode(values).encode('UTF-8')
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

        # 2. POST 방식 urllib.request 전송
        req = Request(get_info_url, param, headers)
        response = urlopen(req).read().decode('UTF-8')
        soup = BeautifulSoup(response, 'lxml')

        # 3. 데이터 분류 작업 (같은 변수를 덮어쓰면서 사용하므로 헷갈리지 않게 주의할 것)
        # 3-1. 추천 스펠
        obj_list = [self.spell_img_1, self.spell_img_2,
                    self.spell_rate_1, self.spell_rate_2,
                    self.spell_img_3, self.spell_img_4,
                    self.spell_rate_3, self.spell_rate_4,
                    self.spell_img_5, self.spell_img_6,
                    self.spell_rate_5, self.spell_rate_6]

        data_list = soup.find_all(["thead", "tbody"])
        match_count = 0
        idx = 0

        for count in range(0, len(data_list), 2):
            match_string = data_list[count].find_all("th")[0]
            if match_string.string.replace(" ", "") == "소환사주문":
                match_count = count

        data_list = data_list[match_count + 1].find_all('td')

        for i in range(len(data_list)):
            if i <= 8:
                if data_list[i].find('img') is None:
                    if i == 1 or i == 4 or i == 7:
                        obj_list[idx].setText("픽률: " + data_list[i].string.strip())
                    else:
                        obj_list[idx].setText("승률: " + data_list[i].string.strip())
                else:
                    img_url = data_list[i].find_all('img')[0].attrs['src'].replace("//", "http://")
                    self.input_img_data(img_url, obj_list[idx])
                    idx += 1
                    img_url = data_list[i].find_all('img')[1].attrs['src'].replace("//", "http://")
                    self.input_img_data(img_url, obj_list[idx])
                idx += 1
            else:
                break

        # 3-2. 추천 신발
        obj_list = [self.shoes_img_1, self.shoes_rate_1, self.shoes_rate_2,
                    self.shoes_img_2, self.shoes_rate_3, self.shoes_rate_4]

        data_list = soup.find_all(["thead", "tbody"])
        match_count = 0

        for count in range(0, len(data_list), 2):
            match_string = data_list[count].find_all("th")[0]
            if match_string.string.replace(" ", "") == "최종신발":
                match_count = count

        data_list = data_list[match_count + 1].find_all('td')

        for i in range(len(data_list)):
            if i <= 5:
                if data_list[i].find('img') is None:
                    if i == 1 or i == 4:
                        obj_list[i].setText("픽률: " + data_list[i].string.strip())
                    else:
                        obj_list[i].setText("승률: " + data_list[i].string.strip())
                else:
                    img_url = data_list[i].find('img').attrs['src'].replace("//", "http://")
                    self.input_img_data(img_url, obj_list[i])
            else:
                break

        # 3-3. 룬 선택
        obj_list = [self.lune_img_1, self.lune_img_2,
                    self.lune_rate_1, self.lune_rate_2,
                    self.lune_img_3, self.lune_img_4,
                    self.lune_rate_3, self.lune_rate_4]

        data_list = soup.find_all(["thead", "tbody"])
        match_count = 0
        idx = 0

        for count in range(0, len(data_list), 2):
            match_string = data_list[count].find_all("th")[0]
            if match_string.string.replace(" ", "") == "룬선택":
                match_count = count

        data_list = data_list[match_count + 1].find_all('td')

        for i in range(len(data_list)):
            if i <= 5:
                if data_list[i].find('img') is None:
                    if i == 1 or i == 4:
                        obj_list[idx].setText("픽률: " + data_list[i].string.strip())
                    else:
                        obj_list[idx].setText("승률: " + data_list[i].string.strip())
                else:
                    img_url = data_list[i].find_all('img')[0].attrs['src'].replace("//", "http://")
                    self.input_img_data(img_url, obj_list[idx])
                    idx += 1
                    img_url = data_list[i].find_all('img')[1].attrs['src'].replace("//", "http://")
                    self.input_img_data(img_url, obj_list[idx])
                idx += 1
            else:
                break

        # 3-4. 추천 아이템
        obj_list = [self.startitem_img_1, self.startitem_img_2, self.startitem_img_3,
                    self.startitem_rate_1, self.startitem_rate_2,
                    self.startitem_img_4, self.startitem_img_5, self.startitem_img_6,
                    self.startitem_rate_3, self.startitem_rate_4]

        data_list = soup.find_all(["thead", "tbody"])
        match_count = 0
        idx = 0

        for count in range(0, len(data_list), 2):
            match_string = data_list[count].find_all("th")[0]
            if match_string.string.replace(" ", "") == "시작아이템":
                match_count = count

        data_list = data_list[match_count + 1].find_all('td')

        for i in range(len(data_list)):
            if i <= 5:
                if data_list[i].find('img') is None:
                    if i == 1 or i == 4:
                        obj_list[idx].setText("픽률: " + data_list[i].string.strip())
                    else:
                        obj_list[idx].setText("승률: " + data_list[i].string.strip())
                else:
                    img_url = data_list[i].find_all('img')[0].attrs['src'].replace("//", "http://")
                    self.input_img_data(img_url, obj_list[idx])
                    idx += 1
                    if len(data_list[i].find_all('img')) == 1:
                        idx += 1
                    elif len(data_list[i].find_all('img')) == 2:
                        img_url = data_list[i].find_all('img')[1].attrs['src'].replace("//", "http://")
                        self.input_img_data(img_url, obj_list[idx])
                        idx += 1
                    elif len(data_list[i].find_all('img')) == 3:
                        img_url = data_list[i].find_all('img')[1].attrs['src'].replace("//", "http://")
                        self.input_img_data(img_url, obj_list[idx])
                        idx += 1
                        img_url = data_list[i].find_all('img')[2].attrs['src'].replace("//", "http://")
                        self.input_img_data(img_url, obj_list[idx])
                idx += 1
            else:
                break

        # 3-5. 아이템 빌드
        obj_list = [self.item_img_1, self.item_img_2, self.item_img_3,
                    self.item_rate_1, self.item_rate_2,
                    self.item_img_4, self.item_img_5, self.item_img_6,
                    self.item_rate_3, self.item_rate_4,
                    self.item_img_7, self.item_img_8, self.item_img_9,
                    self.item_rate_5, self.item_rate_6]

        data_list = soup.find_all(["thead", "tbody"])
        match_count = 0
        idx = 0

        for count in range(0, len(data_list), 2):
            match_string = data_list[count].find_all("th")[0]
            if match_string.string.replace(" ", "") == "아이템빌드":
                match_count = count

        data_list = data_list[match_count + 1].find_all('td')

        for i in range(len(data_list)):
            if i <= 8:
                if data_list[i].find('img') is None:
                    if i == 1 or i == 4 or i == 7:
                        obj_list[idx].setText("픽률: " + data_list[i].string.strip())
                    else:
                        obj_list[idx].setText("승률: " + data_list[i].string.strip())
                else:
                    img_url = data_list[i].find_all('img')[0].attrs['src'].replace("//", "http://")
                    self.input_img_data(img_url, obj_list[idx])
                    idx += 1
                    img_url = data_list[i].find_all('img')[1].attrs['src'].replace("//", "http://")
                    self.input_img_data(img_url, obj_list[idx])
                    idx += 1
                    img_url = data_list[i].find_all('img')[2].attrs['src'].replace("//", "http://")
                    self.input_img_data(img_url, obj_list[idx])
                idx += 1
            else:
                break

        # 3-6. 스킬 빌드
        self.skill_name_build(champ_name)
        obj_list = [self.skill_img_1, self.skill_name_1,
                    self.skill_img_2, self.skill_name_2,
                    self.skill_img_3, self.skill_name_3,
                    self.skill_rate_1, self.skill_rate_2,
                    self.skill_img_4, self.skill_name_4,
                    self.skill_img_5, self.skill_name_5,
                    self.skill_img_6, self.skill_name_6,
                    self.skill_rate_3, self.skill_rate_4]

        data_list = soup.find_all(["thead", "tbody"])
        match_count = 0
        idx = 0

        for count in range(0, len(data_list), 2):
            match_string = data_list[count].find_all("th")[0]
            if match_string.string.replace(" ", "") == "스킬순서":
                match_count = count

        data_list = data_list[match_count + 1].find_all('td')
        self.skill_name_build(champ_name)

        for i in range(len(data_list)):
            skill_tree = data_list[i].string.strip().replace(" ", "")
            if i <= 5:
                if '▶' not in skill_tree:
                    if i == 1 or i == 4 or i == 7:
                        obj_list[idx].setText("픽률: " + data_list[i].string.strip())
                    else:
                        obj_list[idx].setText("승률: " + data_list[i].string.strip())
                else:
                    skill_name = ""
                    skill_tree = skill_tree.split('▶')
                    for k in range(len(skill_tree)):
                        if skill_tree[k] == 'Q':
                            skill_name = self.skill_list[0]
                        elif skill_tree[k] == 'W':
                            skill_name = self.skill_list[1]
                        elif skill_tree[k] == 'E':
                            skill_name = self.skill_list[2]
                        elif skill_tree[k] == 'R':
                            skill_name = self.skill_list[3]
                        skill_img_url = "http://ddragon.leagueoflegends.com/cdn/" + self.get_img_version + "/img/spell/" + skill_name + ""
                        self.input_img_data(skill_img_url, obj_list[idx])
                        idx += 1
                        obj_list[idx].setText(skill_tree[k])
                        if k <= 1:
                            idx += 1
                idx += 1
            else:
                break

        # 3-7. 1~3 레벨 스킬 트리
        op_pos = ""

        if pos == "TOP":
            op_pos = "top"
        elif pos == "JUNGLE":
            op_pos = "jungle"
        elif pos == "MIDDLE":
            op_pos = "mid"
        elif pos == "DUO_CARRY":
            op_pos = "bot"
        elif pos == "DUO_SUPPORT":
            op_pos = "support"

        get_info_url = "http://www.op.gg/champion/" + self.champ_dic[champ_name] + "/statistics/" + op_pos
        page = urlopen(get_info_url).read()
        soup = BeautifulSoup(page, 'lxml')
        low_level_skill_data = soup.select('table.champion-skill-build__table tbody tr')[1]

        skill_build = low_level_skill_data.select('td')[0].string.strip() + " ▶ "\
            + low_level_skill_data.select('td')[1].string.strip() + " ▶ "\
            + low_level_skill_data.select('td')[2].string.strip()

        self.skill_1_to_3.setText(skill_build)

        # 3-8. 룬 세부 선택
        obj_list = [self.det_lune_1, self.det_lune_2, self.det_lune_3, self.det_lune_4,
                    self.det_lune_5, self.det_lune_6, self.det_lune_7, self.det_lune_8,
                    self.det_lune_9, self.det_lune_10, self.det_lune_11]
        idx = 0
        lune_rep = soup.select("div.perk-page__item--mark")
        mini_lune = soup.select("img.active.tip")
        lune_page = soup.select("div.perk-page .perk-page__item--active")

        for i in range(0, 6):
            if i == 0:
                img_url = lune_rep[0].find('img')['src'].replace("//", "http://")
                self.input_img_data(img_url, obj_list[idx])
                idx += 1
            elif i == 4:
                img_url = lune_rep[1].find('img')['src'].replace("//", "http://")
                self.input_img_data(img_url, obj_list[idx])
                idx += 1

            img_url = lune_page[i].find('img')['src'].replace("//", "http://")
            self.input_img_data(img_url, obj_list[idx])
            idx += 1

        for j in range(0, 3):
            img_url = mini_lune[j]['src'].replace("//", "http://")
            self.input_img_data(img_url, obj_list[idx])
            idx += 1

    # 챔피언이 선택되었을 경우 데이터 로드 (칼바람 나락)
    def all_random_game(self, champ_name):
        # 텍스트, 이미지 레이블 데이터 초기화
        self.init_label_data()

        # 챔피언 한글 이름 영문 변환
        eng_name = self.champ_dic[champ_name]

        # 1. 필요 데이터 셋팅
        ar_url = "https://poro.gg/ko/champions/" + eng_name + "/aram"
        page = urlopen(ar_url).read()
        soup = BeautifulSoup(page, 'lxml')
        data_list = soup.select("div.stat-table.font-size-0 div.tbody")

        # 2. 데이터 분류 작업 (같은 이름의 변수를 덮어쓰며 사용하므로 주의할 것)
        # 2-1. 시작 아이템
        obj_list = [self.startitem_img_1, self.startitem_img_2, self.startitem_img_3,
                    self.startitem_rate_1, self.startitem_rate_2,
                    self.startitem_img_4, self.startitem_img_5, self.startitem_img_6,
                    self.startitem_rate_3, self.startitem_rate_4]
        idx = 0  # obj 처리 순서 결정 변수

        # img_list => 이미지 링크 + 픽률 + 승률 데이터
        img_list = data_list[0].select("div.tr")

        for i in range(len(img_list)):
            if i >= 2:
                break

            self.input_img_data(img_list[i].select('div div')[0].find_all('img')[0]['src']
                                .replace("//", "https://"), obj_list[idx])
            idx += 1

            if len(img_list[i].select('div div')[0].find_all('img')) == 1:
                idx += 2

            elif len(img_list[i].select('div div')[0].find_all('img')) == 2:
                self.input_img_data(img_list[i].select('div div')[0].find_all('img')[1]['src']
                                    .replace("//", "https://"), obj_list[idx])
                idx += 2

            elif len(img_list[i].select('div div')[0].find_all('img')) == 3:
                self.input_img_data(img_list[i].select('div div')[0].find_all('img')[1]['src']
                                    .replace("//", "https://"), obj_list[idx])
                idx += 1
                self.input_img_data(img_list[i].select('div div')[0].find_all('img')[2]['src']
                                    .replace("//", "https://"), obj_list[idx])
                idx += 1

            obj_list[idx].setText("승률: " + img_list[i].select('div div span.font-size-sm')[0].string)
            idx += 1
            obj_list[idx].setText("픽률: " + img_list[i].select('div div span.font-size-sm')[1].string)
            idx += 1

        # 2-2. 핵심 아이템
        obj_list = [self.item_img_1, self.item_img_2, self.item_img_3,
                    self.item_rate_1, self.item_rate_2,
                    self.item_img_4, self.item_img_5, self.item_img_6,
                    self.item_rate_3, self.item_rate_4,
                    self.item_img_7, self.item_img_8, self.item_img_9,
                    self.item_rate_5, self.item_rate_6]
        idx = 0

        img_list = data_list[1].select("div.tr")

        for i in range(len(img_list)):
            if i >= 3:
                break

            # 핵심 아이템은 이미지 3개로 고정
            self.input_img_data(img_list[i].select('div div')[0].find_all('img')[0]['src']
                                .replace("//", "https://"), obj_list[idx])
            idx += 1
            self.input_img_data(img_list[i].select('div div')[0].find_all('img')[1]['src']
                                .replace("//", "https://"), obj_list[idx])
            idx += 1
            self.input_img_data(img_list[i].select('div div')[0].find_all('img')[2]['src']
                                .replace("//", "https://"), obj_list[idx])
            idx += 1

            obj_list[idx].setText("승률: " + img_list[i].select('div div span.font-size-sm')[0].string)
            idx += 1
            obj_list[idx].setText("픽률: " + img_list[i].select('div div span.font-size-sm')[1].string)
            idx += 1

        # 2-3. 신발 아이템
        img_list = data_list[2].select("div.tr img")
        obj_list = [self.shoes_rate_1, self.shoes_rate_2, self.shoes_rate_3, self.shoes_rate_4]

        # 신발 데이터가 없으므로 - 표시
        for k in range(len(obj_list)):
            if (k + 1) % 2 != 0:
                obj_list[k].setText("승률: -")
            else:
                obj_list[k].setText("픽률: -")

        obj_list = [self.shoes_img_1, self.shoes_img_2]
        for i in range(len(img_list)):
            if i >= 2:
                break

            # 신발 아이템 이미지는 두 개로 고정 => 이름 직접 할당 방식 사용
            self.input_img_data(img_list[i]['src']
                                .replace("//", "https://"), obj_list[i])

        # 2-4. 스킬 트리
        obj_list = [self.skill_img_1, self.skill_name_1,
                    self.skill_img_2, self.skill_name_2,
                    self.skill_img_3, self.skill_name_3,
                    self.skill_rate_1, self.skill_rate_2,
                    self.skill_img_4, self.skill_name_4,
                    self.skill_img_5, self.skill_name_5,
                    self.skill_img_6, self.skill_name_6,
                    self.skill_rate_3, self.skill_rate_4]
        idx = 0

        img_list = data_list[4].select('div')
        target_list = data_list[4].select('div.champion-stats__spell-header')

        for i in range(len(img_list)):
            if i >= 2:
                break

            # 스킬 트리 처리 순서 (이미지 -> 스킬 단축키(x3) -> 승률 -> 픽률)
            for k in range(0, 3):
                self.input_img_data(target_list[i].find_all('img')[k]['src']
                                    .replace("//", "https://"), obj_list[idx])
                idx += 1

                obj_list[idx].setText(target_list[i].select('span.champion-stats__slot')[k].string)
                idx += 1

            # 승률
            obj_list[idx].setText("승률: " + target_list[i].select('span.font-size-sm')[0]
                                  .string.replace(' ', '').replace('\n', ''))
            idx += 1

            # 픽률
            obj_list[idx].setText("픽률: " + target_list[i].select('span.font-size-sm')[1]
                                  .string.replace(' ', '').replace('\n', ''))
            idx += 1

        # 2-5. 추천 스펠
        obj_list = [self.spell_img_1, self.spell_img_2,
                    self.spell_rate_1, self.spell_rate_2,
                    self.spell_img_3, self.spell_img_4,
                    self.spell_rate_3, self.spell_rate_4,
                    self.spell_img_5, self.spell_img_6,
                    self.spell_rate_5, self.spell_rate_6]
        idx = 0

        img_list = data_list[7].select("div.tr")

        for i in range(len(img_list)):
            if i >= 3:
                break

            self.input_img_data(img_list[i].find_all('img')[0]['src']
                                .replace("//", "https://"), obj_list[idx])
            idx += 1
            self.input_img_data(img_list[i].find_all('img')[1]['src']
                                .replace("//", "https://"), obj_list[idx])
            idx += 1
            obj_list[idx].setText("승률: " + img_list[i].select('div div span.font-size-sm')[0].string)
            idx += 1
            obj_list[idx].setText("픽률: " + img_list[i].select('div div span.font-size-sm')[1].string)
            idx += 1

        # 2-6. 룬 셋팅
        obj_list = [self.lune_img_1, self.lune_img_2,
                    self.lune_img_3, self.lune_img_4,
                    self.lune_rate_1, self.lune_rate_2,
                    self.lune_rate_3, self.lune_rate_4]

        img_list = soup.select("header.rune__header")
        idx = 0

        for i in range(len(img_list)):
            for j in range(0, 2):
                self.input_img_data(img_list[i].find_all("img")[j]['src'].replace("//", "https://"), obj_list[idx])
                idx += 1

        img_list = soup.select("div.champion-stats__rune__right")

        for i in range(len(img_list)):
            for j in range(2):
                if j == 0:
                    obj_list[idx].setText("승률: " + img_list[i].select("span.text-black")[j].string)
                else:
                    obj_list[idx].setText("픽률: " + img_list[i].select("span.text-black")[j].string)
                idx += 1

        # 2-7. 룬 세부 세팅
        obj_list = [self.det_lune_1, self.det_lune_2, self.det_lune_3, self.det_lune_4,
                    self.det_lune_5, self.det_lune_6, self.det_lune_7, self.det_lune_8,
                    self.det_lune_9, self.det_lune_10, self.det_lune_11]

        idx = 0

        lune_rep = soup.select("div.rune__item.tooltip.is-active img")
        lune_pri = soup.select("div.rune__header__primary img")[0]['src'].replace("//", "http://")
        lune_sec = soup.select("div.rune__header__sub img")[0]['src'].replace("//", "http://")

        for i in range(0, 6):
            if i == 0:
                self.input_img_data(lune_pri, obj_list[idx])
                idx += 1

            if i == 4:
                self.input_img_data(lune_sec, obj_list[idx])
                idx += 1

            img_url = lune_rep[i]['src'].replace("//", "http://")
            self.input_img_data(img_url, obj_list[idx])
            idx += 1

        lune_sub = soup.select("div.rune__content__stats__col.tooltip.is-active img")
        for j in range(0, 3):
            self.input_img_data(lune_sub[j]['src'], obj_list[idx])
            idx += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MiniGG()
    window.show()
    app.exec_()
