#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gpxpy
import matplotlib.pyplot as plt
import numpy as np
import sys

lat = []
lon = []
ele = []
dis = []
dis_all = []

# ヒュベニの公式
def hyubeni(pre_lat,next_lat,pre_lon,next_lon):
    pre_lat = pre_lat * np.pi / 180
    next_lat = next_lat * np.pi / 180
    pre_lon = pre_lon * np.pi / 180
    next_lon = next_lon * np.pi / 180
    elat = next_lat - pre_lat
    elon = next_lon - pre_lon
    mlat = elat/2
     
    M = 6334834/ np.sqrt((1- 0.006674 * np.sin(mlat) * np.sin(mlat)**3))
    N = 6377397/ np.sqrt(1-0.006674 * np.sin(mlat) * np.sin(mlat))
     
    dis = np.sqrt((M * elon) * (M * elon) + (N * np.cos(mlat) * elon) * (N * np.cos(mlat) * elon))
    return(dis)

# 距離を計算する
def calc_distance():
    # 二点間の距離を計算
    for count in range(len(lon)):
        if count == 0:
            dis.append(0)
        else:
            pre_lon = lon[count-1]
            next_lon = lon[count]
            pre_lat = lat[count-1]
            next_lat = lat[count]
            dis.append(hyubeni(pre_lat,next_lat,pre_lon,next_lon))
    # 距離を積算し，走行距離の計算と格納
    for count in range(len(lon)):
        if count == 0:
            dis_all.append(dis[count])
        else:
            dis_all.append(dis_all[count-1]+dis[count])
    # 距離の単位をkmに
    for count in range(len(lon)):
            dis_all[count] = dis_all[count]/1000

args = sys.argv

# gpx_file = open(args[0], 'r')
gpx_file = open('yamap_2020-03-21_08_37.gpx','r')
gpx = gpxpy.parse(gpx_file)

# 緯度・軽度・標高データの格納
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            # 各データを抽出
            lat.append(point.latitude)
            lon.append(point.longitude)
            ele.append(point.elevation)

# 距離の計算
calc_distance()

fig = plt.figure(facecolor='0.05')

# 座標をプロットする設定
coordinate_ax = fig.add_subplot(2,1,1)
coordinate_ax.set_aspect('equal', adjustable='box')
coordinate_ax.set_axis_off()
# 標高をプロットする設定
elevation_ax = fig.add_subplot(2,1,2)
# いい感じのアスペクト比にする
elevation_ax.set_aspect('0.012', adjustable='box')
elevation_ax.set_xlim(0.,25.)
elevation_ax.set_xlabel("distance[km]", fontsize = 12)
elevation_ax.set_ylabel("elevation[m]", fontsize = 12)

# 軸の設定
axis=['top', 'bottom', 'left', 'right']
line_width=[0,2,2,0]
for a,w in zip(axis, line_width):
    elevation_ax.spines[a].set_linewidth(w)

# グラフをプロット
coordinate_ax.plot(lon, lat, color ='white', lw = 3, alpha = 1 )
elevation_ax.plot(dis_all,ele, color ='white', lw = 3, alpha = 1 )
# plt.show()
plt.savefig("result.png",transparent=True, bbox_inches='tight', pad_inches=0, dpi=300)


