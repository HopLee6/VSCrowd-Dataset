import shutil
from pathlib import Path
import yaml

import numpy as np
from PIL import Image
from tqdm import tqdm

# replace target dir after unzip file
ROOT = Path(r"C:\Users\87658\Documents\dataset\CrowCount\VSCrowd-Dataset")

save_images_path = ROOT / "images"
save_labels_path = ROOT / "labels"


train_images_path = save_images_path / "train"
val_images_path = save_images_path / "val"

if not train_images_path.exists():
    train_images_path.mkdir()
if not val_images_path.exists():
    val_images_path.mkdir()

train_labels_path = save_labels_path / "train"
val_labels_path = save_labels_path / "val"

if not train_labels_path.exists():
    train_labels_path.mkdir()
if not val_labels_path.exists():
    val_labels_path.mkdir()

annotations_dir_path = ROOT / "annotations"

annotations = annotations_dir_path.glob("*.txt")

videos_root_dir_path = ROOT / "videos"

videos_dir_path = videos_root_dir_path.glob("*")


# copy image?
COPY = False
# use gui show bbox?
GUI = False
if GUI:
    import cv2
stop_flag = -1

for video_dir_path in tqdm(videos_dir_path):

    if video_dir_path.is_file():
        continue
    annotation_file_path = annotations_dir_path / (video_dir_path.name + ".txt")

    assert annotation_file_path.exists(), "annotation not found"

    with open(annotation_file_path) as f:
        lines = f.read().strip().split("\n")

    if "train" in video_dir_path.name:
        save_image_dir_path = train_images_path / video_dir_path.name
        save_label_dir_path = train_labels_path / video_dir_path.name
    else:
        save_image_dir_path = val_images_path / video_dir_path.name
        save_label_dir_path = val_labels_path / video_dir_path.name

    # create directory
    if COPY and not save_image_dir_path.exists():
        save_image_dir_path.mkdir()
    if not save_label_dir_path.exists():
        save_label_dir_path.mkdir()

    for line in lines:
        datas = line.split(" ")
        FrameID = datas.pop(0)
        datas = np.array([float(it) for it in datas], dtype=np.float32).reshape(-1, 7)
        image_file_paths = video_dir_path / (FrameID + ".jpg")
        assert image_file_paths.exists(), f"image not found: {image_file_paths}"

        bboxes = datas[:, 1:5]

        image = Image.open(image_file_paths)
        w, h = image.size
        if GUI:
            image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
            for bbox in bboxes:
                bbox = bbox.astype(np.int32)
                image = cv2.rectangle(
                    image, bbox[:2], bbox[2:], (0, 0, 255), 2
                )
            cv2.imshow("image", image)
            stop_flag = cv2.waitKey(100)

        if stop_flag == 27 or stop_flag == ord("q"):
            break

        # xyxy => cxcywh
        datas[..., 3:5] = (datas[..., 1:3] + datas[..., 3:5]) / 2
        datas[..., 1:3] = datas[..., 1:3] + datas[..., 3:5] / 2
        bboxes = datas[:, 1:5]

        bboxes[..., [0, 2]] /= w
        bboxes[..., [1, 3]] /= h

        # copy image file to target file
        if COPY:
            shutil.copy(image_file_paths, save_image_dir_path / (FrameID + ".jpg"))

        # write txt as yolo format
        save_label_path = save_label_dir_path / (FrameID + ".txt")
        output_strs = ["0" + " ".join([str(it) for it in bbox]) for bbox in bboxes]
        with open(save_label_path, "w") as f:
            f.write("\n".join(output_strs))
        del image

    if not COPY:
        # if exist then remove it
        if save_image_dir_path.exists():
            save_image_dir_path.unlink()
        # move the image directory
        shutil.move(video_dir_path, save_image_dir_path)

    if stop_flag == 27:
        break

if GUI:
    cv2.destroyAllWindows()

# make yaml file
dataset_yaml = ROOT / "data.yaml"

if dataset_yaml.exists():
    # 存在则删除文件
    dataset_yaml.unlink()

yaml_data = dict(
    path=str(ROOT),
    train=str(train_images_path),
    val=str(val_images_path),
    nc=1,
    ch=3,
    names=["head"],
)

with open(dataset_yaml, "w") as f:
    yaml.dump(yaml_data, f, indent=4)
