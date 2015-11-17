CREATE TABLE logs
(
    name CHAR(22),
    PRIMARY KEY (name)
);

CREATE TABLE chat
(
    log_name CHAR(22),
    time TIMESTAMP,
    line_num INTEGER,
    chat_type VARCHAR(6),
    uid INTEGER, 
    user VARCHAR(15),
    info TEXT,
    CHECK (chat_type = 'PUBLIC' OR 
            chat_type = 'GUILD' OR
            chat_type = 'REPLY' OR
            chat_type = 'PARTY'),
    PRIMARY KEY (time, uid),
    FOREIGN KEY (log_name)
        REFERENCES logs (name)
);