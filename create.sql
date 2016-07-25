CREATE TABLE logs
(
    name VARCHAR,
    hashed_contents CHAR(64),
    PRIMARY KEY (hashed_contents)
);
--
CREATE TABLE chat
(
    log_hash  CHAR(64),
    line_hash CHAR(64),
    stamp     TIMESTAMP,
    line_num  INTEGER,
    chat_type VARCHAR(6),
    uid       INTEGER, 
    username  VARCHAR(20),
    info TEXT,
    occur INTEGER,
    CHECK (chat_type = 'PUBLIC' OR 
            chat_type = 'GUILD' OR
            chat_type = 'REPLY' OR
            chat_type = 'PARTY'),
    PRIMARY KEY (line_hash),
    FOREIGN KEY (log_hash)
        REFERENCES logs (hashed_contents)
        ON UPDATE CASCADE
);
