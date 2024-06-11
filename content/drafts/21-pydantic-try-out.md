Title: Pydantic 小试牛刀
Slug: pydantic-try-out
Category: Computer Science
Date: 2024-04-27 19:00
Tags: Python
Status: draft
Summary: 

最近在个人项目中使用了Pydantic用来定义一些基本类型。虽然Pydantic在开发过程中使用起来较为费劲，没有`@dataclass`一把梭的快感，但是带来了诸多好处。

首先，使用Pyantic提供了更加严格的类型检查和标注。后续开发过程中可以避免很多因为类型导致的微小错误在运行时才能够被暴露出来的问题。其次，Pydantic抽象出来的序列化方法能够很好地帮助我们实现一些自定义的逻辑。此外，Pydanic的校验逻辑也比较快，因为核心逻辑都是使用rust编写。

## 一个简单的例子

```python
from datetime import datetime
from typing import Tuple

from pydantic import BaseModel


class Delivery(BaseModel):
    timestamp: datetime
    dimensions: Tuple[int, int]
```

让我们来试用一下
```python
In [2]: m = Delivery(timestamp='2020-01-02T03:04:05Z', dimensions=['10', '20'])
   ...: 
In [3]: m.timestamp
Out[3]: datetime.datetime(2020, 1, 2, 3, 4, 5, tzinfo=TzInfo(UTC))

In [4]: m.dimensions
Out[4]: (10, 20)

In [5]: m.dict()
Out[5]: 
{'timestamp': datetime.datetime(2020, 1, 2, 3, 4, 5, tzinfo=TzInfo(UTC)),
 'dimensions': (10, 20)}
```

如果输入不合法的数据，会报错。

```python
In [12]: try:
    ...:     Delivery(timestamp='not a timestamp', dimensions=['10', '20'])
    ...: except ValidationError as e:
    ...:     print(e)
    ...: 
1 validation error for Delivery
timestamp
  Input should be a valid datetime or date, invalid character in year [type=datetime_from_date_parsing, input_value='not a timestamp', input_type=str]
    For further information visit https://errors.pydantic.dev/2.7/v/datetime_from_date_parsing
```

每个Pydantic模型都自带了三种序列化和反序列化方法：

* `model_validate` & 

```python
In [14]: Delivery.model_validate_json('{"timestamp":"2020-01-02T03:04:05Z","dimensions":[10,20]}')
Out[14]: Delivery(timestamp=datetime.datetime(2020, 1, 2, 3, 4, 5, tzinfo=TzInfo(UTC)), dimensions=(10, 20))

In [16]: try:
    ...:     Delivery.model_validate_json('{"timestamp":"not a string","dimensions":[10,20]}')
    ...: except ValidationError as e:
    ...:     print(e)
    ...: 
1 validation error for Delivery
timestamp
  Input should be a valid datetime or date, invalid character in year [type=datetime_from_date_parsing, input_value='not a string', input_type=str]
    For further information visit https://errors.pydantic.dev/2.7/v/datetime_from_date_parsing
```
