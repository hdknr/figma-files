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
from lxml import etree
from cssutils.css import CSSStyleSheet
from functools import partial


@click.group()
@click.pass_context
def group(ctx):
    ctx.ensure_object(dict)
    load_dotenv()


@group.command()
@click.argument("file_key")
@click.option("--no_image", "-ni", is_flag=True)
@click.option("--output", "-o", default=None)
@click.pass_context
def get_doc(ctx, file_key, no_image, output):
    """ドキュメント取得"""
    output = output or f"/tmp/{file_key}"
    Path(output).mkdir(exist_ok=True, parents=True)

    document, images = None, None
    response = rest.get_file(file_key, os.getenv("TOKEN"))
    if response.status_code == 200:
        path = Path(output) / "document.json"
        document = response.json()
        with open(path, "w") as out:
            json.dump(document, out, indent=2, ensure_ascii=False)

    response = rest.get_images(file_key, os.getenv("TOKEN"))
    if response.status_code == 200 and not no_image:
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


def walk_frame(elm, sheet, node):
    if isinstance(node, dict) and "type" in node and "name" in node:
        klass = mapper.get(node["type"], None)
        if not klass:
            print(f"{node['type']} is invalid node")
            return

        children = node.get("children", [])
        try:
            instance = klass(**node)
            elm = instance.to_element(elm, sheet)
        except Exception as e:
            print(f"{e}")

        for child in children:
            walk_frame(elm, sheet, child)


def get_meta():
    return [
        {"charset": "utf-8"},
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"},
    ]


def create_meta(head, meta):
    return etree.SubElement(head, "meta", attrib=meta)


def add_tailwind(head):
    elm = etree.SubElement(
        head, "script", attrib={"src": "https://cdn.tailwindcss.com"}
    )
    elm.text = ""
    return elm


def frame_to_html(output: Path, name: str, frame: dict):
    html_path: Path = output / f"{name}.{frame['name']}.html"
    html_path.parent.mkdir(exist_ok=True, parents=True)

    sheet = CSSStyleSheet()
    html = etree.Element("html")
    head = etree.SubElement(html, "head")
    add_tailwind(head)
    body = etree.SubElement(html, "body")

    walk_frame(body, sheet, frame)

    css_code = sheet.cssText.decode("utf-8")

    e = etree.SubElement(head, "style")
    e.text = css_code

    doctype = "<!DOCTYPE html>"

    html_string = etree.tostring(
        html, pretty_print=True, encoding="unicode", doctype=doctype
    )
    with open(html_path, "w") as out:
        out.write(html_string)


def canvas_to_html(output: Path, canvas: dict):
    name = canvas["name"]
    if not name[0] == "/":
        # / で始まらないページはテンプレートと判断する
        return

    name = name[1:]
    list(map(partial(frame_to_html, output, name), canvas["children"]))


@group.command()
@click.argument("path")
@click.pass_context
def to_html(ctx, path):
    dst = Path(path) / "html"
    dst.mkdir(exist_ok=True, parents=True)

    document_path = Path(path) / "document.json"
    document = json.load(open(document_path))["document"]
    canvas_set = document.pop("children")
    list(map(partial(canvas_to_html, dst), canvas_set))


if __name__ == "__main__":
    group()
