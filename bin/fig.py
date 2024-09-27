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
from figma_files.base.files import FigmaFile
from figma_files.base.utils import sanitize_id
from lxml import etree
from cssutils.css import CSSStyleSheet
from functools import partial
from bs4 import BeautifulSoup as Soup
import pandas as pd


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

        img = Path(output) / "html/img"
        img.mkdir(exist_ok=True)

        def _download(entry):
            key, url = entry
            print(key, url)
            response = requests.get(url)
            if response.status_code == 200:
                ext = mimetypes.guess_extension(response.headers["Content-Type"])
                path = img / f"{key}{ext}"
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


def walk_frame(elm, sheet, file: FigmaFile, node):
    if isinstance(node, dict) and "type" in node and "name" in node:
        klass = mapper.get(node["type"], None)
        if not klass:
            print(f"{node['type']} is invalid node")
            return

        children = node.get("children", [])
        try:
            instance = klass(**node)
            elm = instance.to_element(elm, sheet, file)
        except Exception:
            import traceback

            print(traceback.format_exc())

        for child in children:
            walk_frame(elm, sheet, file, child)


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


def frame_to_html(file: FigmaFile, output: Path, name: str, frame: dict):
    html_path: Path = output / f"{name}.{frame['name']}.html"
    html_path.parent.mkdir(exist_ok=True, parents=True)

    sheet = CSSStyleSheet()
    html = etree.Element("html")
    head = etree.SubElement(html, "head")
    add_tailwind(head)
    body = etree.SubElement(html, "body")

    walk_frame(body, sheet, file, frame)

    css_code = sheet.cssText.decode("utf-8")

    e = etree.SubElement(head, "style")
    e.text = css_code

    tailwind_config = file.tailwind_config.json()
    e = etree.SubElement(head, "script")
    e.text = f"tailwind.config = JSON.parse('{tailwind_config}');"

    doctype = "<!DOCTYPE html>"

    html_string = etree.tostring(
        html,
        pretty_print=True,
        encoding="unicode",
        doctype=doctype,
        method="html",  # self-closing tags を無効
    )
    html_string = Soup(html_string, "html.parser").prettify()
    with open(html_path, "w") as out:
        out.write(html_string)


def canvas_to_html(file: FigmaFile, output: Path, canvas: dict):
    name = canvas["name"]
    if not name[0] == "/":
        # / で始まらないページはテンプレートと判断する
        return

    name = name[1:]
    list(map(partial(frame_to_html, file, output, name), canvas["children"]))


@group.command()
@click.argument("path")
@click.option("--page", "-p", default=None)
@click.pass_context
def to_html(ctx, path, page):
    dst = Path(path) / "html"
    dst.mkdir(exist_ok=True, parents=True)

    document_path = Path(path) / "document.json"
    images_path = Path(path) / "html/img"
    figma = json.load(open(document_path))

    images_map = dict((i.stem, f"img/{i.name}") for i in images_path.glob("*"))
    figma_file = FigmaFile(**figma, images=images_map)

    canvas_set = figma_file.document["children"]
    if page:
        canvas_set = list(filter(lambda i: i["name"] == page, canvas_set))
    list(map(partial(canvas_to_html, figma_file, dst), canvas_set))


@group.command()
@click.argument("path")
@click.pass_context
def export_styles(ctx, path):
    document_path = Path(path) / "document.json"
    figma = json.load(open(document_path))

    styles = figma["styles"]
    values = map(
        lambda i: dict(
            styleType=i[1]["styleType"],
            name=i[1]["name"],
        ),
        styles.items(),
    )
    df = pd.DataFrame(values).sort_values(["styleType", "name"])
    out = Path(path) / "styles.csv"
    df.to_csv(out, index=False)


@group.command()
@click.argument("path")
@click.argument("id")
@click.option("--exclude_children", "-ec", is_flag=True)
@click.pass_context
def export_node(ctx, path, id, exclude_children):
    document_path = Path(path) / "document.json"
    figma = json.load(open(document_path))

    def _walk(node):
        if node["id"] == id:
            return node

        children = node.get("children", [])
        for child in children:
            res = _walk(child)
            if res:
                return res

    node = _walk(figma["document"])
    if exclude_children:
        node.pop("children")

    id_str = sanitize_id(id)
    output = Path(path) / f"node_{id_str}.json"
    with open(output, "w") as out:
        json.dump(node, out, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    group()
