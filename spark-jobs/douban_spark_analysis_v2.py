from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, when, trim, lit, round as spark_round,
    avg, stddev, min as spark_min, max as spark_max,
    desc, split, explode, row_number
)
from pyspark.sql.types import IntegerType, DoubleType
from pyspark.sql.window import Window
import time

def print_title(title):
    print("\n" + "=" * 90)
    print(title)
    print("=" * 90)

def main():
    total_start = time.time()

    spark = SparkSession.builder \
        .appName("DoubanMoviesSparkAnalysisV2") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    data_path = "/opt/spark/work-dir/data/douban_movies.csv"

    print_title("A-1-1 读取豆瓣电影 CSV 数据")
    df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .option("multiLine", "true") \
        .option("quote", '"') \
        .option("escape", '"') \
        .csv(data_path)

    print_title("A-1-2 数据 Schema")
    df.printSchema()

    print_title("A-1-3 前 5 行数据")
    df.select(
        "movie_id", "title", "year", "rating_score",
        "rating_count", "genres", "countries", "directors"
    ).show(5, truncate=False)

    raw_count = df.count()

    print_title("A-1-4 原始数据规模")
    print("原始数据总行数:", raw_count)
    print("原始数据总列数:", len(df.columns))

    print_title("A-1-5 各字段缺失值数量与缺失值比例")
    missing_rows = []
    for c in df.columns:
        missing_count = df.filter(col(c).isNull() | (trim(col(c).cast("string")) == "")).count()
        missing_ratio = missing_count / raw_count if raw_count > 0 else 0
        missing_rows.append((c, missing_count, round(missing_ratio, 4)))

    missing_df = spark.createDataFrame(
        missing_rows,
        ["field_name", "missing_count", "missing_ratio"]
    )
    missing_df.show(50, truncate=False)

    print_title("A-1-6 不同字段采用不同清洗策略")
    print("清洗策略 1：year、rating_score、genres、countries 是分析关键字段，缺失会影响统计结果，因此采用 dropna / filter 删除。")
    print("清洗策略 2：directors 和 summary 是描述性字段，缺失不影响核心统计，因此采用 fillna 填充为“未知导演”和“暂无简介”。")

    typed_df = df.select(
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
    )

    filled_df = typed_df.fillna({
        "directors": "未知导演",
        "summary": "暂无简介",
        "original_title": "未知原名"
    })

    clean_df = filled_df.filter(
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

    print_title("A-1-7 数值字段基本统计信息 mean/std/min/max")
    clean_df.select(
        "year", "rating_score", "rating_count", "collect_count"
    ).describe().show(truncate=False)

    clean_df.createOrReplaceTempView("movies")

    print_title("A-2-1 GROUP BY 聚合：电影类型数量 Top 10")
    genre_df = clean_df.withColumn("genre", explode(split(col("genres"), "/"))) \
        .withColumn("genre", trim(col("genre"))) \
        .filter(col("genre") != "")

    genre_df.groupBy("genre") \
        .count() \
        .orderBy(desc("count")) \
        .show(10, truncate=False)

    print_title("A-2-2 ORDER BY Top-N：高评分电影 Top 10")
    spark.sql("""
        SELECT title, year, rating_score, rating_count, genres, countries
        FROM movies
        WHERE rating_count >= 10000
        ORDER BY rating_score DESC, rating_count DESC
        LIMIT 10
    """).show(10, truncate=False)

    print_title("A-2-3 时间维度趋势分析：年份电影数量 Top 15")
    clean_df.groupBy("year") \
        .count() \
        .orderBy(desc("count")) \
        .show(15, truncate=False)

    print_title("A-2-4 窗口函数：每年评分最高电影 Top 3")
    window_spec = Window.partitionBy("year").orderBy(desc("rating_score"), desc("rating_count"))

    clean_df.withColumn("rank_in_year", row_number().over(window_spec)) \
        .filter(col("rank_in_year") <= 3) \
        .select("year", "rank_in_year", "title", "rating_score", "rating_count", "genres") \
        .orderBy(desc("year"), "rank_in_year") \
        .show(30, truncate=False)

    print_title("A-2-5 国家或地区电影数量 Top 10")
    country_df = clean_df.withColumn("country", explode(split(col("countries"), "/"))) \
        .withColumn("country", trim(col("country"))) \
        .filter(col("country") != "")

    country_df.groupBy("country") \
        .count() \
        .orderBy(desc("count")) \
        .show(10, truncate=False)

    print_title("A-2-6 Spark SQL 综合分析")
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

    print_title("A-3-1 性能对比查询：按类型统计电影数量 Top 10")

    spark_perf_start = time.time()
    spark_perf_df = genre_df.groupBy("genre") \
        .count() \
        .orderBy(desc("count")) \
        .limit(10)
    spark_perf_df.show(10, truncate=False)
    spark_perf_time = time.time() - spark_perf_start

    print_title("A-3-2 Pandas 单机性能测试")
    try:
        import pandas as pd

        pandas_start = time.time()
        pdf = pd.read_csv(data_path)
        pdf = pdf.dropna(subset=["genres"])
        genre_series = pdf["genres"].astype(str).str.split("/").explode().str.strip()
        pandas_result = genre_series.value_counts().head(10)
        pandas_time = time.time() - pandas_start

        print("Pandas 类型统计 Top 10:")
        print(pandas_result)
        print("Pandas 查询耗时: %.3f 秒" % pandas_time)
    except Exception as e:
        pandas_time = -1
        print("Pandas 测试失败:", str(e))

    print_title("A-3-3 PySpark 性能测试结果")
    print("PySpark 查询耗时: %.3f 秒" % spark_perf_time)
    print("当前 SparkApplication executor 实例数请参考 YAML 中 executor.instances 字段。")
    print("将本作业分别以 executor.instances=1 和 executor.instances=2 运行，即可得到 PySpark 单 executor 与双 executor 的耗时对比。")

    total_time = time.time() - total_start

    print_title("A-3-4 Amdahl 定律分析说明")
    print("根据 Amdahl 定律，程序总体加速比受限于无法并行化的串行部分。")
    print("本实验中，CSV 读取、任务调度、Executor 启动、网络通信、序列化与反序列化都会产生额外开销。")
    print("因此 executor 数量从 1 增加到 2 时，运行时间通常不会严格缩短为原来的一半。")
    print("当数据量较小或任务较轻时，调度和通信开销占比更高，加速比会更不明显。")

    print_title("实验总耗时")
    print("Spark 作业总耗时: %.3f 秒" % total_time)

    spark.stop()

if __name__ == "__main__":
    main()
