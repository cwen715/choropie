# Own pie-map
import geopandas

import numpy as np
import matplotlib.pyplot as plt
import pandas
import matplotlib.patches as mpatches
import mapclassify
import matplotlib.patheffects as pe

plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False 

fig,ax = plt.subplots(figsize=(16,20))
plt.style.use("ggplot")
ax.grid(True, linestyle='-')
for row in bj2.to_dict("records"):
    x_loc = row["geometry"].centroid.x
    y_loc = row["geometry"].centroid.y
    r = [0,
         row["常住户籍人口"]/row["常住人口"],
         1]
    for i in range(2):
        x = np.cos(2 * np.pi * np.linspace(r[i], r[i+1]))
        y = np.sin(2 * np.pi * np.linspace(r[i], r[i+1]))
        xy = np.row_stack([[0, 0], np.column_stack([x, y])])
        ax.scatter([x_loc],[y_loc], marker=xy, s=row["常住人口"]*5,
                   facecolor=color[i],alpha=0.9
                  ,zorder=20,
                   path_effects=[pe.withStroke(linewidth=3, foreground="w")])
bj2.plot(ax=ax,column="常住人口密度",cmap="Reds",scheme=scheme,k=k)
labels = ["常住户籍人口比例","常住外来人口比例"]
patches = [mpatches.Patch(color=color[i], 
                          label="{:s}".format(labels[i])) for i in range(len(color))] 

leg1 = ax.legend(handles=patches,fontsize=15,loc=4,
                title="常住人口比例",title_fontsize=17,
                bbox_to_anchor=(0.99,0.2))

cmap = plt.get_cmap("Reds")
bp = mapclassify.NaturalBreaks(np.array(bj2["常住人口密度"]),k=k+1)
if len(bp.bins) < k:
    k = len(bp.bins)-1
patches2 = []
for i in range(k):
    facecolor=cmap(i*(1/(k-1)))
    label=f'{bp.bins[i]} - {bp.bins[i+1]}'
    patches2.append(mpatches.Patch(facecolor=facecolor,label=label))
leg2 = ax.legend(handles=patches2,fontsize=15,loc=4,title="常住人口密度",
                 title_fontsize=17)
plt.gca().add_artist(leg1)
plt.savefig("bj.jpg",bbox_inches='tight',pad_inches=0.3)
