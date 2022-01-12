import httpx
from bs4 import BeautifulSoup as bs
import regex as re

reg = re.compile(r"(?:name|im|i'm):?\s+(?:is|called)?\s*?([a-zA-Z/ ]+)", re.IGNORECASE, re.MULTILINE)

ema = re.compile(r"(?:email):?\s+(?:is)?\s*?([a-zA-Z0-9@. ]+)", re.IGNORECASE, re.MULTILINE)

dis = re.compile(r"([a-zA-Z0-9@._\-! ]+#[0-9]{4})", re.IGNORECASE, re.MULTILINE)

red = re.compile(r"u/([a-zA-Z0-9@]+)", re.IGNORECASE, re.MULTILINE)

twi = re.compile(r"(@[a-zA-Z0-9. ]+)", re.IGNORECASE, re.MULTILINE)

fem = re.compile(r"(she/her)|(female)", re.IGNORECASE, re.MULTILINE)

male = re.compile(r"(he/him)|(male)", re.IGNORECASE, re.MULTILINE)

nb = re.compile(r"(they/them)|(non[- ]*binary)", re.IGNORECASE, re.MULTILINE)

name = "GitHub"

url = "https://github.com/{}"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def run(username):
    global name
    name = "GitHub (downloading)"
    yield
    profile = httpx.get(url.format(username), headers=headers).text
    name = "GitHub (parsing)"
    yield
    prof = bs(profile, features="html.parser")

    extra = {}

    text = prof.find("article", class_="markdown-body entry-content container-lg f5")
    if text:
        text = text.get_text()
        fname = None
        for line in text.split('\n'):
            line = line.strip()
            name = re.search(reg, line)
            if name:
                fname = name
            if re.search(nb, line):
                extra["Gender (gh bio)"] = "Non-binary"
            elif re.search(male, line):
                extra['Gender (gh bio)'] = "Male"
            elif re.search(fem, line):
                extra["Gender (gh bio)"] = "Female"            
            emailbio = re.search(ema, line)

            if emailbio:
                extra["Email (gh bio)"] = emailbio.group(1).strip()
            
            discord = re.search(dis, line)

            if discord:
                extra["Discord (gh bio)"] = discord.group(1).strip()

            reddit = re.search(red, line)

            if reddit:
                extra["Reddit (gh bio)"] = reddit.group(1).strip()
    
            twitter = re.search(twi, line)

            if twitter:
                extra["Twitter (gh bio)"] = twitter.group(1).strip()
    
        if fname:
            extra["Name (gh bio)"] = fname.group(1)
    
    email = prof.find(itemprop="email") # TODO: Does not work as the email only shows when logged in
    if email:
        extra["Email (gh profile)"] = email.get_text().strip()
    loc = prof.find(itemprop="homeLocation")
    if loc:
        extra["Location (gh profile)"] = loc.get_text().strip()
    
    name = "GitHub"
    yield
    return {"Username": username, **extra}
