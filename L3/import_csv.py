import pandas as pd
import sqlite3

# 读取 CSV 文件
df = pd.read_csv("campaign_performance_4weeks.csv")

# 连接 SQLite 数据库(不存在则自动创建)
conn = sqlite3.connect("marketing.db")

# 将数据写入名为 campaign_performance 的表
df.to_sql("campaign_performance", conn, if_exists="replace", index=False)

conn.close()
print("导入完成:marketing.db / 表 campaign_performance")
