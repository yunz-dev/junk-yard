from sqlalchemy.orm import Session
from . import models

DEFAULT_CARDS = [
    {"chinese": "你好", "pinyin": "nǐ hǎo", "english": "hello", "category": "Greetings"},
    {"chinese": "再见", "pinyin": "zài jiàn", "english": "goodbye", "category": "Greetings"},
    {"chinese": "谢谢", "pinyin": "xiè xie", "english": "thank you", "category": "Greetings"},
    {"chinese": "对不起", "pinyin": "duì bu qǐ", "english": "sorry", "category": "Greetings"},
    {"chinese": "请", "pinyin": "qǐng", "english": "please", "category": "Greetings"},

    {"chinese": "一", "pinyin": "yī", "english": "one", "category": "Numbers"},
    {"chinese": "二", "pinyin": "èr", "english": "two", "category": "Numbers"},
    {"chinese": "三", "pinyin": "sān", "english": "three", "category": "Numbers"},
    {"chinese": "四", "pinyin": "sì", "english": "four", "category": "Numbers"},
    {"chinese": "五", "pinyin": "wǔ", "english": "five", "category": "Numbers"},

    {"chinese": "米饭", "pinyin": "mǐ fàn", "english": "rice", "category": "Food"},
    {"chinese": "面条", "pinyin": "miàn tiáo", "english": "noodles", "category": "Food"},
    {"chinese": "茶", "pinyin": "chá", "english": "tea", "category": "Food"},
    {"chinese": "水", "pinyin": "shuǐ", "english": "water", "category": "Food"},
    {"chinese": "肉", "pinyin": "ròu", "english": "meat", "category": "Food"},

    {"chinese": "飞机", "pinyin": "fēi jī", "english": "airplane", "category": "Travel"},
    {"chinese": "火车", "pinyin": "huǒ chē", "english": "train", "category": "Travel"},
    {"chinese": "酒店", "pinyin": "jiǔ diàn", "english": "hotel", "category": "Travel"},
    {"chinese": "机场", "pinyin": "jī chǎng", "english": "airport", "category": "Travel"},
    {"chinese": "地图", "pinyin": "dì tú", "english": "map", "category": "Travel"},

    {"chinese": "我", "pinyin": "wǒ", "english": "I/me", "category": "HSK 1"},
    {"chinese": "你", "pinyin": "nǐ", "english": "you", "category": "HSK 1"},
    {"chinese": "他", "pinyin": "tā", "english": "he/him", "category": "HSK 1"},
    {"chinese": "她", "pinyin": "tā", "english": "she/her", "category": "HSK 1"},
    {"chinese": "们", "pinyin": "men", "english": "plural suffix", "category": "HSK 1"},

    {"chinese": "喜欢", "pinyin": "xǐ huān", "english": "to like", "category": "HSK 2"},
    {"chinese": "觉得", "pinyin": "jué de", "english": "to feel/think", "category": "HSK 2"},
    {"chinese": "应该", "pinyin": "yīng gāi", "english": "should", "category": "HSK 2"},
    {"chinese": "已经", "pinyin": "yǐ jīng", "english": "already", "category": "HSK 2"},
    {"chinese": "准备", "pinyin": "zhǔn bèi", "english": "to prepare", "category": "HSK 2"},

    {"chinese": "突然", "pinyin": "tū rán", "english": "suddenly", "category": "HSK 3"},
    {"chinese": "环境", "pinyin": "huán jìng", "english": "environment", "category": "HSK 3"},
    {"chinese": "态度", "pinyin": "tài dù", "english": "attitude", "category": "HSK 3"},
    {"chinese": "优点", "pinyin": "yōu diǎn", "english": "advantage", "category": "HSK 3"},
    {"chinese": "缺点", "pinyin": "quē diǎn", "english": "disadvantage", "category": "HSK 3"},

    {"chinese": "拒绝", "pinyin": "jù jué", "english": "to refuse", "category": "HSK 4"},
    {"chinese": "批评", "pinyin": "pī píng", "english": "to criticize", "category": "HSK 4"},
    {"chinese": "竞争", "pinyin": "jìng zhēng", "english": "to compete", "category": "HSK 4"},
    {"chinese": "灵活", "pinyin": "líng huó", "english": "flexible", "category": "HSK 4"},
    {"chinese": "效率", "pinyin": "xiào lǜ", "english": "efficiency", "category": "HSK 4"},

    {"chinese": "妥协", "pinyin": "tuǒ xié", "english": "to compromise", "category": "HSK 5"},
    {"chinese": "宽容", "pinyin": "kuān róng", "english": "tolerant", "category": "HSK 5"},
    {"chinese": "谨慎", "pinyin": "jǐn shèn", "english": "cautious", "category": "HSK 5"},
    {"chinese": "诚恳", "pinyin": "chéng kěn", "english": "sincere", "category": "HSK 5"},
    {"chinese": "虚伪", "pinyin": "xū wěi", "english": "hypocritical", "category": "HSK 5"},

    {"chinese": "诡辩", "pinyin": "guǐ biàn", "english": "sophistry", "category": "HSK 6"},
    {"chinese": "辩驳", "pinyin": "biàn bó", "english": "to refute", "category": "HSK 6"},
    {"chinese": "笃信", "pinyin": "dǔ xìn", "english": "to firmly believe", "category": "HSK 6"},
    {"chinese": "佯装", "pinyin": "yáng zhuāng", "english": "to feign", "category": "HSK 6"},
    {"chinese": "怂恿", "pinyin": "sǒng yǒng", "english": "to instigate", "category": "HSK 6"},
]

def seed_database(db: Session):
    existing = db.query(models.Flashcard).count()
    if existing == 0:
        for card_data in DEFAULT_CARDS:
            card = models.Flashcard(**card_data)
            db.add(card)
        db.commit()

def add_default_cards(db: Session):
    for card_data in DEFAULT_CARDS:
        card = models.Flashcard(**card_data)
        db.add(card)
    db.commit()
