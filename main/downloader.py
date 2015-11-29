#!/usr/bin/env python3.5
"""Async multiple downloader script."""

from argparse import ArgumentParser
from os.path import split
from urllib.parse import unquote_plus

import aiohttp
import asyncio
import curses


class Screen:

    """
    Grid screen where coroutines write streaming metadata (View).

    Downloading 1MB.zip... 1.0MB
      1.0MB | 100% |==========|
      1MB.zip downloaded.
    --------------------------------------------------------------------------------
    Downloading 5MB.zip... 5.0MB
      5.0MB | 100% |==========|
      5MB.zip downloaded.
    --------------------------------------------------------------------------------
    Downloading 10MB.zip... 10.0MB
      10.0MB | 100% |==========|
      10MB.zip downloaded.


    Press Ctrl+C to exit. All pending downloads will be cancelled.
    """

    def __init__(self, stdscr, separator='-'):
        """Constructor."""
        self.rows = []
        self.stdscr = stdscr
        self.separator = separator

    def add_row(self, content):
        """Add a row."""
        row = Row(self, content)
        self.rows.append(row)
        return row

    def set_row(self, index, content):
        """Set row."""
        row = Row(self, content)
        self.rows[index] = row
        self.update_screen(True)
        return row

    def clear_screen(self):
        """Clear screen."""
        self.stdscr.clear()

    def update_screen(self, clear=False):
        """Update screen."""
        content = '{}\n'.format(self.separator * 80).join(row.content for row in self.rows)
        if clear:
            self.clear_screen()

        self.stdscr.addstr(0, 0, content)
        self.stdscr.refresh()


class Row:

    """Model."""

    def __init__(self, screen, content=''):
        """Constructor."""
        self.screen = screen
        self.content = content

    def update(self, content):
        """Update row content."""
        self.content = content
        self.screen.update_screen()


class Downloader:

    """Controller."""

    def __init__(self, stdscr, urls):
        """Constructor."""
        self.urls = urls
        self.screen = Screen(stdscr)

    def add_row(self, content):
        """Add a row."""
        self.screen.add_row(content)

    def set_row(self, index, content):
        """Set row."""
        self.screen.set_row(index, content)

    @property
    def downloads(self):
        """Get all download coroutines."""
        coroutines = []
        for url in self.urls:
            row = self.screen.add_row('')
            coroutines.append(self._download(row, url))

        return coroutines

    async def _download(self, row, url):
        grid = ['', '', '']
        try:
            response = await aiohttp.get(url)
            fname = unquote_plus(split(url)[-1])
            size = int(response.headers['Content-Length'])
            grid[0] = 'Downloading {}... {}MB'.format(fname, round(size / 1024 ** 2, 1))
            row.update('\n'.join(grid))

            chunk_size = int(size / 100)
            total = 0
            with open(fname, 'wb') as f:
                while True:
                    chunk = await response.content.read(chunk_size)
                    if not chunk:
                        break

                    f.write(chunk)

                    total += len(chunk)
                    percent = total / size
                    length = int(percent * 10)
                    percent = int(percent * 100)

                    message = '  {:.2f}MB | {}% |{:<10}|'.format(
                        round(total / 1024 ** 2, 2),
                        percent,
                        '=' * length
                    )
                    grid[1] = message
                    row.update('\n'.join(grid))

        finally:
            response.close()

        grid[2] = '  {} downloaded.\n'.format(fname)
        row.update('\n'.join(grid))


def main():
    """Run downloader."""
    cancelled = False
    all_finished = False

    parser = ArgumentParser()
    parser.add_argument('urls', type=str, nargs='+', help='Files to download.')
    args = parser.parse_args()

    if args:
        try:
            stdscr = curses.initscr()
            downloader = Downloader(stdscr, args.urls)

            file_names = map(lambda url: unquote_plus(split(url)[-1]), args.urls)
            header = 'Downloading files: {}\n'.format(', '.join(file_names))

            downloader.add_row(header)
            downloads = downloader.downloads
            downloader.add_row('Press Ctrl+C to exit. All pending downloads will be cancelled.')

            loop = asyncio.get_event_loop()
            tasks = asyncio.gather(*downloads)
            loop.run_until_complete(tasks)
            downloader.set_row(-1, 'Downloads finished. Press any key to exit.')

            all_finished = True
            stdscr.getkey()

        except KeyboardInterrupt:
            cancelled = True

        finally:
            curses.endwin()
            if cancelled and not all_finished:
                print('Downloads cancelled by user.', flush=True)

if __name__ == '__main__':
    main()
