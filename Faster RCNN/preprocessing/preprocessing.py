import tensorflow as tf
import numpy as np
import imgaug as ia
from imgaug import augmenters as iaa
from functools import partial

def _get_default_iaa_sequence():
    return [
        iaa.Fliplr(0.5),
    ]



def image_argument_with_imgaug(image, bboxes, iaa_sequence=None):
    """
    增强一张图片
    输入图像是 tf.uint8 类型，数据范围 [0, 255]
    输入bboxes是 tf.float32 类型，数据范围 [0, 1]
    返回结果与输入相同
    :param image:   一张图片，类型为ndarray，shape为[None, None, 3]
    :param bboxes:  一组bounding box，shape 为 [bbox_number, 4]，顺序为 ymin, xmin, ymax, xmax
                        float类型，取值范围[0, 1]
    :param iaa_sequence:
    :return:        图像增强结果，包括image和bbox，其格式与输入相同
    """ 
    bboxes_list = []
    height, width, channels = image.shape
    for bbox in bboxes:
        ymin, xmin, ymax, xmax = int(bbox[0] * height), int(bbox[1] * width), int(bbox[2] * height), int(bbox[3] * width)
        bboxes_list.append(ia.BoundingBox(x1=xmin, y1=ymin, x2=xmax, y2=ymax))
    bboxes_ia = ia.BoundingBoxesOnImage(bboxes_list, shape=image.shape)

    if iaa_sequence is None:
        iaa_sequence = _get_default_iaa_sequence()
    seq = iaa.Sequential(iaa_sequence)

    seq_det = seq.to_deterministic()

    image_aug = seq_det.augment_images([image])[0]
    bbs_aug = seq_det.augment_bounding_boxes([bboxes_ia])[0]

    bboxes_aug_list = []
    height, width, channels = image_aug.shape
    for iaa_bbox in bbs_aug.bounding_boxes:
        bboxes_aug_list.append([iaa_bbox.y1 / height, iaa_bbox.x1 / width, iaa_bbox.y2 / height, iaa_bbox.x2 / width])
    bboxes_aug_np = np.array(bboxes_aug_list)
    bboxes_aug_np[bboxes_aug_np < 0] = 0
    bboxes_aug_np[bboxes_aug_np > 1] = 1
    return image_aug, bboxes_aug_np.astype(np.float32)


def _caffe_preprocessing(image, pixel_means):
    # 输入 uint8 RGB 的图像，转换为 tf.float32 BGR 格式，并减去 imagenet 平均数
    image = tf.cast(image, tf.float32)
    image = tf.reverse(image, axis=[-1])
    channels = tf.split(axis=-1, value=image, num_or_size_splits=3)
    channels = [channels[i] - pixel_means[i] for i in range(3)]
    return tf.concat(axis=-1, values=channels)


def _tf_preprocessing(image):
    # 输入 uint8 RGB 的图像，转换为 tf.float32 RGB 格式，取值范围[-1, 1]
    return tf.image.convert_image_dtype(image, dtype=tf.float32) * 2.0 - 1.0


def preprocessing_training_func(image, bboxes, height, width, labels,
                                min_size, max_size, preprocessing_type, caffe_pixel_means=None):
    """
    输入 rgb 图片，进行以下预处理
    1) 短边最短为 min_size，长边最长为 max_size，矛盾时，优先满足长边
    2) 通过 preprocessing_type 选择 preprocessing 函数
    """

    if preprocessing_type == 'caffe':
        preprocessing_fn = partial(_caffe_preprocessing, pixel_means=caffe_pixel_means)
    elif preprocessing_type == 'tf':
        preprocessing_fn = _tf_preprocessing
    else:
        raise ValueError('unknown preprocessing type {}'.format(preprocessing_type))
    
    image = preprocessing_fn(image)
    height = tf.cast(height[0], dtype=tf.float32)
    width = tf.cast(width[0], dtype=tf.float32)

    # 短边最短为 min_size，长边最长为 max_size．矛盾时，优先满足长边
    min_scale = min_size / tf.minimum(height, width)
    max_scale = max_size / tf.maximum(height, width)
    scale = tf.minimum(min_scale, max_scale)


    height = tf.cast(scale * height, dtype=tf.int32)
    width = tf.cast(scale * width, dtype=tf.int32)

    image = tf.image.resize_bilinear(image, (height, width))

    channels = tf.split(axis=-1, num_or_size_splits=4, value=bboxes)
    channels[0] = channels[0] * tf.cast(height, dtype=tf.float32)
    channels[1] = channels[1] * tf.cast(width, dtype=tf.float32)
    channels[2] = channels[2] * tf.cast(height, dtype=tf.float32)
    channels[3] = channels[3] * tf.cast(width, dtype=tf.float32)
    bboxes = tf.concat(channels, axis=-1)

    return image, bboxes, labels


def preprocessing_eval_func(image, height, width,
                            min_size, max_size, preprocessing_type, caffe_pixel_means=None):
    """
    输入 rgb 图片，进行以下预处理
    1) 短边最短为 min_size，长边最长为 max_size，矛盾时，优先满足长边
    2) 通过 preprocessing_type 选择 preprocessing 函数
    """
    if preprocessing_type == 'caffe':
        preprocessing_fn = partial(_caffe_preprocessing, pixel_means=caffe_pixel_means)
    elif preprocessing_type == 'tf':
        preprocessing_fn = _tf_preprocessing
    else:
        raise ValueError('unknown preprocessing type {}'.format(preprocessing_type))
    image = preprocessing_fn(image)

    height = tf.to_float(height[0])
    width = tf.to_float(width[0])
    scale1 = min_size / tf.minimum(height, width)
    scale2 = max_size / tf.maximum(height, width)
    scale = tf.minimum(scale1, scale2)
    n_height = tf.to_int32(scale * height)
    n_width = tf.to_int32(scale * width)

    image = tf.image.resize_bilinear(image, (n_height, n_width))

    return image, scale, tf.to_int32(height), tf.to_int32(width)