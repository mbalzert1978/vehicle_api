BEGIN;



CREATE TABLE alembic_version (

    version_num VARCHAR(32) NOT NULL, 

    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)

);



-- Running upgrade  -> e122c6fc87d4



CREATE TABLE vehicle (

    id SERIAL NOT NULL, 

    name VARCHAR NOT NULL, 

    year_of_manufacture INTEGER NOT NULL, 

    body JSON NOT NULL, 

    ready_to_drive BOOLEAN NOT NULL, 

    PRIMARY KEY (id)

);



INSERT INTO alembic_version (version_num) VALUES ('e122c6fc87d4') RETURNING alembic_version.version_num;



COMMIT;