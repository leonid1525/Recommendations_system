import pandas as pd
from sqlalchemy import create_engine
print(1)
user = pd.read_csv('u-2 (1).csv', sep=";")
print(2)
post = pd.read_csv('p-2 (1).csv', sep=";")
print(3)
engine = create_engine("postgresql://1234:5678@postgres.lab.karpov.courses:6432/startml")
print(4)
user.to_sql("LEONID_NORGELLO_USERS", con=engine, if_exists="replace")
print(5)
post.to_sql("LEONID_NORGELLO_POSTS", con=engine, if_exists="replace")
print(6)