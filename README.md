# 云计算技术课程设计

本仓库为《云计算技术》课程设计代码仓库，报告题目为“云计算平台搭建与 Spark 大数据分析”。实验分为两部分：第一部分在华为云 CCE 上部署 Flask 后端、Nginx 前端和 Redis 数据库组成的容器化 Web 应用；第二部分选择方向 A，使用 Spark Operator 在 Kubernetes 集群中运行 PySpark 作业，完成豆瓣电影数据集的数据清洗、统计分析和性能对比。

## 小组成员

| 姓名 | 学号 |
|---|---|
| 赵璟心 | 2023112556 |
| 娜菲沙 | 2023112429 |

## 项目结构

```text
cloud-course-design/
├── backend/                 # Flask 后端 API、Dockerfile、Python 依赖
├── frontend/                # Nginx 前端页面、Dockerfile、反向代理配置
├── spark-jobs/              # WordCount 示例和豆瓣电影 PySpark 分析脚本
├── docs/screenshots/        # 第一部分云计算平台搭建截图
├── docs/screenshots2/       # 第二部分 Spark 大数据分析截图
├── docker-compose.yml       # 本地 Docker Compose 联调配置
├── .gitignore               # 忽略报告、密钥、离线镜像包等文件
└── README.md                # 项目说明
```

## 第一部分：云计算平台搭建

第一部分主要完成 Flask + Redis + Nginx 应用的容器化部署与云端验证，涉及 Docker、SWR、CCE、ELB、PVC、ConfigMap 和 HPA 等内容。

主要实现内容如下：

1. 使用多阶段 Dockerfile 构建 Flask 后端镜像，并在 `requirements.txt` 中额外加入 `requests` 自选 Python 包。
2. 使用 Nginx 构建前端镜像，首页展示两名小组成员姓名与学号。
3. 使用 `docker-compose.yml` 在本地联调 backend、frontend 和 redis 三个服务。
4. 将前后端镜像推送到华为云 SWR。
5. 在 CCE 集群中部署后端、前端和 Redis，并通过 LoadBalancer Service 绑定 ELB 公网访问后端 `/api/ping`。
6. 使用 ConfigMap 和 Secret 分离非敏感配置与 Redis 密码配置。
7. 使用 PVC 挂载 Redis `/data` 目录，实现 Pod 重建后数据不丢失。
8. 使用 ConfigMap Volume 挂载 Nginx 配置文件，实现前端反向代理配置分离。
9. 使用 HPA 对后端 Deployment 进行弹性伸缩验证。

## 第二部分：方向 A Spark 大数据分析

第二部分使用 Spark Operator 在 Kubernetes 集群中提交 SparkApplication 作业。实验先运行 WordCount 示例作业验证 Spark on K8s 环境，再运行豆瓣电影数据分析作业。

主要实现内容如下：

1. 使用 Spark Operator 提交 WordCount 示例作业，验证 Driver Pod 与 Executor Pod 能够正常创建和运行。
2. 使用 PySpark 读取豆瓣电影 CSV 数据集，输出 Schema 和前 5 行数据。
3. 统计各字段缺失值，并对核心字段采用删除策略，对描述性字段采用填充策略。
4. 使用 Spark SQL 和 DataFrame API 完成电影类型统计、高评分电影 Top-N、年份趋势分析和分组统计等查询。
5. 对比 Pandas 单机执行与 PySpark 单 Executor、双 Executor 执行时间，并结合 Amdahl 定律分析加速比未线性的原因。

## 本地运行方式

在本地使用 Docker Compose 启动前后端和 Redis：

```bash
docker compose up --build
```

启动后访问前端页面：

```text
http://localhost:8080
```

后端接口：

```text
http://localhost:5000/api/ping
```

## 主要目录说明

### backend/

后端基于 Flask 实现，提供 `/api/ping` 接口。该接口会连接 Redis，并对 `ping_count` 进行自增，用于验证前后端通信和 Redis 连接是否正常。

### frontend/

前端基于 Nginx 静态页面实现，页面中展示课程设计标题、小组成员姓名学号，并提供按钮调用 `/api/ping` 接口。Nginx 配置用于将 `/api/` 请求反向代理到后端服务。

### spark-jobs/

包含 Spark 作业代码：

- `wordcount.py`：WordCount 示例作业，用于验证 Spark Operator 环境。
- `douban_spark_analysis.py`：豆瓣电影数据分析脚本，用于完成数据读取、清洗、统计分析和运行时间输出。

### docs/screenshots/ 与 docs/screenshots2/

保存实验报告中使用的关键截图，分别对应第一部分云计算平台搭建和第二部分 Spark 大数据分析。

## 注意事项

本仓库不上传真实 Secret、`.env` 文件、PDF/DOCX 报告文件以及大型离线镜像包。相关敏感信息和云资源配置以实验报告截图和本地环境为准。