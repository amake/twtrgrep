# -*- coding: utf-8; -*-
from __future__ import print_function
import logging
import tweepy
import json
import os
import re
from argparse import ArgumentParser

creds_file = 'credentials.json'

credentials = {}

if os.path.isfile(creds_file):
    with open(creds_file) as infile:
        credentials = json.load(infile)
else:
    print('Credentials not found. Run auth_setup.py first.')
    exit(1)

auth = tweepy.OAuthHandler(credentials['ConsumerKey'],
                           credentials['ConsumerSecret'])
auth.set_access_token(credentials['AccessToken'],
                      credentials['AccessSecret'])

api = tweepy.API(auth)

# Default is first key
target_to_method = {
    'timeline': api.user_timeline,
    'favorites': api.favorites,
}


def _iter_tweets(method, user=None):
    for status in tweepy.Cursor(method, id=user, tweet_mode='extended').items():
        yield status


def _find_matches(pattern, target, username):
    method = target_to_method[target]
    for tweet in _iter_tweets(method, username):
        if pattern.search(tweet.full_text):
            yield tweet


def _get_url(tweet):
    return f'https://twitter.com/{tweet.author.screen_name}/status/{tweet.id}'


def _format_result(tweet):
    return f'{_get_url(tweet)}: {tweet.full_text}'


def search(pattern, target, username, max_count=None):
    for i, result in enumerate(_find_matches(pattern, target, username)):
        print(_format_result(result))
        if max_count is not None and i + 1 >= max_count:
            return


def main():
    try:
        parser = ArgumentParser(
            description='Search through tweets')
        parser.add_argument('pattern', help='search pattern (regexp)')
        parser.add_argument('username', nargs='?',
                            help='the @ handle to search'
                            ' (the signed-in user if unspecified)')
        parser.add_argument('--ignore-case', '-i', action='store_true',
                            help='perform case-insensitive matching')
        parser.add_argument('--max-count', '-m', type=int,
                            help='maximum number of matches')
        parser.add_argument('--target', '-t', choices=target_to_method.keys(),
                            default=list(target_to_method.keys())[0],
                            help='what to search')
        parser.add_argument('--verbose', '-v', action='count', default=0)
        args = parser.parse_args()

        levels = [logging.WARNING, logging.INFO, logging.DEBUG]
        level = levels[min(len(levels) - 1, args.verbose)]
        logging.basicConfig(level=level)

        flags = 0
        if args.ignore_case:
            flags |= re.IGNORECASE
        pattern = re.compile(args.pattern, flags=flags)
        logging.debug('Pattern: %s', pattern)

        search(pattern, args.target, args.username, max_count=args.max_count)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
