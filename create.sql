CREATE TABLE logs
(
    name CHAR(22),
    PRIMARY KEY (name)
);
--
CREATE TABLE chat
(
    log_name CHAR(22),
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
    FOREIGN KEY (log_name)
        REFERENCES logs (name)
);