CREATE TABLE logs
(
    name CHAR(22),
    hashed_contents CHAR(64)
    PRIMARY KEY (name)
);
--
CREATE TABLE chat
(
    log_hash CHAR(64),
    stamp TIMESTAMP,
    line_num INTEGER,
    chat_type VARCHAR(6),
    uid INTEGER, 
    username VARCHAR(20),
    info TEXT,
    CHECK (chat_type = 'PUBLIC' OR 
            chat_type = 'GUILD' OR
            chat_type = 'REPLY' OR
            chat_type = 'PARTY'),
    PRIMARY KEY (stamp, uid, line_num),
    FOREIGN KEY (log_hash)
        REFERENCES logs (hashed_contents)
);
