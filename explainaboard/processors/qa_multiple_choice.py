from typing import List
from explainaboard.info import Result, SysOutputInfo
from explainaboard import feature
from explainaboard.tasks import TaskType
from explainaboard.processors.processor import Processor
from explainaboard.processors.processor_registry import register_processor
from explainaboard.builders.qa_multiple_choice import (
    QAMultipleChoiceExplainaboardBuilder,
)


@register_processor(TaskType.qa_multiple_choice)
class QAMultipleChoiceProcessor(Processor):
    _task_type = TaskType.qa_multiple_choice
    _features = feature.Features(
        {
            "context": feature.Value("string"),
            "question": feature.Value("string"),
            "options": feature.Sequence(feature.Value("string")),
            "answers": {
                "text": feature.Value("string"),
                "option_index": feature.Value("int32"),
            },
            "context_length": feature.Value(
                dtype="float",
                description="the length of context",
                is_bucket=True,
                bucket_info=feature.BucketInfo(
                    method="bucket_attribute_specified_bucket_value",
                    number=4,
                    setting=(),
                ),
            ),
            "question_length": feature.Value(
                dtype="float",
                description="the length of question",
                is_bucket=True,
                bucket_info=feature.BucketInfo(
                    method="bucket_attribute_specified_bucket_value",
                    number=4,
                    setting=(),
                ),
            ),
            "answer_length": feature.Value(
                dtype="float",
                description="the length of answer",
                is_bucket=True,
                bucket_info=feature.BucketInfo(
                    method="bucket_attribute_specified_bucket_value",
                    number=4,
                    setting=(),
                ),
            ),
            "num_oov": feature.Value(
                dtype="float",
                description="the number of out-of-vocabulary words",
                is_bucket=True,
                bucket_info=feature.BucketInfo(
                    method="bucket_attribute_specified_bucket_value",
                    number=4,
                    setting=(),
                ),
                require_training_set=True,
            ),
            "fre_rank": feature.Value(
                dtype="float",
                description="the average rank of each work based on its frequency in training set",
                is_bucket=True,
                bucket_info=feature.BucketInfo(
                    method="bucket_attribute_specified_bucket_value",
                    number=4,
                    setting=(),
                ),
                require_training_set=True,
            ),
        }
    )

    def __init__(self) -> None:
        super().__init__()

    def process(self,
                metadata: dict,
                sys_output: List[dict]) -> Result:
        if metadata is None:
            metadata = {}
        if "task_name" not in metadata.keys():
            metadata["task_name"] = TaskType.qa_multiple_choice.value
        if "metric_names" not in metadata.keys():
            metadata["metric_names"] = ["Accuracy"]
        sys_info = SysOutputInfo.from_dict(metadata)
        sys_info.features = self._features
        builder = QAMultipleChoiceExplainaboardBuilder()
        return builder.run(sys_info, sys_output)
