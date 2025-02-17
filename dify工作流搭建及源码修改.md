# 源码修改

## 1.回答修改：### 用于修改回答时代码执行的修改，用于制作酒店卡片

### 文件路径
`api/core/workflow/nodes/answer/answer_node.py`

### 修改内容

#### 导入模块
```python
from collections.abc import Mapping, Sequence
from typing import Any, cast

from oci.data_flow.models import NodeCount

from core.variables import ArrayFileSegment, FileSegment
from core.workflow.entities.node_entities import NodeRunResult
from core.workflow.nodes.answer.answer_stream_generate_router import AnswerStreamGeneratorRouter
from core.workflow.nodes.answer.entities import (
    AnswerNodeData,
    GenerateRouteChunk,
    TextGenerateRouteChunk,
    VarGenerateRouteChunk,
)
from core.workflow.nodes.base import BaseNode
from core.workflow.nodes.enums import NodeType
from core.workflow.utils.variable_template_parser import VariableTemplateParser
from models.workflow import WorkflowNodeExecutionStatus

class AnswerNode(BaseNode[AnswerNodeData]):
    _node_data_cls = AnswerNodeData
    _node_type: NodeType = NodeType.ANSWER

def _run(self) -> NodeRunResult:
    """
    Run node
    :return:
    """
    # Generate routes
    generate_routes = AnswerStreamGeneratorRouter.extract_generate_route_from_node_data(self.node_data)
    print('0000', generate_routes)
    
    answer = ""
    answer1 = ""
    files = []

    for part in generate_routes:
        if part.type == GenerateRouteChunk.ChunkType.VAR:
            part = cast(VarGenerateRouteChunk, part)
            value_selector = part.value_selector
            
            if value_selector[1] == 'result':
                variable_1 = self.graph_runtime_state.variable_pool.get(value_selector)
                if variable_1:
                    if isinstance(variable_1, FileSegment):
                        files.append(variable_1.value)
                    elif isinstance(variable_1, ArrayFileSegment):
                        files.extend(variable_1.value)
                    answer1 += variable_1.markdown
            else:
                variable = self.graph_runtime_state.variable_pool.get(value_selector)
                if variable:
                    if isinstance(variable, FileSegment):
                        files.append(variable.value)
                    elif isinstance(variable, ArrayFileSegment):
                        files.extend(variable.value)
                    answer += variable.markdown
        else:
            part = cast(TextGenerateRouteChunk, part)
            answer += part.text

    return NodeRunResult(
        status=WorkflowNodeExecutionStatus.SUCCEEDED,
        outputs={"answer": answer, "files": files, 'code': answer1}
    )

@classmethod
def _extract_variable_selector_to_variable_mapping(
    cls,
    *,
    graph_config: Mapping[str, Any],
    node_id: str,
    node_data: AnswerNodeData,
) -> Mapping[str, Sequence[str]]:
    """
    Extract variable selector to variable mapping
    :param graph_config: graph config
    :param node_id: node id
    :param node_data: node data
    :return:
    """
    variable_template_parser = VariableTemplateParser(template=node_data.answer)
    variable_selectors = variable_template_parser.extract_variable_selectors()

    variable_mapping = {}
    for variable_selector in variable_selectors:
        variable_mapping[node_id + "." + variable_selector.variable] = variable_selector.value_selector

    return variable_mapping
```

## 2.提示词的修改

### 例：
```
<instruction>
根据当前查询（{{#sys.query#}}）和最近3轮对话历史，判断用户是否最终确认具体酒店。输出仅包含数字1或2。

<判断逻辑>
1. 返回1的条件（优先级从高到低）：
   a) 当前查询含酒店全称（例："禧沃酒店"）
   b) 最近3轮存在明确酒店锁定（例："君悦酒店详情"），且当前查询涉及：
      - 房型/价格/设施等属性词
      - 使用指示代词（"这家/那家"）
      - 预订相关动作词（"订/预订/下单"）
   c) 对话历史中连续2次提及同一酒店简称（例："沃酒店"→"禧沃"）

2. 返回2的条件（优先级从高到低）：
   a) 用户明确表示重新推荐（例："重新推荐一家酒店"）
   b) 最近3轮对话未提及任何酒店信息（例：首次咨询酒店）
   c) 泛询酒店列表/推荐（例："附近四星酒店"）
   d) 跨酒店比较（例："对比禧沃和君悦"）
   e) 未形成酒店锁定链（间隔1轮以上未提及）

<强制规则>
1. 输出必须为单数字符（1/2）
2. 不添加任何解释说明
3. 模糊情况从严判定（倾向返回2）
4. 仅返回1或2，不对问题做回答

<决策树>
是否含酒店全称 → 是→1
↓否
用户是否明确重新推荐 → 是→2
↓否
前三轮是否无酒店信息 → 是→2
↓否
最近3轮存在锁定酒店 → 是→检查当前查询是否关联属性 → 是→1
↓否 ↓否
返回2
</决策树>
</instruction>
```

## 3.上下文长度修改

## 4.酒店数据修改
### 例：
```
[
  {
    "address": "山西省长治市潞州区大辛庄街道西环路57号长治禧沃酒店",
    "carousel_image": "/profile/upload/2024/10/14/Group 1321316982@2x_20241014141159A002.png,/profile/upload/2024/10/14/Group 1321316665@2x_20241014141201A003.png",
    "check_in_description": "\u003Cp\u003E\u003Cstrong style=\"color: rgb(96, 98, 102);\"\u003E入住说明\u003C/strong\u003E\u003C/p\u003E",
    "check_in_time": "12:00:00",
    "check_in_way": "拎包入住",
    "cover_image": "/profile/upload/2024/10/14/Group 1321316665@2x_20241014141156A001.png",
    "decoration_time": "2024-05-01",
    "hour_room_check_in_time": null,
    "hour_room_leave_time": null,
    "id": 1,
    "important_notice": "重要通知",
    "invoice": "Y",
    "label": "好好好,住住住",
    "label_name": "免费停车,智能机器人,深睡房",
    "latitude": "36.215547",
    "leave_time": "13:00:00",
    "longitude": "113.092551",
    "min_limited_age": 18,
    "name": "禧沃酒店",
    "opening_time": "2024-10-01",
    "pet": "Y",
    "phone": null,
    "price": "428.00",
    "price1": "277.00",
    "star": 4,
    "type": 2
  },
  {
    "address": "山西省长治市壶关县集店镇花美时民宿酒店(壶关欢乐太行谷店)欢乐太行谷",
    "carousel_image": "/profile/upload/2024/12/09/1c1fc2a4-7a52-489f-a1f2-608899700c9f_20241127165356A119_20241209091052A011.jpg,/profile/upload/2024/12/09/微信图片_20241127165510_20241127165614A121_20241209091058A012.jpg,/profile/upload/2024/12/09/微信图片_20241127165511_20241127165618A122_20241209091102A013.jpg",
    "check_in_description": "\u003Cp\u003E\u003Cspan style=\"color: rgb(96, 98, 102);\"\u003E‌花美时温泉酒店‌位于山西省长治市壶关县325省道欢乐太行谷景区内，是一个集客房住宿、休闲度假、康体娱乐、团体拓建为一体的综合度假旅游地。酒店总投资4800万元，占地面积34000平方米，按五星级标准建造，拥有徽派建筑风格，营造出浓厚的田园气息‌。\u003C/span\u003E\u003C/p\u003E",
    "check_in_time": "14:00:00",
    "check_in_way": "不限制",
    "cover_image": "/profile/upload/2024/12/09/1c1fc2a4-7a52-489f-a1f2-608899700c9f_20241127165356A119_20241209091047A010.jpg",
    "decoration_time": "2023-06-01",
    "hour_room_check_in_time": "16:00:00",
    "hour_room_leave_time": "19:00:00",
    "id": 2,
    "important_notice": "\u003Cp\u003E酒店前台可用支付方式：微信支付、支付宝支付、银联云闪付。（酒店价格为参考价格，一切以入住当天的实际价格为准）\u003C/p\u003E",
    "invoice": "Y",
    "label": "温泉,花园,温泉汤泡,烧烤,家庭房",
    "label_name": "温泉酒店,儿童用品,庭院景,上下铺",
    "latitude": "36.170878",
    "leave_time": "12:00:00",
    "longitude": "113.238401",
    "min_limited_age": 1,
    "name": "花美时温泉酒店",
    "opening_time": "2023-06-01",
    "pet": "N",
    "phone": "0355-8668555",
    "price": "398.00",
    "price1": "373.00",
    "star": 1,
    "type": 1
  }
 ]
```
