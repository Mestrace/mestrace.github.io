Title: RocketMQ是什么
Slug: rocket-mq-history
Date: 2021-09-11
Category: Middleware
Tags: RocketMQ, Kafka


> Apache RocketMQ is a distributed messaging and streaming platform with low latency, high performance and reliability, trillion-level capacity and flexible scalability.

RocketMQ 是一个分布式消息中间件，其具有低延迟、高性能和可靠性、万亿级容量、灵活的可扩展性特性。

![异构数据下的ETL(Extract, Transform and Load) 处理]({static}/images/2/etl_process.png)

Kafka诞生于所谓的“大数据”时代的早期, 本质是LinkedIn为了解决在不同子系统中进行日志流同步的产物. 在设计之初就专注于对于解决ETL(Extract, transform, and load) 场景连续, 大量的消息数据的生产与消费. 作为一个通用场景的MQ系统, Kafka在大数据领域的实时计算以及日志采集领域被大规模使用. 基于Kafka, LinkedIn构建了一个以日志为中心的大规模分布式系统. 每天产生超过600亿条数据. 

![Kafka在LinkedIn的使用场景]({static}/images/2/linkedin_kafka_usage.png)

无疑, 基于MQ构建的数据驱动的系统给业务上带来了各种各样的便利和简化. 越来越多的开发者基于Kafka来构建各种应用. 随着时间的推移, 大量的使用也暴露了Kafka的在不同场景下的缺陷, 例如缺乏重试机制, 非严格顺序消费, 和不支持分布式事务. 因此, 阿里巴巴中间件团队针对订单, 交易和充值场景下对于MQ的使用进行了优化, 并与Apache基金会一起开源了RocketMQ. RocketMQ在淘宝的各种活动场景经历了大量的考验. 2017年, 阿里巴巴将RocketMQ开源并捐赠给Apache基金会, 由社区进行维护.

![Rocket MQ的历史]({static}/images/2/kafka_history.png)


一个有意思的点: RocketMQ项目只维护核心功能，且去除了所有其他运行时依赖，核心功能最简化。每个BU的个性化需求都在RocketMQ项目之上进行深度定制。RocketMQ向其他BU提供的仅仅是Jar包，例如要定制一个Broker，那么只需要依赖rocketmq-broker这个jar包即可，可通过API进行交互，如果定制client，则依赖rocketmq-client这个jar包，对其提供的api进行再封装。


| 名词                   | 定义                                                                                                                                                                                                                                                                                                                                                                                                                |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 生产组 Producer Group  | 标识发送同一类消息的Producer，通常发送逻辑一致。发送普通消息的时候，仅标识使用，并无特别用处。 若事务消息，如果某条发送某条消息的producer-A宕机，使得事务消息一直处于PREPARED状态并超时，则broker会回查同一个group的其 他producer，确认这条消息应该commit还是rollback。但开源版本并不支持事务消息。 注: 字节RMQ暂不支持事务.                                                                                        |
| 消费组 Consumer Group  | 标识一类Consumer的集合名称，这类Consumer通常消费一类消息，且消费逻辑一致。同一个Consumer Group下的各个实例将共同消费topic的消息，起到负载均衡的作用。 消费进度以Consumer Group为粒度管理，不同Consumer Group之间消费进度彼此不受影响，即消息A被Consumer Group1消费过，也会再给Consumer Group2消费。 注： RocketMQ要求同一个Consumer Group的消费者必须要拥有相同的注册信息，即必须要监听一样的topic(并且tag也一样)。 |
| Topic                  | 标识一类消息的逻辑名字，消息的逻辑管理单位。无论消息生产还是消费，都需要指定Topic。                                                                                                                                                                                                                                                                                                                                 |
| Tag                    | RocketMQ支持给在发送的时候给topic打tag，同一个topic的消息虽然逻辑管理是一样的。但是消费topic1的时候，如果你订阅的时候指定的是tagA，那么tagB的消息将不会投递。 注: PPE泳道不是以这种方式实现的                                                                                                                                                                                                                       |
| 逻辑队列 Message Queue | 消息物理管理单位。一个Topic将有若干个Queue。若Topic同时创建在不通的Broker，则不同的broker上都有若干Queue，消息将物理地存储落在不同Broker结点上，具有水平扩展的能力。 无论生产者还是消费者，实际的生产和消费都是针对Queue级别。例如Producer发送消息的时候，会预先选择（默认轮询）好该Topic下面的某一条Queue地发送.                                                                                                   |
| 集群消费               | 消费者的一种消费模式。一个Consumer Group中的各个Consumer实例分摊去消费消息，即一条消息只会投递到一个Consumer Group下面的一个实例。                                                                                                                                                                                                                                                                                  |
| 广播消费               | 消费者的一种消费模式。消息将对一个Consumer Group下的各个Consumer实例都投递一遍。即即使这些 Consumer 属于同一个Consumer Group，消息也会被Consumer Group 中的每个Consumer都消费一次。 注: 字节RMQ暂不支持广播消费                                                                                                                                                                                                     |