import pandas as pd
import datasets
import os
import logging

# 数据集路径设置
META_DATA_PATH = "/root/autodl-tmp/RoboTwin/data/dataset.jsonl"
IMAGE_DIR = ""         #输入文件夹路径
CONDITION_IMAGE_DIR = ""      #输出文件夹路径


# 定义数据集中有哪些特征，及其类型
_FEATURES = datasets.Features(
    {
        "input_image": datasets.Image(),
        "output_image": datasets.Image(),
        "edit_prompt": datasets.Value("string"),
    },
)


# 定义数据集
class roboframe(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [datasets.BuilderConfig(name="default", version=datasets.Version("0.0.2"))]
    DEFAULT_CONFIG_NAME = "default"

    def _info(self):
        return datasets.DatasetInfo(
            description="None",
            features=_FEATURES,
            supervised_keys=None,
            homepage="None",
            license="None",
            citation="None",
        )

    def _split_generators(self, dl_manager):

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "metadata_path": META_DATA_PATH,
                    "images_dir": IMAGE_DIR,
                    "conditioning_images_dir": CONDITION_IMAGE_DIR,
                },
            ),
        ]

    def _generate_examples(self, metadata_path, images_dir, conditioning_images_dir):
        metadata = pd.read_json(metadata_path, lines=True)

        for i, row in metadata.iterrows():
            text = row["edit_prompt"]

            image_path = row["input_image"]
            image_path = os.path.join(images_dir, image_path)

            # 打开文件错误时直接跳过
            try:
                image = open(image_path, "rb").read()
            except Exception as e:
                logging.error(e)
                continue

            conditioning_image_path = os.path.join(
                conditioning_images_dir, row["output_image"]
            )

            # 打开文件错误直接跳过
            try:
                conditioning_image = open(conditioning_image_path, "rb").read()
            except Exception as e:
                logging.error(e)
                continue

            yield row["input_image"], {
                "edit_prompt": text,
                "input_image": {
                    "path": image_path,
                    "bytes": image,
                },
                "output_image": {
                    "path": conditioning_image_path,
                    "bytes": conditioning_image,
                },
            }


    # def _generate_examples(self, metadata_path, images_dir, conditioning_images_dir):
    #     metadata = pd.read_json(metadata_path, lines=True)
    #     row1=metadata.iloc[0]
    #     text = row1["text"]

    #     for t in range(400):
    #         i=t+1
            

    #         image_path = row1["input_image"]
    #         image_path = os.path.join(images_dir, image_path)

    #         # 打开文件错误时直接跳过
    #         try:
    #             image = open(image_path, "rb").read()
    #         except Exception as e:
    #             logging.error(e)
    #             continue

    #         conditioning_image_path = os.path.join(
    #             conditioning_images_dir, row1["output_image"].format(i=i)
    #         )

    #         # 打开文件错误直接跳过
    #         try:
    #             conditioning_image = open(conditioning_image_path, "rb").read()
    #         except Exception as e:
    #             logging.error(e)
    #             continue

    #         yield row1["input_image"].format(i=i), {
    #             "text": text,
    #             "input_image": {
    #                 "path": image_path,
    #                 "bytes": image,
    #             },
    #             "output_image": {
    #                 "path": conditioning_image_path,
    #                 "bytes": conditioning_image,
    #             },
    #         }
