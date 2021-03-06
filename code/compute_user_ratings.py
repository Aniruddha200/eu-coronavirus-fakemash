import random
import os 
from entry_creation_schemes import create_connection


def get_expert_transaction_id(conn, tr_id):
    """
    get expert attributes with given id
    """
    cur = conn.cursor()
    cur.execute('''SELECT given_score FROM transaction_experts WHERE id=?''', (tr_id,))
    result = cur.fetchall()
    return result


def get_users(conn):
    """
    get users
    """
    cur = conn.cursor()
    cur.execute('''SELECT id FROM users''')
    result = cur.fetchall()
    return result


def update_user_rating(conn, user):
    """
    update user rating
    """
    sql = ''' UPDATE users
              SET rating = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()


def main_compute_user_rating():
    """
    Creating user's output and comparing it to expert_response 
    :return: 
    """
    database_path = os.path.join(os.getcwd(), "data.db")

    # create a code connection
    conn = create_connection(database_path)
    with conn:
        users = get_users(conn)
        discount_factor_experience = 0.7
        for i, user in enumerate(users):
            curr_diff = 0.0
            beg = 1.0 
            end = 10.0 

            num_transactions = 100 
            for _ in range(num_transactions):
                tr_id = random.randint(1, 100)
                user_response = random.uniform(beg, end)
                expert_response = get_expert_transaction_id(conn, tr_id)[0][0]
                curr_diff += abs(expert_response - user_response)

            total_score = 9 * num_transactions
            user_rating = discount_factor_experience * (1 - (curr_diff/total_score))
            update_user_rating(conn, (round(user_rating, 3), user[0]))


if __name__ == '__main__':
    main_compute_user_rating()

