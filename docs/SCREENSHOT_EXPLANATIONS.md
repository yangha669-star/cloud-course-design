# 截图说明索引

本文件用于说明 `docs/screenshots` 与 `docs/screenshots2` 中各截图在实验报告中的作用。报告中插入截图时，建议按照任务顺序引用，并在图下方添加“图号 + 标题 + 简要说明”。

## 第一部分：云计算平台搭建截图说明

### 任务1：应用容器化

| 截图文件 | 报告中建议标题 | 说明 |
|---|---|---|
| `本地 Docker 镜像构建结果.png` | 图 1-1 本地 Docker 镜像构建结果 | 证明后端与前端镜像已在本地成功构建，为后续推送 SWR 和部署到 CCE 做准备。 |
| `Docker Compose 启动成功.png` | 图 1-2 Docker Compose 本地联调启动成功 | 证明本地使用 `docker compose up` 启动了前端、后端和 Redis 服务。 |
| `任务1-前端调用后端成功.png` | 图 1-3 前端页面访问后端 API 成功 | 证明前端页面能够访问后端接口，前后端通信正常。 |
| `任务1-后端api返回status-ok.png` | 图 1-4 后端 API 返回 status ok | 证明 Flask 后端 `/api/ping` 接口能够正常返回响应。 |
| `任务1-后端日志收到请求.png` | 图 1-5 后端日志收到前端请求 | 证明前端访问后，后端日志中记录到了请求，满足本地联调验收要求。 |
| `任务1-06-SWR镜像列表.png` 或 `任务1-06-SWR镜像列表..png` | 图 1-6 SWR 镜像列表 | 证明前端和后端镜像已经推送到华为云 SWR，截图中应能看到镜像名称和 Tag。 |

### 任务2：CCE 集群搭建

| 截图文件 | 报告中建议标题 | 说明 |
|---|---|---|
| `任务2-01-CCE集群概览.png` | 图 2-1 CCE 集群概览 | 展示 CCE 集群基本信息，可用于说明实验所用华为云环境。 |
| `任务2-02-CCE节点列表.png` | 图 2-2 CCE Worker 节点列表 | 展示集群 Worker 节点信息，证明集群包含至少 2 个 Worker 节点。 |
| `任务2-03-kubectl节点Ready.png` | 图 2-3 kubectl 查看节点 Ready 状态 | 证明 `kubectl get nodes -o wide` 中所有 Worker 节点状态为 Ready，并且 VERSION 列满足 Kubernetes 版本要求。 |

### 任务3：应用部署

| 截图文件 | 报告中建议标题 | 说明 |
|---|---|---|
| `任务3-01-应用YAML部署成功.png` | 图 3-1 应用 YAML 资源创建成功 | 证明后端、Redis、Service、ConfigMap 和 Secret 等 Kubernetes 资源已经通过 YAML 应用到集群。 |
| `任务3-02-Pod运行状态.png` | 图 3-2 应用 Pod 运行状态 | 证明后端、前端和 Redis Pod 均处于 Running 状态。 |
| `任务3-03-后端LoadBalancer-ELB公网IP.png` | 图 3-3 后端 LoadBalancer 获取 ELB 公网 IP | 证明后端 Service 类型为 LoadBalancer，并已绑定公网访问地址。 |
| `任务3-04-ELB公网访问api成功.png` | 图 3-4 ELB 公网访问 `/api/ping` 成功 | 证明通过公网 ELB 访问后端 `/api/ping` 能返回 `status: ok`，满足对外暴露验收要求。 |
| `任务3-05-ConfigMap和Secret.png` | 图 3-5 ConfigMap 与 Secret 配置 | 证明 Redis 地址通过 ConfigMap 注入，Redis 密码通过 Secret 以 base64 编码方式保存。 |
| `任务3-06-Deployment副本状态.png` | 图 3-6 Deployment 副本状态 | 证明后端副本数为 2、Redis 副本数为 1，Deployment 运行状态正常。 |

说明：旧的 NodePort 截图、集群内部访问截图不建议放入正式报告，因为最终验收要求是后端 LoadBalancer 公网访问。

### 任务4：Redis 持久化存储

| 截图文件 | 报告中建议标题 | 说明 |
|---|---|---|
| `任务4-00-Redis挂载PVC配置.png` | 图 4-1 Redis Deployment 挂载 PVC 配置 | 证明 Redis 的 `/data` 目录通过 Volume 挂载到 `redis-data-pvc`。 |
| `任务4-01-PVC绑定成功.png` | 图 4-2 PVC Bound 状态 | 证明 `redis-data-pvc` 已成功绑定云硬盘，StorageClass 为 `csi-disk`，容量为 10Gi。 |
| `任务4-02-Redis写入和读取数据.png` | 图 4-3 Redis 写入并读取测试数据 | 证明向 Redis 写入 `testkey=hello` 后能够正常读取。 |
| `任务4-03-删除RedisPod.png` | 图 4-4 删除 Redis Pod | 证明通过删除 Redis Pod 触发 Pod 重建，用于验证持久化效果。 |
| `任务4-04-RedisPod重建.png` | 图 4-5 Redis Pod 重建成功 | 证明删除后新的 Redis Pod 已重新变为 Running 状态。 |
| `任务4-05-数据恢复验证.png` | 图 4-6 Redis 数据恢复验证 | 证明 Pod 重建后再次读取 `testkey` 仍返回 `hello`，说明数据已持久化。 |

### 任务5：ConfigMap Volume 挂载

| 截图文件 | 报告中建议标题 | 说明 |
|---|---|---|
| `任务5-01-nginx-configmap配置.png` | 图 5-1 Nginx ConfigMap 配置 | 证明 Nginx 反向代理配置以 ConfigMap 形式保存。 |
| `任务5-02-frontend-volume挂载后Pod运行.png` | 图 5-2 frontend 挂载 ConfigMap 后运行状态 | 证明前端 Deployment 已将 ConfigMap 以 Volume 形式挂载。 |
| `任务5-03-Pod内查看nginx配置.png` | 图 5-3 Pod 内查看 Nginx 配置文件 | 证明在前端 Pod 内 `/etc/nginx/conf.d/default.conf` 可以读取到 ConfigMap 中的配置内容。 |
| `任务5-04-ConfigMap修改端口后Pod内配置更新.png` | 图 5-4 修改 ConfigMap 后 Pod 内配置更新 | 证明将后端端口临时改为 5001 并重新应用后，Pod 内配置文件已经更新。 |
| `任务5-05-前端反向代理api成功.png` | 图 5-5 前端反向代理访问后端 API 成功 | 证明前端 Nginx 通过反向代理访问后端 `/api/ping` 成功。 |

说明：完成端口修改验证后，应将 Nginx 配置恢复为正常后端服务地址，避免前端 API 访问失败。

### 任务6：HPA 弹性伸缩

| 截图文件 | 报告中建议标题 | 说明 |
|---|---|---|
| `任务6-01-metrics可用.png` | 图 6-1 metrics-server 可用 | 证明 `kubectl top nodes` 能返回 CPU 和内存数据，HPA 有可用指标来源。 |
| `任务6-02-HPA创建成功.png` | 图 6-2 HPA 创建成功 | 证明 HPA 已创建，配置为 minReplicas=1、maxReplicas=4、CPU 目标利用率 60%。 |
| `任务6-03-压测开始.png` | 图 6-3 压测开始 | 证明使用压测请求持续访问后端 `/api/ping`，用于触发 CPU 负载升高。 |
| `任务6-04-Pod扩容截图.png` | 图 6-4 HPA 扩容结果 | 证明压测后 backend Pod 数量从 1 增加到 2 个或更多，实验中扩容到了 4 个。 |
| `任务6-05-Pod缩容截图.png` | 图 6-5 HPA 缩容结果 | 证明停止压测后，backend Pod 数量缩回 1 个。 |
| `任务6-06-HPA详情.png` | 图 6-6 HPA 详情与扩缩容事件 | 证明 HPA 记录了 SuccessfulRescale 事件，包括扩容和缩容过程。 |

## 第二部分：Spark 大数据分析截图说明

### A-0 Spark on K8s 环境部署

| 截图文件 | 报告中建议标题 | 说明 |
|---|---|---|
| `Spark-00-wordcount-Driver和Executor运行中.png` | 图 A0-1 WordCount Driver 与 Executor 运行中 | 证明 WordCount SparkApplication 提交后创建了 Driver Pod 和两个 Executor Pod，满足 executor.instances=2 的要求。 |
| `Spark-00-wordcount示例作业完成.png` | 图 A0-2 WordCount 示例作业完成 | 证明 WordCount Driver Pod 最终进入 Completed 状态。 |
| `Spark-00-wordcount日志结果.png` | 图 A0-3 WordCount 日志输出 | 证明 WordCount 示例作业成功执行并输出 Top 10 words。 |
| `Spark-01-SWR镜像上传成功.png` | 图 A0-4 PySpark 基础镜像上传 SWR | 证明用于 Spark 作业的 PySpark 镜像已上传到 SWR。 |
| `Spark-02-SparkOperator运行.png` | 图 A0-5 Spark Operator 运行状态 | 证明 Spark Operator controller 和 webhook 在集群中正常运行。 |
| `Spark-03-douban-spark镜像上传成功.png` | 图 A0-6 豆瓣分析镜像上传 SWR | 证明包含分析脚本的 Spark 镜像已上传到 SWR。 |
| `Spark-04-SparkApplication运行完成.png` | 图 A0-7 豆瓣分析 SparkApplication 完成 | 证明主分析作业已经通过 Spark Operator 提交并成功完成。 |

### A-1 数据清洗

| 截图文件 | 报告中建议标题 | 说明 |
|---|---|---|
| `Spark-05-数据Schema和前5行.png` | 图 A1-1 数据 Schema 和前 5 行 | 证明数据已加载到 Spark DataFrame，并展示字段结构和样例数据。 |
| `Spark-06-缺失值统计和数据清洗.png` | 图 A1-2 缺失值统计与清洗策略 | 证明对各字段统计缺失值数量与比例，并使用 dropna/filter 与 fillna 两种策略进行处理。 |
| `Spark-07-字段基本统计信息.png` | 图 A1-3 字段基本统计信息 | 证明输出了 count、mean、stddev、min、max 等基本统计信息。 |

### A-2 Spark SQL 统计分析

| 截图文件 | 报告中建议标题 | 说明 |
|---|---|---|
| `Spark-08-电影类型和高评分电影Top10.png` | 图 A2-1 电影类型统计与高评分电影 Top10 | 证明完成了 GROUP BY 聚合和 ORDER BY Top-N 查询。 |
| `Spark-09-年份趋势分析.png` | 图 A2-2 年份维度趋势分析 | 证明按年份完成时间维度趋势统计。 |
| `Spark-10-窗口函数每年高分电影Top3.png` | 图 A2-3 窗口函数查询每年高分电影 Top3 | 证明使用窗口函数完成每年分组内 Top-N 查询。 |

说明：A-2 报告中每个查询结果后应添加不少于 50 字的分析说明，不能只放截图。

### A-3 性能对比与 Amdahl 分析

| 截图文件 | 报告中建议标题 | 说明 |
|---|---|---|
| `Spark-11-性能对比和Amdahl分析.png` | 图 A3-1 性能对比与 Amdahl 分析（一） | 说明选取的查询、对比方法和 Amdahl 分析思路。 |
| `Spark-11-性能对比和Amdahl分析（2）.png` | 图 A3-2 性能对比与 Amdahl 分析（二） | 补充说明加速比未线性提升的原因。 |
| `Spark-12-executor1运行完成.png` | 图 A3-3 PySpark 单 Executor 作业完成 | 证明 executor.instances=1 的 PySpark 性能实验已运行完成。 |
| `Spark-13-executor1-PySpark查询耗时.png` | 图 A3-4 单 Executor PySpark 查询耗时 | 记录单 Executor 下所选查询的执行时间。 |
| `Spark-13-executor1-Spark总耗时.png` | 图 A3-5 单 Executor Spark 总耗时 | 记录单 Executor 下 Spark 作业总耗时。 |
| `Spark-14-executor2运行完成.png` | 图 A3-6 双 Executor 作业完成 | 证明 executor.instances=2 的 PySpark 性能实验已运行完成。 |
| `Spark-15-executor2-PySpark查询耗时.png` | 图 A3-7 双 Executor PySpark 查询耗时 | 记录双 Executor 下所选查询的执行时间。 |
| `Spark-15-executor2-Spark总耗时.png` | 图 A3-8 双 Executor Spark 总耗时 | 记录双 Executor 下 Spark 作业总耗时。 |
| `Spark-16-性能对比图.png` | 图 A3-9 Pandas 与 PySpark 性能对比图 | 以柱状图方式对比 Pandas、PySpark 单 Executor、PySpark 双 Executor 的耗时。 |
