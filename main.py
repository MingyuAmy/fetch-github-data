#!/usr/bin/env python3
# -*- encoding:utf-8 -*-
import requests
import json
import csv


class GithubSpider:
    def __init__(self):
        # per_page: The number of results per page (max 100). default 30.
        # %3E == '>' in url encoding
        self.star_url = 'https://api.github.com/search/repositories?q=stars:%3E1&sort=stars&per_page=100'
        self.fork_url = 'https://api.github.com/search/repositories?q=forks:%3E1&sort=forks&per_page=100'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.113 Safari/537.36'}


    def get_data_from_url(self, url):
        """获取html/json数据, 并且解码"""
        res = requests.get(url, headers=self.headers)
        return res.content.decode()

    def parse_data(self, json_str):
        data = json.loads(json_str)
        result, cols = [], ['full_name', 'stargazers_count', 'forks_count', 'watchers_count', 'html_url']
        seq = 1
        for x in data['items']:
            row = [seq] + [x[col] for col in cols]
            result.append(row)
            seq += 1
        return result


    def save_to_csv(self, filename, header, rows):
        """
        Save data to csv file
        """
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            # first write header
            writer.writerow(header)
            # write data to csv file
            for row in rows:
                writer.writerow(row)

    def process_single(self, url, filename):
        csv_header = ['id', 'name', 'star_count', 'forks_count', 'watch_count', 'url']
        json_str = self.get_data_from_url(url)
        rows = self.parse_data(json_str)
        self.save_to_csv(filename, csv_header, rows)

    def run(self):

        # fetch repos by star number
        self.process_single(self.star_url, 'data-star.csv')

        # fetch repos by fork number
        self.process_single(self.fork_url, 'data-fork.csv')


if __name__ == '__main__':
    print('Fetch github data and store to csv files')
    spider = GithubSpider()
    spider.run()
    print('Done, please check "data-star.csv" and "data-fork.csv"')
