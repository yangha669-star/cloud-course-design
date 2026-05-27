from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, avg, desc, split, explode, trim,
    when, isnan, year as spark_year
)
from pyspark.sql.types import IntegerType, DoubleType
import time
import os

def print_title(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)

def main():
    start_time = time.time()

    spark = SparkSession.builder \
        .appName("DoubanMoviesSparkAnalysis") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    data_path = "/opt/spark/work-dir/data/douban_movies.csv"

    print_title("Spark 豆瓣电影数据分析开始")
    print("数据文件路径:", data_path)

    print_title("1. 读取 CSV 数据")
    df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .option("multiLine", "true") \
        .option("quote", '"') \
        .option("escape", '"') \
        .csv(data_path)

    print_title("2. 数据 Schema")
    df.printSchema()

    print_title("3. 前 5 行数据")
    df.select(
        "movie_id", "title", "year", "rating_score",
        "rating_count", "genres", "countries", "directors"
    ).show(5, truncate=False)

    print_title("4. 原始数据量")
    raw_count = df.count()
    print("原始数据总行数:", raw_count)
    print("原始数据总列数:", len(df.columns))

    print_title("5. 缺失值统计")
    missing_exprs = []
    for c in df.columns:
        missing_exprs.append(
            count(when(col(c).isNull() | (trim(col(c).cast("string")) == ""), c)).alias(c)
        )
    df.select(missing_exprs).show(truncate=False)

    print_title("6. 数据清洗")
    clean_df = df.select(
        col("movie_id").cast(IntegerType()).alias("movie_id"),
        col("title"),
        col("original_title"),
        col("year").cast(IntegerType()).alias("year"),
        col("rating_score").cast(DoubleType()).alias("rating_score"),
        col("rating_count").cast(IntegerType()).alias("rating_count"),
        col("genres"),
        col("countries"),
        col("directors"),
        col("collect_count").cast(IntegerType()).alias("collect_count"),
        col("summary")
    ).filter(
        col("title").isNotNull() &
        col("year").isNotNull() &
        col("rating_score").isNotNull() &
        col("rating_count").isNotNull() &
        col("genres").isNotNull() &
        col("countries").isNotNull()
    ).filter(
        (col("rating_score") >= 0) &
        (col("rating_score") <= 10) &
        (col("year") >= 1900) &
        (col("year") <= 2026)
    )

    clean_count = clean_df.count()
    print("清洗前数据量:", raw_count)
    print("清洗后数据量:", clean_count)
    print("删除异常或缺失数据量:", raw_count - clean_count)

    clean_df.createOrReplaceTempView("movies")

    print_title("7. 高评分电影 Top 10")
    spark.sql("""
        SELECT title, year, rating_score, rating_count, genres, countries
        FROM movies
        WHERE rating_count >= 10000
        ORDER BY rating_score DESC, rating_count DESC
        LIMIT 10
    """).show(10, truncate=False)

    print_title("8. 电影类型数量 Top 10")
    genre_df = clean_df.withColumn("genre", explode(split(col("genres"), "/"))) \
        .withColumn("genre", trim(col("genre"))) \
        .filter(col("genre") != "")

    genre_df.groupBy("genre") \
        .count() \
        .orderBy(desc("count")) \
        .show(10, truncate=False)

    print_title("9. 国家或地区电影数量 Top 10")
    country_df = clean_df.withColumn("country", explode(split(col("countries"), "/"))) \
        .withColumn("country", trim(col("country"))) \
        .filter(col("country") != "")

    country_df.groupBy("country") \
        .count() \
        .orderBy(desc("count")) \
        .show(10, truncate=False)

    print_title("10. 年份电影数量 Top 15")
    clean_df.groupBy("year") \
        .count() \
        .orderBy(desc("count")) \
        .show(15, truncate=False)

    print_title("11. 各类型平均评分 Top 10")
    genre_df.groupBy("genre") \
        .agg(
            count("*").alias("movie_count"),
            avg("rating_score").alias("avg_rating")
        ) \
        .filter(col("movie_count") >= 100) \
        .orderBy(desc("avg_rating")) \
        .show(10, truncate=False)

    print_title("12. 评分人数最高电影 Top 10")
    clean_df.select("title", "year", "rating_score", "rating_count", "genres") \
        .orderBy(desc("rating_count")) \
        .show(10, truncate=False)

    print_title("13. Spark SQL 综合分析")
    spark.sql("""
        SELECT 
            countries,
            COUNT(*) AS movie_count,
            ROUND(AVG(rating_score), 2) AS avg_rating,
            MAX(rating_score) AS max_rating
        FROM movies
        GROUP BY countries
        HAVING movie_count >= 50
        ORDER BY avg_rating DESC
        LIMIT 10
    """).show(10, truncate=False)

    end_time = time.time()
    spark_time = end_time - start_time

    print_title("14. Spark 运行时间")
    print("Spark 分析总耗时: %.3f 秒" % spark_time)

    print_title("15. 实验结论")
    print("本次实验使用 PySpark 对豆瓣电影数据集进行读取、清洗、统计和 SQL 分析。")
    print("实验完成了电影评分、类型、国家地区、年份趋势等多个维度的统计。")
    print("结果说明 Spark 能够以分布式方式处理结构化 CSV 数据，并适合进行大规模数据分析任务。")

    spark.stop()

if __name__ == "__main__":
    main()
