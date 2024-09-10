#!/usr/bin/env python
import click
from pathlib import Path
from dotenv import load_dotenv
import os
from figma_files import rest
import json
import requests
import mimetypes
from figma_files.node import mapper


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

        img = Path(output) / "img"
        img.mkdir(exist_ok=True)

        def _download(entry):
            key, url = entry
            print(key, url)
            response = requests.get(url)
            if response.status_code == 200:
                ext = mimetypes.guess_extension(response.headers["Content-Type"])
                path = img / f"{key}.{ext}"
                with open(path, "wb") as f:
                    f.write(response.content)

        list(map(_download, images["meta"]["images"].items()))


def find_node(document, type, name):
    if isinstance(document, dict) and "type" in document and "name" in document:
        if document["type"] == type and document["name"] == name:
            return document
        if "children" in document:
            for child in document["children"]:
                node = find_node(child, type, name)
                if node:
                    return node


def walk_frame(elm, node):
    if isinstance(node, dict) and "type" in node and "name" in node:
        klass = mapper.get(node["type"], None)
        if not klass:
            print(f"{node['type']} is invalid node")
            return

        children = node.get("children", [])
        try:
            instance = klass(**node)
            elm = instance.to_element(elm)
        except Exception as e:
            print(f"{e}")

        for child in children:

def get_meta():
    return [
        {"charset": "utf-8"},
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"},
    ]


def create_meta(head, meta):
    return etree.SubElement(head, "meta", attrib=meta)




@group.command()
@click.argument("path")
@click.argument("frame_name")
@click.pass_context
def to_html(ctx, path, frame_name):
    """HTML 変換"""
    from lxml import etree

    html = etree.Element("html")
    body = etree.SubElement(html, "body")
    list(map(partial(create_meta, head), get_meta()))
    add_tailwind(head)

    document_path = Path(path) / "document.json"
    document = json.load(open(document_path))["document"]
    frame = find_node(document, "FRAME", frame_name)
    if not frame:
        print(f"{frame_name} というFRAMEがありません")
        return
    walk_frame(body, frame)

    html_string = etree.tostring(html, pretty_print=True, encoding="unicode")
    print(html_string)


if __name__ == "__main__":
    group()
