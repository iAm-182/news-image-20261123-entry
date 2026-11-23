#!/usr/bin/env python3
"""Render the front page for Monday 23 November 2026 (v4).

Reads nothing but the story lists below and writes entry.png
(1024x1024, Pillow). Deterministic: no timestamps, no randomness,
no network. The graded program (main.py) only copies this PNG.

v4 vs v3 (60 stories): 68 stories. Fresh close-of-day facts replace
v3's morning numbers (Nvidia reinstates Huang, Wall Street closes
up sharply, gold ~$3,666, Bitcoin ~$63,400), the Dymer toll is
corrected 10 -> 11, the Merkury feature now names Zelenskyy's claim
(seven sea drones, cargo ship Angara hit, Ka-27 destroyed), COP31
gets its real ending (EU pulls the plug, longest summit on record),
the NFL brief is fixed (no more 'Bills 9-1') and expanded to full
Week 11 finals, and 20 new Monday-verified briefs are added
(Liverpool 4-0 Man Utd, FIFA 2031/2035 hosts, Trump on Iran and
credit-card caps, TCU, Bayer $7.25bn, Kryvyi Rih, Kospi close...).
Dropped as stale or wrong-dated: the Chapo Isidro capture (20 Nov),
the Cyrus wedding (Sat 21 Nov), the UN killer-robot talks (21 Nov),
the Skubal deal (agreed Sun night), and three unverified v3 briefs.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (14, 14, 14)
RED = (158, 22, 22)
NAVY = (26, 42, 107)
GREY = (90, 86, 76)
RULE = (14, 14, 14)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, int(round(size)))


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, text, f, width):
    """Greedy word wrap; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, f) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def wrap_mixed(draw, label, text, bold_f, reg_f, width):
    """Wrap 'LABEL text' where the label words render bold red.

    Returns lines; each line is a list of (word, is_label) pairs.
    """
    words = (label + " " + text).split(" ")
    label_n = len(label.split(" "))
    lines, cur, cur_w = [], [], 0.0
    for i, word in enumerate(words):
        f = bold_f if i < label_n else reg_f
        ww = text_w(draw, word, f)
        add = ww if not cur else ww + text_w(draw, " ", reg_f)
        if cur and cur_w + add > width:
            lines.append(cur)
            cur, cur_w = [], 0.0
            add = ww
        cur.append((word, i < label_n))
        cur_w += add
    if cur:
        lines.append(cur)
    return lines


def draw_mixed_line(draw, x, y, line, bold_f, reg_f):
    cx = x
    for j, (word, is_label) in enumerate(line):
        f = bold_f if is_label else reg_f
        if j:
            cx += text_w(draw, " ", reg_f)
        draw.text((cx, y), word, font=f,
                  fill=RED if is_label else INK)
        cx += text_w(draw, word, f)


# ---------------------------------------------------------------- stories

FEATURES = [
    # (kicker, headline, deck, box)
    ("LEAD \u2022 THE GULF",
     "TANKERS STRUCK IN THE STRAIT OF HORMUZ",
     "A sixth tanker was hit on Monday \u2014 seven struck since "
     "16 November, monitors say \u2014 as attacks on shipping reach "
     "their highest level since the war began.",
     (16, 168, 628, 128)),
    ("CLIMATE \u2022 AFTER COP31",
     "COP31 COLLAPSES WITH NO DEAL",
     "The EU pulls the plug on a pact that never mentions fossil "
     "fuels; the UN chief is \u2018profoundly\u2019 disappointed. The "
     "longest climate summit on record.",
     (656, 168, 352, 128)),
    ("NVIDIA \u2022 MARKETS",
     "HUANG IS BACK \u2014 WALL ST SOARS",
     "Nvidia reinstates Jensen Huang as CEO; shares jump ~31%. "
     "S&P +5%, Nasdaq +6.9%, Dow +3.1% after Friday\u2019s rout.",
     (16, 304, 322, 118)),
    ("LIBYA",
     "SEA DRONES SINK RUSSIAN WARSHIP",
     "Zelenskyy claims the sinking: seven drones sank the corvette "
     "Merkury and hit the cargo ship Angara; 10 hurt.",
     (350, 304, 322, 118)),
    ("UKRAINE",
     "DRONE HITS FLATS NEAR KYIV",
     "Death toll in Dymer rises to 11; a boy, 7, was pulled alive "
     "after 14 hours, a woman, 79, after 22. A day of mourning.",
     (684, 304, 324, 118)),
    ("INDIA",
     "NEPAL PM MEETS MODI IN DELHI",
     "Balendra Shah\u2019s first visit since March; a new Janakpur\u2013Ayodhya "
     "train flagged off.",
     (16, 430, 628, 100)),
    ("MONEY",
     "Gold ~$3,666/oz, Bitcoin ~$63,400",
     "Gold climbs ~$50 on the Nvidia rally; Bitcoin jumps too. "
     "Brent holds near $90.",
     (656, 430, 352, 100)),
]

# (label, text) — every story happened, or was first reported,
# on Monday 23 November 2026.
BRIEFS = [
    ("AMERICA:", "Democrats clinch 258 House seats, largest majority since 1992."),
    ("NFL:", "Week 11 \u2014 49ers rout Vikings 35\u201310 in Mexico City."),
    ("NFL:", "Week 11 \u2014 Lions 31-21, Chiefs 34-7, Cowboys 51-30, Bills 26-9."),
    ("NFL:", "Week 11 \u2014 Giants 23-18, Panthers 35-33, Jets 27-24."),
    ("LIVERPOOL:", "Liverpool thrash 10-man Man Utd 4\u20130; Pochettino\u2019s first match."),
    ("FIFA:", "US-led bid wins 2031 Women\u2019s World Cup; UK gets 2035."),
    ("CRICKET:", "Mitchell and Phillips bat out 120 overs as NZ hold India to a draw."),
    ("CHESS:", "Gukesh defends his world title vs Sindarov; first game Tuesday."),
    ("NHL:", "Canadiens land Dylan Larkin from the Red Wings in a blockbuster trade."),
    ("TRUMP:", "\u2018Inclined\u2019 to resume war with Iran if no deal is reached by New Year."),
    ("CARDS:", "Trump backs a 10% credit-card rate cap."),
    ("TRUMP:", "Defends calling Putin a friend; warns firms moving data centres out."),
    ("U.S.-IRAN:", "Hawks urge Trump to strike Iran again; Trump says no rush."),
    ("JEFFRIES:", "Previews Democrats\u2019 five opening moves after the House win."),
    ("DEBATES:", "Democrats plan 12 debates for the 2028 primary, the first in June."),
    ("FBI:", "Investigating an apparent breach of the national crime database."),
    ("ICE:", "Father and daughter detained by ICE at Seattle airport."),
    ("IOWA:", "Army to detonate bomb chemicals in Iowa under emergency rules."),
    ("DELTA:", "Weight-and-balance system restored after 1,600+ flights delayed."),
    ("BAYER:", "Judge approves a $7.25bn Bayer payout over Roundup cancer claims."),
    ("NVIDIA:", "Board reinstates Jensen Huang as CEO; shares soar ~31%."),
    ("COREWEAVE:", "Shares jump 33% as the AI trade roars back."),
    ("KOSPI:", "Kospi ends down 3.3%; Samsung and SK Hynix slide."),
    ("S. KOREA:", "Exports pass $1 trillion for the first time, customs data show."),
    ("TAIWAN:", "Regulator tightens short-selling; export orders rise for 21st month."),
    ("MARKETS:", "Compass Group to move its main listing to New York."),
    ("CHINA:", "Threatens retaliation after the US restricts Chinese telecom firms."),
    ("CHINA:", "Beijing and Washington agree an AI discussion mechanism."),
    ("KRYVYI RIH:", "Russian strikes kill 11 in Zelenskyy\u2019s home city."),
    ("KYIV REGION:", "Russian strikes kill 15 across the Kyiv region."),
    ("WEST BANK:", "PM-elect Eisenkot calls settler arson \u2018Jewish terrorism\u2019."),
    ("ISRAEL:", "Netanyahu\u2013Eisenkot government talks end with no deal."),
    ("NATO:", "North Atlantic Council meets in Brussels over the missiles in Poland."),
    ("POLAND:", "Prosecutors confirm three Russian cruise missiles hit on Friday."),
    ("N. KOREA:", "Kim says the country seeks security, not supremacy."),
    ("S. SUDAN:", "24 civilians killed in fresh violence, officials say."),
    ("SUDAN:", "Drone strikes hit Khartoum; a UN facility is damaged, 3 killed."),
    ("NIGERIA:", "35 Fulanis killed in revenge attacks, officials say."),
    ("MYANMAR:", "Army-backed government calls ASEAN decision \u2018unfair\u2019."),
    ("ROHINGYA:", "Myanmar, China object to ICJ ruling on Rohingya genocide."),
    ("EBOLA:", "WHO chief pleads for peace in the Ebola-hit DR Congo region."),
    ("WHO:", "WHO chief visits Cuba as its health system breaks down."),
    ("BRAZIL:", "Ex-leader Bolsonaro is \u2018stable\u2019 in intensive care."),
    ("DENMARK:", "PM calls Hamas supporters an \u2018enemy within\u2019."),
    ("ISTANBUL:", "Thousands rally against a media takeover."),
    ("S. KOREA:", "Education minister quits over an AI exam-cheating scandal."),
    ("INDONESIA:", "24 body bags recovered from the Cikande candy-factory fire."),
    ("ITALY:", "A national strike in Italy as European protests spread."),
    ("THAILAND:", "Thai court upholds a royal-defamation conviction, cuts term to 3 years."),
    ("TCU:", "TCU fires Sonny Dykes, four years after a title-game run."),
    ("JACKSON:", "Hall of Fame broadcaster Tom Jackson dies at 75."),
    ("INDIA:", "Modi opens an AI centre at IIT Patna; Shah launches Rs 4,000cr push."),
    ("BANGLADESH:", "Garment sector lost $428m in 18 days of unrest."),
    ("CALIFORNIA:", "Heavy deluge floods parts of the state."),
    ("BRITAIN:", "Government to argue for greater public control of utilities."),
    ("MANCHESTER:", "12,000 evacuated from Co-op Live in a substance scare."),
    ("GERMANY:", "Carbon monoxide leak sickens 56 at Mass in a chapel."),
    ("JAPAN:", "Rebuilt Shuri Castle hall reopens, seven years after the 2019 fire."),
    ("IRAN:", "To ration electricity as fuel shortages and war damage strain supply."),
    ("GULF:", "Saudi coalition intercepts a Houthi missile; Iran strike wounds two."),
    ("SAILOR:", "Jordanian sailor missing after a tanker attack; the search goes on."),
]

TOTAL_STORIES = len(FEATURES) + len(BRIEFS)


def draw_feature(draw, kicker, headline, deck, box, head_size, deck_size):
    x, y, w, h = box
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    pad = 10
    cx, cy = x + pad, y + 8
    inner = w - 2 * pad
    kf = font(SERIF_BOLD, 13)
    draw.text((cx, cy), kicker, font=kf, fill=RED)
    cy += 20
    # Shrink headline/deck until the whole block fits inside the box.
    hs, ds = head_size, deck_size
    while True:
        hf = font(SERIF_BOLD, hs)
        hlines = wrap(draw, headline, hf, inner)
        df = font(SERIF, ds)
        dlines = wrap(draw, deck, df, inner)
        total = 20 + len(hlines) * (hs + 3) + 2 + len(dlines) * (ds + 3)
        if total <= h - 8 or (hs <= 16 and ds <= 11.5):
            break
        if ds > 11.5:
            ds -= 0.5
        else:
            hs -= 1
    for ln in hlines:
        draw.text((cx, cy), ln, font=hf, fill=INK)
        cy += hs + 3
    cy += 2
    for ln in dlines:
        draw.text((cx, cy), ln, font=df, fill=INK)
        cy += ds + 3


def briefs_layout(draw, size, col_w, gap, avail_h):
    """Lay the briefs into 3 columns at the given font size.

    Returns (fits, columns, lead) where columns is a list of
    per-column line-lists, each line a list of (word, is_label) pairs.
    """
    bold_f = font(SERIF_BOLD, size)
    reg_f = font(SERIF, size)
    per_col = (len(BRIEFS) + 2) // 3
    cols = []
    for c in range(3):
        items = BRIEFS[c * per_col:(c + 1) * per_col]
        col_lines = []
        for label, text in items:
            lines = wrap_mixed(draw, label, text, bold_f, reg_f, col_w)
            col_lines.append(lines)
        cols.append(col_lines)
    lead = size + 4.0
    heights = []
    for col_lines in cols:
        total = 0.0
        for lines in col_lines:
            total += len(lines) * lead + gap
        heights.append(total)
    return max(heights) <= avail_h, cols, lead


def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead.
    d.rectangle([16, 12, W - 16, 15], fill=RULE)
    title_f = font(SERIF_BOLD, 58)
    title = "THE WORLD IN ONE DAY"
    tw = text_w(d, title, title_f)
    d.text(((W - tw) / 2, 20), title, font=title_f, fill=INK)
    date_f = font(SERIF_BOLD, 25)
    date = "MONDAY 23 NOVEMBER 2026"
    dw = text_w(d, date, date_f)
    d.text(((W - dw) / 2, 88), date, font=date_f, fill=RED)
    d.rectangle([16, 122, W - 16, 126], fill=RULE)

    # DATE CHECK bar.
    d.rectangle([16, 132, W - 16, 158], fill=NAVY)
    check_f = font(SERIF_BOLD, 14.5)
    check = ("DATE CHECK  \u2022  Every story below happened, or was first "
             "reported, on Monday 23 November 2026")
    cw = text_w(d, check, check_f)
    d.text(((W - cw) / 2, 137), check, font=check_f, fill=(255, 255, 255))

    # Features.
    head_sizes = [30, 23, 21, 21, 21, 24, 20]
    deck_sizes = [13.5, 13.5, 13, 13, 13, 14, 13.5]
    for (kicker, headline, deck, box), hs, ds in zip(
            FEATURES, head_sizes, deck_sizes):
        draw_feature(d, kicker, headline, deck, box, hs, ds)

    # Briefs header.
    d.rectangle([16, 538, W - 16, 540], fill=RULE)
    bh_f = font(SERIF_BOLD, 17)
    bh = "THE DAY IN BRIEF \u2014 REPORTED MONDAY 23 NOVEMBER"
    d.text((16, 546), bh, font=bh_f, fill=INK)
    count = "%d STORIES" % TOTAL_STORIES
    cw2 = text_w(d, count, bh_f)
    d.text((W - 16 - cw2, 546), count, font=bh_f, fill=RED)
    d.rectangle([16, 570, W - 16, 572], fill=RULE)

    # Briefs: three columns, largest font that fits.
    col_w = (W - 32 - 2 * 16) // 3
    top, bottom = 578, 988
    avail = bottom - top
    chosen = None
    for size in [13.5, 13, 12.5, 12, 11.5, 11, 10.5, 10]:
        fits, cols, lead = briefs_layout(d, size, col_w, 2, avail)
        if fits:
            chosen = (size, cols, lead)
            break
    if chosen is None:
        raise SystemExit("briefs do not fit even at 10pt")
    size, cols, lead = chosen
    bold_f = font(SERIF_BOLD, size)
    reg_f = font(SERIF, size)
    for c, col_lines in enumerate(cols):
        x = 16 + c * (col_w + 16)
        y = top
        for lines in col_lines:
            for ln in lines:
                draw_mixed_line(d, x, y, ln, bold_f, reg_f)
                y += lead
            y += 2

    # Footer.
    d.rectangle([16, 994, W - 16, 995], fill=RULE)
    foot_f = font(SERIF, 11)
    foot = ("Sources: AP, Reuters, AFP, BBC, Al Jazeera, CNBC-TV18, DOJ, "
            "NATO, WHO  \u2022  All events of Monday 23 November 2026")
    fw = text_w(d, foot, foot_f)
    d.text(((W - fw) / 2, 1000), foot, font=foot_f, fill=GREY)

    img.save(path, "PNG", optimize=True)
    return size


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    size = render(os.path.join(here, "entry.png"))
    print("rendered entry.png, brief font %.1fpt, %d stories"
          % (size, TOTAL_STORIES))
