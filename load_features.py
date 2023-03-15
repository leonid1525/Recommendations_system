import pandas as pd

from database import engine

# Общая функция загрузки и подготовки данных для рекомендательной системы
def load_features():
    # функция принимает строку SQL-запроса, возвращает датафрейм
    def batch_load_sql(query: str) -> pd.DataFrame:

        CHUNKSIZE = 500  # chunk size

        conn = engine.connect().execution_options(stream_results=True)
        chunks = []
        for chunk_dataframe in pd.read_sql(query, conn,
                                           chunksize=CHUNKSIZE):
            chunks.append(chunk_dataframe)
        conn.close()
        X = pd.concat(chunks, ignore_index=True)
        return X

    # Загружаем данные из базы данных
    merge_user = batch_load_sql('SELECT * FROM "LEONID_NORGELLO_USERS"')
    merge_post = batch_load_sql('SELECT * FROM "LEONID_NORGELLO_POSTS"')
    # Создаем список идентификаторов постов
    spisok_posts = merge_post["post_id"].tolist()
    # Удаляем лишние столбцы, образовавшиеся при загрузке
    merge_post = merge_post.drop(["index"], axis=1)
    merge_user = merge_user.drop(["index"], axis=1)

    return merge_user, merge_post, spisok_posts