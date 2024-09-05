#!/usr/bin/env python
import click
from pathlib import Path


@click.group()
@click.pass_context
def group(ctx):
    ctx.ensure_object(dict)


if __name__ == "__main__":
    group()


@group.command()
@click.argument("file_key")
@click.open_file("--out", "-o", default=None)
@click.pass_context
def get_document(ctx, file_key, out):
    """ドキュメント取得"""
    out = out or f"/tmp/{file_key}"
    Path.mkdir(out, exist_ok=True)
    path = out / "document.json"
