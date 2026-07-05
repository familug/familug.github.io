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
import dataclasses
import enum
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import markdown
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/blogger"]
SITE_URL = "https://familug.github.io"
MARKER_PREFIX = "pelican-file"
CONTENT_DIR = "content"

# Markdown extensions for conversion (no extra deps beyond `markdown`)
MD_EXTENSIONS = ["fenced_code", "tables", "toc", "attr_list"]


@dataclasses.dataclass(frozen=True)
class PelicanPost:
    """A parsed Pelican markdown file with typed metadata fields."""

    title: str
    category: str
    tags: list[str]
    date: str
    body: str
    # WHY: file_id is derived from the source filename and used as the
    # unique key for matching posts on Blogger (via HTML marker comments).
    file_id: str

    @staticmethod
    def from_file(filepath: str | Path) -> "PelicanPost":
        """Parse a Pelican markdown file into a typed PelicanPost.

        Pelican metadata is a block of ``Key: Value`` lines at the top of the
        file, separated from the body by a blank line.
        """
        filepath = Path(filepath)
        text = filepath.read_text(encoding="utf-8")
        lines = text.split("\n")

        raw_metadata: dict[str, str] = {}
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
                raw_metadata[match.group(1)] = match.group(2).strip()
            else:
                # Not a metadata line — body starts here
                body_start = i
                break

        body = "\n".join(lines[body_start:])
        tags_raw = raw_metadata.get("Tags", "")
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()]

        return PelicanPost(
            title=raw_metadata.get("Title", filepath.stem),
            category=raw_metadata.get("Category", "").strip(),
            tags=tags,
            date=raw_metadata.get("Date", ""),
            body=body,
            file_id=filepath.stem,
        )


class SyncAction(enum.StrEnum):
    """Possible outcomes of syncing a single post."""

    CREATE = "create"
    UPDATE = "update"
    SKIP = "skip"


@dataclasses.dataclass(frozen=True)
class SyncResult:
    """Outcome of syncing a single post to Blogger."""

    action: SyncAction
    title: str


@dataclasses.dataclass
class SyncStats:
    """Aggregated sync statistics."""

    create: int = 0
    update: int = 0
    skip: int = 0
    error: int = 0

    def record(self, action: SyncAction) -> None:
        match action:
            case SyncAction.CREATE:
                self.create += 1
            case SyncAction.UPDATE:
                self.update += 1
            case SyncAction.SKIP:
                self.skip += 1

    def record_error(self) -> None:
        self.error += 1

    def summary(self, *, dry_run: bool = False) -> str:
        prefix = "[DRY-RUN] " if dry_run else ""
        return (
            f"\n{prefix}Done!  "
            f"Created: {self.create}  Updated: {self.update}  "
            f"Skipped: {self.skip}  Errors: {self.error}"
        )


def md_to_html(md_body: str) -> str:
    """Convert Pelican markdown body to HTML.

    Handles Pelican-specific ``{static}`` and ``{filename}`` references by
    rewriting them to absolute URLs on the published site.
    """
    # Rewrite {static} asset references to absolute URLs
    md_body = re.sub(r"\{static\}", SITE_URL, md_body)

    # Rewrite {filename} cross-references: .md/.rst -> .html
    def _rewrite_filename(m: re.Match[str]) -> str:
        path = m.group(1)
        path = re.sub(r"\.(md|rst)$", ".html", path)
        return f"{SITE_URL}/{path}"

    md_body = re.sub(r"\{filename\}/?(.*?)(?=[\)\s])", _rewrite_filename, md_body)

    return markdown.markdown(md_body, extensions=MD_EXTENSIONS)


def make_marker(file_id: str) -> str:
    """Return the hidden HTML comment embedded in every synced post."""
    return f"<!-- {MARKER_PREFIX}: {file_id} -->"


def extract_marker(html_content: str) -> str | None:
    """Extract a file-id from the marker comment, or *None*."""
    m = re.search(rf"<!-- {MARKER_PREFIX}: ([a-zA-Z0-9_-]+) -->", html_content or "")
    return m.group(1) if m else None


def get_blogger_service(
    credentials_file: str = "credentials.json",
    token_file: str = "token.json",
) -> Any:
    """Build an authenticated Blogger API v3 service object.

    On first run (``--auth``), opens a browser for OAuth consent and saves
    the resulting token.  On subsequent runs the saved token (which contains
    a refresh-token) is reused automatically.
    """
    creds: Credentials | None = None

    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    # Happy path: valid credentials already loaded
    if creds and creds.valid:
        return build("blogger", "v3", credentials=creds)

    # Expired but refreshable
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        # Need fresh credentials via OAuth flow
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


def fetch_existing_posts(service: Any, blog_id: str) -> dict[str, dict[str, Any]]:
    """Fetch every post from *blog_id* and return ``{file_id: post}``."""
    mapping: dict[str, dict[str, Any]] = {}
    page_token: str | None = None
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


def format_date_for_blogger(date_str: str) -> str | None:
    """Convert Pelican date (e.g. ``2021-02-20``, ``2025/02/20``, ``2021-02-13 14:00:00``, or ``20260630``) to RFC 3339."""
    date_str = date_str.strip().replace("/", "-")
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%Y%m%d",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%dT%H:%M:%S+07:00")
        except ValueError:
            continue
    return None



def build_post_body(post: PelicanPost, html_content: str) -> dict[str, Any]:
    """Assemble a Blogger post resource dict from a typed PelicanPost."""
    marker = make_marker(post.file_id)
    full_html = f"{marker}\n{html_content}"

    body: dict[str, Any] = {
        "kind": "blogger#post",
        "title": post.title,
        "content": full_html,
    }

    # Labels = Category (if not "frontpage") + Tags
    labels: list[str] = []
    if post.category and post.category.lower() != "frontpage":
        labels.append(post.category)
    labels.extend(post.tags)
    if labels:
        body["labels"] = labels

    pub_date = format_date_for_blogger(post.date)
    if pub_date:
        body["published"] = pub_date

    return body


def sync_post(
    service: Any,
    blog_id: str,
    filepath: str | Path,
    existing_posts: dict[str, dict[str, Any]],
    *,
    dry_run: bool = False,
) -> SyncResult:
    """Sync one markdown file to Blogger."""
    post = PelicanPost.from_file(filepath)
    html_content = md_to_html(post.body)
    post_body = build_post_body(post, html_content)

    existing = existing_posts.get(post.file_id)

    # New post — create it
    if not existing:
        if dry_run:
            print(f"  DRY-RUN CREATE: {post.title}")
            return SyncResult(SyncAction.CREATE, post.title)

        result = (
            service.posts()
            .insert(blogId=blog_id, body=post_body)
            .execute()
        )
        print(f"  CREATED: {post.title}  [post_id={result['id']}]")
        time.sleep(1)  # Rate limit: Blogger API allows ~100 req/100s
        return SyncResult(SyncAction.CREATE, post.title)

    # Existing post — check if content, title, labels, or publication date changed
    marker_re = rf"<!-- {MARKER_PREFIX}: [a-zA-Z0-9_-]+ -->\n?"
    old = re.sub(marker_re, "", existing.get("content", "")).strip()
    new = html_content.strip()

    # Avoid TypeError if labels is None or missing
    old_labels = sorted(existing.get("labels") or [])
    new_labels = sorted(post_body.get("labels") or [])

    old_pub = existing.get("published")
    new_pub = post_body.get("published")

    dates_match = True
    if new_pub:  # Only compare dates if local metadata defines a publication date
        if old_pub:
            try:
                # Parse to timezone-aware datetimes and compare UNIX timestamps
                old_dt = datetime.fromisoformat(old_pub)
                new_dt = datetime.fromisoformat(new_pub)
                dates_match = int(old_dt.timestamp()) == int(new_dt.timestamp())
            except ValueError:
                # Fallback to standard string slice comparison if parsing fails
                dates_match = old_pub[:19] == new_pub[:19]
        else:
            dates_match = False

    # Debug print to troubleshoot skip condition
    print(f"  DEBUG: {post.title}")
    print(f"    - content matches: {old == new}")
    print(f"    - title matches: {existing.get('title') == post.title} (Blogger: '{existing.get('title')}', Local: '{post.title}')")
    print(f"    - labels match: {old_labels == new_labels} (Blogger: {old_labels}, Local: {new_labels})")
    print(f"    - dates match: {dates_match} (Blogger: '{old_pub}', Local: '{new_pub}')")

    if (
        old == new
        and existing.get("title") == post.title
        and old_labels == new_labels
        and dates_match
    ):
        print(f"  SKIP (unchanged): {post.title}")
        return SyncResult(SyncAction.SKIP, post.title)

    if dry_run:
        print(f"  DRY-RUN UPDATE: {post.title}  [post_id={existing['id']}]")
        return SyncResult(SyncAction.UPDATE, post.title)

    result = (
        service.posts()
        .update(blogId=blog_id, postId=existing["id"], body=post_body)
        .execute()
    )
    print(f"  UPDATED: {post.title}  [post_id={result['id']}]")
    time.sleep(1)  # Rate limit: Blogger API allows ~100 req/100s
    return SyncResult(SyncAction.UPDATE, post.title)


def main() -> None:
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

    if args.auth:
        print("Starting OAuth authentication flow …")
        get_blogger_service(args.credentials, args.token)
        print("Authentication complete!")
        return

    if not args.files and not args.sync_all:
        parser.error("Specify --files FILE [FILE …] or --all  (use --auth for first-time setup)")

    if not args.blog_id:
        parser.error("Specify --blog-id ID or set the BLOGGER_BLOG_ID env var")

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

    service = get_blogger_service(args.credentials, args.token)
    print("Fetching existing posts from Blogger …")
    existing_posts = fetch_existing_posts(service, args.blog_id)

    stats = SyncStats()

    for filepath in files:
        try:
            sync_result = sync_post(
                service, args.blog_id, filepath, existing_posts,
                dry_run=args.dry_run,
            )
            stats.record(sync_result.action)
        except Exception as exc:
            print(f"  ERROR syncing {filepath}: {exc}", file=sys.stderr)
            stats.record_error()

    print(stats.summary(dry_run=args.dry_run))
    if stats.error:
        sys.exit(1)


if __name__ == "__main__":
    main()
