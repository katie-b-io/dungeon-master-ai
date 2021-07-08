import argparse
import os

import dmai
from dmai.utils.config import Config
from dmai.utils.output_builder import OutputBuilder
from dmai.utils.logger import get_logger

logger = get_logger(__name__, Config.session.session_id)


def build_arg_parser() -> argparse.ArgumentParser:
    """Function constructs an argument parser"""
    description = "Play a game of D&D with the Dungeon Master AI"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-i",
                        "--interactive",
                        action="store_true",
                        help="Run in interactive mode")
    parser.add_argument("-c",
                        "--cleric",
                        action="store_true",
                        help="Play as a cleric")
    parser.add_argument("-f",
                        "--fighter",
                        action="store_true",
                        help="Play as a fighter")
    parser.add_argument("-r",
                        "--rogue",
                        action="store_true",
                        help="Play as a rogue")
    parser.add_argument("-w",
                        "--wizard",
                        action="store_true",
                        help="Play as a wizard")
    parser.add_argument(
        "-n",
        "--name",
        help="Set character name (must set character class too)")
    parser.add_argument("--skip-intro",
                        action="store_true",
                        help="Skip the intro")
    parser.add_argument("--cleanup",
                        action="store_true",
                        help="On exit, remove any files produced during game")
    parser.add_argument("--god-mode",
                        action="store_true",
                        help="Enable god mode, all player rolls return 30")
    parser.add_argument("--no-monsters",
                        action="store_true",
                        help="Disable monsters")
    return parser


def main() -> None:
    """Main entry point to the DMAI"""
    logger.debug("Starting game")
    Config.set_uuid()
    Config.set_root(os.path.dirname(os.path.abspath(__file__)))

    OutputBuilder.append(
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nWelcome to the Dungeon Master AI!\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    )
    OutputBuilder.append(
        "This is an MSc project created by Katie Baker at Heriot-Watt University. You are reminded not to input any identifying or confidential information. This interaction will be logged for analysis."
    )

    # get the command line arguments
    args = build_arg_parser().parse_args()

     # game settings in Config
    if args.cleanup:
        Config.cleanup_on_exit()
    if args.god_mode:
        Config.enable_god_mode()
    if args.no_monsters:
        Config.disable_monsters()
        
    # start the game
    char_class = None
    if args.cleric:
        char_class = "cleric"
    elif args.fighter:
        char_class = "fighter"
    elif args.rogue:
        char_class = "rogue"
    elif args.wizard:
        char_class = "wizard"

    if char_class:
        if args.name:
            game = dmai.start(char_class=char_class,
                              char_name=args.name,
                              skip_intro=args.skip_intro)
        else:
            game = dmai.start(char_class=char_class,
                              skip_intro=args.skip_intro)
    else:
        game = dmai.start(skip_intro=args.skip_intro)

    # start an interactive session on the command line
    if args.interactive:
        OutputBuilder.print()
        OutputBuilder.clear()
        dmai.run(game)


if __name__ == "__main__":
    main()
