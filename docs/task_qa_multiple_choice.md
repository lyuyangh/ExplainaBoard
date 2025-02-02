# Analyzing Multiple Choices QA

In this file we describe how to analyze multiple-choice QA models.
We will give an example using the  [metaphor_qa](http://datalab.nlpedia.ai/normal_dataset/62139f3dc5fa557614d36df2/dataset_metadata) dataset, but other datasets
can be analyzed in a similar way.

## Data Preparation

In order to perform analysis of your results, they should be in the following json format:

```json
[
    {
        "context": "The girl was as down-to-earth as a Michelin-starred canape",
        "question": "",
        "answers": {
            "text": "The girl was not down-to-earth at all.",
            "option_index": 0
        },
        "options": [
            "The girl was not down-to-earth at all.",
            "The girl was very down-to-earth."
        ],
        "predicted_answers": {
            "text": "The girl was not down-to-earth at all.",
            "option_index": 0
        }
    },
  ...
]
```
where
* `context` represents the text providing context information
* `question` represents the question, which could be null in some scenario
* `options` is a list of string, denoting all potential options.
* `answers` is a dictionary with two elements:
    * `text`: the true answer text
    * `option_index`: the index options for true answer
* `predicted_answers` is a dictionary with two elements:
    * `text`: the predicted answer text
    * `option_index`: the index options for predicted answer
    

Let's say we have several files such as 
* [gpt2.json](https://github.com/neulab/ExplainaBoard/blob/main/data/system_outputs/metaphor_qa/gpt2.json) 


etc. from different systems.


## Performing Basic Analysis

In order to perform your basic analysis, we can run the following command:

```shell
    explainaboard --task qa-multiple-choice --system_outputs ./data/system_outputs/metaphor_qa/gpt2.json > report.json
```
where
* `--task`: denotes the task name, you can find all supported task names [here](https://github.com/neulab/ExplainaBoard/blob/main/docs/supported_tasks.md)
* `--system_outputs`: denote the path of system outputs. Multiple one should be 
  separated by space, for example, system1 system2
* `--dataset`:optional, denotes the dataset name
* `report.json`: the generated analysis file with json format. You can find the file [here](https://github.com/ExpressAI/ExplainaBoard/blob/main/data/reports/report.json). Tips: use a json viewer
                  like [this one](http://jsonviewer.stack.hu/) for better interpretation.




Now let's look at the results to see what sort of interesting insights we can
glean from them.

TODO: add insights

## Advanced Analysis Options

One also can perform pair-wise analysis:
```shell
explainaboard --task qa-multiple-choice --system_outputs model_1 model_2 > report.json
```
where two system outputs are fed separated by space.
* `report.json`: the generated analysis file with json format, whose schema is similar to the above one with single system evaluation except that
   all performance values are obtained using the sys1 subtract sys2.