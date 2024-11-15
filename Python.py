import os
import sys
import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth
import time

def get_file_path(file_name):
    file_path = input(f"Enter {file_name} file path: ")
    return file_path

def get_time_gap():
    time_gap = int(input("Enter Time Gap (seconds): "))
    return time_gap

def get_post_link():
    post_link = input("Enter Post Link: ")
    return post_link

def main():
    token_file = get_file_path("Token")
    comment_file = get_file_path("Comment")
    time_gap = get_time_gap()
    post_link = get_post_link()

    tokens = []
    with open(token_file, "r") as file:
        tokens = file.readlines()
    comments = []
    with open(comment_file, "r") as file:
        comments = file.readlines()

    async def async_main():
        browser = await launch(headless=True, args=["--disable-gpu"])
        stealth(browser)

        for token in tokens:
            page = await browser.newPage()
            # Facebook login karein using token
            await page.goto("(link unavailable)")
            await page.evaluate(f"localStorage.setItem('token', '{token.strip()}')")
            await page.goto(post_link)

            for comment in comments:
                await page.type("textarea", comment.strip())
                await page.click("button[type=submit]")
                await page.waitFor(2)
                print(f"Comment posted using token {token.strip()}. Waiting for {time_gap} seconds...")
                await asyncio.sleep(time_gap)

            await page.close()

        await browser.close()

    asyncio.run(async_main())
