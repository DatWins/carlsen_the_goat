r"""Make "Guess the Move" game pages from a PGN file.

Usage (Windows, from the repo folder):
    py tools\make_game.py mygame.pgn
    py tools\make_game.py mygame.pgn --start 7 --side b
    py tools\make_game.py many_games.pgn --all --source "Bruce Pandolfini, *Pandolfini's Solitaire Chess*"

  --start   how many half-moves (plies) are shown before the guessing starts.
            6 = after 1.e4 e5 2.Nf3 d6 3.d4 f5. Default: the game's [PliesShown]
            header if it has one, otherwise 6.
  --side    w or b: the side the player takes. Default: the side that won.
  --total   the par for the whole game, shared evenly over the moves to guess.
            Default 100. Leftover points go to the last moves, so the total is exact.
  --pars    give each move's par yourself instead, separated by commas.
  --all     make a page for every game in the file (otherwise only the first game).
  --name    folder name for the page (single game only). Default: the players' surnames.
  --source  where the game was found, shown on the page as "Game selected from ...".

Each page is written to content\en\games\<name>\index.md, and the game shows up by
itself in the right opening menu (1.e4 e5, 1.e4 Others, 1.d4 d5, 1.d4 Others, Other).
Needs:  py -m pip install chess
"""
import argparse, pathlib, re, sys, unicodedata
import chess, chess.pgn


def surname(name):
    s = name.split(",")[0].strip() if "," in name else name.strip().split()[-1]
    if name.strip().lower().startswith("deep blue"): s = "deep-blue"
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "player"


def split_par(total, n):
    base, extra = divmod(total, n)
    return [base] * (n - extra) + [base + 1] * extra


def make_page(game, a, name=None):
    h = game.headers
    board, sans = game.board(), []
    for m in game.mainline_moves():
        sans.append(board.san(m)); board.push(m)
    start = a.start if a.start is not None else int(h.get("PliesShown", 6))
    side = a.side or ("b" if h.get("Result") == "0-1" else "w")
    plies = [p for p in range(start, len(sans)) if (p % 2 == 0) == (side == "w")]
    if not plies:
        print(f"skipped {h.get('White')} - {h.get('Black')}: no moves left to guess"); return
    if a.pars:
        pars = [int(x) for x in a.pars.split(",") if x.strip()]
        if len(pars) != len(plies):
            sys.exit(f"{len(pars)} pars given but there are {len(plies)} moves to guess.")
    else:
        pars = split_par(a.total, len(plies))

    white, black = h.get("White", "?").strip(), h.get("Black", "?").strip()
    year = h.get("Date", "")[:4].replace("?", "").strip()
    place = (h.get("Event") or h.get("Site") or "").replace("?", "").strip()
    where = ", ".join(x for x in (place, year) if x)
    opening = h.get("Opening") or h.get("ECO", "")
    name = name or f"{surname(white)}-{surname(black)}"
    out = pathlib.Path("content/en/games") / name
    out.mkdir(parents=True, exist_ok=True)
    ending = "checkmate" if board.is_checkmate() else "resignation"
    me = "White" if side == "w" else "Black"
    page = f'''---
title: "{white} – {black}"
where: "{where}"
year: {year or 0}
opening: "{opening}"
moves: "{' '.join(sans)}"
startply: {start}
side: "{side}"
pars: [{','.join(map(str, pars))}]
---
{white} – {black}, {where}. {opening}. {me} to find {len(plies)} moves; the game ends in {ending}. Par for the game is {sum(pars)}.
{f"{chr(10)}Game selected from {a.source}. Par scores are this site's own: {sum(pars)} points shared evenly across the moves.{chr(10)}" if a.source else ""}
{{{{< guessgame >}}}}
'''
    (out / "index.md").write_text(page, encoding="utf-8")
    print(f"wrote {out / 'index.md'}: {len(plies)} moves to guess, par {sum(pars)}, ends in {ending}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pgn")
    ap.add_argument("--start", type=int)
    ap.add_argument("--side", choices=["w", "b"])
    ap.add_argument("--total", type=int, default=100)
    ap.add_argument("--pars", default="")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--name")
    ap.add_argument("--source", default="")
    a = ap.parse_args()
    with open(a.pgn, encoding="utf-8", errors="replace") as f:
        while True:
            game = chess.pgn.read_game(f)
            if game is None: break
            if game.errors:
                sys.exit(f"Could not read {game.headers.get('White')} - {game.headers.get('Black')}: {game.errors}")
            make_page(game, a, None if a.all else a.name)
            if not a.all: break


if __name__ == "__main__":
    main()
