from pydantic import BaseModel
from typing import Literal, Optional, List


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
    type: Literal[
        "SOLID",
        "GRADIENT_LINEAR",
        "GRADIENT_RADIAL",
        "GRADIENT_ANGULAR",
        "GRADIENT_DIAMOND",
        "IMAGE",
        "EMOJI",
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
    pattern: Literal["COLUMNS", "ROWS", "GRID"]
    sectionSizeN: float
    visible: bool
    color: Color
    alignment: Literal["MIN", "STRETCH", "CENTER"]
    gutterSize: float
    offset: float
    count: float
    boundVariables: Optional[dict] = None


class Effect(BaseModel):
    type: Literal["INNER_SHADOW", "DROP_SHADOW", "LAYER_BLUR", "BACKGROUND_BLUR"]
    visible: Optional[bool] = None
    radius: Optional[float] = None
    color: Optional[Color] = None
    blendMode: Optional[BlendMode] = None
    offset: Optional[Vector] = None
    spread: Optional[float] = 0
    showShadowBehindNode: bool
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
    fontPostScriptName: str
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
    lineHeightPercent: Optional[float] = 100
    lineHeightPercentFontSize: Optional[float] = None
    lineHeightUnit: Optional[Literal["PIXELS", "FONT_SIZE_%", "INTRINSIC_%"]] = None
    isOverrideOverTextStyle: Optional[bool] = None
    semanticWeight: Optional[Literal["BOLD", "NORMAL"]] = None
    semanticItalic: Optional[Literal["ITALIC", "NORMAL"]] = None


class Overrides(BaseModel):
    id: str
    overriddenFields: Optional[List[str]] = []
