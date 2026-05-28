# 云计算课程设计报告撰写指导

本文件用于指导正式 PDF 实验报告的编写。报告应突出“做了什么、如何验证、结果说明”，不要把所有命令无序堆叠，也不要放失败过程截图。建议最终 PDF 按任务顺序组织，每个任务包含：目标说明、操作步骤摘要、关键截图、结果分析。

## 一、报告整体结构建议

1. 封面
2. 华为云环境信息
3. 第一部分：云计算平台搭建
   - 任务1：应用容器化
   - 任务2：CCE 集群搭建
   - 任务3：应用部署
   - 任务4：持久化存储
   - 任务5：ConfigMap Volume 挂载
   - 任务6：HPA 弹性伸缩
4. 第二部分：方向 A Spark 大数据分析
   - A-0：Spark on K8s 环境部署
   - A-1：数据清洗
   - A-2：Spark SQL 统计分析
   - A-3：性能对比与 Amdahl 分析
5. 总结与收获
6. 附录：核心 YAML、Dockerfile、Python 代码和 GitHub 仓库链接

## 二、封面写法

封面建议包含以下信息：

- 课程名称：云计算技术课程设计
- 报告题目：云计算平台搭建与 Spark 大数据分析实验报告
- 学号
- 姓名
- 班级
- 日期
- GitHub 仓库链接

## 三、第一部分报告写法

### 任务1：应用容器化

本任务主要说明如何将 Flask 后端和 Nginx 前端分别制作成 Docker 镜像，并使用 Docker Compose 完成本地联调。报告中应说明后端 Dockerfile 保留了多阶段构建结构，先在 builder 阶段安装依赖，再复制到运行时镜像中，减少运行时镜像体积；requirements.txt 中额外加入了自选 Python 包；前端首页 index.html 中加入了本人学号和姓名用于验收识别。随后展示本地 docker compose 启动截图、前后端通信截图、后端日志收到请求截图和 SWR 镜像列表截图。

建议分析文字：

> 本任务完成了前后端应用的容器化构建。后端镜像采用多阶段构建，依赖安装与运行时环境分离，能够减少最终镜像体积并提高部署稳定性。前端使用 Nginx 承载静态页面，并在首页中加入学号和姓名作为验收标识。通过 Docker Compose 在本地同时启动后端、前端和 Redis，前端访问后端接口成功，后端日志中也能看到请求记录，说明本地联调正常。最后将镜像推送到华为云 SWR，为后续 CCE 部署提供镜像来源。

### 任务2：CCE 集群搭建

本任务说明在华为云 CCE 中创建 Kubernetes 集群，并使用 CloudShell 或 kubectl 连接集群。报告中重点展示 `kubectl get nodes -o wide` 截图，说明集群包含两个 Worker 节点，节点状态均为 Ready，且 VERSION 字段满足 Kubernetes 版本不低于 1.27 的要求。

建议分析文字：

> 本任务在华为云 CCE 中完成 Kubernetes 集群搭建。集群采用托管 Master 节点和两个 Worker 节点的结构，用户主要负责 Worker 节点资源和工作负载部署。通过 kubectl 查看节点状态可以看到两个 Worker 节点均处于 Ready 状态，说明集群调度能力正常。VERSION 列显示 Kubernetes 版本满足课程要求，为后续 Deployment、Service、PVC、HPA 和 Spark Operator 作业运行提供基础环境。

### 任务3：应用部署

本任务说明如何使用 Kubernetes YAML 将第一部分镜像部署到 CCE。报告中应展示后端 Deployment、Redis Deployment、LoadBalancer Service、Redis ClusterIP Service、ConfigMap 和 Secret 的关键配置。重点说明后端副本数为 2，Redis 副本数为 1，后端镜像来自 SWR，后端 Service 使用 LoadBalancer 并绑定华为云 ELB，Redis Service 使用 ClusterIP 仅供集群内部访问。最后通过 ELB 公网 IP 访问 `/api/ping` 并返回 `status: ok`。

建议分析文字：

> 本任务将容器化后的后端服务和 Redis 数据库部署到 CCE 集群中。后端 Deployment 设置两个副本，以提高可用性；Redis Deployment 设置一个副本，并通过 Service 在集群内部提供访问入口。后端 Service 使用 LoadBalancer 类型并绑定华为云 ELB，使外部用户能够通过公网 IP 访问 `/api/ping` 接口。Redis 地址等非敏感配置通过 ConfigMap 注入，Redis 密码通过 Secret 注入，体现了配置分离和敏感信息保护的设计思想。

### 任务4：持久化存储

本任务说明如何为 Redis 配置 PVC，并验证 Pod 重建后数据不丢失。报告中应展示 `redis-data-pvc` Bound 状态、Redis `/data` 目录挂载 PVC、写入 `testkey=hello`、删除 Redis Pod、Pod 重建、重建后再次读取 `testkey` 仍返回 `hello` 的截图。

建议分析文字：

> 本任务通过 PVC 为 Redis 配置持久化存储。Redis 容器的 `/data` 目录挂载到 `redis-data-pvc`，PVC 使用华为云 `csi-disk` StorageClass，容量为 10Gi。验证时首先向 Redis 写入 `testkey=hello`，随后删除 Redis Pod 触发重建。新的 Redis Pod 启动后再次读取 `testkey`，仍能够返回 `hello`，说明数据没有因为容器重建而丢失，持久化存储配置生效。

### 任务5：ConfigMap Volume 挂载

本任务说明如何将 Nginx 反向代理配置以 ConfigMap Volume 的方式挂载到前端 Pod 的 `/etc/nginx/conf.d/default.conf`。报告中应展示 ConfigMap 内容、frontend Deployment 的 Volume 挂载配置、Pod 内 cat 配置文件结果、修改端口后配置文件更新结果，以及前端反向代理访问后端 API 成功结果。

建议分析文字：

> 本任务将 Nginx 配置文件从镜像中解耦出来，改为通过 ConfigMap Volume 挂载到前端 Pod。这样可以在不重新构建镜像的情况下调整反向代理配置。实验中将 ConfigMap 挂载到 `/etc/nginx/conf.d/default.conf`，并进入 Pod 内查看配置文件内容，验证挂载成功。随后修改 ConfigMap 中后端端口值并重新应用，Pod 内配置文件更新，说明 ConfigMap Volume 能够用于管理文件型配置。

Volume 与 envFrom 区别可写：

> ConfigMap 以 Volume 挂载时，适合注入配置文件类内容，例如 Nginx 的 `default.conf`。容器内部可以像读取普通文件一样读取配置，适合配置内容较长、具有层级结构或需要被程序按文件加载的场景。`envFrom` 则适合注入简单的键值对环境变量，例如 `REDIS_HOST`、`REDIS_PORT` 等，适用于程序启动时读取少量参数。相比之下，Volume 更适合配置文件管理，envFrom 更适合简单参数注入。

### 任务6：HPA 弹性伸缩

本任务说明如何创建 HPA，并通过压测验证后端 Deployment 能够自动扩缩容。报告中应展示 metrics-server 可用、HPA 配置为 minReplicas=1、maxReplicas=4、CPU 目标 60%，压测后 Pod 数从 1 扩到更多，停止压测后缩回 1，以及 HPA 详情中 SuccessfulRescale 事件。

建议分析文字：

> 本任务为后端 Deployment 配置 HPA，实现基于 CPU 利用率的自动扩缩容。HPA 配置最小副本数为 1，最大副本数为 4，CPU 目标利用率为 60%。压测开始后，后端 CPU 利用率超过目标值，HPA 将 Pod 数量从 1 个扩容到 4 个；停止压测并等待一段时间后，Pod 数量缩回 1 个。扩容存在一定延迟，主要原因是 metrics-server 需要周期性采集指标，HPA 控制器也按固定周期进行评估。缩容冷却时间可以避免短时间负载波动导致频繁扩缩容，从而减少系统抖动。HPA 能在低负载时减少副本数，在高负载时增加副本数，提高资源利用率并降低云资源成本。

## 四、第二部分方向 A 报告写法

### A-0：Spark on K8s 环境部署

报告中应说明使用 Spark Operator 在 CCE 上提交 SparkApplication 作业。重点展示 Spark Operator Running、WordCount Driver 与 Executor Pod 运行、WordCount Completed、日志输出 Top 10 words，以及主分析 SparkApplication Completed。还应在报告中列出 SparkApplication 关键参数，例如 SWR 镜像地址、`executor.instances=2`、`executor.memory=1g`。

建议分析文字：

> 本实验使用 Spark Operator 在 Kubernetes 集群中提交 SparkApplication 作业。Spark Operator 负责监听 SparkApplication 资源，并自动创建 Driver Pod 和 Executor Pod。WordCount 示例作业中，Driver Pod 负责提交和协调 Spark 任务，两个 Executor Pod 负责执行并行计算。作业运行完成后，Driver Pod 进入 Completed 状态，日志中输出 Top 10 words，说明 Spark on K8s 环境部署成功。

### A-1：数据清洗

报告中应说明选择豆瓣电影评分数据集，使用 Spark 读取数据到 DataFrame，打印 Schema 和前 5 行，统计各字段缺失值数量与比例。清洗策略必须说明至少两种：例如对核心分析字段使用 dropna/filter，对描述性字段使用 fillna。

建议分析文字：

> 本实验选择豆瓣电影评分数据集作为分析对象。首先使用 Spark 将数据加载为 DataFrame，并通过 `printSchema()` 查看字段结构，通过 `show(5)` 查看前 5 行样例数据。随后统计各字段缺失值数量和缺失值比例。对于 `year`、`rating_score`、`genres`、`countries` 等分析关键字段，缺失会直接影响统计结果，因此采用 dropna/filter 删除异常或缺失记录。对于 `directors` 和 `summary` 等描述性字段，缺失不会影响核心统计，因此使用 fillna 分别填充为“未知导演”和“暂无简介”。清洗后数据量由 67132 行减少到 56886 行，删除异常或缺失记录 10246 行。

### A-2：Spark SQL 统计分析

报告中至少写 4 个查询，每个查询后必须有不少于 50 字分析。建议安排为：

1. 电影类型数量 Top10：GROUP BY 聚合 + ORDER BY Top-N。
2. 高评分电影 Top10：ORDER BY Top-N。
3. 年份趋势分析：按年份统计电影数量，属于时间维度趋势分析。
4. 每年高分电影 Top3：使用窗口函数完成组内排名。

示例分析文字：

> 电影类型统计结果显示，数据集中数量靠前的电影类型代表了豆瓣电影数据中较常见的题材分布。通过对类型字段进行分组聚合，可以观察不同题材电影的数量差异，为后续分析评分与类型之间的关系提供基础。Top-N 排序能够快速找出占比最高的类型，使结果更直观，也便于在报告中展示主要电影类型的分布特点。

> 高评分电影 Top10 查询通过对评分字段进行降序排序，筛选出评分较高的电影。为了避免评分人数过少导致结果偶然性较强，可以结合评分人数或收藏人数进行辅助判断。该查询体现了 ORDER BY 和 Top-N 分析的应用价值，能够帮助快速定位数据集中综合表现较好的电影样本。

> 年份趋势分析按照年份对电影数量进行分组统计，可以反映不同年份电影样本数量的变化情况。通过时间维度分析，可以观察电影数据在年份上的集中区间和变化趋势。如果某些年份电影数量明显较多，可能与数据来源、电影发行数量或用户记录活跃度有关。

> 每年高分电影 Top3 使用窗口函数在每个年份内部进行排序，能够找出不同年份评分最高的代表性电影。与普通全局 Top-N 不同，窗口函数保留了年份分组信息，适合解决“每个分组内取前几名”的问题。本查询满足了窗口函数分析要求，也展示了 Spark SQL 在复杂分组统计中的能力。

### A-3：性能对比与 Amdahl 分析

报告中应说明选取 A-2 中一个查询，分别使用 Pandas、PySpark executor=1、PySpark executor=2 实现，记录执行时间并绘制柱状图。分析中要说明为什么加速比没有线性提升。

建议分析文字：

> 本实验选取 A-2 中的统计查询作为性能对比对象，分别使用 Pandas 单机方式、PySpark 单 Executor 和 PySpark 双 Executor 实现，并记录执行时间。实验结果显示，在当前数据规模下，Pandas 的耗时较低，而 PySpark 增加 Executor 后并未获得线性加速。原因是豆瓣数据集规模相对有限，单机内存即可完成处理，Spark 的任务调度、DAG 构建、Executor 启动、网络通信和序列化开销占比较高。根据 Amdahl 定律，程序总体加速比受不可并行部分限制，数据读取、任务调度、结果收集和部分全局聚合操作无法完全并行，因此增加 Executor 数量后整体加速比不会线性增长。

## 五、总结与收获写法

总结不少于 200 字，建议包含具体量化数据，例如：

- CCE 集群包含 2 个 Worker 节点。
- 后端 Deployment 副本数为 2。
- Redis PVC 容量为 10Gi。
- HPA 从 1 个 Pod 扩容到 4 个 Pod，再缩容回 1 个。
- 豆瓣数据原始 67132 行，清洗后 56886 行，删除 10246 行。
- Pandas 与 PySpark 的耗时对比结果。

示例总结：

> 通过本次课程设计，我完整实践了从应用容器化、镜像仓库管理、Kubernetes 部署到弹性伸缩和 Spark 大数据分析的完整流程。在第一部分中，我将 Flask 后端和 Nginx 前端制作成 Docker 镜像并推送到华为云 SWR，随后在 CCE 集群中部署两层 Web 应用。后端 Deployment 设置 2 个副本，Redis 使用 PVC 挂载 10Gi 云硬盘，删除 Pod 后仍能读取 `testkey=hello`，说明持久化配置生效。HPA 实验中，后端 Pod 在压测时从 1 个扩容到 4 个，停止压测后缩容回 1 个，体现了云平台按需伸缩和节省资源的特点。在第二部分中，我使用 Spark Operator 提交 SparkApplication 作业，对 67132 行豆瓣电影数据进行清洗，清洗后保留 56886 行，并完成了类型统计、Top-N、年份趋势和窗口函数分析。性能实验也让我认识到并行计算并不总是线性加速，Spark 在小规模数据下会受到调度、通信和序列化开销影响。整体来看，本实验加深了我对容器、Kubernetes、对象存储、弹性伸缩和大数据计算框架的理解。

## 六、附录建议

附录中建议放以下内容或 GitHub 链接：

- `backend/Dockerfile`
- `backend/requirements.txt`
- `frontend/Dockerfile`
- Kubernetes Deployment、Service、ConfigMap、Secret、PVC、HPA YAML
- SparkApplication YAML
- Spark 分析 Python 代码
- GitHub 仓库链接

正式提交时，PDF 报告中可以引用 GitHub 仓库作为完整代码和截图备份。