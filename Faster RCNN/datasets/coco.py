# # import os
# # import numpy as np
# # import tensorflow as tf
# # from functools import partial
# # from pycocotools.coco import COCO

# # _COCO_TRAIN_DATASET = None
# # _COCO_VAL_DATASET = None
# # _COCO_TEST_DATASET = None


# # class CoCoDataset:
# #     # global _COCO_TRAIN_DATASET, _COCO_VAL_DATASET, _COCO_TEST_DATASET
# #     def __init__(self, root_dir='../data/COCO2017', sub_dir='train', year='2017'):
# #         if sub_dir not in ['train', 'val', 'minival']:
# #             raise ValueError('unknown sub dir {}'.format(sub_dir))
# #         if year not in ['2014', '2017']:
# #             raise ValueError('unknown year dir {}'.format(year))

# #         annotation_file_path = os.path.join(root_dir, 'annotations', 'instances_{}{}.json'.format(sub_dir, year))
# #         if sub_dir == 'minival':
# #             sub_dir = 'val'
# #         self._image_dir = os.path.join(root_dir, sub_dir + year)
# #         self._coco = COCO(annotation_file=annotation_file_path)
        
# #     @property
# #     def image_id

# #     def _get_category_id_name_dict(self):
# #         '''
# #         getCatIds(catNms=[], supNms=[], catIds=[]) 
# #         通过输入类别的名字、大类的名字或是种类的id，来筛选得到图片所属类别的id 
# #         比如，我们想知道dog类的id是多少
# #         catIds = coco.getCatIds(catNms=['dog'])
# #         '''
# #         category_ids = self._coco.getCatIds()
# #         category_id2name = {0: 'background'}
# #         name2category_id = {'background', 0}
# #         category_id2raw_id = {}
# #         raw_id2category_id = {}
# #         for index, category_id in enumerate(category_ids):
# #             category_name = self._coco.loadCats(category_id)[0]['name']
# #             category_id2name[category_id] = category_name
# #             name2category_id[category_id] = category_id
# #             category_id2raw_id[category_id] = index + 1
# #             raw_id2category_id[index + 1] = category_id
# #         self._category_id2name_dict = category_id2name
# #         self._name2category_id_dict = name2category_id
# #         self._category_id2raw_id = category_id2raw_id
# #         self._raw_id2category_id = raw_id2category_id


# # def get_global_dataset(mode, year, root_dir):
# #     if mode not in ['train', 'val', 'test', 'minival']:
# #         raise ValueError('unknown mode {}'.format(mode))
    
# #     if mode == 'train':
# #         if _COCO_TRAIN_DATASET is None:
# #             _COCO_TRAIN_DATASET = CoCoDataset()

# import os
# import numpy as np
# import tensorflow as tf
# from functools import partial
# from pycocotools.coco import COCO

# from preprocessing.preprocessing import image_argument_with_imgaug, preprocessing_training_func, \
#     preprocessing_eval_func

# _COCO_TRAIN_DATASET = None
# _COCO_VAL_DATASET = None
# _COCO_TEST_DATASET = None


# def _get_global_dataset(mode, year, root_dir):
#     global _COCO_TRAIN_DATASET, _COCO_VAL_DATASET, _COCO_TEST_DATASET
#     if mode not in ['train', 'val', 'test', 'minival']:
#         raise ValueError('unknown mode {}'.format(mode))
#     if mode == 'train':
#         if _COCO_TRAIN_DATASET is None:
#             _COCO_TRAIN_DATASET = CocoDataset(root_dir=root_dir, sub_dir=mode, year=year)
#         coco_dataset = _COCO_TRAIN_DATASET
#     elif mode == 'val':
#         if _COCO_VAL_DATASET is None:
#             _COCO_VAL_DATASET = CocoDataset(root_dir=root_dir, sub_dir=mode, year=year)
#         coco_dataset = _COCO_VAL_DATASET
#     else:
#         if _COCO_TEST_DATASET is None:
#             _COCO_TEST_DATASET = CocoDataset(root_dir=root_dir, sub_dir=mode, year=year)
#         coco_dataset = _COCO_TEST_DATASET
#     return coco_dataset


# class CocoDataset:
#     def __init__(self, root_dir='/ssd/zhangyiyang/COCO2017', sub_dir='train', year="2017",
#                  min_edge=32, ):
#         if sub_dir not in ['train', 'val', 'minival']:
#             raise ValueError('unknown sub dir {}'.format(sub_dir))
#         if year not in ['2014', '2017']:
#             raise ValueError('unknown year dir {}'.format(year))

#         annotation_file_path = os.path.join(root_dir, 'annotations', 'instances_{}{}.json'.format(sub_dir, year))
#         if sub_dir == 'minival':
#             sub_dir = 'val'
#         self._image_dir = os.path.join(root_dir, sub_dir + year)

#         self._coco = COCO(annotation_file=annotation_file_path)
#         self._get_cat_id_name_dict()
#         self._img_ids, self._img_info_dict = self._filter_images(min_edge=min_edge)

#     @property
#     def img_ids(self):
#         return self._img_ids

#     @property
#     def img_info_dict(self):
#         return self._img_info_dict

#     @property
#     def cat_id_to_name_dict(self):
#         return self._cat_id_to_name_dict

#     @property
#     def name_to_cat_id_dict(self):
#         return self._name_to_cat_id_dict

#     @property
#     def cat_id_to_raw_id(self):
#         return self._cat_id_to_raw_id

#     @property
#     def raw_id_to_cat_id(self):
#         return self._raw_id_to_cat_id

#     def _get_cat_id_name_dict(self):
#         cat_ids = self._coco.getCatIds()
#         cat_id_to_name = {0: 'background'}
#         name_to_cat_id = {'background': 0}
#         cat_id_to_raw_id = {}
#         raw_id_to_cat_id = {}
#         for idx, cat_id in enumerate(cat_ids):
#             cat_name = self._coco.loadCats(cat_id)[0]['name']
#             cat_id_to_name[cat_id] = cat_name
#             name_to_cat_id[cat_name] = cat_id
#             cat_id_to_raw_id[cat_id] = idx + 1
#             raw_id_to_cat_id[idx + 1] = cat_id
#         self._cat_id_to_name_dict = cat_id_to_name
#         self._name_to_cat_id_dict = name_to_cat_id
#         self._cat_id_to_raw_id = cat_id_to_raw_id
#         self._raw_id_to_cat_id = raw_id_to_cat_id

#     def _filter_images(self, min_edge):
#         all_img_ids = list(set([_['image_id'] for _ in self._coco.anns.values()]))
#         img_ids = []
#         img_info_dict = {}
#         for i in all_img_ids:
#             info = self._coco.loadImgs(i)[0]

#             ann_ids = self._coco.getAnnIds(imgIds=i)
#             ann_info = self._coco.loadAnns(ann_ids)
#             _, labels, _ = self._parse_ann_info(ann_info)

#             if min(info['width'], info['height']) >= min_edge and labels.shape[0] != 0:
#                 img_ids.append(i)
#                 img_info_dict[i] = info
#         return img_ids, img_info_dict

#     def _parse_ann_info(self, ann_infos):
#         """Parse bbox annotation.
#         Args
#         ---
#             ann_info (list[dict]): Annotation info of an image.
#         Returns
#         ---
#             dict: A dict containing the following keys: bboxes,
#                 bboxes_ignore, labels.
#         """
#         gt_bboxes = []
#         gt_labels = []
#         gt_labels_text = []

#         for i, ann in enumerate(ann_infos):
#             if ann.get('ignore', False):
#                 continue
#             x1, y1, w, h = ann['bbox']
#             if ann['area'] <= 0 or w < 1 or h < 1:
#                 continue
#             bbox = [y1, x1, y1 + h - 1., x1 + w - 1.]
#             gt_bboxes.append(bbox)
#             gt_labels.append(self._cat_id_to_raw_id[ann['category_id']])
#             gt_labels_text.append(self._cat_id_to_name_dict[ann['category_id']])

#         if gt_bboxes:
#             gt_bboxes = np.array(gt_bboxes, dtype=np.float32)
#             gt_labels = np.array(gt_labels, dtype=np.int64)
#             gt_labels_text = np.array(gt_labels_text, dtype=np.string_)
#         else:
#             gt_bboxes = np.zeros((0, 4), dtype=np.float32)
#             gt_labels = np.array([], dtype=np.int64)
#             gt_labels_text = np.array([], dtype=np.string_)

#         return gt_bboxes, gt_labels, gt_labels_text

#     def __getitem__(self, img_id):
#         # 获取 annotation dict 信息
#         ann_ids = self._coco.getAnnIds(imgIds=img_id)
#         ann_infos = self._coco.loadAnns(ann_ids)
#         gt_bboxes, gt_labels, _ = self._parse_ann_info(ann_infos)

#         # 设置 bboxes 范围为 [0, 1]
#         image_height, image_width = self._img_info_dict[img_id]['height'], self._img_info_dict[img_id]['width']
#         gt_bboxes[:, ::2] = gt_bboxes[:, ::2] / image_height
#         gt_bboxes[:, 1::2] = gt_bboxes[:, 1::2] / image_width

#         file_path = os.path.join(self._image_dir, self._img_info_dict[img_id]['file_name'])
#         return file_path, gt_bboxes, image_height, image_width, gt_labels


# def get_training_dataset(root_dir='D:\\data\\COCO2017',
#                          mode='train', year="2017",
#                          min_size=600, max_size=1000,
#                          preprocessing_type='caffe', caffe_pixel_means=None,
#                          batch_size=1,
#                          repeat=1,
#                          shuffle=False, shuffle_buffer_size=1000,
#                          prefetch=False, prefetch_buffer_size=1000,
#                          argument=True, iaa_sequence=None):
#     coco_dataset = _get_global_dataset(mode, year, root_dir)

#     def _parse_coco_data_py(img_id):
#         file_path, gt_bboxes, image_height, image_width, gt_labels = coco_dataset[img_id]
#         return file_path, gt_bboxes, image_height, image_width, gt_labels

#     tf_dataset = tf.data.Dataset.from_tensor_slices(coco_dataset.img_ids).map(
#         lambda img_id: tuple([*tf.py_func(_parse_coco_data_py, [img_id],
#                                           [tf.string, tf.float32, tf.int64, tf.int64, tf.int64])])
#     )

#     tf_dataset = tf_dataset.map(
#         lambda file_path, gt_bboxes, image_height, image_width, gt_labels: tuple([
#             tf.image.decode_jpeg(tf.read_file(file_path), channels=3),
#             gt_bboxes, image_height, image_width, gt_labels
#         ])
#     )

#     if argument:
#         image_argument_partial = partial(image_argument_with_imgaug, iaa_sequence=iaa_sequence)
#         tf_dataset = tf_dataset.map(
#             lambda image, bboxes, image_height, image_width, labels: tuple([
#                 *tf.py_func(image_argument_partial, [image, bboxes], [image.dtype, bboxes.dtype]),
#                 image_height, image_width, labels]),
#             num_parallel_calls=5
#         )

#     preprocessing_partial_func = partial(preprocessing_training_func,
#                                          min_size=min_size, max_size=max_size,
#                                          preprocessing_type=preprocessing_type, caffe_pixel_means=caffe_pixel_means)

#     tf_dataset = tf_dataset.batch(batch_size=batch_size).map(preprocessing_partial_func, num_parallel_calls=5)

#     if shuffle:
#         tf_dataset = tf_dataset.shuffle(buffer_size=shuffle_buffer_size)
#     if prefetch:
#         tf_dataset = tf_dataset.prefetch(buffer_size=prefetch_buffer_size)

#     return tf_dataset.repeat(repeat)


# def get_eval_dataset(root_dir='D:\\data\\COCO2017',
#                      mode='train', year='2017',
#                      min_size=600, max_size=1000,
#                      preprocessing_type='caffe', caffe_pixel_means=None,
#                      batch_size=1,
#                      repeat=1, ):
#     coco_dataset = _get_global_dataset(mode, year, root_dir)

#     preprocessing_partial_func = partial(preprocessing_eval_func,
#                                          min_size=min_size, max_size=max_size,
#                                          preprocessing_type=preprocessing_type, caffe_pixel_means=caffe_pixel_means)

#     def _parse_coco_data_py(img_id):
#         file_path, _, img_height, img_width, _ = coco_dataset[img_id]
#         img = tf.image.decode_jpeg(tf.read_file(file_path), channels=3)
#         return img, img_height, img_width, img_id

#     def _preprocessing_after_batch(img, img_height, img_width, img_id):
#         img, img_scale, img_height, img_width = preprocessing_partial_func(img, img_height, img_width)
#         return img, img_scale, img_height, img_width, img_id[0]

#     tf_dataset = tf.data.Dataset.from_tensor_slices(coco_dataset.img_ids).map(
#         lambda img_id: tuple([*tf.py_func(_parse_coco_data_py, [img_id],
#                                           [tf.uint8, tf.int64, tf.int64, tf.int32])])
#     ).batch(batch_size).map(_preprocessing_after_batch)

#     return tf_dataset.repeat(repeat)