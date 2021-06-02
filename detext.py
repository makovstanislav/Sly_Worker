
class Doc:
    # предмет (вид) документа
    subjects = ["Contract", "Letter", "Other"]

    # уникальные слова (аргументы метода count_check). цифра означает сколько условий должно быть правдой
    __contract_must_2 = {"цей договір": 1, "даний договір": 1, "догов": 3, "угод": 3, "agreement": 3,
                       "contract": 3, "сторон": 3, "особі": 1, "parties": 3}
    __letter_must_1 = {"з повагою": 1, 'шановний': 1, 'просимо': 1, 'прошу': 1, 'kindly': 1, 'sincerely': 1,
                     'best regards': 1, 'best wishes': 1}

    def __init__(self, text):
        self.text = text

    #!!!!!!!!!! переделать
    # !!!!! кваргс скорей всего можно без звездочек. проверить!!!
    # лучше аргументы задавать в определении функции
    # проверка на минимальное количество уникальных слов
    def count_check(self, kwargs, minimum=None):
        text_low = self.text.lower()
        validations = 0
        for key, value in kwargs.items():
            key_low = key.lower()
            if text_low.count(key_low) >= value:
                validations += 1
        if minimum:
            return validations >= minimum
        else:
            return validations == len(kwargs)

    # определяет тип офисного документа

    def subject(self):
        subject_is = "Other"
        if self.count_check(self.__contract_must_2, 2) and not self.count_check(self.__letter_must_1, 1):
            subject_is = "Contract"
        elif self.count_check(self.__letter_must_1, 1) and not self.count_check(self.__contract_must_2, 1):
            subject_is = "Letter"
        return subject_is

    # возвращает какого шаблонного текста нет
    def check_boilerplates(self, kwargs):
        doc_subject = self.subject()
        absent_bp = []
        boilerplate_lst = kwargs.get(doc_subject)
        for bp in boilerplate_lst:
            if bp not in self.text:
                absent_bp.append(bp)
        print("Отсутствует такой текст: ", absent_bp)
        return absent_bp


class ContractDoc(Doc):
    # Предметы договоров
    subjects = ["Rent", "Modernization", "Agency", "NDA", "Factoring", "Insurance", "Servitude" , "AdPlacement", "Sales",
                "Contractor", "Softdev", "License", "Creative", "Channels", "Access", "Termination", "Amendment", "Annex", "Other"]
    # уникальные слова (аргументы метода count_check)
    uniques = {"Rent": {"орендар": 3, "орендодавець": 3}, "Insurance": {"страх": 10}, "Contractor": {"підрядн": 5},
        "Sales": {"постачальн": 6}, "Agency": {"агентськ": 3}, "Servitude": {"сервітут": 4}, "Modernization": {"модерніз": 3, "доступ": 2},
        "Factoring": {"фактор": 3}, "AdPlacement": {"реклам": 2, "розміщ": 3}, "Softdev": {"розроб": 3, "програм": 3},
        "License": {"ліценз": 10}, "Creative": {"реклам": 2, "розроб": 2, "майн": 2}, "Channels": {"канал": 3, "терит": 1},
        "Access": {"доступ": 4, "телекомунікац": 2, "акт": 1}, "NDA": {"конфіденц": 5, "доступ": 2},
        "Amendment": {"ця додаткова угода": 1, "дана додаткова угода": 1, "наступній редакції": 2, "додаткова угода": 2},
        "Annex": {"цей додаток": 1, "даний додаток": 1}}

    # реквизиты компаний
    bank_details = {'воля-кабель': ['UA383510050000026003062793500', '30777913', '162810450034'],
                    'телесвіт': ['UA373510050000026006237322800', '33103969', '1628104500340'],
                    'київські телекомунікаційні мережі': ['UA373510050000026006237322800', '33103969', '1628104500340'],
                    'віа медіа': ['UA183510050000026009386138500', '35362752', '353627526531']}

    def __init__(self, text):
        self.text = text

    # detecting of a subject by unique words counting
    def subject(self):
        for key, value in self.uniques.items():
            if self.count_check(value):
                return key
        return "Other"

    # возращает название юр лица с нашей стороны
    def __check_entity(self):
        uniques = {'воля-кабель': 2, 'телесвіт': 2, 'київські телекомунікаційні мережі': 2, 'віа медіа': 2}
        for key, value in uniques.items():
            if self.count_check({key:value}):
                return key


class Letter(Doc):
    pass
