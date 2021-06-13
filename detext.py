class Doc:

    def __init__(self, text):
        self.text = text

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

    def subject(self):
        subject_is = "Other"
        from main import data

        # определяет принадлежит ли документ к конкретной категории. параметр - значения ключа в виде словаря
        def validate_category(category_properties):
            uniques = category_properties["uniques"]
            unq_req = category_properties["unq_req"]
            if unq_req == "all":
                unq_req = len(uniques)
            return self.count_check(uniques, unq_req)

        for type, type_properties in data.items():
            if validate_category(type_properties):
                if "subtypes" in type_properties:
                    for subtype, subtype_properties in type_properties["subtypes"].items():
                        if validate_category(subtype_properties):
                            return type + "/" + subtype
                    return type + "/" + "Other"
                else:
                    return type
            else:
                continue
        return subject_is


