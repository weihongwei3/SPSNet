# encoding: utf-8
"""
@author:  sherlock
@contact: sherlockliao01@gmail.com

@author: Li Tianjiao
@contact: tianjiao_li@mymail.sutd.edu.sg
"""

import glob
import re

import os.path as osp

from .bases import BaseImageDataset


class UAVHuman(BaseImageDataset):

    def __init__(self, root='./data',
                 verbose=True, **kwargs):
        super(UAVHuman, self).__init__()
        # self.dataset_dir = '/data0/ReIDData/uav_reid_data/'
        self.dataset_dir = '../../Dataset/uavhumanReID/'
        self.train_dir = osp.join(self.dataset_dir, 'bounding_box_train')


        self.query_dir = osp.join(self.dataset_dir, 'query')
        self.gallery_dir = osp.join(self.dataset_dir, 'bounding_box_test')


        self._check_before_run()

        train = self._process_dir(self.train_dir, relabel=True)

        query = self._process_dir(self.query_dir, relabel=False)
        gallery = self._process_dir(self.gallery_dir, relabel=False)


        if verbose:
            print("=> UAVHuman loaded")

            self.print_dataset_statistics(train, query, gallery)

        self.train = train

        self.query = query
        self.gallery = gallery


        self.num_train_pids, self.num_train_imgs, self.num_train_cams, self.num_train_vids  = self.get_imagedata_info(self.train)
        self.num_query_pids, self.num_query_imgs, self.num_query_cams, self.num_query_vids  = self.get_imagedata_info(self.query)
        self.num_gallery_pids, self.num_gallery_imgs, self.num_gallery_cams,self.num_gallery_vids = self.get_imagedata_info(self.gallery)


    def _check_before_run(self):
        """Check if all files are available before going deeper"""
        if not osp.exists(self.dataset_dir):
            raise RuntimeError("'{}' is not available".format(self.dataset_dir))
        if not osp.exists(self.train_dir):
            raise RuntimeError("'{}' is not available".format(self.train_dir))
        if not osp.exists(self.query_dir):
            raise RuntimeError("'{}' is not available".format(self.query_dir))
        if not osp.exists(self.gallery_dir):
            raise RuntimeError("'{}' is not available".format(self.gallery_dir))


    def _process_dir(self, dir_path, relabel=False):
        img_paths = glob.glob(osp.join(dir_path, '*.jpg'))
        pattern_pid = re.compile(r'P([-\d]+)S([-\d]+)')
        pattern_camid = re.compile(r'A([-\d]+)R([-\d])_([-\d]+)_([-\d]+)')
        distractor_pid = 50000

        pid_container = set()
        for img_path in img_paths:
            fname = osp.split(img_path)[-1]
            if fname.startswith('D'):
                pid = int(distractor_pid)
            else:
                pid_part1, pid_part2 = pattern_pid.search(fname).groups()
                pid = int(pid_part1 + pid_part2)

            if pid == -1: continue  # junk images are just ignored
            if pid == 3109 or pid == 8405:
                import ipdb;
                ipdb.set_trace()
                continue

            pid_container.add(pid)
        pid2label = {pid: label for label, pid in enumerate(pid_container)}

        dataset = []
        for img_path in img_paths:
            fname = osp.split(img_path)[-1]
            if fname.startswith('D'):
                pid = int(distractor_pid)
                camid = int(fname[-13:-8])
            else:
                pid_part1, pid_part2 = pattern_pid.search(fname).groups()
                pid = int(pid_part1 + pid_part2)
                camid_part1, _, _, camid_part2 = pattern_camid.search(fname).groups()
                camid = int(camid_part1 + camid_part2)
            if pid == -1: continue  # junk images are just ignored
            if relabel: pid = pid2label[pid]
            dataset.append((img_path, pid, camid,1))

        return dataset









# # encoding: utf-8
# """
# @author:  sherlock
# @contact: sherlockliao01@gmail.com
#
# @author: Li Tianjiao
# @contact: tianjiao_li@mymail.sutd.edu.sg
# """
#
# import glob
# import re
#
# import os.path as osp
#
# from .bases import BaseImageDataset
#
#
# class UAVHuman(BaseImageDataset):
#
#     def __init__(self, root='/data0/ReIDData/uav_reid_data',
#                  verbose=False, **kwargs):
#         super(UAVHuman, self).__init__()
#         self.dataset_dir = '/data0/ReIDData/uav_reid_data/submit_trans_reid'
#         self.dataset_dir_1 = '/data0/ReIDData/uav_reid_data'
#         self.train_dir = osp.join(self.dataset_dir, 'bounding_box_train')
#
#         """Comment for Competition Splits
#         self.query_dir = osp.join(self.dataset_dir, 'query')
#         self.gallery_dir = osp.join(self.dataset_dir, 'bounding_box_test')
#         """
#         self.query_dir = osp.join(self.dataset_dir_1, 'query')
#         self.gallery_dir = osp.join(self.dataset_dir_1, 'bounding_box_test')
#
#         self._check_before_run()
#
#         train = self._process_dir(self.train_dir, relabel=True)
#         query = self._process_dir(self.query_dir, relabel=False)
#         gallery = self._process_dir(self.gallery_dir, relabel=False)
#         print("")
#
#         """Comment for Competition Splits
#         query = self._process_dir(self.query_dir, relabel=False)
#         gallery = self._process_dir(self.gallery_dir, relabel=False)
#         """
#
#         if verbose:
#             print("=> UAVHuman loaded")
#
#             """Comment for Competition Split
#             self.print_dataset_statistics(train, query, gallery)
#             """
#
#             self.print_dataset_statistics_for_train_only(train)
#
#         self.train = train
#         self.query = query
#         self.gallery = gallery
#         print(" ")
#
#         """Comment for Competition Splits
#         # self.query = query
#         # self.gallery = gallery
#         """
#
#         self.num_train_pids, self.num_train_imgs, self.num_train_cams, self.num_train_vids = self.get_imagedata_info(
#             self.train)
#         self.num_query_pids, self.num_query_imgs, self.num_query_cams, self.num_train_vids = self.get_imagedata_info(
#             self.query)
#         self.num_gallery_pids, self.num_gallery_imgs, self.num_gallery_cams, self.num_train_vids = self.get_imagedata_info(
#             self.gallery)
#
#         """Comment for Competition Splits
#         self.num_query_pids, self.num_query_imgs, self.num_query_cams = self.get_imagedata_info(self.query)
#         self.num_gallery_pids, self.num_gallery_imgs, self.num_gallery_cams = self.get_imagedata_info(self.gallery)
#         """
#
#     def _check_before_run(self):
#         """Check if all files are available before going deeper"""
#         if not osp.exists(self.dataset_dir):
#             raise RuntimeError("'{}' is not available".format(self.dataset_dir))
#         if not osp.exists(self.train_dir):
#             raise RuntimeError("'{}' is not available".format(self.train_dir))
#
#         """Comment for Competition Splits
#         if not osp.exists(self.query_dir):
#             raise RuntimeError("'{}' is not available".format(self.query_dir))
#         if not osp.exists(self.gallery_dir):
#             raise RuntimeError("'{}' is not available".format(self.gallery_dir))
#         """
#
#     def _process_dir(self, dir_path, relabel=False):
#         img_paths = glob.glob(osp.join(dir_path, '*.jpg'))
#         pattern_pid = re.compile(r'P([-\d]+)S([-\d]+)')
#         pattern_camid = re.compile(r'A([-\d]+)R([-\d])_([-\d]+)_([-\d]+)')
#         distractor_pid = 50000
#
#         pid_container = set()
#         for img_path in img_paths:
#             fname = osp.split(img_path)[-1]
#             if fname.startswith('D'):
#                 pid = int(distractor_pid)
#             else:
#                 pid_part1, pid_part2 = pattern_pid.search(fname).groups()
#                 pid = int(pid_part1 + pid_part2)
#
#             if pid == -1: continue  # junk images are just ignored
#             if pid == 3109 or pid == 8405:
#                 import ipdb;
#                 ipdb.set_trace()
#                 continue
#
#             pid_container.add(pid)
#         pid2label = {pid: label for label, pid in enumerate(pid_container)}
#
#         dataset = []
#         for img_path in img_paths:
#             fname = osp.split(img_path)[-1]
#             if fname.startswith('D'):
#                 pid = int(distractor_pid)
#                 camid = int(fname[-13:-8])
#             else:
#                 pid_part1, pid_part2 = pattern_pid.search(fname).groups()
#                 pid = int(pid_part1 + pid_part2)
#                 camid_part1, _, _, camid_part2 = pattern_camid.search(fname).groups()
#                 camid = int(camid_part1 + camid_part2)
#             if pid == -1: continue  # junk images are just ignored
#             if relabel: pid = pid2label[pid]
#             dataset.append((img_path, pid, camid, 1))
#
#         return dataset
#
#     def _process_dir_2(self, dir_path, relabel=False):
#         img_paths = glob.glob(osp.join(dir_path, '*.jpg'))
#         pattern = re.compile(r'([-\d]+)_([-\d]+)_c(\d+)')
#
#         pid_container = set()
#         for img_path in sorted(img_paths):
#             _, pid, _ = map(int, pattern.search(img_path).groups())
#             # if pid == -1: continue  # junk images are just ignored
#             pid_container.add(pid)
#         pid2label = {pid: label for label, pid in enumerate(pid_container)}
#         dataset = []
#         for img_path in sorted(img_paths):
#             _, pid, camid = map(int, pattern.search(img_path).groups())
#             # if pid == -1: continue  # junk images are just ignored
#             # assert 0 <= pid <= 1501  # pid == 0 means background
#             # assert 1 <= camid <= 6
#             # camid -= 1  # index starts from 0
#             if relabel: pid = pid2label[pid]
#
#             dataset.append((img_path, pid, camid, 1))
#         return dataset
#
#     def _process_dir_3(self, dir_path, relabel=False):
#         img_paths = glob.glob(osp.join(dir_path, '*.jpg'))
#         pattern = re.compile(r'([-\d]+)_c([-\d]+)')
#
#         pid_container = set()
#         for img_path in sorted(img_paths):
#             _, pid = map(int, pattern.search(img_path).groups())
#             # if pid == -1: continue  # junk images are just ignored
#             pid_container.add(pid)
#         pid2label = {pid: label for label, pid in enumerate(pid_container)}
#         dataset = []
#         for img_path in sorted(img_paths):
#             camid, pid = map(int, pattern.search(img_path).groups())
#             # if pid == -1: continue  # junk images are just ignored
#             # assert 0 <= pid <= 1501  # pid == 0 means background
#             # assert 1 <= camid <= 6
#             # camid -= 1  # index starts from 0
#             if relabel: pid = pid2label[pid]
#
#             dataset.append((img_path, pid, camid, 1))
#         return dataset
#
