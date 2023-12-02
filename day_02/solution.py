#!/usr/bin/env python3

import io
import logging
import re
import sys

from collections import defaultdict


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


cubes = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def determine_games(games_documnent):
    with io.open(games_documnent) as games_doc_fh:
        sum_game_ids = 0
        game_split_re = re.compile(r"^Game (?P<game_id>\d+): (?P<game_sets>.*)")

        for game in games_doc_fh.readlines():
            re_match = game_split_re.search(game)
            assert re_match is not None
            logger.debug(
                f"{game} => game_id: {re_match.group('game_id')} game_sets: {re_match.group('game_sets')}"
            )

            sum_up = True
            for game_set in re_match.group("game_sets").split(";"):
                sum_cubes = defaultdict(lambda: 0)
                for count_color in game_set.split(","):
                    logger.debug(f"  {count_color}")
                    count, color = count_color.strip().split(" ")
                    logger.debug(f"     count: {count} color: {color}")

                    color = color.strip()
                    sum_cubes[color] += int(count)
                    if sum_cubes[color] > cubes[color]:
                        logger.debug(
                            f"         don't sum up  {re_match.group('game_id')}"
                        )
                        sum_up = False
                        break

            if sum_up:
                logger.debug(f"sum up {re_match.group('game_id')}")
                sum_game_ids += int(re_match.group("game_id"))

        logger.info(f"Sum of possible game ids: {sum_game_ids} for {games_documnent}")
        return sum_game_ids


if __name__ == "__main__":
    assert determine_games("data/games_verification.txt") == 8
    determine_games("data/games_test.txt")
