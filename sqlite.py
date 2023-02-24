import sqlite3 as sq


async def db_start():
    global db, cur

    db = sq.connect('db/new.db')
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS profile(user_id INTEGER PRIMARY KEY, username VARCHAR(100))")
    cur.execute("CREATE TABLE IF NOT EXISTS vocab(id_word INTEGER PRIMARY KEY AUTOINCREMENT, word VARCHAR(300), "
                "translation VARCHAR(500), vocab_id INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS knowledge_base(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "user_id INTEGER, id_word INTEGER, is_knowing BOOLEAN);")
    cur.execute("CREATE TABLE IF NOT EXISTS vocabs(id INTEGER PRIMARY KEY AUTOINCREMENT, vocab_id TEXT, "
                "vocab_name VARCHAR(300), "
                "vocab_source VARCHAR(100));")
    db.commit()


async def create_profile(user_id, username):
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO profile VALUES(?, ?)", (user_id, username))
        db.commit()


async def add_word_to_vocab(word, translation, vocab_id):
    word_exists = cur.execute("SELECT 1 FROM vocab WHERE word == '{word}'".format(word=word)).fetchone()
    if not word_exists:
        cur.execute("INSERT INTO vocab(word, translation, vocab_id) VALUES(?, ?, ?)", (word, translation, vocab_id))
        db.commit()


async def get_random_word_from_vocab(user_id):
    id, word, translation, vocab_id = cur.execute(f"SELECT * FROM vocab "
                                                  f"WHERE id_word = ("
                                                  f"SELECT id_word FROM knowledge_base "
                                                  f"WHERE user_id=='{user_id}' AND is_knowing=0 "
                                                  f"ORDER BY RANDOM() LIMIT 1);").fetchone()
    return word, translation


async def get_word_translaition(word):
    return cur.execute("SELECT translation FROM vocab WHERE word == '{word}'".format(word=word)).fetchone()[0]


async def add_vocab(vocab_id, vocab_name, vocab_source):
    vocab_exists = cur.execute("SELECT 1 FROM vocabs WHERE vocab_id == '{key}'".format(key=vocab_id)).fetchone()
    if not vocab_exists:
        cur.execute("INSERT INTO vocabs(vocab_id, vocab_name, vocab_source) VALUES(?, ?, ?)", (vocab_id, vocab_name, vocab_source))
        db.commit()


async def add_word_to_knowledge_base(user_id, id_word, is_knowing):
    word_exists = cur.execute("SELECT id_word, user_id FROM knowledge_base WHERE user_id='{user_id}' AND id_word='{"
                              "id_word}'".format(user_id=user_id, id_word=id_word)).fetchone()
    if not word_exists:
        cur.execute("INSERT INTO knowledge_base(user_id, id_word, is_knowing) VALUES(?, ?, ?)", (user_id, id_word, is_knowing))
        db.commit()


async def get_word_id(word):
    return cur.execute("SELECT id_word FROM vocab WHERE word == '{word}'".format(word=word)).fetchone()[0]


async def upgrade_word_status(user_id, id_word):
    cur.execute(f"UPDATE knowledge_base SET is_knowing=1 WHERE user_id=='{user_id}' AND id_word='{id_word}';")
    db.commit()
