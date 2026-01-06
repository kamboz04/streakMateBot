#for db operations means table create etc

from app.db.connection import get_connection

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS streakTB (
            user_id BIGINT PRIMARY KEY,
            streak INT DEFAULT 0,
            last_increment_date DATE NOT NULL,
            start_date DATE NOT NULL
        );
    """)

    conn.commit()

    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS statsTB (
            user_id BIGINT PRIMARY KEY,
           attempt INT DEFAULT 1,
           rank varchar(50),
           max_streak INT NOT NULL,
                
           FOREIGN KEY (user_id)
           REFERENCES streakTB(user_id)
        );
    """)


    cur.execute("""
        CREATE TABLE IF NOT EXISTS ranksTB (
            rank_name VARCHAR(100),
           min INT,
           max INT
        );
    """)

    conn.commit()

    cur.close()
    conn.close()
