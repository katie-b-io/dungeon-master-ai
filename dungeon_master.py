import argparse

import dmai

def build_arg_parser() -> argparse.ArgumentParser:
    '''Function constructs an argument parser'''
    description = "Play a game of D&D with the Dungeon Master AI"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-i", "--interactive", action="store_true", 
                        help="Run in interactive mode")
    return parser
    
def main() -> None:
    '''Main entry point to the DMAI'''
    print("Welcome to the Dungeon Master AI!")
    
    # get the command line arguments
    args = build_arg_parser().parse_args()
    
    # start the game
    game = dmai.start()
    
    # start an interactive session on the command line
    if args.interactive:
        dmai.run(game)
    
if __name__ == "__main__":
    main()