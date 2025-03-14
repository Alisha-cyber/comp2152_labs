# Lab 10 - Create functions to automate our query execution and fetching

# Prepare and execute the query
def query_executor(cursor, query_name):
    print("---")
    print(f"Query: {query_name}")

    # The `execute` method runs the query, generating a result set
    cursor.execute(query_name)
    return cursor

# Fetch from a pre-executed query
def query_responder(cursor, fetch_type, fetch_amount=3):
    all_rows = []

    # The `fetchall` method causes the cursor to traverse the result set,
    # returning the records it finds into the `all_rows` variable
    if fetch_type == "fetchall":
        all_rows = cursor.fetchall()
        for row in all_rows:
            print(row)

    # The `fetchone` method only traverses one row through the result set,
    # so if there are more rows in the result set, they won't get returned by this
    elif fetch_type == "fetchone":
        all_rows = cursor.fetchone()
        print(all_rows)

    # The `fetchmany` method traverses `fetch_amount` rows,
    # returning the records it finds into the `all_rows` variable
    elif fetch_type == "fetchmany":
        all_rows = cursor.fetchmany(fetch_amount)
        for row in all_rows:
            print(row)

    else:
        print("Invalid fetch type")

    return all_rows

