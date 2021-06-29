class Doc:

    def __init__(self, text):
        self.text = text

    # returns True if text contains minimum number of unique words occurrences required by the dictionary
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

    # detects a type of the document. If the document belongs to a subtype the fn will return "type/subtype"
    def subject(self):
        subject_is = "Other"
        from main import data

        # returns True if the document belongs to specific category (type or subtype).
        # Parameter: value (in form of a dict) of a key
        def validate_category(category_requisites):
            uniques = category_requisites["uniques"]
            unq_req = category_requisites["unq_req"]
            if unq_req == "all":
                unq_req = len(uniques)
            return self.count_check(uniques, unq_req)

        # iteration through types and subtypes in the data.yaml to check if the document matches any
        for type, type_requisites in data.items():
            if validate_category(type_requisites):
                # a type may not contain subtypes
                if "subtypes" in type_requisites:
                    for subtype, subtype_requisites in type_requisites["subtypes"].items():
                        if validate_category(subtype_requisites):
                            return type + "/" + subtype
                    return type + "/" + "Other"
                else:
                    return type
            else:
                continue
        return subject_is


