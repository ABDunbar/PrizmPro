import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

data = pd.read_csv("314-3_GR_at_1m_interval.csv")

data = data[(data.DEPTH > 2672) & (data.DEPTH < 2932)]
# data.head()

data["sand-shale"] = data["GR"].apply(lambda x: 0 if x > 70 else 1)
# data.sample(10)

# reverse dataframe so window works from bottom up (deeper -> shallower)
df = data.iloc[::-1]  # may need to reset index??

# step to test if resetting index has any impact...
# comment out if not used
df = df.reset_index(drop=True)
# df.head()

# Calculate moving window averages
df["NTG"] = df["sand-shale"].rolling(15, center=True).mean()
df["NTG10"] = df["sand-shale"].rolling(10, center=True).mean()
df["NTG15"] = df["sand-shale"].rolling(15, center=True).mean()
df["NTG21"] = df["sand-shale"].rolling(21, center=True).mean()
df["NTG29"] = df["sand-shale"].rolling(29, center=True).mean()

# Override window edge effects by zeroing out non-reservoir sections
df["NTG"] = np.where(df["sand-shale"] == 0, 0, df["NTG"])
df["NTG10"] = np.where(df["sand-shale"] == 0, 0, df["NTG10"])
df["NTG15"] = np.where(df["sand-shale"] == 0, 0, df["NTG15"])
df["NTG21"] = np.where(df["sand-shale"] == 0, 0, df["NTG21"])
df["NTG29"] = np.where(df["sand-shale"] == 0, 0, df["NTG29"])

# top and base of Statfjord at 31/4-3 well
df = df[(df.DEPTH > 2702) & (df.DEPTH < 2880)]

fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(1, 5, sharey=True, figsize=(10, 10))

# PLOTS
ax1.plot(df["GR"], df["DEPTH"], color="k", lw=0.5)
ax1.fill_betweenx(df["DEPTH"], 70, df["GR"], where=df["GR"] <= 70, facecolor="#fbce50")
ax1.fill_betweenx(df["DEPTH"], 70, df["GR"], where=df["GR"] >= 70, facecolor="#bca89f")
ax1.axvline(x=70, color="k", linestyle="-")
ax2.plot(df["sand-shale"], df["DEPTH"], color="#fbce50")
ax2.fill_betweenx(
    df["DEPTH"], 0, df["NTG10"], where=df["NTG10"] >= 0, facecolor="#fbce50"
)
ax2.plot(df["NTG10"], df["DEPTH"])
ax3.plot(df["sand-shale"], df["DEPTH"], color="#fbce50")
ax3.plot(df["NTG"], df["DEPTH"], color="k")
ax3.fill_betweenx(df["DEPTH"], 0, df["NTG"], where=df["NTG"] >= 0, facecolor="#fbce50")
ax4.plot(df["sand-shale"], df["DEPTH"], color="#fbce50")
ax4.fill_betweenx(
    df["DEPTH"], 0, df["NTG21"], where=df["NTG21"] >= 0, facecolor="#fbce50"
)
ax4.plot(df["NTG21"], df["DEPTH"])
ax5.plot(df["sand-shale"], df["DEPTH"], color="#fbce50")
ax5.fill_betweenx(
    df["DEPTH"], 0, df["NTG29"], where=df["NTG29"] >= 0, facecolor="#fbce50"
)
ax5.plot(df["NTG29"], df["DEPTH"])

# TITLES, LABELS
fig.suptitle(
    "Comparison of Moving Window Average (MWA) calculations of Net-to-gross (NTG)"
)
ax1.set_title("GR")
ax1.set_xlabel("API")
ax1.set_ylabel("Depth [mMD]")
ax2.set_title("MWA NTG\n[10m]")
ax3.set_xlabel("Net-to-gross")
ax3.set_title("MWA NTG\n[15m]")
ax4.set_title("MWA NTG\n[21m]")
ax5.set_title("MWA NTG\n[29m]")

ax1.set_xlim(30, 120)
ax2.set_xlim(1, 0)
ax3.set_xlim(1, 0)
ax4.set_xlim(1, 0)
ax5.set_xlim(1, 0)  # ; ax6.set_xlim(1,0)
plt.gca().invert_yaxis()
# plt.setp(ax2.get_yticklabels(), visible=False)
# plt.legend()
plt.show()

channel_width_percent = {
    "NTG": [5, 15, 25, 35, 45, 55, 65, 75, 85, 95],
    "10pc": [70, 75, 90, 110, 110, 155, 170, 225, 240, 250],
    "20pc": [90, 100, 120, 150, 155, 220, 250, 300, 300, 320],
    "30pc": [120, 130, 145, 200, 205, 260, 340, 355, 375, 450],
    "40pc": [145, 145, 200, 240, 290, 355, 470, 520, 500, 510],
    "50pc": [170, 195, 230, 350, 390, 500, 555, 600, 550, 660],
    "60pc": [210, 210, 270, 470, 500, 570, 600, 670, 600, 920],
    "70pc": [240, 250, 345, 555, 590, 850, 850, 920, 945, 1050],
    "80pc": [330, 350, 455, 630, 880, 1005, 1045, 1050, 1250, 1300],
    "90pc": [545, 550, 600, 1000, 1270, 1320, 1345, 1300, 1345, 1380],
    "100pc": [1050, 1450, 1450, 1450, 1450, 1450, 1450, 1450, 1450, 1450],
}

data_preproc = pd.DataFrame(channel_width_percent)
# sns.lineplot(x='NTG', y='value', hue='variable', data=pd.melt(data_preproc, ['NTG']))
for col in data_preproc.columns:
    if not col == "NTG":
        plt.plot(data_preproc["NTG"], data_preproc[col], label=col)
plt.xlabel("Net-to-gross (NTG) [%]")
plt.ylabel("Sandbody Widths [m]")
plt.xticks(np.arange(5, 100, 10))
plt.legend()
plt.show()

ntg = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]

ntg_ranges = [
    (df["NTG"].ge(ntg[0]) & df["NTG"].lt(ntg[1])),
    (df["NTG"].ge(ntg[1]) & df["NTG"].lt(ntg[2])),
    (df["NTG"].ge(ntg[2]) & df["NTG"].lt(ntg[3])),
    (df["NTG"].ge(ntg[3]) & df["NTG"].lt(ntg[4])),
    (df["NTG"].ge(ntg[4]) & df["NTG"].lt(ntg[5])),
    (df["NTG"].ge(ntg[5]) & df["NTG"].lt(ntg[6])),
    (df["NTG"].ge(ntg[6]) & df["NTG"].lt(ntg[7])),
    (df["NTG"].ge(ntg[7]) & df["NTG"].lt(ntg[8])),
    (df["NTG"].ge(ntg[8]) & df["NTG"].lt(ntg[9])),
    (df["NTG"].ge(ntg[9])),
]

# channel_width_probability_choice = {
#     "10pc" : channel_width_percent["10pc"],                                                                               # "10pc":  [  70,   75,   90,  110,  110,  155,  170,  225,  240,  250]
#     "20pc" : channel_width_percent["20pc"],                                                                               # "20pc":  [  90,  100,  120,  150,  155,  220,  250,  300,  300,  320]
#     "30pc" : channel_width_percent["30pc"],                                                                               # "30pc":  [ 120,  130,  145,  200,  205,  260,  340,  355,  375,  450],
#     "40pc" : channel_width_percent["40pc"],                                                                               # "40pc":  [ 145,  145,  200,  240,  290,  355,  470,  520,  500,  510],
#     "50pc" : channel_width_percent["50pc"],                                                                               # "50pc":  [ 170,  195,  230,  350,  390,  500,  555,  600,  550,  660],
#     "60pc" : channel_width_percent["60pc"],                                                                               # "60pc":  [ 210,  210,  270,  470,  500,  570,  600,  670,  600,  920],
#     "70pc" : channel_width_percent["70pc"],                                                                               # "70pc":  [ 240,  250,  345,  555,  590,  850,  850,  920,  945, 1050],
#     "80pc" : channel_width_percent["80pc"],                                                                               # "80pc":  [ 330,  350,  455,  630,  880, 1005, 1045, 1050, 1250, 1300],
#     "90pc" : channel_width_percent["90pc"],                                                                               # "90pc":  [ 545,  550,  600, 1000, 1270, 1320, 1345, 1300, 1345, 1380],
#     "100pc" : channel_width_percent["100pc"]                                                                              #
# }

channel_width_probability_choice = {
    "10pc": [
        70 + 5 * df.NTG / ntg[1],
        75 + 15 * df.NTG / ntg[2],
        90 + 10 * df.NTG / ntg[3],
        110,
        110 + 45 * df.NTG / ntg[5],
        155 + 15 * df.NTG / ntg[6],
        170 + 55 * df.NTG / ntg[7],
        225 + 15 * df.NTG / ntg[8],
        240 + 10 * df.NTG / ntg[9],
        250,
    ],
    "20pc": [
        90 + 10 * df.NTG / ntg[1],
        100 + 20 * df.NTG / ntg[2],
        120 + 30 * df.NTG / ntg[3],
        150 + 5 * df.NTG / ntg[4],
        155 + 65 * df.NTG / ntg[5],
        220 + 30 * df.NTG / ntg[6],
        250 + 50 * df.NTG / ntg[7],
        300,
        300 + 20 * df.NTG / ntg[9],
        320,
    ],
    "30pc": [
        120 + 10 * df.NTG / ntg[1],
        130 + 15 * df.NTG / ntg[2],
        145 + 55 * df.NTG / ntg[3],
        200 + 5 * df.NTG / ntg[4],
        205 + 55 * df.NTG / ntg[5],
        260 + 80 * df.NTG / ntg[6],
        340 + 15 * df.NTG / ntg[7],
        355 + 20 * df.NTG / ntg[8],
        370 + 75 * df.NTG / ntg[9],
        450,
    ],
    "40pc": [
        145,
        145 + 55 * df.NTG / ntg[2],
        200 + 40 * df.NTG / ntg[3],
        240 + 50 * df.NTG / ntg[4],
        290 + 65 * df.NTG / ntg[5],
        355 + 115 * df.NTG / ntg[6],
        470 + 50 * df.NTG / ntg[7],
        520 - 20 * df.NTG / ntg[8],
        500 + 10 * df.NTG / ntg[9],
        510,
    ],
    "50pc": [
        170 + 25 * df.NTG / ntg[1],
        195 + 35 * df.NTG / ntg[2],
        230 + 120 * df.NTG / ntg[3],
        350 + 40 * df.NTG / ntg[4],
        390 + 110 * df.NTG / ntg[5],
        500 + 55 * df.NTG / ntg[6],
        555 + 45 * df.NTG / ntg[7],
        600 - 50 * df.NTG / ntg[8],
        550 + 110 * df.NTG / ntg[9],
        660,
    ],
    "60pc": [
        210,
        210 + 60 * df.NTG / ntg[2],
        270 + 200 * df.NTG / ntg[3],
        470 + 30 * df.NTG / ntg[4],
        500 + 70 * df.NTG / ntg[5],
        570 + 30 * df.NTG / ntg[6],
        600 + 70 * df.NTG / ntg[7],
        670 - 70 * df.NTG / ntg[8],
        600 + 320 * df.NTG / ntg[9],
        920,
    ],
    "70pc": [
        240 + 10 * df.NTG / ntg[1],
        250 + 95 * df.NTG / ntg[2],
        345 + 210 * df.NTG / ntg[3],
        555 + 35 * df.NTG / ntg[4],
        590 + 260 * df.NTG / ntg[5],
        850,
        850 + 70 * df.NTG / ntg[7],
        920 + 25 * df.NTG / ntg[8],
        945 + 105 * df.NTG / ntg[9],
        1050,
    ],
    "80pc": [
        330 + 20 * df.NTG / ntg[1],
        350 + 105 * df.NTG / ntg[2],
        455 + 175 * df.NTG / ntg[3],
        630 + 240 * df.NTG / ntg[4],
        870 + 135 * df.NTG / ntg[5],
        1005 + 40 * df.NTG / ntg[6],
        1045 + 5 * df.NTG / ntg[7],
        1050 + 200 * df.NTG / ntg[8],
        1250 + 50 * df.NTG / ntg[9],
        1300,
    ],
    "90pc": [
        545 + 5 * df.NTG / ntg[1],
        550 + 50 * df.NTG / ntg[2],
        600 + 400 * df.NTG / ntg[3],
        1000 + 270 * df.NTG / ntg[4],
        1270 + 50 * df.NTG / ntg[5],
        1320 + 25 * df.NTG / ntg[6],
        1345 - 45 * df.NTG / ntg[7],
        1300 + 45 * df.NTG / ntg[8],
        1345 + 35 * df.NTG / ntg[9],
        1380,
    ],
    "100pc": [
        1050 + 400 * df.NTG / ntg[1],
        1450,
        1450,
        1450,
        1450,
        1450,
        1450,
        1450,
        1450,
        1450,
    ],
}

df["10pc"] = np.select(ntg_ranges, channel_width_probability_choice["10pc"], 0)
df["20pc"] = np.select(ntg_ranges, channel_width_probability_choice["20pc"])
df["30pc"] = np.select(ntg_ranges, channel_width_probability_choice["30pc"])
df["40pc"] = np.select(ntg_ranges, channel_width_probability_choice["40pc"])
df["50pc"] = np.select(ntg_ranges, channel_width_probability_choice["50pc"])
df["60pc"] = np.select(ntg_ranges, channel_width_probability_choice["60pc"])
df["70pc"] = np.select(ntg_ranges, channel_width_probability_choice["70pc"])
df["80pc"] = np.select(ntg_ranges, channel_width_probability_choice["80pc"])
df["90pc"] = np.select(ntg_ranges, channel_width_probability_choice["90pc"])
df["100pc"] = np.select(ntg_ranges, channel_width_probability_choice["100pc"])

fig = plt.figure(layout="constrained")

gs = GridSpec(20, 15, figure=fig)
ax1 = fig.add_subplot(gs[0:, 0])
ax2 = fig.add_subplot(gs[0:, 1:], sharey=ax1)
plt.setp(ax2.get_yticklabels(), visible=False)
ax1.plot(df["sand-shale"], df["DEPTH"], color="orange")
# ax1.axvline(x = 0.5, color = 'k', linestyle = '-')
ax1.fill_betweenx(
    df["DEPTH"],
    0.5,
    df["sand-shale"],
    where=df["sand-shale"] >= 0.5,
    facecolor="orange",
)

ax2.plot(df["60pc"], df["DEPTH"], color="blue", label="60%")
ax2.barh(df["DEPTH"], df["60pc"], color="orange")

plt.gca().invert_yaxis()
fig.suptitle("31/4-3 Sandbody Widths (m) ")
plt.title("60% probability that channel width is less than $X$")
plt.ylabel("DEPTH (m)")
plt.xlabel("$X$: Sandbody widths (m)")
# plt.legend()
plt.show()

df.head()
