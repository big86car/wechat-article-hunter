#!/usr/bin/env python3
"""Validate or submit one article to a WeChat Official Account draft box."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests


API_ROOT = "https://api.weixin.qq.com/cgi-bin"
TOKEN_EXPIRY_CODES = {40014, 42001}
ERROR_CLASSES = {
    40001: "authentication", 40013: "authentication", 40125: "authentication",
    40164: "ip_allowlist", 48001: "permission", 48002: "permission",
    45009: "quota", 45028: "quota", 40007: "validation", 40008: "validation",
    40009: "validation", 40018: "validation", 40097: "validation",
}
DISALLOWED_TAGS = re.compile(r"<(script|iframe|form|object|embed)\b", re.I)
PLACEHOLDERS = re.compile(r"TODO|TBD|<!--\s*(?:IMAGE|NOTE):", re.I)
IMG_SRC = re.compile(r"(<img\b[^>]*?\bsrc\s*=\s*)([\"'])(.*?)(\2)", re.I | re.S)
WECHAT_IMAGE_HOSTS = ("mmbiz.qpic.cn", "mmbiz.qlogo.cn")


class PublishError(RuntimeError):
    def __init__(self, message: str, category: str = "platform", code=None):
        super().__init__(message)
        self.category = category
        self.code = code


def safe_json(response: requests.Response) -> dict:
    try:
        data = response.json()
    except ValueError as exc:
        raise PublishError(f"non-JSON response (HTTP {response.status_code})", "transport") from exc
    if response.status_code >= 400:
        raise PublishError(f"HTTP {response.status_code}", "transport")
    code = data.get("errcode", 0)
    if code:
        category = ERROR_CLASSES.get(code, "authentication" if code in TOKEN_EXPIRY_CODES else "platform")
        raise PublishError(data.get("errmsg", "WeChat API error"), category, code)
    return data


class WeChatClient:
    def __init__(self, app_id: str, app_secret: str, cache_path: Path, timeout: int = 30):
        self.app_id = app_id
        self.app_secret = app_secret
        self.cache_path = cache_path
        self.timeout = timeout

    def token(self, refresh: bool = False) -> str:
        if not refresh and self.cache_path.exists():
            try:
                cached = json.loads(self.cache_path.read_text(encoding="utf-8"))
                if cached.get("app_id") == self.app_id and cached.get("expires_at", 0) > time.time() + 120:
                    return cached["access_token"]
            except (OSError, ValueError, KeyError):
                pass
        response = requests.get(
            f"{API_ROOT}/token",
            params={"grant_type": "client_credential", "appid": self.app_id, "secret": self.app_secret},
            timeout=self.timeout,
        )
        data = safe_json(response)
        token = data.get("access_token")
        if not token:
            raise PublishError("token response did not include access_token", "authentication")
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(json.dumps({
            "app_id": self.app_id, "access_token": token,
            "expires_at": time.time() + int(data.get("expires_in", 7200)),
        }), encoding="utf-8")
        self.cache_path.chmod(stat.S_IRUSR | stat.S_IWUSR)
        return token

    def _post(self, endpoint: str, *, data=None, files=None, json_body=None, retry_token=True) -> dict:
        token = self.token()
        try:
            response = requests.post(
                f"{API_ROOT}/{endpoint}", params={"access_token": token}, data=data,
                files=files, json=json_body, timeout=self.timeout,
            )
            return safe_json(response)
        except PublishError as exc:
            if retry_token and exc.code in TOKEN_EXPIRY_CODES:
                self.token(refresh=True)
                return self._post(endpoint, data=data, files=files, json_body=json_body, retry_token=False)
            raise

    def upload_body_image(self, path: Path) -> str:
        with path.open("rb") as handle:
            data = self._post("media/uploadimg", files={"media": (path.name, handle)})
        if not data.get("url"):
            raise PublishError("body image upload did not return url", "platform")
        return data["url"]

    def upload_cover(self, path: Path) -> str:
        with path.open("rb") as handle:
            data = self._post("material/add_material?type=image", files={"media": (path.name, handle)})
        if not data.get("media_id"):
            raise PublishError("cover upload did not return media_id", "platform")
        return data["media_id"]

    def create_draft(self, article: dict) -> str:
        data = self._post("draft/add", json_body={"articles": [article]})
        if not data.get("media_id"):
            raise PublishError("draft creation did not return media_id", "platform")
        return data["media_id"]


def validate_inputs(html_path: Path, cover_path: Path, html: str) -> list[Path]:
    errors = []
    if DISALLOWED_TAGS.search(html):
        errors.append("HTML contains a disallowed active tag")
    if PLACEHOLDERS.search(html):
        errors.append("HTML contains unresolved editorial placeholders")
    if not cover_path.is_file():
        errors.append(f"cover does not exist: {cover_path}")
    local_images = []
    for match in IMG_SRC.finditer(html):
        src = match.group(3).strip()
        parsed = urlparse(src)
        if parsed.scheme in {"http", "https"}:
            if not any(parsed.hostname == host or (parsed.hostname or "").endswith("." + host) for host in WECHAT_IMAGE_HOSTS):
                errors.append(f"external body image is not WeChat-hosted: {src}")
        elif parsed.scheme == "data":
            errors.append("data URI images are not supported")
        else:
            path = (html_path.parent / src).resolve()
            if not path.is_file():
                errors.append(f"local body image does not exist: {src}")
            else:
                local_images.append(path)
    if errors:
        raise PublishError("; ".join(errors), "validation")
    return local_images


def replace_local_images(html_path: Path, html: str, client: WeChatClient) -> str:
    replacements = {}
    def replace(match):
        src = match.group(3).strip()
        if urlparse(src).scheme in {"http", "https"}:
            return match.group(0)
        path = (html_path.parent / src).resolve()
        if path not in replacements:
            replacements[path] = client.upload_body_image(path)
        return f"{match.group(1)}{match.group(2)}{replacements[path]}{match.group(4)}"
    return IMG_SRC.sub(replace, html)


def strip_leading_h1(html: str) -> str:
    return re.sub(r"^\s*(?:<section\b[^>]*>\s*)?<h1\b[^>]*>.*?</h1>", lambda m: m.group(0).split("<h1", 1)[0], html, count=1, flags=re.I | re.S)


def fingerprint(title: str, html: str, cover: Path) -> str:
    digest = hashlib.sha256()
    digest.update(title.encode("utf-8"))
    digest.update(html.encode("utf-8"))
    digest.update(cover.read_bytes())
    return digest.hexdigest()


def write_receipt(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", required=True, type=Path)
    parser.add_argument("--cover", required=True, type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--author", default="")
    parser.add_argument("--digest", default="")
    parser.add_argument("--source-url", default="")
    parser.add_argument("--account-label", default="default")
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--token-cache", type=Path, default=Path("~/.cache/wechat-article-hunter/token.json"))
    parser.add_argument("--keep-leading-h1", action="store_true")
    parser.add_argument("--commit", action="store_true", help="perform network writes; otherwise dry-run")
    parser.add_argument("--force", action="store_true", help="allow a duplicate local fingerprint")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    receipt_path = args.receipt or args.html.parent / "publish-receipt.json"
    html = args.html.read_text(encoding="utf-8")
    local_images = validate_inputs(args.html, args.cover, html)
    item_fingerprint = fingerprint(args.title, html, args.cover)
    if receipt_path.exists() and not args.force:
        try:
            previous = json.loads(receipt_path.read_text(encoding="utf-8"))
            if previous.get("status") == "submitted" and previous.get("fingerprint") == item_fingerprint:
                raise PublishError("matching draft was already submitted; use --force only for an intentional duplicate", "validation")
        except json.JSONDecodeError:
            pass
    receipt = {
        "status": "prepared", "scope": "draft_box_only", "account_label": args.account_label,
        "title": args.title, "submitted_at": None, "draft_id": "", "fingerprint": item_fingerprint,
        "artifacts": {"html": str(args.html), "cover": str(args.cover)},
        "platform_response": {"code": "", "message": ""}, "publicly_published": False,
        "notes": [f"validated {len(local_images)} local inline image(s)", "dry-run: no network mutation"],
    }
    if not args.commit:
        write_receipt(receipt_path, receipt)
        print(f"PREPARED: {receipt_path}")
        return 0
    app_id, app_secret = os.getenv("WECHAT_APP_ID"), os.getenv("WECHAT_APP_SECRET")
    if not app_id or not app_secret:
        raise PublishError("WECHAT_APP_ID and WECHAT_APP_SECRET must be configured in the environment", "authentication")
    try:
        client = WeChatClient(app_id, app_secret, args.token_cache.expanduser())
        hosted_html = replace_local_images(args.html, html, client)
        if not args.keep_leading_h1:
            hosted_html = strip_leading_h1(hosted_html)
        cover_media_id = client.upload_cover(args.cover)
        article = {
            "title": args.title, "author": args.author, "digest": args.digest,
            "content": hosted_html, "content_source_url": args.source_url,
            "thumb_media_id": cover_media_id, "need_open_comment": 0,
            "only_fans_can_comment": 0,
        }
        draft_id = client.create_draft(article)
        receipt.update({
            "status": "submitted", "submitted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "draft_id": draft_id, "notes": [f"uploaded {len(local_images)} local inline image(s)", "draft created; not publicly published"],
        })
        write_receipt(receipt_path, receipt)
        print(f"SUBMITTED: draft_id={draft_id}")
        return 0
    except PublishError as exc:
        receipt.update({"status": "failed", "platform_response": {"code": exc.code or "", "message": str(exc)}, "notes": [f"failure_class={exc.category}"]})
        write_receipt(receipt_path, receipt)
        print(f"FAILED [{exc.category}]: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except PublishError as exc:
        print(f"FAILED [{exc.category}]: {exc}", file=sys.stderr)
        raise SystemExit(1)
