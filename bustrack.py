#!/usr/bin/env python3
import argparse


def _parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands', dest='command', required=True)

    record_parser = subparsers.add_parser('record', help='record line\'s position')
    record_parser.add_argument('--line', type=int, required=True)

    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()

    if args.command == 'record':
        pass