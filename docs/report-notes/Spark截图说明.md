# 第二部分 Spark 大数据分析截图说明

> 本文档用于整理第二部分 Spark 大数据分析实验截图，并说明每张截图在报告中的作用。  
> 截图统一存放路径：`docs/screenshots2/`

---

# 一、Spark 镜像与 Spark Operator 部署

## 图 Spark-01 SWR 镜像上传成功

**截图文件：**

`Spark-01-SWR镜像上传成功.png`

**截图说明：**

该截图展示华为云 SWR 镜像仓库中已经成功上传 `pyspark` 和 `spark-operator` 镜像，为后续在 CCE 集群中部署 Spark Operator 和运行 Spark 作业提供镜像来源。

**报告图下注释：**

如图 Spark-01 所示，Spark 作业运行镜像 `pyspark:v9` 和 Spark Operator 控制器镜像 `spark-operator:2.5.0` 已成功上传至华为云 SWR 镜像仓库。

---

## 图 Spark-02 Spark Operator 运行状态

**截图文件：**

`Spark-02-SparkOperator运行.png`

**截图说明：**

该截图展示 `spark-operator` 命名空间下 controller 和 webhook Pod 均处于 Running 状态，说明 Spark Operator 已成功部署。

**报告图下注释：**

如图 Spark-02 所示，Spark Operator 的 controller 和 webhook Pod 均处于 Running 状态，说明 Spark Operator 已成功部署到 CCE 集群中，可以用于提交和管理 SparkApplication 作业。

---

## 图 Spark-03 Spark 作业镜像上传成功

**截图文件：**

`Spark-03-douban-spark镜像上传成功.png`

**截图说明：**

该截图展示 `douban-spark` 镜像已经成功上传到 SWR。该镜像中包含豆瓣电影分析脚本和 `douban_movies.csv` 数据集文件。

**报告图下注释：**

如图 Spark-03 所示，`douban-spark:v1` 镜像已成功上传到华为云 SWR 镜像仓库，该镜像包含豆瓣电影数据分析脚本和数据集文件，可用于后续 SparkApplication 作业运行。

---

# 二、SparkApplication 作业运行

## 图 Spark-04 SparkApplication 运行完成

**截图文件：**

`Spark-04-SparkApplication运行完成.png`

**截图说明：**

该截图展示 SparkApplication `douban-movies-analysis` 状态为 COMPLETED，Driver Pod 状态为 Completed，说明 Spark 作业已成功运行完成。

**报告图下注释：**

如图 Spark-04 所示，提交 `douban-movies-analysis` SparkApplication 后，作业状态为 COMPLETED，Driver Pod 状态为 Completed，说明基于 Spark Operator 的豆瓣电影数据分析任务已成功在 CCE 集群中运行完成。

---

# 三、Spark 数据读取与清洗结果

## 图 Spark-05 数据 Schema 和前 5 行

**截图文件：**

`Spark-05-数据Schema和前5行.png`

**截图说明：**

该截图展示 Spark 读取 `douban_movies.csv` 后的数据字段结构和前 5 行电影数据。字段包括 `movie_id`、`title`、`year`、`rating_score`、`rating_count`、`genres`、`countries`、`directors` 等。

**报告图下注释：**

如图 Spark-05 所示，Spark 成功读取豆瓣电影数据集，并输出了数据 Schema 和前 5 行样例数据，说明数据集能够被 Spark 正常加载和解析。

---

## 图 Spark-06 缺失值统计和数据清洗

**截图文件：**

`Spark-06-缺失值统计和数据清洗.png`

**截图说明：**

该截图展示原始数据量、各字段缺失值数量和数据清洗结果。原始数据共有 67132 行、11 列，清洗后剩余 56886 条有效数据，删除异常或缺失数据 10246 条。

**报告图下注释：**

如图 Spark-06 所示，原始数据集共有 67132 条记录和 11 个字段。经过缺失值过滤、字段类型转换和异常值处理后，保留 56886 条有效数据，删除异常或缺失数据 10246 条。

---

# 四、Spark 统计分析结果

## 图 Spark-07 高评分电影 Top10

**截图文件：**

`Spark-07-高评分电影Top10.png`

**截图说明：**

该截图展示评分人数不少于 10000 的高评分电影 Top10。结果中《肖申克的救赎》评分为 9.7，排名第一；《霸王别姬》《控方证人》《阿甘正传》《美丽人生》等电影也位于榜单前列。

**报告图下注释：**

如图 Spark-07 所示，在高评分电影 Top10 中，《肖申克的救赎》评分最高，为 9.7；《霸王别姬》《控方证人》《阿甘正传》等电影也具有较高评分和较多评分人数。

---

## 图 Spark-08 电影类型和国家地区统计

**截图文件：**

`Spark-08-电影类型和国家地区统计.png`

**截图说明：**

该截图展示电影类型数量 Top10 和国家或地区电影数量 Top10。剧情类电影数量最多，共 28090 部；国家或地区统计中，美国电影数量最多，共 16476 部。

**报告图下注释：**

如图 Spark-08 所示，电影类型统计中剧情类电影数量最多，其次为喜剧、动作、爱情等类型；国家或地区统计中，美国电影数量最多，中国大陆、日本、法国、英国等地区也占比较高。

---

## 图 Spark-09 年份电影数量 Top15

**截图文件：**

`Spark-09-年份电影数量Top15.png`

**截图说明：**

该截图展示不同年份电影数量 Top15。结果显示 2017 年电影数量最多，共 2968 部，其次是 2016 年、2018 年和 2015 年。

**报告图下注释：**

如图 Spark-09 所示，2017 年电影数量最多，共 2968 部；2016 年、2018 年、2015 年等年份电影数量也较多，说明数据集中近十年电影记录占比较高。

---

## 图 Spark-10 评分人数最高电影 Top10

**截图文件：**

`Spark-10-评分人数最高电影Top10.png`

**截图说明：**

该截图展示评分人数最高的电影 Top10。《肖申克的救赎》评分人数为 1992071，位居第一；《这个杀手不太冷》《千与千寻》《阿甘正传》《霸王别姬》等影片用户关注度较高。

**报告图下注释：**

如图 Spark-10 所示，评分人数最高的电影为《肖申克的救赎》，评分人数达到 1992071；《这个杀手不太冷》《千与千寻》《阿甘正传》等电影也具有较高用户关注度。

---

## 图 Spark-11 Spark SQL 综合分析和运行时间

**截图文件：**

`Spark-11-SparkSQL综合分析和运行时间.png`

**截图说明：**

该截图展示 Spark SQL 综合分析结果和 Spark 作业运行时间。Spark 作业总耗时为 53.967 秒，说明 Spark 能够在 Kubernetes 集群环境中完成豆瓣电影数据的读取、清洗和统计分析。

**报告图下注释：**

如图 Spark-11 所示，Spark SQL 综合分析统计了不同国家或地区组合下的电影数量、平均评分和最高评分。最终 Spark 作业总耗时为 53.967 秒，说明 Spark 能够在 CCE 集群中完成结构化电影数据分析任务。

---

# 五、第二部分实验总结

本实验基于 Spark Operator 在华为云 CCE 集群中提交 PySpark 作业，对豆瓣电影数据集进行了读取、字段解析、缺失值统计、数据清洗和多维度统计分析。实验结果表明，Spark 能够较好地处理结构化 CSV 数据，并支持通过 Spark SQL 完成电影评分、类型、国家地区、年份趋势等统计分析任务。通过本实验，验证了 Spark Operator 在 Kubernetes 集群中管理 Spark 作业的可行性。
