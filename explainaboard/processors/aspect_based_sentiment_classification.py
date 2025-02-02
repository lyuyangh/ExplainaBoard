from explainaboard import feature
from explainaboard.tasks import TaskType
from explainaboard.processors.processor import Processor
from explainaboard.processors.processor_registry import register_processor
from explainaboard.utils.spacy_loader import get_named_entities


@register_processor(TaskType.aspect_based_sentiment_classification)
class AspectBasedSentimentClassificationProcessor(Processor):
    _task_type = TaskType.aspect_based_sentiment_classification
    _features = feature.Features(
        {
            "aspect": feature.Value("string"),
            "text": feature.Value("string"),
            "true_label": feature.ClassLabel(
                names=["positive", "negative"], is_bucket=False
            ),
            "predicted_label": feature.ClassLabel(
                names=["positive", "negative"], is_bucket=False
            ),
            "label": feature.Value(
                dtype="string",
                description="category",
                is_bucket=True,
                bucket_info=feature.BucketInfo(
                    method="bucket_attribute_discrete_value", number=4, setting=1
                ),
            ),
            "sentence_length": feature.Value(
                dtype="float",
                description="sentence length",
                is_bucket=True,
                bucket_info=feature.BucketInfo(
                    method="bucket_attribute_specified_bucket_value",
                    number=4,
                    setting=(),
                ),
            ),
            "token_number": feature.Value(
                dtype="float",
                description="the number of chars",
                is_bucket=True,
                bucket_info=feature.BucketInfo(
                    method="bucket_attribute_specified_bucket_value",
                    number=4,
                    setting=(),
                ),
            ),
            "entity_number": feature.Value(
                dtype="float",
                description="entity numbers",
                is_bucket=True,
                bucket_info=feature.BucketInfo(
                    method="bucket_attribute_specified_bucket_value",
                    number=4,
                    setting=(),
                ),
            ),
            "aspect_length": feature.Value(
                dtype="float",
                description="aspect length",
                is_bucket=True,
                bucket_info=feature.BucketInfo(
                    method="bucket_attribute_specified_bucket_value",
                    number=4,
                    setting=(),
                ),
            ),
            "aspect_index": feature.Value(
                dtype="float",
                description="aspect position",
                is_bucket=True,
                bucket_info=feature.BucketInfo(
                    method="bucket_attribute_specified_bucket_value",
                    number=4,
                    setting=(),
                ),
            ),
        }
    )
    _default_metrics = ["Accuracy"]

    def __init__(self):
        super().__init__()

    # --- Feature functions accessible by ExplainaboardBuilder._get_feature_func()
    def _get_sentence_length(self, existing_features: dict):
        return len(existing_features["text"].split(" "))

    def _get_token_number(self, existing_feature: dict):
        return len(existing_feature["text"])

    def _get_entity_number(self, existing_feature: dict):
        return len(get_named_entities(existing_feature["text"]))

    def _get_label(self, existing_feature: dict):
        return existing_feature["true_label"]

    def _get_aspect_length(self, existing_features: dict):
        return len(existing_features["aspect"].split(" "))

    def _get_aspect_index(self, existing_features: dict):
        return existing_features["text"].find(existing_features["aspect"])

    # --- End feature functions
