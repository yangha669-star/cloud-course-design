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

如图 Spark-03 所示，`douban-spark:v2` 镜像已成功上传到华为云 SWR 镜像仓库，该镜像包含豆瓣电影数据分析脚本和数据集文件，可用于后续 SparkApplication 作业运行。

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

该截图展示原始数据规模、各字段缺失值数量与缺失比例，以及不同字段采用的清洗策略。原始数据共有 67132 行、11 列。对于 `year`、`rating_score`、`genres`、`countries` 等关键字段，采用删除缺失值的策略；对于 `directors` 和 `summary` 等描述性字段，采用填充默认值的策略。清洗后剩余 56886 条有效数据，删除异常或缺失数据 10246 条。

**报告图下注释：**

如图 Spark-06 所示，原始数据集共有 67132 条记录和 11 个字段。实验统计了各字段缺失值数量与比例，并针对不同字段采用不同清洗策略，最终保留 56886 条有效数据。

---

## 图 Spark-07 字段基本统计信息

**截图文件：**

`Spark-07-字段基本统计信息.png`

**截图说明：**

该截图展示 `year`、`rating_score`、`rating_count`、`collect_count` 等数值字段的 count、mean、stddev、min、max 统计结果。

**报告图下注释：**

如图 Spark-07 所示，实验对数值字段进行了基本统计分析，包括均值、标准差、最小值和最大值等指标，为后续电影评分和热度分析提供数据基础。

---

# 四、Spark SQL 与 DataFrame 统计分析结果

## 图 Spark-08 电影类型和高评分电影 Top10

**截图文件：**

`Spark-08-电影类型和高评分电影Top10.png`

**截图说明：**

该截图展示了 GROUP BY 聚合和 ORDER BY Top-N 查询结果。电影类型统计中，剧情类电影数量最多；高评分电影 Top10 中，《肖申克的救赎》《霸王别姬》《控方证人》等电影位于前列。

**报告图下注释：**

如图 Spark-08 所示，电影类型统计结果显示剧情类电影数量最多；高评分电影 Top10 中，《肖申克的救赎》评分最高，说明该影片在数据集中具有较高评价和用户关注度。

---

## 图 Spark-09 年份趋势分析

**截图文件：**

`Spark-09-年份趋势分析.png`

**截图说明：**

该截图展示按照年份统计电影数量的时间维度趋势分析结果。结果显示 2017 年电影数量最多，其次为 2016 年、2018 年和 2015 年。

**报告图下注释：**

如图 Spark-09 所示，2017 年电影数量最多，2016 年、2018 年和 2015 年也具有较高数量，说明数据集中近年电影记录占比较高。

---

## 图 Spark-10 窗口函数每年高分电影 Top3

**截图文件：**

`Spark-10-窗口函数每年高分电影Top3.png`

**截图说明：**

该截图展示通过窗口函数 `row_number()` 对每一年电影按照评分和评分人数进行排序，并输出每年评分最高的前 3 部电影。该结果满足 Spark SQL 统计分析中窗口函数的要求。

**报告图下注释：**

如图 Spark-10 所示，实验使用窗口函数对不同年份的电影进行分组排序，筛选出每年评分最高的 Top3 电影，实现了按时间维度的分组排名分析。

---

# 五、性能对比与 Amdahl 分析

## 图 Spark-11-1 性能对比结果

**截图文件：**

`Spark-11-性能对比和Amdahl分析.png`

**截图说明：**

该截图展示同一类型统计查询在 Pandas 和 PySpark 中的执行耗时。Pandas 查询耗时约 0.597 秒，PySpark 查询耗时约 0.681 秒。

**报告图下注释：**

如图 Spark-11-1 所示，在本实验数据规模下，Pandas 单机查询耗时约 0.597 秒，PySpark 查询耗时约 0.681 秒。由于数据量相对不大，Spark 的任务调度和分布式执行开销会对性能结果产生影响。

---

## 图 Spark-11-2 Amdahl 定律分析

**截图文件：**

`Spark-11-性能对比和Amdahl分析（2）.png`

**截图说明：**

该截图展示 Amdahl 定律分析说明。实验指出 CSV 读取、任务调度、Executor 启动、网络通信、序列化与反序列化等因素都会限制并行加速效果。

**报告图下注释：**

如图 Spark-11-2 所示，根据 Amdahl 定律，程序总体加速比受限于无法并行化的串行部分。在本实验中，任务调度、网络通信、序列化与反序列化等开销会导致增加 Executor 数量后加速比无法达到理想线性增长。

---

# 六、第二部分实验总结

本实验基于 Spark Operator 在华为云 CCE 集群中提交 PySpark 作业，对豆瓣电影数据集进行了读取、字段解析、缺失值统计、数据清洗和多维度统计分析。实验结果表明，Spark 能够较好地处理结构化 CSV 数据，并支持通过 Spark SQL、DataFrame API 和窗口函数完成电影评分、类型、国家地区、年份趋势等统计分析任务。同时，通过 Pandas 与 PySpark 性能对比和 Amdahl 定律分析，说明分布式计算在实际运行中会受到任务调度、通信和序列化开销的影响。