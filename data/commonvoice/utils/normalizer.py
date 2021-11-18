import string
from tokenizers import normalizers
from tokenizers.normalizers import BertNormalizer, NFKC, Strip

class CommonVoiceNormalizer():
    def __init__(self) -> None:
        self.normalizer = normalizers.Sequence([BertNormalizer(clean_text=True, handle_chinese_chars=True,
                                                  strip_accents=False, lowercase=True), NFKC(), Strip()])
        self.discard_by_characters = ['°', 'þ', '≡', '东', '泽', '毛', 'μ', '临', '道', '孙', 'к', 'ш', 'ч', 'в', 'м', 'и', 'ф', 'а', 'カ', 'ན', '無', 'ѹ', 'о', '辶', '尣', 'р', 'е', 'с', '支', 'œ', '生', 'נ', 'ב', 'א', 'ע', 'ש']
        self.trans_map = {
                            'ś': 's',
                            'ě': 'e',
                            'ý': 'y',
                            'ə': 'e',
                            'ę': 'e',
                            'â': 'a',
                            '‹': '',
                            '›': '',
                            'ă': 'a',
                            'ő': 'o',
                            'ž': 'z',
                            '乡': '',
                            '幺': '',
                            'ñ': 'n',
                            '»': '',
                            '«': '',
                            'ọ': 'o',
                            'ứ': 'u',
                            'đ': 'd',
                            'ê': 'e',
                            '→': '',
                            'ã': 'a',
                            'ø': 'o',
                            'ț': 't',
                            'ș': 's',
                            'ź': 'z',
                            'á': 'a',
                            'ř': 'r',
                            'ð': 'd',
                            'ū': 'u',
                            'ʿ': '',
                            'ā': 'a',
                            'ł': 'l',
                            'å': 'a',
                            'ë': 'e',
                            'ú': 'u',
                            '·': '',
                            'ş': 's',
                            'č': 'c',
                            'æ': 'a',
                            'ò': 'o',
                            '”': '',
                            'ć': 'c',
                            '‚': '',
                            'ğ': 'g',
                            'ı': 'i',
                            '̇': '', 
                            '‘': '',
                            'ç': 'c',
                            '’': '',
                            'ō': 'o',
                            'ó': 'o',
                            'à': 'a',
                            'é': 'e',
                            '–': '',
                            'í': 'i',
                            'ï': 'i',
                            'ń': 'n',
                            'ʻ': '',
                            '“': '',
                            'š': 's',
                            '„': '',
                            '′': '',
                            'ṣ': 's',
                            'ằ': 'a',
                            'ạ': 'a',
                            'ễ': 'e',
                            'ộ': 'o',
                            'ṭ': 't',
                            'ġ': 'g',
                            'ù': 'u',
                            '⟩': '',
                            '−': ' ',
                            '¡': '',
                            '‟': '',
                            'ì': '',
                            'ả': 'a',
                            'ṣ': 's',
                            '‐': ' ',
                            'è': 'e',
                            'ắ': 'a',
                            'û': 'u',
                            'ụ': 'u',
                            'ħ': 'h',
                            'ʾ': '',
                            'ŏ': '',
                            '̆': '',
                            'õ': 'o',
                            'ņ': 'n',
                            'ḫ': 'h',
                            'ť': 't',
                            'ḫ': 'h',
                            'ť': 't',
                            'ů': 'u',
                            '比': '',
                            'ơ': 'o',
                            'î': 'i',
                            'ė': 'e',
                            '臣': '',
                            '་': '',
                            '́': '',
                            'ǐ': 'i',
                            'ż': 'z',
                            'ī': 'i',
                            'ď': 'd',
                            'ô': 'o',
                            'ą': 'a',
                            '—': '',
                            '⟨': '',
                            'ē': 'e',
                            'ṟ': 'r',
                            'ň': 'n',
                            'ế': 'e',
                            'ồ': 'o',
                            'ǔ': 'u',
                            'ệ': 'e',
                            'ß': 'ss'
                        }

    def normalize(self, sentence):
        sentence = self.normalizer.normalize_str(sentence)
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        sentence = ''.join(self.trans_map.get(ch, ch) for ch in sentence)
        sentence = sentence.lower()
        return sentence

    def get_trans_map(self):
        return self.trans_map

    def get_discard_chars(self):
        return self.discard_by_characters

    def keep_trans_characters(self, characters):
        ''' Pops out characters from the translation map, 
            ideal to keep certain characters like ñ in Spanish or
            ß in German'''

        for char in characters:
            self.trans_map.pop(char)