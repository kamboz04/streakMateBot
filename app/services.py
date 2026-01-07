#streak logicfrom datetime import date
from datetime import date
from app.db.connection import get_connection


# Daily streak Updation logic
def increment_daily():
    today = date.today()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
         UPDATE StreakTB
        SET
        streak = streak + (CURRENT_DATE - last_increment_date),
        last_increment_date = CURRENT_DATE
        WHERE last_increment_date < CURRENT_DATE;
        """)

        
        cur.execute("""
        UPDATE statsTB
        SET max_streak = streakTB.streak
        FROM streakTB
        WHERE statsTB.user_id = streakTB.user_id
        AND streakTB.streak > statsTB.max_streak;
        """)


        cur.execute("""
        UPDATE statsTB
        SET rank = ranksTB.rank_name
        FROM streakTB
        JOIN ranksTB
        ON streakTB.streak BETWEEN ranksTB.min AND ranksTB.max
        WHERE statsTB.user_id = streakTB.user_id;
        """)


        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e
    finally:
    
        cur.close()
        conn.close()

    



#start a streak logic means here we will insert new user to DB

def addUser(userid):

    today = date.today()
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
        INSERT INTO StreakTB (user_id, streak, last_increment_date,start_date)
        VALUES (%s, 0, %s,%s)
        ON CONFLICT (user_id) DO NOTHING;
        """, (userid, today,today))


        cur.execute("""
        INSERT INTO statsTB (user_id, attempt, rank,max_streak)
        VALUES (%s, 1, %s,%s)
        ON CONFLICT (user_id) DO NOTHING;
        """, (userid,"begineer",0))

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
    
        cur.close()
        conn.close()

#to check if user exists or not

def user_exists(userId):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT 1 FROM StatsTB WHERE user_id = %s;",
            (userId,)
        )
        return cur.fetchone() is not None
    finally:
        cur.close()
        conn.close()


def getStreak(userid):

    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
        SELECT streak FROM streakTB WHERE user_id = %s;
        """, (userid,))

        row = cur.fetchone()
        return row[0] 
    except Exception as e:
        conn.rollback()
        raise e
    finally:
    
        cur.close()
        conn.close()


#reset the streak - relapse

def resetStreak(userid):

    today = date.today()
    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
        UPDATE streakTB
        SET streak = 0,
            last_increment_date = %s,start_date = %s
            WHERE user_id = %s;
        """, (today,today,userid))
        
        cur.execute("""
        UPDATE statsTB
        SET attempt = attempt + 1
        WHERE user_id = %s;
        """,(userid,))

        conn.commit()
    except Exception as e:
         conn.rollback()
         raise e
    finally:
    
        cur.close()
        conn.close()



# Set custom streak
def customSet(userid,userStreak):

    today = date.today()
    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
        UPDATE streakTB
        SET streak = %s,
            last_increment_date = %s,start_date = %s
            WHERE user_id = %s;
        """, (userStreak,today,today,userid))
        
        cur.execute("""
        UPDATE statsTB
        SET max_streak = %s
        WHERE user_id = %s AND max_streak < %s;
        """,(userStreak,userid,userStreak))

        conn.commit()
    except Exception as e:
         conn.rollback()
         raise e
    finally:
    
        cur.close()
        conn.close()



#get stats of user 
def getStats(userid):

    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
        SELECT * FROM statsTB WHERE user_id = %s;
        """, (userid,))

        row = cur.fetchone()
        return row
    except Exception as e:
        conn.rollback()
        raise e
    finally:
    
        cur.close()
        conn.close()