import yaml

class Doc:

    def __init__(self, text):
        self.text = text

    def read_yaml(self):
        with open('data.yaml') as f:
            data = yaml.safe_load(f)
            return data

    def count_check(self, dictionary, min_validations=None):
        text_low = self.text.lower()
        validations = 0
        for key, value in dictionary.items():
            key_low = key.lower()
            if text_low.count(key_low) >= value:
                validations += 1
        if min_validations:
            return validations >= min_validations
        else:
            return validations == len(dictionary)

    # возвращает подтип документа

    # !!! Возможно декоратор заюзать для скорости
    # !!! возможно дату стоит запустить в конструкторе
    def subject(self):
        subject_is = "Other"
        data = self.read_yaml()
        for type in data:
            type_uniques = data[type]["uniques"]
            type_unq_req = data[type]["unq_req"]
            # что-то сделать с not
            # and not self.count_check(self.__letter_must_1, 1)
            if self.count_check(uniques, unq_req):
                if "subtypes" in data[type]:
                    subtypes = data[type]["subtypes"]
                    for sub in subtypes:
                        subtype_uniques = subtypes[sub]["uniques"]
                        subtype_unq_req = subtypes[sub]["unq_req"]
                        if subtype_unq_req == "all":
                            subtype_unq_req = len(subtype_uniques)
                        if self.count_check(subtype_uniques, subtype_unq_req):
                            return data[type]["name"] + "/" + subtypes[sub]["name"]
                    return data[type]["name"] + "/" + "Other"
                else:
                    return data[type]["name"]
            else:
                continue
        return subject_is
