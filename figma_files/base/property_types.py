# Property Type
# https://www.figma.com/developers/api#files-types

from pydantic import BaseModel
from typing import Literal, Optional, List
from cssutils.css import CSSStyleRule


class Size(BaseModel):
    width: float
    height: float


class Vector(BaseModel):
    x: float
    y: float


class Rectangle(Vector, Size):
    pass


class Color(BaseModel):
    r: float
    g: float
    b: float
    a: float


class ColorStop(BaseModel):
    position: float
    color: Color
    boundVariables: Optional[dict] = None


class Constraint(BaseModel):
    type: str
    value: float


class MeasurementStartEnd(BaseModel):
    nodeId: str
    side: Literal["TOP", "RIGHT", "BOTTOM", "LEFT"]


class MeasurementOffset(BaseModel):
    type: Literal["INNER", "OUTER"]
    relative: Optional[float] = None
    fixed: Optional[float] = None


class Measurement(BaseModel):
    id: str
    start: MeasurementStartEnd
    end: MeasurementStartEnd
    offset: MeasurementOffset


class FlowStartingPoint(BaseModel):
    nodeId: str
    name: str


class PrototypeDevice(BaseModel):
    type: Literal["NONE", "PRESET", "CUSTOM", "PRESENTATION"]
    size: Size
    presetIdentifier: str
    rotation: Literal["NONE", "CCW_90"]


class ExportSetting(BaseModel):
    suffix: str
    format: str
    constraint: Constraint


BlendMode = Literal[
    "PASS_THROUGH",
    "NORMAL",
    "DARKEN",
    "MULTIPLY",
    "LINEAR_BURN",
    "COLOR_BURN",
    "LIGHTEN",
    "SCREEN",
    "LINEAR_DODGE",
    "COLOR_DODGE",
    "OVERLAY",
    "SOFT_LIGHT",
    "HARD_LIGHT",
    "DIFFERENCE",
    "EXCLUSION",
    "HUE",
    "SATURATION",
    "COLOR",
    "LUMINOSITY",
]

Transform = List[List[float]]


class ImageFilters(BaseModel):
    exposure: Optional[float] = 0
    contrast: Optional[float] = 0
    saturation: Optional[float] = 0
    temperature: Optional[float] = 0
    tint: Optional[float] = 0
    highlights: Optional[float] = 0
    shadows: Optional[float] = 0


class Paint(BaseModel):
    """
    Paints in Figma
    https://help.figma.com/hc/en-us/articles/360041003694-Paints-in-Figma
    """

    type: Literal[
        # 単色またはペイント
        "SOLID",
        # 線形(グラデーション):直線上の2つの色間の漸進的な遷移。線の角度を選べます。
        "GRADIENT_LINEAR",
        # 放射状(グラデーション):中央に色があり、エッジで別の色に遷移する円形のグラデーション。
        # これは、別の色であったり、透明にフェードしたりする可能性があります。
        "GRADIENT_RADIAL",
        # 角度(グラデーション):開始位置から時計回りにグラデーションを作成します。
        # グラデーション内の両方の色の位置を調整して、よりソフトな角度またはより厳しい角度を作成できます。
        "GRADIENT_ANGULAR",
        # ひし形(グラデーション):オブジェクトまたはレイヤーの中央から始まる4つのポイントを持つグラデーション。
        # グラデーションの幅と高さは個別に調整できます。
        "GRADIENT_DIAMOND",
        # 画像または GIF: 静止画像またはアニメーション GIF。
        # https://help.figma.com/hc/en-us/articles/360040028034-Add-Images-to-your-designs
        "IMAGE",
        "EMOJI",
        # ビデオ: .mp4、.mov、または .webm ビデオ ファイルをアップロードします。
        # https://help.figma.com/hc/en-us/articles/8878274530455-Use-videos-in-prototypes
        "VIDEO",
    ]

    visible: Optional[bool] = True
    opacity: Optional[float] = 1
    color: Optional[Color] = None
    blendMode: Optional[BlendMode] = None
    gradientHandlePositions: Optional[list[Vector]] = []
    gradientStops: Optional[list[ColorStop]] = []
    scaleMode: Optional[Literal["FILL", "FIT", "TILE", "STRETCH"]] = None
    imageTransform: Optional[Transform] = []
    scalingFactor: Optional[float] = None
    rotation: Optional[float] = None
    imageRef: Optional[str] = 0
    filters: Optional[ImageFilters] = None
    gifRef: Optional[str] = None
    boundVariables: Optional[dict] = None


class LayoutConstraint(BaseModel):
    vertical: Literal["TOP", "BOTTOM", "CENTER", "TOP_BOTTOM", "SCALE"]
    horizontal: Literal["LEFT", "RIGHT", "CENTER", "LEFT_RIGHT", "SCALE"]


EasingType = Literal["EASE_IN", "EASE_OUT", "EASE_IN_AND_OUT", "LINEAR", "GENTLE_SPRING"]


class LayoutGrid(BaseModel):
    """Guides to align and place objects within a frame"""

    pattern: Literal["COLUMNS", "ROWS", "GRID"]
    # Orientation of the grid as a string enum

    sectionSize: float
    # Width of column grid or height of row grid or square grid spacing

    visible: bool
    # Is the grid currently visible?

    color: Color
    # Color of the grid

    # The following properties are only meaningful for directional grids (COLUMNS or ROWS)

    alignment: Literal["MIN", "STRETCH", "CENTER"]
    # Positioning of grid as a string enum
    # MIN: Grid starts at the left or top of the frame
    # STRETCH: Grid is stretched to fit the frame
    # CENTER: Grid is center aligned

    gutterSize: float
    # Spacing in between columns and rows

    offset: float
    # Spacing before the first column or row

    count: float
    # Number of columns or rows

    boundVariables: Optional[dict] = None
    # A mapping of field to the VariableAlias of the bound variable.


class Effect(BaseModel):
    """
    A visual effect such as a shadow or blur
    """

    type: Literal["INNER_SHADOW", "DROP_SHADOW", "LAYER_BLUR", "BACKGROUND_BLUR"]
    visible: Optional[bool] = None
    radius: Optional[float] = None
    color: Optional[Color] = None
    blendMode: Optional[BlendMode] = None
    offset: Optional[Vector] = None
    spread: Optional[float] = 0

    # Boolean Whether to show the shadow behind translucent or transparent pixels (applies only to drop shadows)
    showShadowBehindNode: Optional[bool] = None

    boundVariables: Optional[dict] = None


class DevStatus(BaseModel):
    type: Literal["READY_FOR_DEV", "COMPLETED"]
    description: Optional[str] = ""


class AnnotationProperty(BaseModel):
    type: Literal[
        "width",
        "height",
        "maxWidth",
        "minWidth",
        "maxHeight",
        "minHeight",
        "fills",
        "strokes",
        "effects",
        "strokeWeight",
        "cornerRadius",
        "textStyleId",
        "textAlignHorizontal",
        "fontFamily",
        "fontStyle",
        "fontSize",
        "fontWeight",
        "lineHeight",
        "letterSpacing",
        "itemSpacing",
        "padding",
        "layoutMode",
        "alignItems",
        "opacity",
        "mainComponent",
    ]


class Annotation(BaseModel):
    label: str
    properties: AnnotationProperty


class ArcData(BaseModel):
    startingAngle: float
    endingAngle: float
    innerRadius: float


class Hyperlink(BaseModel):
    type: Optional[Literal["URL", "NODE"]]
    url: str
    nodeID: str


class TypeStyle(BaseModel):
    fontFamily: str
    fontPostScriptName: Optional[str] = None
    paragraphSpacing: Optional[float] = 0
    paragraphIndent: Optional[float] = 0
    listSpacing: Optional[float] = 0
    italic: Optional[bool] = None
    fontWeight: Optional[float] = None
    fontSize: Optional[float] = None
    textCase: Optional[Literal["ORIGINAL", "UPPER", "LOWER", "TITLE", "SMALL_CAPS", "SMALL_CAPS_FORCED"]] = "ORIGINAL"
    textDecoration: Optional[
        Literal[
            "NONE",
            "STRIKETHROUGH",
            "UNDERLINE",
        ]
    ] = "NONE"
    textAutoResize: Optional[Literal["NONE", "HEIGHT", "WIDTH_AND_HEIGHT", "WIDTH_AND_HEIGHT"]] = "NONE"
    textTruncation: Optional[
        Literal[
            "DISABLED",
            "ENDING",
        ]
    ] = "DISABLED"
    maxLines: Optional[float] = None
    textAlignHorizontal: Optional[Literal["LEFT", "RIGHT", "CENTER", "JUSTIFIED"]] = None
    textAlignVertical: Optional[
        Literal[
            "TOP",
            "CENTER",
            "BOTTOM",
        ]
    ] = None
    letterSpacing: Optional[float] = None
    fills: Optional[List[Paint]] = []
    hyperlink: Optional[Hyperlink] = None
    opentypeFlags: Optional[dict] = {}

    lineHeightPx: Optional[float] = None
    # Line height in px

    lineHeightPercent: Optional[float] = 100
    # Line height as a percentage of normal line height. This is deprecated; in a future version of the API only

    lineHeightPercentFontSize: Optional[float] = None
    # Line height as a percentage of the font size. Only returned when lineHeightPercent is not 100.

    lineHeightUnit: Optional[Literal["PIXELS", "FONT_SIZE_%", "INTRINSIC_%"]] = None
    # The unit of the line height value specified by the user.

    isOverrideOverTextStyle: Optional[bool] = None
    semanticWeight: Optional[Literal["BOLD", "NORMAL"]] = None
    semanticItalic: Optional[Literal["ITALIC", "NORMAL"]] = None

    def set_rule(self, rule: CSSStyleRule):
        if self.fontFamily:
            rule.style.setProperty("font-family", self.fontFamily)


class Overrides(BaseModel):
    """
    Fields directly overridden on an instance.
    Inherited overrides are not included.
    """

    id: str  # A unique ID for a node
    overriddenFields: Optional[List[str]] = []  #  An array of properties


class DocumentationLink(BaseModel):
    uri: str  # Should be a valid URI (e.g. https://www.figma.com).


class Component(BaseModel):
    key: str  #  The key of the component
    name: str  # The name of the component
    description: str  # The description of the component as entered in the editor

    # The ID of the component set if the component belongs to one
    componentSetId: Optional[str] = None
    # The documentation links for this component.
    documentationLinks: Optional[List[DocumentationLink]] = []

    # Whether this component is a remote component that doesn't live in this file
    remote: Optional[bool] = None


class ComponentSet(Component):
    pass


class Style(Component):
    # https://www.figma.com/developers/api#files-types
    key: str  # The key of the style
    name: str  # The name of the style
    description: str  # The description of the style
    # Whether this style is a remote style that doesn't live in this file
    remote: bool
    styleType: Literal["FILL", "TEXT", "EFFECT", "GRID"]
