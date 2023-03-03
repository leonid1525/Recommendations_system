import pandas as pd

from database import engine


def load_features():
    def batch_load_sql(query: str) -> pd.DataFrame:  # the function accepts a SQL query string, returns a dataframe

        CHUNKSIZE = 500  # chunk size

        conn = engine.connect().execution_options(stream_results=True)
        chunks = []
        for chunk_dataframe in pd.read_sql(query, conn,
                                           chunksize=CHUNKSIZE):  # a string comes from the function, connection to the database, chunk size
            chunks.append(chunk_dataframe)
        conn.close()
        X = pd.concat(chunks, ignore_index=True)
        return X

    def loading_features(request:str) -> pd.DataFrame:
        return batch_load_sql(request)  # passed the request to the batch_load_sql function

    merge_user = loading_features('SELECT * FROM "LEONID_NORGELLO_USERS"')
    merge_post = loading_features('SELECT * FROM "LEONID_NORGELLO_POSTS"')
    spisok_posts = merge_post["post_id"].tolist()
    merge_post = merge_post.drop(["index"], axis=1)
    merge_user = merge_user.drop(["index"], axis=1)

    return merge_user, merge_post, spisok_posts