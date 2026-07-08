import re
from rapidfuzz import fuzz


class AadhaarParser:

    def __init__(self, ocr_report):

        self.lines = []

        for item in ocr_report["results"]:

            text = item["text"].strip()

            if len(text) < 2:
                continue

            self.lines.append(text)

        self.full_text = " ".join(self.lines)

    ########################################################
    def extract_aadhaar(self):

        

        for line in self.lines:

            # Ignore VID line
            if "vid" in line.lower():
                continue

            # Extract groups of 4 digits
            groups = re.findall(r"\d{4}", line)

            if len(groups) >= 3:

                return " ".join(groups[:3])

        return None

    ########################################################

    def extract_gender(self):

    

        text = self.full_text.lower()

        # Remove punctuation
        text = re.sub(r"[^a-z ]", " ", text)

        if "female" in text:
            return "Female"

        if "male" in text:
            return "Male"

        return None

    ########################################################

    def extract_dob(self):

        # Standard formats
        patterns = [

            r"\d{2}/\d{2}/\d{4}",

            r"\d{2}-\d{2}-\d{4}",

            r"\d{2}\.\d{2}\.\d{4}"

        ]

        for p in patterns:

            m = re.search(p, self.full_text)

            if m:
                return m.group()

        # Search only around DOB lines
        for i, line in enumerate(self.lines):

            l = line.lower()

            score = max(

                fuzz.ratio(l, "dob"),

                fuzz.ratio(l, "date of birth"),

                fuzz.ratio(l, "date"),

                fuzz.ratio(l, "birth"),

                fuzz.ratio(l, "pebob")

            )

            if score < 40:
                continue

            nearby = line

            if i + 1 < len(self.lines):
                nearby += " " + self.lines[i + 1]

            digits = re.sub(r"\D", "", nearby)

            # OCR like 267011979
            if len(digits) == 9:
                digits = digits[:2] + digits[3:]

            if len(digits) != 8:
                continue

            dd = int(digits[:2])
            mm = int(digits[2:4])
            yy = int(digits[4:])

            if (
                1 <= dd <= 31
                and
                1 <= mm <= 12
                and
                1900 <= yy <= 2100
            ):

                return f"{digits[:2]}/{digits[2:4]}/{digits[4:]}"

        return None

    ########################################################

    

    def extract_name(self):

        ignore = [

            "government",
            "india",
            "govemment",
            "govemmen",
            "govt",
            "aadhaar",
            "dob",
            "birth",
            "date",
            "male",
            "female",
            "vid"

        ]

        candidates = []

        for line in self.lines:

            # Remove punctuation while keeping letters and spaces
            text = re.sub(r"[^A-Za-z ]", " ", line)

            # Remove extra spaces
            text = " ".join(text.split())

            if len(text) < 4:
                continue

            lower = text.lower()

            if any(word in lower for word in ignore):
                continue

            # Ignore lines containing digits
            if re.search(r"\d", text):
                continue

            words = text.split()

            # Aadhaar names usually have 2–5 words
            if len(words) < 2 or len(words) > 5:
                continue

            candidates.append(text)

        if candidates:

            # Choose the longest candidate
            candidates.sort(key=len, reverse=True)

            return candidates[0]

        return None

    ########################################################

    def confidence(self, result):

        score = 0

        if result["name"]:
            score += 25

        if result["dob"]:
            score += 25

        if result["gender"]:
            score += 25

        if result["aadhaar_number"]:
            score += 25

        return score

    ########################################################

    def parse(self):

        result = {

            "status": "PASS",

            "name": self.extract_name(),

            "dob": self.extract_dob(),

            "gender": self.extract_gender(),

            "aadhaar_number": self.extract_aadhaar()

        }

        result["confidence"] = self.confidence(result)

        return result

    ########################################################

    def print_ocr(self):

        print("\nOCR LINES\n")

        for i, line in enumerate(self.lines):

            print(i + 1, line)

        print()