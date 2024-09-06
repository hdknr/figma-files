#!/usr/bin/env python
import click
from pathlib import Path
from dotenv import load_dotenv
import os
from figma_files import rest
import json


@click.group()
@click.pass_context
def group(ctx):
    ctx.ensure_object(dict)
    load_dotenv()


@group.command()
@click.argument("file_key")
@click.option("--output", "-o", default=None)
@click.pass_context
def get_doc(ctx, file_key, output):
    """ドキュメント取得"""
    output = output or f"/tmp/{file_key}"
    Path(output).mkdir(exist_ok=True)

    document, images = None, None
    response = rest.get_file(file_key, os.getenv("TOKEN"))
    if response.status_code == 200:
        path = Path(output) / "document.json"
        document = response.json()
        with open(path, "w") as out:
            json.dump(document, out, indent=2, ensure_ascii=False)

    response = rest.get_images(file_key, os.getenv("TOKEN"))
    if response.status_code == 200:
        path = Path(output) / "images.json"
        images = response.json()
        with open(path, "w") as out:
            json.dump(images, out, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    group()
