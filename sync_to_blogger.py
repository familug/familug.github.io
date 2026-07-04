#!/usr/bin/env python3
"""Sync Pelican blog posts to Blogger (www.familug.org).

Detects which posts already exist on Blogger by embedding a hidden HTML
comment ``<!-- pelican-file: FILENAME -->`` in each post's content.
No mapping file is needed — the script queries the Blogger API directly.

Usage:
    # One-time OAuth setup (run locally, opens browser)
    python sync_to_blogger.py --auth

    # Sync specific changed files
    python sync_to_blogger.py --files content/alpine.md content/hello.md

    # Sync all posts (initial bulk import)
    python sync_to_blogger.py --all

    # Preview without making changes
    python sync_to_blogger.py --all --dry-run

Environment variables:
    BLOGGER_BLOG_ID  - Numeric blog ID (from Blogger dashboard URL)
"""

import argparse
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import markdown
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SCOPES = ["https://www.googleapis.com/auth/blogger"]
SITE_URL = "https://familug.github.io"
MARKER_PREFIX = "pelican-file"
CONTENT_DIR = "content"

# Markdown extensions for conversion (no extra deps beyond `markdown`)
MD_EXTENSIONS = ["fenced_code", "tables", "toc", "attr_list"]


# ---------------------------------------------------------------------------
# Pelican post parsing
# ---------------------------------------------------------------------------
def parse_pelican_post(filepath):
    """Parse a Pelican markdown file into (metadata_dict, body_string).

    Pelican metadata is a block of ``Key: Value`` lines at the top of the
    file, separated from the body by a blank line.
    """
    text = Path(filepath).read_text(encoding="utf-8")
    lines = text.split("\n")

    metadata = {}
    body_start = 0

    # Skip leading blank lines (some files start with an empty line)
    first_content = 0
    for i, line in enumerate(lines):
        if line.strip():
            first_content = i
            break

    for i in range(first_content, len(lines)):
        line = lines[i]
        if not line.strip():
            body_start = i + 1
            break
        match = re.match(r"^([A-Za-z_]\w*):\s*(.*)", line)
        if match:
            metadata[match.group(1)] = match.group(2).strip()
        else:
            # Not a metadata line — body starts here
            body_start = i
            break

    body = "\n".join(lines[body_start:])
    return metadata, body


def md_to_html(md_body):
    """Convert Pelican markdown body to HTML.

    Handles Pelican-specific ``{static}`` and ``{filename}`` references by
    rewriting them to absolute URLs on the published site.
    """
    # Rewrite {static} asset references to absolute URLs
    md_body = re.sub(r"\{static\}", SITE_URL, md_body)

    # Rewrite {filename} cross-references: .md/.rst → .html
    def _rewrite_filename(m):
        path = m.group(1)
        path = re.sub(r"\.(md|rst)$", ".html", path)
        return f"{SITE_URL}/{path}"

    md_body = re.sub(r"\{filename\}/?(.*?)(?=[\)\s])", _rewrite_filename, md_body)

    return markdown.markdown(md_body, extensions=MD_EXTENSIONS)


# ---------------------------------------------------------------------------
# File-ID helpers (the key to mapping without a file)
# ---------------------------------------------------------------------------
def get_file_id(filepath):
    """Return the filename stem, used as the unique post identifier."""
    return Path(filepath).stem


def make_marker(file_id):
    """Return the hidden HTML comment embedded in every synced post."""
    return f"<!-- {MARKER_PREFIX}: {file_id} -->"


def extract_marker(html_content):
    """Extract a file-id from the marker comment, or *None*."""
    m = re.search(rf"<!-- {MARKER_PREFIX}: ([a-zA-Z0-9_-]+) -->", html_content or "")
    return m.group(1) if m else None


# ---------------------------------------------------------------------------
# Blogger API helpers
# ---------------------------------------------------------------------------
def get_blogger_service(credentials_file="credentials.json",
                        token_file="token.json"):
    """Build an authenticated Blogger API v3 service object.

    On first run (``--auth``), opens a browser for OAuth consent and saves
    the resulting token.  On subsequent runs the saved token (which contains
    a refresh-token) is reused automatically.
    """
    creds = None

    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_file):
                print(f"Error: '{credentials_file}' not found.", file=sys.stderr)
                print(
                    "Download OAuth credentials from Google Cloud Console.",
                    file=sys.stderr,
                )
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Write with restrictive permissions (owner-only read/write)
        fd = os.open(token_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as fh:
            fh.write(creds.to_json())
        print(f"Token saved to {token_file}")

    return build("blogger", "v3", credentials=creds)


def fetch_existing_posts(service, blog_id):
    """Fetch every post from *blog_id* and return ``{file_id: post}``."""
    mapping = {}
    page_token = None
    total = 0

    while True:
        resp = (
            service.posts()
            .list(
                blogId=blog_id,
                maxResults=50,
                pageToken=page_token,
                fields="items(id,title,content,labels,published,updated),"
                       "nextPageToken",
            )
            .execute()
        )

        for post in resp.get("items", []):
            total += 1
            fid = extract_marker(post.get("content", ""))
            if fid:
                mapping[fid] = post

        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    print(f"Blogger: {total} total posts, {len(mapping)} managed by sync")
    return mapping


# ---------------------------------------------------------------------------
# Date formatting
# ---------------------------------------------------------------------------
def format_date_for_blogger(date_str):
    """Convert Pelican date (``2021-02-20`` or ``2025/02/20``) to RFC 3339."""
    date_str = date_str.strip().replace("/", "-")
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%Y-%m-%dT%H:%M:%S+07:00")
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Post body builder
# ---------------------------------------------------------------------------
def build_post_body(metadata, html_content, file_id):
    """Assemble a Blogger post resource dict."""
    marker = make_marker(file_id)
    full_html = f"{marker}\n{html_content}"

    post = {
        "kind": "blogger#post",
        "title": metadata.get("Title", file_id),
        "content": full_html,
    }

    # Labels = Category (if not "frontpage") + Tags
    labels = []
    category = metadata.get("Category", "").strip()
    if category and category.lower() != "frontpage":
        labels.append(category)
    if "Tags" in metadata:
        labels.extend(t.strip() for t in metadata["Tags"].split(",") if t.strip())
    if labels:
        post["labels"] = labels

    pub_date = format_date_for_blogger(metadata.get("Date", ""))
    if pub_date:
        post["published"] = pub_date

    return post


# ---------------------------------------------------------------------------
# Single-post sync logic
# ---------------------------------------------------------------------------
def sync_post(service, blog_id, filepath, existing_posts, *, dry_run=False):
    """Sync one markdown file to Blogger.

    Returns ``(action, title)`` where *action* is one of
    ``'create'``, ``'update'``, or ``'skip'``.
    """
    file_id = get_file_id(filepath)
    metadata, body = parse_pelican_post(filepath)
    html_content = md_to_html(body)
    post_body = build_post_body(metadata, html_content, file_id)
    title = post_body["title"]

    existing = existing_posts.get(file_id)

    if existing:
        # Strip marker from both sides before comparing
        marker_re = rf"<!-- {MARKER_PREFIX}: [a-zA-Z0-9_-]+ -->\n?"
        old = re.sub(marker_re, "", existing.get("content", "")).strip()
        new = html_content.strip()

        if old == new and existing.get("title") == title:
            print(f"  SKIP (unchanged): {title}")
            return "skip", title

        if dry_run:
            print(f"  DRY-RUN UPDATE: {title}  [post_id={existing['id']}]")
            return "update", title

        result = (
            service.posts()
            .update(blogId=blog_id, postId=existing["id"], body=post_body)
            .execute()
        )
        print(f"  UPDATED: {title}  [post_id={result['id']}]")
        time.sleep(1)  # Rate limit: Blogger API allows ~100 req/100s
        return "update", title

    # New post
    if dry_run:
        print(f"  DRY-RUN CREATE: {title}")
        return "create", title

    result = (
        service.posts()
        .insert(blogId=blog_id, body=post_body)
        .execute()
    )
    print(f"  CREATED: {title}  [post_id={result['id']}]")
    time.sleep(1)  # Rate limit: Blogger API allows ~100 req/100s
    return "create", title


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Sync Pelican blog posts to Blogger (www.familug.org)",
    )
    parser.add_argument(
        "--auth", action="store_true",
        help="Run the one-time OAuth authentication flow",
    )
    parser.add_argument(
        "--files", nargs="+", metavar="FILE",
        help="Specific markdown files to sync",
    )
    parser.add_argument(
        "--all", action="store_true", dest="sync_all",
        help="Sync every .md file in content/",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview actions without making Blogger API changes",
    )
    parser.add_argument(
        "--blog-id",
        default=os.environ.get("BLOGGER_BLOG_ID"),
        help="Blogger blog ID (or set BLOGGER_BLOG_ID env var)",
    )
    parser.add_argument(
        "--credentials", default="credentials.json",
        help="Path to OAuth client-secrets file (default: credentials.json)",
    )
    parser.add_argument(
        "--token", default="token.json",
        help="Path to saved OAuth token file (default: token.json)",
    )

    args = parser.parse_args()

    # --- Auth-only mode ---------------------------------------------------
    if args.auth:
        print("Starting OAuth authentication flow …")
        get_blogger_service(args.credentials, args.token)
        print("Authentication complete!")
        return

    # --- Validation -------------------------------------------------------
    if not args.files and not args.sync_all:
        parser.error("Specify --files FILE [FILE …] or --all  (use --auth for first-time setup)")

    if not args.blog_id:
        parser.error("Specify --blog-id ID or set the BLOGGER_BLOG_ID env var")

    # --- Collect files ----------------------------------------------------
    if args.sync_all:
        content_path = Path(CONTENT_DIR)
        files = sorted(content_path.glob("*.md"))
        print(f"Collecting all posts from {CONTENT_DIR}/ … {len(files)} files")
    else:
        files = []
        for f in args.files:
            p = Path(f)
            if p.suffix == ".md" and p.exists():
                files.append(p)
            else:
                print(f"  WARNING: skipping {f} (not found or not .md)")
        print(f"Syncing {len(files)} specified post(s) …")

    if not files:
        print("Nothing to sync.")
        return

    # --- Connect & sync ---------------------------------------------------
    service = get_blogger_service(args.credentials, args.token)
    print("Fetching existing posts from Blogger …")
    existing_posts = fetch_existing_posts(service, args.blog_id)

    stats = {"create": 0, "update": 0, "skip": 0, "error": 0}

    for filepath in files:
        try:
            action, _title = sync_post(
                service, args.blog_id, filepath, existing_posts,
                dry_run=args.dry_run,
            )
            stats[action] += 1
        except Exception as exc:
            print(f"  ERROR syncing {filepath}: {exc}", file=sys.stderr)
            stats["error"] += 1

    # --- Summary ----------------------------------------------------------
    prefix = "[DRY-RUN] " if args.dry_run else ""
    print(
        f"\n{prefix}Done!  "
        f"Created: {stats['create']}  Updated: {stats['update']}  "
        f"Skipped: {stats['skip']}  Errors: {stats['error']}"
    )
    if stats["error"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
